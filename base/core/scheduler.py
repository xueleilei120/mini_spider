# _*_ coding: utf-8 _*_

""" Scheduler """
import logging

from base.xredis.connection import from_settings
from base.utils.misc import load_object
from base.xredis import defaults


class Scheduler(object):

    """ Scheduler """

    def __init__(self, spider):
        self.server = from_settings(spider.settings)
        # Ensure the connection is working.
        self.server.ping()
        self.serializer = None
        self.persist = defaults.SCHEDULER_PERSIST
        self.flush_on_start = defaults.SCHEDULER_FLUSH_ON_START
        self.idle_before_close = defaults.SCHEDULER_IDLE_BEFORE_CLOSE
        self.queue_key = defaults.SCHEDULER_QUEUE_KEY
        self.queue_cls = defaults.SCHEDULER_QUEUE_CLASS
        self.dupefilter_key = defaults.SCHEDULER_DUPEFILTER_KEY
        self.dupefilter_cls = defaults.SCHEDULER_DUPEFILTER_CLASS
        self.open(spider)

    def __len__(self):
        return len(self.queue)

    def open(self, spider):
        self.spider = spider
        try:
            self.queue = load_object(self.queue_cls)(
                server=self.server,
                spider=spider,
                key=self.queue_key % {'spider': spider.name},
                serializer=self.serializer,
            )
        except TypeError as e:
            raise ValueError("Failed to instantiate queue class '%s': %s",
                             self.queue_cls, e)

        self.df = load_object(self.dupefilter_cls)(
                server=self.server,
                spider=spider
        )

        if self.flush_on_start:
            self.flush()
        if len(self.queue):
            logging.warning("Resuming crawl (%d requests scheduled)" % len(self.queue))

    def close(self, reason):
        if not self.persist:
            self.flush()

    def flush(self):
        self.df.clear()
        self.queue.clear()

    def enqueue_request(self, request):
        if not request.dont_filter and self.df.request_seen(request):
            self.df.log(request, self.spider)
            return False
        self.queue.push(request)
        return True

    def next_request(self):
        block_pop_timeout = self.idle_before_close
        request = self.queue.pop(block_pop_timeout)
        return request

    def has_pending_requests(self):
        return len(self) > 0