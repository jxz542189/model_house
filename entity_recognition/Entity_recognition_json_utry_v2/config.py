# coding:utf-8

"""
    作者：	钱艳
    日期：	2018年9月10日
    文件名：	config.py
    功能：	语义自动标注配置文件
"""
import os
#程序运行路径
parent = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
print("程序运行路径:")
print(parent)

# 日志保存路径
log_info_path =  parent+'/log/info/'
if not os.path.exists(log_info_path):
    os.makedirs(log_info_path)
log_err_path = parent + '/log/err/'
if not os.path.exists(log_err_path):
        os.makedirs(log_err_path)
# 非error信息日志记录文件
info_file =log_info_path+'info_log.txt'
print(info_file)
# error信息日志记录文件
err_file = log_err_path+'err_log.txt'

#数据文件夹
data = parent+'/data/'
#自定义词典路径
dic_path = data+'dic.txt'
address_path = data + 'address.pkl'

# 是否启用地址库识别地址
address_lib = True
# 是否对实体识别结果进行过滤
is_filter = True

