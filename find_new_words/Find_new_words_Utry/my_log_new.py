# coding:utf-8
import logging, logging.handlers
import config

class Logger:
    """
    	作者：	钱艳
    	日期：	2018年9月10日
    	文件名：	my_log_new.py
    	功能：	输出日志
    				- 按照error和非error两类进行输出
    """
    # 创建一个logger
    log_DEBUG = logging.getLogger('D')


    # 设置日志输出级别
    # CRITICAL 50
    # ERROR    40
    # WARNING  30
    # INFO     20
    # DEBUG    10
    log_DEBUG.setLevel(logging.DEBUG)
    """
    TimedRotatingFileHandler参数说明
        when	日志名变更时间单位
            'S'	Seconds
            'M'	Minutes
            'H'	Hours
            'D'	Days
            'W0'-'W6'	Weekday(0=Monday)
            'midnight'	Roll over at midnight
        interval	间隔时间，是指等待N个when单位的时间后，自动重建文件
        backupCount	保留日志最大文件数，超过限制，删除最先创建的文件；默认值0，表示不限制。
        delay		延迟文件创建，直到第一次调用emit()方法创建日志文件
        atTime		在指定的时间（datetime.time格式）创建日志文件。
        utc			是否使用UTC(世界统一时间)时间
    """
    handler_D = logging.handlers.TimedRotatingFileHandler(config.info_file, when='H', interval=3, backupCount=30,
                                                        delay=False, utc=False)
    # 设置日志文件后缀，以当前时间作为日志文件后缀名。
    handler_D.suffix = "%Y%m%d_%H%M.log"
    # 定义handler的输出格式
    formatter = logging.Formatter(
        '[%(asctime)s][%(thread)d][%(filename)s][line: %(lineno)d][%(levelname)s] ## %(message)s')
    handler_D.setFormatter(formatter)

    # 再创建一个handler，用于输出到控制台
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)

    log_DEBUG.addHandler(handler_D)
    log_DEBUG.addHandler(ch)

    # 创建一个logger
    log_ERROR = logging.getLogger('E')
    log_ERROR.setLevel(logging.ERROR)
    handler_E = logging.handlers.TimedRotatingFileHandler(config.err_file, when='H', interval=3, backupCount=30,
                                                        delay=False, utc=False)
    # 设置日志文件后缀，以当前时间作为日志文件后缀名。
    handler_E.suffix = "%Y%m%d_%H%M.log"
    # 定义handler的输出格式
    formatter = logging.Formatter(
        '[%(asctime)s][%(thread)d][%(filename)s][line: %(lineno)d][%(levelname)s] ## %(message)s')
    handler_E.setFormatter(formatter)

    log_ERROR.addHandler(handler_E)
    log_ERROR.addHandler(ch)

if __name__ == '__main__':
    Logger.log_DEBUG.debug('foorbar兔子')
    Logger.log_ERROR.error('foorbar兔子log_ERROR')