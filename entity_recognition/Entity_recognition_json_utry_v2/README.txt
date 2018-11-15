1.命令都要在实体识别目录“Entity_recognition_json_utry_pyc”下运行

2.python环境：
python3

3.安装部署：
python使用requirement.txt批量安装包
pip install -r requirement.txt

4.服务启动命令
nohup python tornado_server.pyc &

5.端口号：6006
默认端口号6006，可在config.py中配置，修改"service_port"参数值即可。

6.测试运行环境是否搭建成功：
终端输入命令“python Entity_recognition.pyc”，出现识别结果则运行环境搭建成功。

7.python服务测试命令
note：测试命令中的“url”、“端口号”需根据实际情况调整
1）输入为一句话
curl -H "Content-Type:application/json" -X POST --data '{"text_type":"sentence","text":"杭州市滨江区，水晶城一幢一单元","dialogic_flag":"False"}' http://10.0.12.112:6006/
2）输入为一段话
curl -H "Content-Type:application/json" -X POST --data '{"text_type":"paragraph","text":"请问您的住址是##滨江区水晶城"}' http://10.0.12.112:6006