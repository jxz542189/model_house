# -*- coding: utf-8 -*-
"""
   作者：	钱艳
   日期：	2018年10月10日
   文件名：	demo_file_server.py
   功能：	新词查找入口函数
"""
from data_read_file_server import data_read
from file_server3x import fileServer
from my_log_new import Logger
import config


def get_new_word_string(file, stopwordID, dicwordID, dataID,text, N=config.N, PMI=config.PMI_limit):
    '''
    得到新词字符串
    :param file: 文件服务器句柄
    :param stopwordID: 停用词文件ID
    :param dicwordID: 自定义词典文件ID
    :param dataID: 数据文件ID
    :param text: 数据字符串
    :param N: 要查找的新词个数
    :param PMI: 互信息阈值
    :return: 前N个新词及得分
    '''
    # 加载停用词
    data_read.load_stopword(file, stopwordID)
    # 加载自定义词典
    data_read.load_dicword(file, dicwordID)
    # 加载字典树
    root = data_read.load_dic_tree(config.jieba_dic_path,PMI, config.is_save)
    # 加载数据集
    if text!='':
        data=data_read.load_date_text(text)
    else:
        data = data_read.load_date(file, dataID)
    if len(data) == 0:
        Logger.log_DEBUG.debug('数据集为空请查看数据集文件！')
        return '数据集为空请查看数据集文件！'
    # 插入数据集节点
    root = data_read.insert_node(root, data)
    # 查找新词
    result, add_word, PMI_min, PMI_max = root.wordFind(N)
    # 对找到的新词进行排序
    add_word_sort = sorted(add_word.items(), key=lambda x: x[1], reverse=True)
    Logger.log_DEBUG.info('增加了%d个新词, 词语和得分分别为' % len(add_word))
    Logger.log_DEBUG.debug('#############################')
    result_list = []
    for i in range(len(add_word_sort)):
        result_list.append(add_word_sort[i][0] + ','+str(round(add_word_sort[i][1],3)))
        Logger.log_DEBUG.debug(add_word_sort[i][0] + ','+str(round(add_word_sort[i][1],3)))
    Logger.log_DEBUG.debug('#############################')
    return '##'.join(result_list),PMI_min,PMI_max

def init_data(stopword_path=config.stopword_path,dic_path=config.dic_path):
    file = fileServer(config.ip, config.up_url, config.down_url, config.access_url, config.access_key,
                      config._init_companyId)
    r = file.get_api_ticket()
    file_data = []
    with open(stopword_path, 'r', encoding='utf8') as f:
        lines = f.readlines()
        for line in lines:
            file_data.append(line.strip())
    f.close()
    # 上传文件
    id = file.upload_file_by_data('##'.join(file_data))
    print('stopwordID--'+id)

    file_data = []
    with open(dic_path, 'r', encoding='utf8') as f:
        lines = f.readlines()
        for line in lines:
            file_data.append(line.strip())
    f.close()
    # 上传文件
    id = file.upload_file_by_data('##'.join(file_data))
    print('dic_pathID--'+id)

if __name__ == '__main__':
    file = fileServer(config.ip, config.up_url, config.down_url, config.access_url, config.access_key,
                      config._init_companyId)
    r = file.get_api_ticket()
    stopwordID='0243e66ecd1d11e8be95000c2961e520'
    dicwordID='0249d9e0cd1d11e8be95000c2961e520'
    dataID='76842f44cd1d11e8be95000c2961e520'
    text=''
    #init_data()
    r=get_new_word_string(file, stopwordID, dicwordID, dataID,text, N=config.N, PMI=config.PMI_limit)
    print(r)

