# coding:utf-8
import fool
import sys
from flask import jsonify
from my_log_new import Logger
from num_extract import num_classify
import optimize_func
import config


class Entity():
    '''
    实体存储类
    '''
    def __init__(self):
        # 时间
        self.time = []
        # 地点
        self.location = []
        # 人名
        self.person = []
        # 机构名
        self.company = []
        # 身份证后四位
        self.ID = ''
        # 金额
        self.money = ''


class Entity_recognition():
    NE=num_classify()
    '''
    实体识别类
    '''
    def get_entity_recognit_sentence(self, sentence, entity, dialogic_flag=False,input_filter=True,sentence_context=False):
        '''
        得到单句实体识别结果
        :param sentence: 句子
        :param entity: 实体存储类
        :param dialogic_flag: 对话标记，True标识是新对话，False标识是原对话
        :return: 更新后的实体存储类
        '''
        try:
            if input_filter:
                sentence = optimize_func.input_filter(sentence, 'sentence')
            # 利用地址库识别地址
            NE_dic = Entity_recognition.NE.sent_extract(sentence, dialogic_flag)
            entity.ID = NE_dic["ID"]
            entity.money = NE_dic["money"]
            if config.address_lib:
                entity = optimize_func.address_search(entity, sentence)
            if sentence_context:
                sentence = optimize_func.sentence_history(sentence, dialogic_flag)
            # print('***********************')
            # print("sentence ", sentence)

            # 命名实体识别
            words, ners = fool.analysis(sentence)

            # print('ners:',ners)

            Logger.log_DEBUG.debug('实体识别结果')
            Logger.log_DEBUG.debug(ners)
            if len(ners[0]) >= 1:
                for ne in ners[0]:
                    ne3_temp = ne[3].replace(' ', '')
                    if ne3_temp in entity.location:
                        continue
                    if ne[2] == 'time' and ne3_temp not in entity.time:
                        entity.time.append(ne3_temp)
                    elif ne[2] == 'location' and ne3_temp not in entity.location:
                        ne3_temp_fil = ne3_temp.replace('呃','').replace('那个','').replace('哪个','').replace('啊','')
                        if len(ne3_temp_fil)>1:
                            entity.location.append(ne3_temp_fil)
                    elif ne[2] == 'person' and ne3_temp not in entity.person:
                        ne3_temp_fil = ne3_temp.replace('呃', '').replace('那个', '').replace('哪个', '').replace('啊', '')
                        if len(ne3_temp_fil)>1:
                            entity.person.append(ne3_temp_fil)
                    elif ne[2] == 'company' and ne3_temp not in entity.company:
                        ne3_temp_fil = ne3_temp.replace('呃', '').replace('那个', '').replace('哪个', '').replace('啊', '')
                        if len(ne3_temp_fil)>1:
                            entity.company.append(ne3_temp_fil)

            # print('entity.location:',entity.location)
            # print('***********************')

            if config.is_filter:
                entity = optimize_func.filter_result(sentence,entity)
            return entity
        except Exception as e:
            s = "得到单句实体识别结果时发生异常get_entity_recognit_sentence" + str(e)
            Logger.log_ERROR.error(s)
            Logger.log_ERROR.exception(sys.exc_info())
            raise TypeError(s)

    def get_entity_recognit_paragraph(self, paragraph, entity, input_filter=True, sentence_context=False):
        '''
        得到段落实体识别结果
        :param paragraph: 段落中的句子list
        :param entity: 实体存储类
        :return: 更新后的实体存储类
        '''
        try:
            if input_filter:
                paragraph = optimize_func.input_filter(paragraph, 'paragraph')
            NE_dic = Entity_recognition.NE.doc_extract(paragraph)
            entity.ID = NE_dic["ID"]
            entity.money = NE_dic["money"]
            if sentence_context:
                paragraph = optimize_func.join_sentence(paragraph)
            for sentence in paragraph:
                # print('***********************')
                # print("sentence ", sentence)


                if config.address_lib:
                    entity = optimize_func.address_search(entity,sentence)
                words, ners = fool.analysis(sentence)

                # print ('ners：',ners)

                Logger.log_DEBUG.debug('实体识别结果')
                Logger.log_DEBUG.debug(ners)
                if len(ners[0]) >= 1:
                    for ne in ners[0]:
                        ne3_temp = ne[3].replace(' ', '')
                        if ne3_temp in entity.location:
                            continue
                        if ne[2] == 'time' and ne3_temp not in entity.time:
                            entity.time.append(ne3_temp)
                        elif ne[2] == 'location' and ne3_temp not in entity.location:
                            ne3_temp_fil = ne3_temp.replace('呃', '').replace('那个', '').replace('哪个', '').replace('啊', '')
                            if len(ne3_temp_fil)>1:
                                entity.location.append(ne3_temp_fil)
                        elif ne[2] == 'person' and ne3_temp not in entity.person:
                            ne3_temp_fil = ne3_temp.replace('呃', '').replace('那个', '').replace('哪个', '').replace('啊', '')
                            if len(ne3_temp_fil)>1:
                                entity.person.append(ne3_temp_fil)
                        elif ne[2] == 'company' and ne3_temp not in entity.company:
                            ne3_temp_fil = ne3_temp.replace('呃', '').replace('那个', '').replace('哪个', '').replace('啊', '')
                            if len(ne3_temp_fil)>1:
                                entity.company.append(ne3_temp_fil)
                # print('entity.location: ',entity.location)
                # print('***********************')
            if config.is_filter:
                text_par = "，".join(paragraph)
                entity = optimize_func.filter_result(text_par,entity)
            # print('time:', entity.time)
            # print('person:', entity.person)
            # print('location', entity.location)
            # print('company', entity.company)
            # print('ID', entity.ID)
            # print('money', entity.money)
            return entity
        except Exception as e:
            s = "读得到段落实体识别结果时发生异常get_entity_recognit_paragraph" + str(e)
            Logger.log_ERROR.error(s)
            Logger.log_ERROR.exception(sys.exc_info())
            raise TypeError(s)

    def get_json_string(self, entity):
        '''
        将实体类转成json字符串
        :param entity: 实体存储类
        :return:
        '''
        try:
            result = {}
            result['time'] = ','.join(entity.time)
            result['location'] = ','.join(entity.location)
            result['person'] = ','.join(entity.person)
            result['company'] = ','.join(entity.company)
            result['ID'] = entity.ID
            result['money'] = entity.money
            result['state'] = 'success'
            Logger.log_DEBUG.info('返回的结果：')
            Logger.log_DEBUG.info(result)
            return jsonify(result)
        except Exception as e:
            s = "将实体类转成json字符串时发生异常get_json_string" + str(e)
            Logger.log_ERROR.error(s)
            Logger.log_ERROR.exception(sys.exc_info())
            raise TypeError(s)

    def get_string(self, entity):
        '''
        将实体类转成json字符串
        :param entity: 实体存储类
        :return:
        '''
        try:
            result = []
            result.append('success')
            if ','.join(entity.time)!='':
                result.append(','.join(entity.time))
            else:
                result.append('null')
            if ','.join(entity.location) != '':
                result.append(','.join(entity.location))
            else:
                result.append('null')
            if ','.join(entity.person) != '':
                result.append(','.join(entity.person))
            else:
                result.append('null')
            if ','.join(entity.company) != '':
                result.append(','.join(entity.company))
            else:
                result.append('null')
            if entity.ID != '':
                    result.append(entity.ID)
            else:
                    result.append('null')
            if entity.money != '':
                result.append(entity.money)
            else:
                result.append('null')

            return '##'.join(result)
        except Exception as e:
            s = "将实体类转成字符串时发生异常get_string" + str(e)
            Logger.log_ERROR.error(s)
            Logger.log_ERROR.exception(sys.exc_info())
            raise TypeError(s)
if __name__ == '__main__':
    entity = Entity()
    ER = Entity_recognition()
    text = "浙江远传技术有限公司位于杭州,浙江属于江南"
    entity = ER.get_entity_recognit_sentence(text, entity,True)
    print('time:',entity.time)
    print('person:',entity.person)
    print('location',entity.location)
    print('company',entity.company)
    print('ID',entity.ID)
    print('money',entity.money)


    # text = ["喂张先生您好我这边是上海华瑞银行的您在青客租房的时候有办理了我行租金分期贷款业务",
    #         "浙江省杭州市滨江区",
    #         "和您做一下信息核实方便吗",
    #         "哦行好的",
    #         "那请问一下您的地址是",
    #         "杭州",
    #         "请问您的姓名是",
    #         "居可宁任职于浙江远传",
    #         "你的公司名字是",
    #         "浙江远传技术",
    #         "是的二十三个月的我说我不是写的写的是一年的吗一下",
    #         "身份证号1046",
    #         "一共900元"]
    # text = ["您的地是",
    #         "涌泉",
    #         '他的名字是']
    # entity = Entity()
    # ER = Entity_recognition()
    # entity = ER.get_entity_recognit_paragraph(text, entity)
    # print('time:',entity.time)
    # print('person:',entity.person)
    # print('location',entity.location)
    # print('company',entity.company)
    # print('ID',entity.ID)
    # print('money',entity.money)
