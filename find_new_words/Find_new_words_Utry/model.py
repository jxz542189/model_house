# -*- coding: utf-8 -*-
# 参考代码地址:https://github.com/zhanzecheng/Chinese_segment_augment
"""
   作者：	钱艳
   日期：	2018年9月10日
   文件名：	model.py
   功能：	新词查找
"""
import math
import sys
from my_log_new import Logger

class Node:
    """
    建立字典树的节点
    """

    def __init__(self, char):
        # 节点名，根节点为*
        self.char = char
        # 标记节点是否完成（完成则表示该节点是一个独立的词语）
        self.word_finish = False
        # 用来计数节点词
        self.count = 0
        # 用来存放子节点
        self.child = {}
        # 判断是否是后缀（方便计算左右熵用来标记前缀词）
        self.isback = False


class TrieNode:
    """
    建立前缀树，并且包含统计词频，计算左右熵，计算互信息的方法
    """

    def __init__(self, node, PMI_limit, data=None):
        """
        初始函数，data为外部词频数据集
        :param node:根节点名
        :param data:外部词频数据集，字典类型，key为词名，value为词频，默认词典为None
        :param PMI_limit 互信息阈值，默认值为20
        """
        # 建立根节点
        self.root = Node(node)
        # 互信息阈值
        self.PMI_limit = PMI_limit
        if not data:
            return
        node = self.root
        for key, values in data.items():
            new_node = Node(key)
            new_node.count = int(values)
            new_node.word_finish = True
            if key not in node.child.keys():
                node.child[key] = new_node
            else:
                s = '键值-' + key + '-已存在请检查导入词典文件'
                Logger.log_DEBUG.debug(s)

    def add(self, word):
        """
        添加节点，对于左熵计算时，这里采用了一个trick，用a->b<-c 来表示 cba
        具体实现是利用 self.isback 来进行判断
        :param word:词语
        :return:添加词语后的字典树
        """
        try:
            node = self.root
            # 正常加载
            for count, char in enumerate(word):
                # 在节点中找字符
                if char in node.child.keys():
                    node = node.child[char]
                else:
                    new_node = Node(char)
                    node.child[char] = new_node
                    node = new_node

                # 判断是否是最后一个节点
                if count == len(word) - 1:
                    node.count += 1
                    node.word_finish = True

            # 当添加三元组时建立后缀表示方便左熵计算
            length = len(word)
            node = self.root
            if length == 3:
                word[0], word[1], word[2] = word[1], word[2], word[0]
                for count, char in enumerate(word):
                    found_in_child = False
                    # 在节点中找字符
                    if count != length - 1:
                        if char in node.child.keys():
                            node = node.child[char]
                            found_in_child = True
                    else:
                        if char in node.child.keys() and node.child[char].isback:
                            node = node.child[char]
                            found_in_child = True

                    if not found_in_child:
                        new_node = Node(char)
                        node.child[char] = new_node
                        node = new_node

                    # 判断是否是最后一个节点
                    if count == len(word) - 1:
                        node.count += 1
                        node.isback = True
                        node.word_finish = True
        except Exception as e:
            s = "添加节点时发生异常add" + str(e)
            Logger.log_ERROR.error(s)
            Logger.log_ERROR.exception(sys.exc_info())
            raise TypeError(s)

    def search_one(self):
        """
        寻找一阶共现词，并返回词概率
        :return:一阶共现词概率字典,和一阶词总频数
        """
        try:
            result = {}
            node = self.root
            if not node.child:
                return False, 0
            total = 0
            for key in node.child.keys():
                if node.child[key].word_finish == True:
                    total = total + node.child[key].count

            for key in node.child.keys():
                if node.child[key].word_finish == True:
                    result[node.child[key].char] = node.child[key].count / total
            return result, total
        except Exception as e:
            s = "寻找一阶共现词，并返回词概率时发生异常search_one" + str(e)
            Logger.log_ERROR.error(s)
            Logger.log_ERROR.exception(sys.exc_info())
            raise TypeError(s)

    def search_right(self):
        """
        统计右熵
        :return:，右熵字典
        """
        try:
            result = {}
            node = self.root
            if not node.child:
                return False, 0

            for key in node.child.keys():
                child = node.child[key]
                for k in child.child.keys():
                    cha = child.child[k]
                    total = 0
                    p = 0.0
                    for k1 in cha.child.keys():
                        ch = cha.child[k1]
                        if ch.word_finish == True and not ch.isback:
                            total += ch.count
                    for k1 in cha.child.keys():
                        ch = cha.child[k1]
                        if ch.word_finish == True and not ch.isback:
                            p += (ch.count / total) * math.log(ch.count / total, 2)
                    result[child.char + cha.char] = -p
            return result
        except Exception as e:
            s = "统计右熵时发生异常search_right" + str(e)
            Logger.log_ERROR.error(s)
            Logger.log_ERROR.exception(sys.exc_info())
            raise TypeError(s)

    def search_left(self):
        """
        统计左频
        :return:，左频字典
        :return:
        """
        try:
            result = {}
            node = self.root
            if not node.child:
                return False, 0

            for key in node.child.keys():
                child = node.child[key]
                for k in child.child.keys():
                    cha = child.child[k]
                    total = 0
                    p = 0.0
                    for k1 in cha.child.keys():
                        ch = cha.child[k1]
                        if ch.word_finish == True and ch.isback:
                            total += ch.count
                    for k1 in cha.child.keys():
                        ch = cha.child[k1]
                        if ch.word_finish == True and ch.isback:
                            p += (ch.count / total) * math.log(ch.count / total, 2)
                    result[child.char + cha.char] = -p

            return result
        except Exception as e:
            s = "统计左频时发生异常search_left" + str(e)
            Logger.log_ERROR.error(s)
            Logger.log_ERROR.exception(sys.exc_info())
            raise TypeError(s)

    def search_bi(self):
        """
        寻找二阶共现，并返回log2( P(X,Y) / (P(X) * P(Y))和词概率
        :return:二元词组互信息和词概率
        """
        try:
            result = {}
            node = self.root
            if not node.child:
                return False, 0

            total = 0
            # 寻找一阶共现，词概率
            one_dict, total_one = self.search_one()

            for key in node.child.keys():
                child = node.child[key]
                for k in child.child.keys():
                    ch = child.child[k]
                    if ch.word_finish == True:
                        total += ch.count
            PMI_min=1000
            PMI_max=0
            for key in node.child.keys():
                child = node.child[key]
                for k in child.child.keys():
                    ch = child.child[k]
                    PMI = math.log(max(ch.count, 1), 2) - math.log(total, 2) - math.log(one_dict[child.char],
                                                                                        2) - math.log(
                        one_dict[ch.char], 2)
                    # 这里做了PMI阈值约束
                    if PMI>PMI_max:
                        PMI_max=PMI
                    if PMI < PMI_min:
                        PMI_min = PMI
                    if PMI > self.PMI_limit:
                        result[child.char + '_' + ch.char] = (PMI, ch.count / total)

            Logger.log_DEBUG.debug("数据集中最小PMI值为：%d",PMI_min)
            Logger.log_DEBUG.debug("数据集中最大PMI值为：%d",PMI_max)
            return result,PMI_min,PMI_max
        except Exception as e:
            s = "寻找二阶共现时发生异常search_bi" + str(e)
            Logger.log_ERROR.error(s)
            Logger.log_ERROR.exception(sys.exc_info())
            raise TypeError(s)

    def wordFind(self, N):
        '''
        新词查找
        :param N: 新词个个数
        :return:  N个新词及打分和经过排序后的所有二元词及打分
        '''
        try:
            #  通过搜索得到互信息
            bi,PMI_min,PMI_max= self.search_bi()
            # 通过搜索得到左右熵
            left = self.search_left()
            right = self.search_right()

            result = {}
            for key, values in bi.items():
                d = "".join(key.split('_'))
                # 计算公式 score = PMI + min(左熵， 右熵)
                result[key] = (values[0] + min(left[d], right[d])) * values[1]
            add_word = {}
            if len(result)==0:
                Logger.log_DEBUG.debug('没有找到任何二元词组，请检查输入数据，或调小互信息阈值PMI_limit')
                return result, add_word

            result = sorted(result.items(), key=lambda x: x[1], reverse=True)
            dict_list = [result[0][0]]

            new_word = "".join(dict_list[0].split('_'))
            # 获得概率
            add_word[new_word] = result[0][1]

            # 取前N个
            for d in result[1:-1]:
                flag = True
                for tmp in dict_list:
                    pre = tmp.split('_')[0]
                    if d[0].split('_')[-1] == pre or "".join(tmp.split('_')) in "".join(d[0].split('_')):
                        flag = False
                        break
                if flag:
                    new_word = "".join(d[0].split('_'))
                    add_word[new_word] = d[1]
                    dict_list.append(d[0])
                if len(dict_list) == N:
                    break
            return result, add_word,PMI_min,PMI_max
        except Exception as e:
            s = "新词查找时发生异常wordFind" + str(e)
            Logger.log_ERROR.error(s)
            Logger.log_ERROR.exception(sys.exc_info())
            raise TypeError(s)
