# _*_ coding: utf-8 _*_
# author : "liuyc"
# date : 2017/12/22 15:11
# desc : "日志打印初始化模块, 在"
import logging
import sys
import os


def init_logger(settings, log_name="base_log", log_path=None):
    # 获取logger实例，如果参数为空则返回name=root, 当直接用logging模块取到的也是root命名的实例
    logger = logging.getLogger()

    # 指定logger输出格式
    formatter = logging.Formatter("[%(levelname)s] [%(process)s] %(asctime)s - %(message)s")

    # 文件日志
    if log_path is None:
        log_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + \
                   "//logs//" + log_name + ".log"
    file_handler = logging.FileHandler(log_path)
    file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式

    # 控制台日志
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.formatter = formatter  # 也可以直接给formatter赋值

    # 为logger添加的日志处理器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # 指定日志的最低输出级别
    if settings.get("DEBUG"):
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    return logger


