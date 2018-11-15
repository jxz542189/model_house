# coding:utf-8
import requests
import datetime
import time
import json
import os
import jieba

def read_data(data_path):
    '''
    读取文件数据测试
    :param data_path: 数据路径
    :return: 数据集字符串，句子之间用“##”分隔
    '''
    data=[]
    if os.path.exists(data_path):
        with open(data_path, 'r', encoding='utf8') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                data.append(line)
        return '##'.join(data)
    else:
        print('date数据集为空请检查数据集文件！！！！！！')
        return data

def file_server_int():
    s_time = time.time()
    ip = '10.0.2.121:80'
    up_url = '/fileManager/api/file/uploadFileP'
    down_url = '/fileManager/api/file/downloadFileP'
    access_url = '/api/gateway/ticket'
    access_key = '33a832d7949c11e89024000c2961e520'
    _init_companyId = '08d181119a7b4c0e94ff368942fd4420'
    user_info = {}
    user_info['ip'] = ip
    user_info['up_url'] = up_url
    user_info['down_url'] = down_url
    user_info['access_url'] = access_url
    user_info['access_key'] = access_key
    user_info['_init_companyId'] = _init_companyId
    #r = requests.post("http://10.0.7.217:3001/fileserver", data=json.dumps(user_info))
    r = requests.post("http://10.0.12.113:3001/fileserver", data=json.dumps(user_info))

    r = json.loads(r.text)
    print('state:' + r['state'])
    time_elapse = time.time() - s_time
    print("新词识别文件服务器初始化耗时: {}s".format(time_elapse))

def test_find_newWord():
    s_time = time.time()
    stopwordID='0243e66ecd1d11e8be95000c2961e520'
    dicwordID='0249d9e0cd1d11e8be95000c2961e520'
    dataID='76842f44cd1d11e8be95000c2961e520'
    N=5
    PMI = 18

    user_info = {}
    user_info['stopwordID'] = stopwordID
    user_info['dicwordID'] = dicwordID
    user_info['dataID']=dataID
    user_info['N'] = str(N)
    user_info['PMI'] = str(PMI)

    # data = json.dumps(user_info)
    # headers = {'Content-Type': 'application/json'}
    # r = requests.post("http://127.0.0.1:3000/",headers =headers, data=data)
    r = requests.post("http://10.0.12.113:3001/str", data=json.dumps(user_info))
    #r = requests.post("http://10.0.7.217:3001/str", data=json.dumps(user_info))
    r = json.loads(r.text)
    print('state:' + r['state'])
    print('trace:' + r['trace'])
    print('PMI_min:' + r['PMI_min'])
    print('PMI_max:' + r['PMI_max'])
    print('newWordString:' + r['newWordString'])
    print('newWordFileID:' + r['newWordFileID'])

    time_elapse = time.time() - s_time
    print("新词识别耗时: {}s".format(time_elapse))

def test_find_newWord_text():
    s_time = time.time()
    stopwordID='0243e66ecd1d11e8be95000c2961e520'
    dicwordID='0249d9e0cd1d11e8be95000c2961e520'
    text=read_data('./data/Questioning_YNNX.txt')
    N=5
    PMI = 18

    user_info = {}
    user_info['stopwordID'] = stopwordID
    user_info['dicwordID'] = dicwordID
    user_info['text']=text
    user_info['N'] = str(N)
    user_info['PMI'] = str(PMI)

    # data = json.dumps(user_info)
    # headers = {'Content-Type': 'application/json'}
    # r = requests.post("http://127.0.0.1:3000/",headers =headers, data=data)
    #r = requests.post("http://10.0.12.112:3000/", data=json.dumps(user_info))
    r = requests.post("http://10.0.7.217:3001/text_str", data=json.dumps(user_info))
    r = json.loads(r.text)
    print('state:' + r['state'])
    print('trace:' + r['trace'])
    print('PMI_min:' + r['PMI_min'])
    print('PMI_max:' + r['PMI_max'])
    print('newWordString:' + r['newWordString'])
    print('newWordFileID:' + r['newWordFileID'])

    time_elapse = time.time() - s_time
    print("新词识别耗时: {}s".format(time_elapse))


file_server_int()
#test_find_newWord_text()
test_find_newWord()


