# coding:utf-8
import sys
import json
from flask import Flask
from flask import request
from flask import jsonify
from Entity_recognition import Entity
from Entity_recognition import Entity_recognition
from my_log_new import Logger


#gunicorn -c gun.py index:app
app = Flask(__name__)

# @app.route('/')
@app.route('/', methods=['POST'])
def application():
    try:
        Logger.log_DEBUG.info('-------开始识别-------')
        entity = Entity()
        ER = Entity_recognition()
        # 句子和段落标识
        data = request.data#获取字符串
        j_data = json.loads(data.decode("utf-8"))  # 转成json
        #j_data = json.loads(data)#转成json
        Logger.log_DEBUG.debug('接收到的信息-----：' )
        Logger.log_DEBUG.debug(j_data)
        text_type = j_data.get('text_type')
        Logger.log_DEBUG.debug('待提取text类型-----' + text_type)
        if text_type == 'paragraph':  # 段落
            text = j_data.get('text')
            test_list = text.split('##')
            Logger.log_DEBUG.debug('本次识别段落总共有%d个句子' % len(test_list))
            entity = ER.get_entity_recognit_paragraph(test_list, entity)
            result = ER.get_json_string(entity)
        elif text_type == 'sentence':  # 单句
            text = j_data.get('text')
            Logger.log_DEBUG.debug('待提取句子为：' + text)
            dialogic_flag = j_data.get('dialogic_flag')#是否是新对话标记
            if dialogic_flag=="True":
                entity = ER.get_entity_recognit_sentence(text, entity,True)
            else:
                entity = ER.get_entity_recognit_sentence(text, entity,False)
            result = ER.get_json_string(entity)
        else:
            Logger.log_DEBUG.info('参数不对提取提取失败！！！！')
            result =  jsonify({'state': "fail"})

        Logger.log_DEBUG.info('-------识别结束-------')
        return result
    except Exception as e:
        s = "得到命名实体发生异常application" + str(e)
        Logger.log_ERROR.error(s)
        Logger.log_ERROR.exception(sys.exc_info())
        raise TypeError(s)


if __name__ == '__main__':
    # app.run(debug=True)
    # app.run(host='127.0.0.1', port=5001, process=4)
    app.run(host='10.0.12.112', port=6000)
