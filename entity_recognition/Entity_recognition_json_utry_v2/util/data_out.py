import pandas as pd
import os
import json
import codecs
import time
import requests


#测试结果批量输出
def GetFileList(dir, fileList, fileNewList):
    for s in os.listdir(dir):
        if len(s) <= 6:
            fDir = os.path.join(dir, s)
            fileList.append(fDir)
        else:
            newDir = os.path.join(dir, s)
            fileNewList.append(newDir)
    return fileList, fileNewList


def test_sentence(line, flag):
    user_info = {}
    user_info['text_type'] = 'sentence'
    user_info['text'] = line
    user_info['dialogic_flag'] = flag
    data = json.dumps(user_info)
    headers = {'Content-Type': 'application/json'}
    # r = requests.post("http://10.0.12.112:6000/", headers =headers, data=data)
    r = requests.post("http://10.0.12.113:3000/", headers=headers, data=data)
    r = json.loads(r.text)
    return r

def test_paragraph(text):

    user_info = {}
    text="##".join(text)
    user_info['text_type'] = 'paragraph'
    user_info['text'] = text
    data = json.dumps(user_info)
    headers = {'Content-Type': 'application/json'}
    # r = requests.post("http://10.0.12.112:6000/", headers=headers, data=data)
    r = requests.post("http://10.0.12.113:3000/", headers=headers, data=data)
    r = json.loads(r.text)
    return r



if __name__ == '__main__':
    # 处理多篇文档
    doc_list,_ = GetFileList('data\\checkdata', [], [])
    text_out = []
    time = []
    location = []
    person = []
    company = []
    ID = []
    money = []
    for d in doc_list:
        text = []
        with open(d,encoding='utf-8') as f:
            for line in f.readlines():
                line_r=line.replace('\n','').replace('\r','')
                text.append(line_r)

        print (len(text))
        r = test_paragraph(text)
        time.append(r['time'])
        location.append(r['location'])
        person.append(r['person'])
        company.append(r['company'])
        ID.append(r['ID'])
        money.append(r['money'])
        text_out.append(text)
    sent_path = 'data/doc_result.xlsx'
    writer = pd.ExcelWriter(sent_path)
    result = pd.DataFrame(data={'text': text_out, 'money': money,
                                'time': time, 'location': location,
                                'person': person, 'company': company,
                                'ID': ID, })
    order = ['text', 'time', 'location', 'person', 'company', 'money', 'ID']
    result = result[order]
    result.to_excel(writer, 'Sheet1', index=False)
    writer.save()


    # # 多篇单句话处理
    # doc_list, _ = GetFileList('data\\checkdata', [], [])
    # line_out = []
    # time = []
    # location = []
    # person = []
    # company = []
    # ID = []
    # money = []
    # print(doc_list)
    # for d in doc_list:
    #     flag = True
    #     with open(d,encoding='utf-8') as f:
    #         for line in f.readlines():
    #             r = test_sentence(line, flag)
    #             flag = False
    #             time.append(r['time'])
    #             location.append(r['location'])
    #             person.append(r['person'])
    #             company.append(r['company'])
    #             ID.append(r['ID'])
    #             money.append(r['money'])
    #             line_out.append(line)
    #
    # sent_path = 'data/doc_sent_result.xlsx'
    # writer = pd.ExcelWriter(sent_path)
    # result = pd.DataFrame(data={'sentences': line_out, 'money': money,
    #                             'time':time,'location':location,
    #                             'person':person,'company':company,
    #                             'ID': ID,})
    # order = ['sentences','time','location','person','company','money', 'ID']
    # result = result[order]
    # result.to_excel(writer, 'Sheet1', index=False)
    # writer.save()

    # # 单篇单句话处理
    # train_path = 'data/checkdata/sentence.txt'
    # line_out = []
    # time = []
    # location = []
    # person = []
    # company = []
    # ID = []
    # money = []
    # flag = True
    # with open(train_path,encoding='utf-8') as f:
    #     for line in f.readlines():
    #         line_re = line.replace('\n','').replace('\r','')
    #         r = test_sentence(line_re, flag)
    #         flag = False
    #         time.append(r['time'])
    #         location.append(r['location'])
    #         person.append(r['person'])
    #         company.append(r['company'])
    #         ID.append(r['ID'])
    #         money.append(r['money'])
    #         line_out.append(line)
    # sent_path = 'data/sent_result.xlsx'
    # writer = pd.ExcelWriter(sent_path)
    # result = pd.DataFrame(data={'sentences': line_out, 'money': money,
    #                             'time': time, 'location': location,
    #                             'person': person, 'company': company,
    #                             'ID': ID, })
    # order = ['sentences', 'time', 'location', 'person', 'company', 'money', 'ID']
    # result = result[order]
    # result.to_excel(writer, 'Sheet1', index=False)
    # writer.save()


