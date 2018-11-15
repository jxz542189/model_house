# encoding=utf-8

import requests
import json
import traceback
import time
import config


class fileServer:
    # 初始化方法一
    def __init__(self, ip, up_url, down_url, access_url, access_key, _init_companyId):
        self.ip = "http://" + ip
        self.up_url = self.ip + up_url
        self.down_url = self.ip + down_url
        self.access_url = self.ip + access_url
        self.accessKey = access_key
        self._init_companyId = _init_companyId

    # 初始化方法二
    # def __init__(self):
    #     c = config.ReadConfig()
    #     #self.up_url = up_url
    #     #self.down_url = down_url
    #     self.ip="http://"+c.get_config_value("ip")
    #     self.up_url =self.ip+c.get_config_value("up_url")
    #     self.down_url = self.ip+c.get_config_value("down_url")
    #     self.access_url =self.ip+ c.get_config_value("access_url")
    #     self.accessKey = c.get_config_value("access_key")
    #     self._init_companyId = c.get_config_value("_init_companyId")

    def get_api_ticket(self):
        try:
            url = self.access_url + "?accessKey=" + self.accessKey
            # 票据
            # headers = {'accessToken': self.accessToken}
            r = requests.get(url)
            p = r.text  # .encode('utf-8')
            ret = json.loads(p)
            self.api_ticket = ret['data']
            return self.api_ticket
        except:
            print("Error--------------get accessToken,maybe some parameters are error or service is not on")
            print(traceback.format_exc())

    # 通过文件内容上传文件服务器
    # file_data的数据类型-----><type 'str'>
    def upload_file_by_data(self, file_data):

        # file_name = 'AI'
        # 表单数据
        # data ={'fileName':file_name}
        # 文件数据
        # if file_data is None:
        #     print('file data is None')
        #     return None

        files = {'file': file_data}
        # 票据
        headers = {'api-ticket': self.api_ticket,
                   '_init_companyId': self._init_companyId
                   }
        try:

            r = requests.post(self.up_url, headers=headers, files=files)
            p = r.text  # .encode('utf-8')
            # 将string转成dict
            ret_dict = json.loads(p)
            # return ret_dict['data']['fileId']
            print('upload file ,return content : ' + p)  # .decode('utf-8'))
            data = ret_dict['fileAttributes']['fileId']
            return data
        except:
            print("Error--------------upload file to file-server error")
            print(traceback.format_exc())

    # 根据id和类型判断取出的文件是什么内容的
    def download_file_by_id(self, id):
        try:
            url = self.down_url + "?fileId=" + id
            # 票据
            headers = {'api-ticket': self.api_ticket,
                       '_init_companyId': self._init_companyId
                       }
            r = requests.get(url, headers=headers)
            # p =r.text.encode('utf-8')
            p = r.text
            return p
        except:
            print("Error--------------down file from file-server error")
            print(traceback.format_exc())


if __name__ == '__main__':
    file = fileServer(config.ip, config.up_url, config.down_url, config.access_url, config.access_key,
                      config._init_companyId)
    r = file.get_api_ticket()
    # print(r)
    # path = u"data/reset2.csv"
    # file_data = []
    #
    # with open(path, "rb") as f:
    #     file_data = f.read()
    #     f.close()
    # # with open(path, 'r', encoding='utf8') as f:
    # #     lines = f.readlines()
    # #     for line in lines:
    # #         file_data.append(line.strip())
    # f.close()
    # print(file_data)
    # print(type(file_data))
    # # 上传文件
    # file.get_api_ticket()
    # # id = file.upload_file_by_data('##'.join(file_data))
    # id = file.upload_file_by_data(file_data)
    # print(id)
    id = 'f29a110dcc3b11e8be95000c2961e520'
    # 根据id下载文件
    text = file.download_file_by_id(id)
    print(text)
    print(type(text))

    from io import StringIO
    import pandas as pd
    TESTDATA = StringIO(text)
    print (TESTDATA)
    df = pd.read_csv(TESTDATA, sep=",")
    print (df)
