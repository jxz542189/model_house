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
data=parent+'/data/'
#停用词路径
stopword_path=data+'stopword.txt'
#结巴分词词典路径
jieba_dic_path=data+'jieba_dict.txt'
#自定义词典路径
dic_path=data+'dic.txt'

#树模型模型是否保存
is_save=False
# 定义取TOPN个
N = 5
#最小互信息阈值
PMI_limit=18

#文件服务器配置参数测试时使用
# down_url = "http://10.0.7.45:8090/fileManager/api/file/downloadFileP"
# up_url = "http://10.0.7.45:8090/fileManager/api/file/uploadFileP"
ip = '10.0.2.121:80'
up_url = '/fileManager/api/file/uploadFileP'
down_url = '/fileManager/api/file/downloadFileP'
access_url = '/api/gateway/ticket'
access_key = '33a832d7949c11e89024000c2961e520'
_init_companyId = '08d181119a7b4c0e94ff368942fd4420'