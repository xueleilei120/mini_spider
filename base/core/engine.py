# _*_ coding: utf-8 _*_

""" Engine """
import asyncio
import signal
from datetime import datetime
import logging
# try:
#     import uvloop
#     asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
# except ImportError:
#     pass

from base.core.scheduler import Scheduler
from base.core.downloader.downloader import Downloader
from base.utils.common import result2list
from base.https.request import Request


class GracefulKiller(object):
    """ 完美kill主进程 """
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        logging.warning("---> exit_gracefully: signum={0} <---".format(signum))
        self.kill_now = True


class Engine(object):
    def __init__(self, spider):
        self.spider = spider
        self.scheduler = Scheduler(spider)
        self.downloader = Downloader(spider)
        self.settings = spider.settings

    def start(self):
        start_requests = iter(self.spider.start_requests())
        self.execute(self.spider, start_requests)

    def execute(self, spider, start_requests):
        self._init_start_requests(start_requests)
        loop = asyncio.get_event_loop()
        start_time = datetime.now()
        try:
            loop.run_until_complete(self._next_request(spider))
        finally:
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()
            logging.info("---------------> %s: end <---------------" % self.spider.name)
            logging.info("---------------> use time: %s <---------------" % (datetime.now() - start_time))

    def _init_start_requests(self, start_requests):
        for req in start_requests:
            self.crawl(req)

    @staticmethod
    async def wait_tasks_done(semaphore, value):
        while semaphore._value != value:
            logging.warning("---------------> Wait all task done! <---------------")
            await asyncio.sleep(1)

    async def _next_request(self, spider):
        loop = asyncio.get_event_loop()
        killer = GracefulKiller()
        task_limit = self.settings.get("TASK_LIMIT", 1)   # 同时允许任务数量
        semaphore = asyncio.Semaphore(value=task_limit, loop=loop)
        while True:
            request = self.scheduler.next_request()
            if not request:
                logging.warning("time.sleep(1)")
                await asyncio.sleep(1)
                continue
            await semaphore.acquire()
            loop.create_task(self._process_request(request, spider, semaphore))

            if killer.kill_now:
                await Engine.wait_tasks_done(semaphore, task_limit)
                break

    async def _process_request(self, request, spider, semaphore):
        try:
            response = await self.download(request, spider)
        except Exception as exc:
            logging.error("download error: %s", str(exc), exc_info=True)
        else:
            self._handle_downloader_output(response, request, spider)
        semaphore.release()

    async def download(self, request, spider):
        response = await self.downloader.fetch(request)
        # response.request = request
        return response

    def _handle_downloader_output(self, response, request, spider):
        if isinstance(response, Request):
            self.crawl(response)
            return
        # 处理下载后的数据
        self.process_response(response, request, spider)

    def process_response(self, response, request, spider):
        callback = request.callback or spider.parse
        result = callback(response)
        ret = result2list(result)
        self.handle_spider_output(ret, spider)

    def handle_spider_output(self, result, spider):
        for item in result:
            if item is None:
                continue
            elif isinstance(item, Request):
                self.crawl(item)
            elif isinstance(item, dict):
                self.process_item(item, spider)
            else:
                logging.error("Spider must retrun Request, dict or None")

    def process_item(self, item, spider):
        spider.process_item(item)

    def crawl(self, request):
        self.scheduler.enqueue_request(request)
