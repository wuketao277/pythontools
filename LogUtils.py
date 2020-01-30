# 提供统一的日志记录方法。
# 方法同时对“控制台”和“文件”进行日志输出；“文件”采用日期滚动方式输出。
import logging
from datetime import datetime, timedelta
import threading


# 日志工具类
class LogUtils:
    # 日志字典，key是日志级别+日期，value是日志对象
    __dict_logger = {}
    # 日志工具类内部锁
    __lock = threading.Lock()

    # 获得日志器名称和文件前缀
    @staticmethod
    def __get_logname_and_fileprefix(log_level):
        log_name = None
        file_prefix = None
        if log_level == logging.DEBUG:
            log_name = 'debug'
            file_prefix = 'log'
        elif log_level == logging.INFO:
            log_name = 'info'
            file_prefix = 'log'
        elif log_level == logging.WARNING:
            log_name = 'warn'
            file_prefix = 'important'
        elif log_level == logging.WARN:
            log_name = 'warn'
            file_prefix = 'important'
        elif log_level == logging.ERROR:
            log_name = 'error'
            file_prefix = 'important'
        elif log_level == logging.CRITICAL:
            log_name = 'critical'
            file_prefix = 'important'
        return log_name, file_prefix

    # 删除前一天的旧日志器
    @staticmethod
    def __pop_old_log(log_level):
        log_name, file_prefix = LogUtils.__get_logname_and_fileprefix(log_level)
        # 获取前一天的日期
        old_date = datetime.now() - timedelta(days=2)
        old_key = log_name + old_date.strftime('%Y%m%d')
        # 两重判断加锁，从字典中移除
        if old_key in LogUtils.__dict_logger:
            try:
                LogUtils.__lock.acquire()
                if old_key in LogUtils.__dict_logger:
                    LogUtils.__dict_logger.pop(old_key)
            except Exception as ex:
                pass
            finally:
                LogUtils.__lock.release()

    # 获得日志对象
    @staticmethod
    def __get_logger(log_level):
        # 检查输入的日志级别
        if log_level not in [logging.DEBUG, logging.INFO, logging.WARN, logging.WARNING, logging.ERROR,
                             logging.CRITICAL]:
            return None
        # 组织日志字典的key
        log_name, _ = LogUtils.__get_logname_and_fileprefix(log_level)
        key = log_name + datetime.now().strftime('%Y%m%d')
        # 判断key是否在字典中
        if key in LogUtils.__dict_logger:
            return LogUtils.__dict_logger.get(key)
        else:
            # 如果key不在字典中，就创建一个日志器并保存在字典中。
            try:
                # 获得同步锁
                LogUtils.__lock.acquire()
                # 再次判断key是否在字典中
                if key in LogUtils.__dict_logger:
                    return LogUtils.__dict_logger.get(key)
                # 创建一个日志器
                log_name, file_prefix = LogUtils.__get_logname_and_fileprefix(log_level)
                # 定义对应的程序模块名name，默认是root
                logger = logging.getLogger(log_name)
                # 设置基本日志级别为DEBUG级别
                logging.basicConfig(level=logging.DEBUG)
                formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')  # 定义日志输出格式
                # 日志输出到屏幕控制台
                ch = logging.StreamHandler()
                ch.setLevel(logging.DEBUG)
                ch.setFormatter(formatter)
                # 向文件输出日志信息。
                fh = logging.FileHandler(file_prefix + datetime.now().strftime('%Y%m%d') + '.txt')
                fh.setLevel(logging.INFO)
                fh.setFormatter(formatter)
                # 日志添加处理器
                logger.addHandler(ch)
                logger.addHandler(fh)
                # 将新创建的logger保存到dict中
                LogUtils.__dict_logger[key] = logger
                # 删除旧的logger
                LogUtils.__pop_old_log(log_level)
                return logger
            except Exception as ex:
                pass
            finally:
                # 释放同步锁
                LogUtils.__lock.release()

    @staticmethod
    def debug(msg):
        logger = LogUtils.__get_logger(logging.DEBUG)
        if logging is not None:
            logger.debug(msg)

    @staticmethod
    def info(msg):
        logger = LogUtils.__get_logger(logging.INFO)
        if logging is not None:
            logger.info(msg)

    @staticmethod
    def warning(msg):
        logger = LogUtils.__get_logger(logging.WARNING)
        if logging is not None:
            logger.warning(msg)

    @staticmethod
    def error(msg):
        logger = LogUtils.__get_logger(logging.ERROR)
        if logging is not None:
            logger.error(msg)

    @staticmethod
    def critical(msg):
        logger = LogUtils.__get_logger(logging.CRITICAL)
        if logging is not None:
            logger.critical(msg)
