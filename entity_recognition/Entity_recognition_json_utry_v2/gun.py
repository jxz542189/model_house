#coding=utf-8
import os
import gevent.monkey
gevent.monkey.patch_all()
import multiprocessing
#https://www.jianshu.com/p/fecf15ad0c9a
#gunicorn部署Flask服务
debug = True
#日辉输出级别
loglevel = 'debug'
bind = '10.0.12.112:6000'
pidfile = 'log/gunicorn.pid'
# logfile = 'log/debug.log'

#开启的每个工作进程的模式类型，默认为sync模式，也可使用gevent模式。
worker_class = 'gunicorn.workers.ggevent.GeventWorker'
#启动的进程数
# workers = multiprocessing.cpu_count() * 2 + 1
workers = 5
#线程数
threads = 2
#字符串传输长度
limit_request_field_size=81900


x_forwarded_for_header = 'X-FORWARDED-FOR'

daemon = False#意味着开启后台运行，默认为False
