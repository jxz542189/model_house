import re
import os
import sys
import pandas as pd
import codecs
from itertools import chain
from my_log_new import Logger

history = []
class num_classify(object):
    #以下在自定义函数外的代码会在该类被导入的时候运行
    # history = []
    def __init__(self):
        #身份证、金额提取
        self.ID_word = ['身份证','后四位']
        self.MONEY_word = ['价格','钱','金额','租金','房租','打折']
        #金额中重复数字去除规则
        filter_rule = r'[幺两一二三四五六七八九零]*[十百千万亿]?'
        self.compile_filter = re.compile(filter_rule)
        #确定金额提取规则
        money_rule = r'[幺两一二三四五六七八九零十百千万亿]+[元块]'
        self.compile_money = re.compile(money_rule)
        #带量词数字提取规则
        delete_rule = r'[幺两一二三四五六七八九零十百千万亿]+[张期次遍个号件年位下笔岁只套月天年时分周粒撞盘盒杯条页名斤克]'
        self.compile_delete = re.compile(delete_rule)
        #剩余数字提取规则
        number_rule = r'[幺两一二三四五六七八九零十百千万亿]+'
        self.compile_number = re.compile(number_rule)

    def history_record(self,line):
        """
        历史信息记录,历史信息跨度'3'可调
        """
        global history
        try:
            if len(history) >= 3:
                history = history[-2:]
            history_money = [i for i in self.MONEY_word if i in line]
            if history_money:
                history_money = 'money'
            else:
                history_money = 'no'
            history_ID = [i for i in self.ID_word if i in line]
            if history_ID:
                history_ID = 'ID'
            else:
                history_ID = 'no'
            history_temp = (history_money, history_ID)
            history.append(history_temp)
            return history
        except Exception as e:
            s = "history record error:" + str(e)
            Logger.log_ERROR.error(s)
            Logger.log_ERROR.exception(sys.exc_info())
            raise TypeError(s)

    def filter_money(self,money_num):
        try:
            # filter_rule = r'[幺两一二三四五六七八九零]*[十百千万亿]?'
            # compile_filter = re.compile(filter_rule)
            filter_money = self.compile_filter.findall(money_num)
            if filter_money:
                money_num = []
                [money_num.append(d) for d in filter_money if not d in money_num]
                money_num = "".join(money_num).replace(' ', '')
            Logger.log_DEBUG.debug('filter money result:{}'.format(money_num))
            return money_num
        except Exception as e:
            s = "filter money process error:" + str(e)
            Logger.log_ERROR.error(s)
            Logger.log_ERROR.exception(sys.exc_info())
            raise TypeError(s)

    def sent_judge(self,str_list,word_list):
        """
        根据句内距离判断是否是ID或money,
        句内间隔的字符距离可进行调整
        :param str_list:
        :param word_list:
        :return:
        """
        try:
            result_judge = False
            for mw in word_list:
                if mw in str_list[0]:
                    mw_right = str_list[0].split(mw)[1]
                    if len(mw_right) <= 3:
                        result_judge = True
                if mw in str_list[1]:
                    mw_left = str_list[1].split(mw)[0]
                    if len(mw_left) <= 1:
                        result_judge = True
            return result_judge
        except Exception as e:
            s = "sentence inner judge error:" + str(e)
            Logger.log_ERROR.error(s)
            Logger.log_ERROR.exception(sys.exc_info())
            raise TypeError(s)

    def true_money(self,line,money_str):
        """
        确定为金额的数字的抽取
        :param line:
        :param money_str:
        :return:
        """
        try:
            pattern_money = self.compile_money.findall(line)
            if pattern_money:
                for i in pattern_money:
                    Logger.log_DEBUG.debug('true money result:{}'.format(i))
                    line = line.replace(i, '')
                    i = self.filter_money(i)
                    money_str = money_str + ' ' + i
            return line,money_str
        except Exception as e:
            s = "true money process error:" + str(e)
            Logger.log_ERROR.error(s)
            Logger.log_ERROR.exception(sys.exc_info())
            raise TypeError(s)

    def delete_num(self,line,money_str,ID_str):
        try:
            # delete_rule = r'[幺两一二三四五六七八九零十百千万亿]+[张期次遍个号件年位下笔岁只套月天年时分周粒撞盘盒杯条页名斤克]'
            # compile_delete = re.compile(delete_rule)
            pattern_delete = self.compile_delete.findall(line)
            if pattern_delete:
                for i in pattern_delete:
                    if len(i) > 4:
                        line_temp = line.split(i)
                        sjm = self.sent_judge(line_temp, self.MONEY_word)
                        sji = self.sent_judge(line_temp, self.ID_word)
                        Logger.log_DEBUG.debug('sentence inner judge result:'
                                               'number__{0},money judge__{1},ID judge'
                                               '__{2}'.format(i,sjm,sji))
                        if sjm:
                            i = self.filter_money(i[:-1])
                            money_str = money_str + ' ' + i
                        if sji:
                            ID_str = ID_str + ' ' + i
                for i in pattern_delete:
                    line = line.replace(i, '')
            return line,money_str,ID_str
        except Exception as e:
            s = "delete number process error:" + str(e)
            Logger.log_ERROR.error(s)
            Logger.log_ERROR.exception(sys.exc_info())
            raise TypeError(s)

    def number_judge(self,line,history,money_str,ID_str,other_str):
        """
        剩余数字的属性判断
        :param line:
        :param history:
        :param money_str:
        :param ID_str:
        :param other_str:
        :return:
        """
        try:
            # number_rule = r'[幺两一二三四五六七八九零十百千万亿]+'
            # compile_number = re.compile(number_rule)
            pattern_number = self.compile_number.findall(line)
            # 判断数字属性
            if pattern_number:
                history_judge = list(chain.from_iterable(history))
                Logger.log_DEBUG.debug('history information:{0}'.format(" ".join(history_judge)))
                for num in pattern_number:
                    if len(num) > 1:
                        if '百' in num or '千' in num or '万' in num or '亿' in num:
                            if "money" in history_judge:
                                num = self.filter_money(num)
                                money_str = money_str + ' ' + num
                            else:
                                other_str = other_str + ' ' + num
                            Logger.log_DEBUG.debug('hundred and so on exist result:number__{0},'
                                                   'money__{1},other__{2}'.format(num,money_str,other_str))
                        elif len(num) == 4:
                            if "ID" in history_judge and 'money' in history_judge:
                                id_index = [ii for ii, v in enumerate(history_judge) if v == 'ID']
                                money_index = [ii for ii, v in enumerate(history_judge) if v == 'money']
                                if id_index[-1] > money_index[-1]:
                                    ID_str = ID_str + ' ' + num
                                else:
                                    money_str = money_str + ' ' + num
                            elif 'money' in history_judge:
                                money_str = money_str + ' ' + num
                            elif "ID" in history_judge:
                                ID_str = ID_str + ' ' + num
                            else:
                                other_str = other_str + ' ' + num
                            Logger.log_DEBUG.debug('number length is four '
                                                   'result:number__{0},'
                                                   'money__{1},ID__{2}'
                                                   'other__{3}'.format(num,money_str,ID_str,other_str))
                        else:
                            if "ID" in history_judge and 'money' in history_judge:
                                id_index = [ii for ii, v in enumerate(history_judge) if v == 'ID']
                                money_index = [ii for ii, v in enumerate(history_judge) if v == 'money']
                                if id_index[-1] > money_index[-1]:
                                    ID_str = ID_str + ' ' + num
                                else:
                                    money_str = money_str + ' ' + num
                            elif 'money' in history_judge:
                                money_str = money_str + ' ' + num
                            elif "ID" in history_judge:
                                ID_str = ID_str + ' ' + num
                            else:
                                other_str = other_str + ' ' + num
                            Logger.log_DEBUG.debug('the last judge '
                                                   'result:number__{0},'
                                                   'money__{1},ID__{2}'
                                                   'other__{3}'.format(num, money_str, ID_str, other_str))
            return money_str,ID_str,other_str
        except Exception as e:
            s = "number judge process error:" + str(e)
            Logger.log_ERROR.error(s)
            Logger.log_ERROR.exception(sys.exc_info())
            raise TypeError(s)

    def doc_extract(self,text):
        """
        对一段话提取金额和ID
        :param text:
        :return:
        """
        try:
            global history
            history = []
            result_infor={}
            money_str = ''
            ID_str = ''
            other_str = ''
            for line in text:
                line = line.replace('\n','').replace('0','零').replace('1','一').replace('2','二').replace('3','三') \
                        .replace('4', '四').replace('5','五').replace('6','六').replace('7','七').replace('8','八')\
                        .replace('9','九')
                Logger.log_DEBUG.debug('the prosess line is:{}'.format(line))
                if line:
                    history = self.history_record(line)
                    #抽取确定的金额
                    line,money_str = self.true_money(line, money_str)
                    #过滤掉非金额和非ID
                    line, money_str, ID_str = self.delete_num(line, money_str, ID_str)
                    money_str, ID_str, other_str = self.number_judge(line, history, money_str,
                                                                ID_str, other_str)
            if money_str:
                money_str = money_str[1:].replace(" ",',')
                result_infor.setdefault('money',money_str)
            else:
                result_infor.setdefault('money', money_str)
            if ID_str:
                ID_str = ID_str[1:].replace(" ", ',')
                result_infor.setdefault('ID',ID_str)
            else:
                result_infor.setdefault('ID', ID_str)
            if other_str:
                other_str = other_str[1:].replace(" ", ',')
                result_infor.setdefault('other',other_str)
            else:
                result_infor.setdefault('other', other_str)
            return result_infor
        except Exception as e:
            s = "doc extract process error:" + str(e)
            Logger.log_ERROR.error(s)
            Logger.log_ERROR.exception(sys.exc_info())
            raise TypeError(s)

    def sent_extract(self,line,flag=False):
        """
        对一句话提取金额和ID
        :param line:
        :param flag:
        :return:
        """
        try:
            global history
            if flag:
                history = []
            result_infor={}
            line = line.replace('\n', '').replace('0', '零').replace('1', '一').replace('2', '二').replace('3', '三') \
                .replace('4', '四').replace('5', '五').replace('6', '六').replace('7', '七').replace('8', '八') \
                .replace('9', '九')
            money_str = ''
            ID_str = ''
            other_str = ''
            Logger.log_DEBUG.debug('the prosess line is:{0},the'
                                   'flag is:{1}'.format(line,flag))
            history = self.history_record(line)
            if line:

                # 抽取确定的金额
                line, money_str = self.true_money(line, money_str)
                # 过滤掉非金额和非ID
                line, money_str, ID_str = self.delete_num(line, money_str, ID_str)
                money_str, ID_str, other_str = self.number_judge(line, history, money_str,
                                                            ID_str, other_str)
            if money_str:
                money_str = money_str[1:].replace(" ",',')
                result_infor.setdefault('money',money_str)
            else:
                result_infor.setdefault('money', money_str)
            if ID_str:
                ID_str = ID_str[1:].replace(" ", ',')
                result_infor.setdefault('ID',ID_str)
            else:
                result_infor.setdefault('ID', ID_str)
            if other_str:
                other_str = other_str[1:].replace(" ", ',')
                result_infor.setdefault('other',other_str)
            else:
                result_infor.setdefault('other', other_str)

            return result_infor
        except Exception as e:
            s = "sentence extract process error:" + str(e)
            Logger.log_ERROR.error(s)
            Logger.log_ERROR.exception(sys.exc_info())
            raise TypeError(s)






