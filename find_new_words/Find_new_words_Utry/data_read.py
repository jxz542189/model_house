# -*- coding: utf-8 -*-
"""
   作者：	钱艳
   日期：	2018年9月11日
   文件名：	data_read.py
   功能：	外部数据数据读取及预处理
"""
import time
import jieba
import sys
import os
from sklearn.externals import joblib
import config
from model import TrieNode
from my_log_new import Logger

class data_read:
    '''
    数据读取及处理类
    '''

    # 停用词集合
    stopword = set()

    # 加载自定义词典
    jieba.load_userdict(config.dic_path)

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

    @staticmethod
    def Load_stopword(stopword_path):
        '''
        加载停用词，初始化通用词集合
        :param stopword_path: 停用词路径
        '''
        try:
            if os.path.exists(stopword_path):
                with open(stopword_path, 'r', encoding='utf8') as f:
                    lines = f.readlines()
                    for line in lines:

                        if line.strip() in data_read.stopword:
                            print(line.strip())
                        data_read.stopword.add(line.strip())
                Logger.log_DEBUG.debug('stopword停用词大小：%d', len(data_read.stopword))
            else:
                Logger.log_DEBUG.error('没有找到停用词典！！！！！！很可能导致程序出错')
        except Exception as e:
            s = "加载停用词时发生异常Load_stopword" + str(e)
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
    def load_date(data_path):
        '''
        加载数据集,并对数据分词去停用词
        :param data_path: 数据路径
        :return:数据集合列表
        '''
        try:
            Logger.log_DEBUG.debug('-----> 开始读取数据集')
            s_time = time.time()
            data = []
            if os.path.exists(data_path):
                with open(data_path, 'r', encoding='utf8') as f:
                    lines = f.readlines()
                    for line in lines:
                        line = line.strip()
                        line = [x for x in jieba.cut(line, cut_all=False) if x not in data_read.stopword]
                        data.append(line)
                time_elapse = time.time() - s_time
                Logger.log_DEBUG.debug("读取完毕耗时: {}s".format(time_elapse))
                Logger.log_DEBUG.debug('date数据集大小：%d', len(data))
                return data
            else:
                Logger.log_DEBUG.debug('date数据集为空请检查数据集文件！！！！！！')
                return data
        except Exception as e:
            s = "加载数据集,并对数据分词去停用词时发生异常load_date" + str(e)
            Logger.log_ERROR.error(s)
            Logger.log_ERROR.exception(sys.exc_info())
            raise TypeError(s)

    @staticmethod
    def load_dic_tree(jieba_dic_path,PMI, is_save=True):
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
                root = TrieNode('*',PMI, word_freq)
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
