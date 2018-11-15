# coding:utf-8
from my_log_new import Logger
import sys
import jieba
import config
import pickle
import copy

history = ''
jieba.load_userdict(config.dic_path)
with open(config.address_path, 'rb') as f:
    address_list = pickle.load(f)


def input_filter(text,text_type):
    if text_type == 'sentence':
        text_new = text.replace("客服：",'').replace("客服:",'').replace("客户:",'').replace("客户：",'').replace('\n','').replace('\r','')
        # print('***********************')
        # print ("sentence ",text_new)
        # print('***********************')
        return text_new
    elif text_type == 'paragraph':
        text_new = []
        for i in text:
            d = i.replace("客服：",'').replace("客服:",'').replace("客户:",'').replace("客户：",'').replace('\n','').replace('\r','')
            text_new.append(d)
        # print('***********************')
        # print("paragraph", text_new)
        # print('***********************')
        return text_new




def sentence_history(sentence, dialogic_flag = False):
    global history
    if dialogic_flag:
        history = ''
    # print('***********************')
    # print("dialogic_flag", dialogic_flag)
    # print("history", history)
    # print('***********************')
    if 1 < len(sentence) <= 4:
        if history:
            sentence_temp =  history + '，' + sentence
        else:
            sentence_temp = sentence
    else:
        sentence_temp = sentence
    history = sentence
    # print('***********************')
    # print ("sentence history",sentence_temp)
    # print('***********************')
    return sentence_temp



def join_sentence(paragraph):
    """
    功能：为paragraph中的元素，添加该元素的上一元素作为该元素的上文信息
    :param paragraph:
    :return: 新的paragraph列表
    """
    try:
        if len(paragraph) <= 1:
            print('the length of paragraph is less than one')
            Logger.log_DEBUG.warning('the length of paragraph is less than one')
            return paragraph
        else:
            new_paragraph = []
            new_paragraph.append(paragraph[0])
            for i in range(1,len(paragraph)):
                if 1<len(paragraph[i])<=4:
                    str_temp = paragraph[i-1] + '，' + paragraph[i]
                    new_paragraph.append(str_temp)
                else:
                    new_paragraph.append(paragraph[i])
            # print('***********************')
            # print("paragraph history", new_paragraph)
            # print('***********************')
            return new_paragraph
    except Exception as e:
        s = "join_sentence error: " + str(e)
        Logger.log_ERROR.error(s)
        Logger.log_ERROR.exception(sys.exc_info())
        raise TypeError(s)

def address_search(entity,sentence):
    """
    功能：基于地址库进行地址识别
    :param entity:
    :param sentence:
    :return:
    """
    try:
        sent_cut = jieba.cut(sentence)
        sent_cut = [i for i in sent_cut]
        address_result = [i for i in sent_cut if i in address_list]
        if address_result:
            for adr in address_result:
                if adr not in entity.location:
                    entity.location.append(adr)
        return entity
    except Exception as e:
        s = "address_search error: " + str(e)
        Logger.log_ERROR.error(s)
        Logger.log_ERROR.exception(sys.exc_info())
        raise TypeError(s)

def filter_result(text,entity):
    """
    对实体识别结果进行过滤，去掉重复值
    :param text:
    :param entity:
    :return:
    """
    try:
        location_list = copy.deepcopy(entity.location)
        for l in location_list:
            temp = copy.deepcopy(entity.location)
            if l in temp:
                temp.remove(l)
            for t in temp:
                if l in t and l in entity.location:
                    entity.location.remove(l)
                    break
        location_list = copy.deepcopy(entity.location)
        for l in location_list:
            for c in entity.company:
                if l in c:
                    l_count = text.count(l)
                    c_count = text.count(c)
                    if l_count == c_count and l in entity.location:
                        entity.location.remove(l)
        company_list = copy.deepcopy(entity.company)
        for c in company_list:
            temp = copy.deepcopy(entity.company)
            if c in temp:
                temp.remove(c)
            for t in temp:
                if c in t and c in entity.company:
                    entity.company.remove(c)
                    break
        return entity
    except Exception as e:
        s = "filter_result error: " + str(e)
        Logger.log_ERROR.error(s)
        Logger.log_ERROR.exception(sys.exc_info())
        raise TypeError(s)
