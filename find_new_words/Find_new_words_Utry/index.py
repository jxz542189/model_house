# coding:utf-8
import sys
import json
from flask import Flask
from flask import request
from flask import jsonify
import traceback
from my_log_new import Logger
from file_server3x import fileServer
import demo_file_server as dfs
import config

# nohup gunicorn -c gun.py index:app &
app = Flask(__name__)
file = None


def find_new_word(request, is_upload=False):
    global file
    try:
        Logger.log_DEBUG.info('-------开始识别-------')
        data = request.data  # 获取字符串
        j_data = json.loads(data.decode("utf-8"))  # 转成json
        # j_data = json.loads(data)#转成json
        Logger.log_DEBUG.debug('接收到的信息-----：')
        Logger.log_DEBUG.debug(j_data)
        #r = file.get_api_ticket()
        stopwordID = ''
        dicwordID = ''
        dataID = ''
        N = config.N
        PMI = config.PMI_limit
        if 'stopwordID' not in j_data or 'dicwordID' not in j_data:
            # file = FileServer()
            # file.get_api_ticket()
            return jsonify(
                {'state': '参数不全，前检查文件ID（stopwordID，dicwordID）!!!', 'trace': '参数不全，前检查文件ID（stopwordID，dicwordID）!!!'})
        else:
            stopwordID = j_data.get('stopwordID')
            dicwordID = j_data.get('dicwordID')
        if 'N' in j_data:
            N = int(j_data.get('N'))
        if 'PMI' in j_data:
            PMI = int(j_data.get('PMI'))
        # 判断是否需要读取文件
        text = ''
        dataID = ''
        if 'dataID' in j_data:
            dataID = j_data.get('dataID')
        else:
            if 'text' in j_data:
                text = j_data.get('text')

        r, PMI_min, PMI_max = dfs.get_new_word_string(file, stopwordID, dicwordID, dataID, text, N, PMI)
        Logger.log_DEBUG.debug('新词：' + r)
        Logger.log_DEBUG.debug('互信息最小值：' + str(PMI_min))
        Logger.log_DEBUG.debug('互信息最大值：' + str(PMI_max))
        r_dic = {}
        r_dic['state'] = 'success'
        r_dic['trace'] = 'success'
        r_dic['PMI_min'] = str(PMI_min)
        r_dic['PMI_max'] = str(PMI_max)
        if is_upload:
            id = file.upload_file_by_data(r)
            r_dic['newWordString'] = ''
            r_dic['newWordFileID'] = id
        else:
            r_dic['newWordString'] = r
            r_dic['newWordFileID'] = ''
        return jsonify(r_dic)
    except Exception as e:
        s = "获取新词发生异常find_new_word" + str(e)
        Logger.log_ERROR.error(s)
        Logger.log_ERROR.exception(sys.exc_info())
        return jsonify({'state': '新词查找失败!!!', 'trace': traceback.format_exc()})


# @app.route('/')
@app.route('/ID', methods=['POST'])
def get_newWord_fileID():
    return find_new_word(request, True)


@app.route('/str', methods=['POST'])
def get_newWord_string():
    return find_new_word(request, False)


@app.route('/text_str', methods=['POST'])
def get_newWord_string_text():
    return find_new_word(request, False)


@app.route('/fileserver', methods=['post'])
def file_server():
    global file
    try:
        try:
            temp_data = request.data  # 获取字符串
            Logger.log_DEBUG.debug('接收到的data：')
            Logger.log_DEBUG.debug(temp_data)
            json_data = json.loads(temp_data.decode("utf-8"))
            Logger.log_DEBUG.debug('解析后的data：')
            Logger.log_DEBUG.debug(json_data)
        except Exception as e:
            Logger.log_DEBUG.warning("请求失败或请求加载失败!!!")
            return jsonify({"state": "请求失败或请求加载失败!!!",
                            'trace': traceback.format_exc()})
        if 'ip' not in json_data or 'up_url' not in json_data or \
                'down_url' not in json_data or 'access_url' not in json_data or \
                'access_key' not in json_data or '_init_companyId' not in json_data:
            # file = FileServer()
            # file.get_api_ticket()
            return jsonify({'state': '参数不全，文件服务器配置失败!!!', 'trace': '参数不全，文件服务器配置失败!!!'})
        else:
            ip = json_data['ip']
            up_url = json_data['up_url']
            down_url = json_data['down_url']
            access_url = json_data['access_url']
            access_key = json_data['access_key']
            _init_companyId = json_data['_init_companyId']
            file = fileServer(ip, up_url, down_url, access_url, access_key, _init_companyId)
            api_ticket = file.get_api_ticket()
            if not api_ticket:
                Logger.log_DEBUG.warning("Error--------------获取accessToken错误")
                return jsonify(
                    {'state': "Error--------------获取accessToken错误", 'trace': "Error--------------获取accessToken错误"})
            return jsonify({'state': 'success', 'trace': 'success'})
    except Exception:
        Logger.log_DEBUG.warning('不可用文件服务器!!!')
        return jsonify({"state": '不可用文件服务器!!!',
                        'trace': traceback.format_exc()})

# if __name__ == '__main__':
#     # app.run(debug=True)
#     # app.run(host='127.0.0.1', port=5001, process=4)
#     app.run(host='127.0.0.1', port=3000)
