# -*- coding: utf-8 -*-
"""
   作者：	钱艳
   日期：	2018年10月10日
   文件名：	data_read_file_server.py
   功能：	从文件服务器读取外部数据数据并做预处理
"""
import time
import jieba
import sys
import os
from sklearn.externals import joblib
from model import TrieNode
from my_log_new import Logger

class data_read:
    '''
    数据读取及处理类
    '''

    # 停用词集合
    stopword = set()

    @staticmethod
    def load_stopword(file,stopwordID):
        '''
        从文件服务器上读取停用词
        :param file: 文件服务器类
        :param stopwordID: 停用词文件ID
        :return: 初始化类stopword集合
        '''
        try:
            data_read.stopword = set()
            if stopwordID=='':
                Logger.log_DEBUG.warning('没有停用词典！！！！！！很可能导致程序出错')
            # 根据id下载文件
            text = file.download_file_by_id(stopwordID)
            w_list=text.split("##")
            for w in w_list:
                if w.strip() in data_read.stopword:
                    print(w.strip())
                data_read.stopword.add(w.strip())
            Logger.log_DEBUG.debug('stopword停用词大小：%d', len(data_read.stopword))
        except Exception as e:
            s = "加载停用词时发生异常Load_stopword" + str(e)
            Logger.log_ERROR.error(s)
            Logger.log_ERROR.exception(sys.exc_info())
            raise TypeError(s)

    @staticmethod
    def load_dicword(file,dicwordID):
        '''
        从文件服务器上读取自定义词并加载到结巴分词组件中
        :param file: 文件服务器类
        :param dicwordID: 自定义词文件ID
        '''
        try:
            if dicwordID=='':
                Logger.log_DEBUG.warning('没有自定义词典！！！！！！')
            # 根据id下载文件
            text = file.download_file_by_id(dicwordID)
            w_list=text.split("##")
            Logger.log_DEBUG.debug('自定义词大小：%d', len(w_list))
            #加载自定义词典
            jieba.load_userdict(w_list)
        except Exception as e:
            s = "加载自定义词时发生异常load_dicword" + str(e)
            Logger.log_ERROR.error(s)
            Logger.log_ERROR.exception(sys.exc_info())
            raise TypeError(s)

    @staticmethod
    def load_date(file,dataID):
        '''
        从文件服务器上加载数据集,并对数据分词去停用词
        :param file: 文件服务器类
        :param dataID: 数据文件ID
        :return:数据集合列表
        '''
        try:
            Logger.log_DEBUG.debug('-----> 开始读取数据集')
            s_time = time.time()
            data = []
            if dataID == '':
                Logger.log_DEBUG.warning('date数据集为空请检查数据集文件！！！！！！')
                return data
                # 根据id下载文件
            text = file.download_file_by_id(dataID)
            s_list = text.split("##")
            Logger.log_DEBUG.debug('数据大小：%d', len(s_list))

            for s in s_list:
                s = s.strip()
                line = [x for x in jieba.cut(s, cut_all=False) if x not in data_read.stopword]
                data.append(line)

            time_elapse = time.time() - s_time
            Logger.log_DEBUG.debug("读取完毕耗时: {}s".format(time_elapse))
            Logger.log_DEBUG.debug('date数据集大小：%d', len(data))
            return data
        except Exception as e:
            s = "从文件服务器上加载数据集,并对数据分词去停用词时发生异常load_date" + str(e)
            Logger.log_ERROR.error(s)
            Logger.log_ERROR.exception(sys.exc_info())
            raise TypeError(s)

    @staticmethod
    def load_date_text(text):
        '''
        解析数据集，并对数据分词去停用词
        :param text: 数据文本
        :return:数据集合列表
        '''
        try:
            Logger.log_DEBUG.debug('-----> 开始解析text数据集')
            s_time = time.time()
            data = []
            s_list = text.split("##")
            Logger.log_DEBUG.debug('数据大小：%d', len(s_list))

            for s in s_list:
                s = s.strip()
                line = [x for x in jieba.cut(s, cut_all=False) if x not in data_read.stopword]
                data.append(line)

            time_elapse = time.time() - s_time
            Logger.log_DEBUG.debug("解析完毕耗时: {}s".format(time_elapse))
            Logger.log_DEBUG.debug('date数据集大小：%d', len(data))
            return data
        except Exception as e:
            s = "解析数据集，并对数据分词去停用词时发生异常load_date_text" + str(e)
            Logger.log_ERROR.error(s)
            Logger.log_ERROR.exception(sys.exc_info())
            raise TypeError(s)

    @staticmethod
    def Load_word_freq(jieba_dic_path):
        '''
        加载外部词频，初始化外部词频字典
        :param jieba_dic_path: 结巴词典路径
        :return 外部词典字典
        '''
        try:
            Logger.log_DEBUG.debug('-----> 开始读取外部词频')
            s_time = time.time()
            # 外部词典字典
            word_freq = {}
            if os.path.exists(jieba_dic_path):
                with open(jieba_dic_path, 'r', encoding='utf8') as f:
                    lines = f.readlines()
                    for line in lines:
                        line = line.split(' ')
                        # 规定最少词频
                        if len(line) < 2:
                            continue
                        if int(line[1]) > 2:
                            if line[0] not in word_freq.keys():
                                word_freq[line[0]] = line[1]
                time_elapse = time.time() - s_time
                Logger.log_DEBUG.debug("读取完毕耗时: {}s".format(time_elapse))
                Logger.log_DEBUG.debug('word_freq外部词典大小：%d', len(word_freq))
                return word_freq
            else:
                Logger.log_DEBUG.error('没有找到外部词典！！！！！！很可能导致程序出错')
        except Exception as e:
            s = "加载外部词频时发生异常Load_word_freq" + str(e)
            Logger.log_ERROR.error(s)
            Logger.log_ERROR.exception(sys.exc_info())
            raise TypeError(s)

    @staticmethod
    def load_dic_tree(jieba_dic_path, PMI, is_save=True):
        '''
        加载字典树
        :param jieba_dic_path: 结巴词典路径
        :param PMI: 互信息阈值
        :param is_save: 是否保存构建好的字典树，直接加载构建好的树可以节约时间
        :return: 返回字典树
        '''
        Logger.log_DEBUG.debug('-----> 开始加载字典树')
        s_time = time.time()
        if is_save:
            try:
                word_freq = data_read.Load_word_freq(jieba_dic_path)
                root = TrieNode('*', PMI, word_freq)
                joblib.dump(root, 'tree.bin')
                time_elapse = time.time() - s_time
                Logger.log_DEBUG.debug("构建字典树完毕耗时: {}s".format(time_elapse))
            except Exception as e:
                s = "构建字典树发生异常load_dic_tree" + str(e)
                Logger.log_ERROR.error(s)
                Logger.log_ERROR.exception(sys.exc_info())
                raise TypeError(s)
        else:
            try:
                root = joblib.load('tree.bin')
                time_elapse = time.time() - s_time
                Logger.log_DEBUG.debug("加载字典树完毕耗时: {}s".format(time_elapse))
            except Exception as e:
                s = "读取字典树发生异常load_dic_tree" + str(e)
                Logger.log_ERROR.error(s)
                Logger.log_ERROR.exception(sys.exc_info())
                raise TypeError(s)
        return root

    @staticmethod
    def insert_node(root, data):
        '''
        将数据集中的1到3元词组插入到字典树种
        :param root: 字典树
        :param data: 数据集列表
        :return: 插入完节点后的字典树
        '''
        try:
            Logger.log_DEBUG.debug('------> 插入节点')
            s_time = time.time()
            for i in data:
                # 得到句子分词1到3元组
                tmp = data_read.generate_ngram(i, 3)
                for d in tmp:
                    root.add(d)
            time_elapse = time.time() - s_time
            Logger.log_DEBUG.debug("插入完毕耗时: {}s".format(time_elapse))
        except Exception as e:
            s = "插入节点发生异常insert_node" + str(e)
            Logger.log_ERROR.error(s)
            Logger.log_ERROR.exception(sys.exc_info())
            raise TypeError(s)
        return root

    @staticmethod
    def generate_ngram(data, n):
        """
        得到句子分词1到n元组
        :param data:分词后句子
        :param n:几元组
        :return:句子分词后的1到n元组列表
        """
        try:
            result = []
            for i in range(1, n + 1):
                if len(data) - i + 1 < 1:
                    break
                for j in range(len(data) - i + 1):
                    result.append(data[j:j + i])
            return result
        except Exception as e:
            s = "得到句子分词1到n元组时发生异常generate_ngram" + str(e)
            Logger.log_ERROR.error(s)
            Logger.log_ERROR.exception(sys.exc_info())
            raise TypeError(s)
