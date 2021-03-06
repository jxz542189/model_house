# coding:utf-8
import requests
import datetime
import time
import json
from my_log_new import Logger


def test_sentence():
    s_time = time.time()
    starttime = datetime.datetime.now()
    text = '一共是98元，身份证是8796'
    # text = '杭州是典型的江南水乡'
    user_info = {}
    user_info['text_type'] = 'sentence'
    user_info['text'] = text
    user_info['dialogic_flag']="True"
    data = json.dumps(user_info)
    headers = {'Content-Type': 'application/json'}
    # r = requests.post("http://127.0.0.1:3000/",headers =headers, data=data)
    r = requests.post("http://172.17.255.255:6000/", data=data)
    # r = requests.post("http://10.0.12.113:3000/", data=data)
    r = json.loads(r.text)
    print('time:' + r['time'])
    print('location:' + r['location'])
    print('person:' + r['person'])
    print('company:' + r['company'])
    print('ID:' + r['ID'])
    print('money:' + r['money'])
    print('state:' + r['state'])

    endtime = datetime.datetime.now()
    elapsed = (endtime - starttime)
    print(endtime)
    print("Time used:", elapsed)
    time_elapse = time.time() - s_time
    print ("实体识别耗时: {}s".format(time_elapse))

def test_paragraph():
    s_time = time.time()
    starttime = datetime.datetime.now()

    user_info = {}
    # text = ['客户:啊好的好的呃您有', '客服:之前有了解我申请的是二十三个月的话是资金被现在还业务吗啊好的这个地址是在上海市哪个区', '客服:呃嘉定区', '客户:恩好', '客服:您办理业务时是否有收到物的胁迫渭滨这些情况' ]
    # text = ['嗯嗯', '四五三八', '我', '请问您的住址是', '钱塘帝景', '那请问一下您的房租的之后多长时间呢']
    # text = ['客户:喂', '客服:周小姐您好', '客户:我这边', '客服:是哎你好小姐你好', '客服:恩好我这里是上海华瑞银行的', '客服:您在', '客户:这个时候', '客服:带我行资金分期贷款业务核对一下个人信息的方便吗', '客服:请问您的住址是', '客户:前所村', '客户:呃就是我想说一下是这样的就是我们是在杭州这边', '客户:台州伟星管业公司', '客户:然后钱是一次性付了但是他可能用你们贷款业务你们确实是有这样子的一个', '客户:自己的是吧', '客服:它适合咱们青岛公司这个合作推广这个业务的', '客户:呃就是我们的话我们钱是', '客户:付了', '客户:然后呢挂的还是我们的贷款', '客服:这个业务的话是否这边进口的韩国人跟您介绍过吗', '客户:呃没有这个具体的介绍过', '客服:那我和您先说一下', '客服:您可以再了解一下这个业务的话是指我们银行的话是京东公司做个办的是个小额消费贷款', '客服:喂现在或者是二十三个月的房租先给清河公司', '客服:然后的话呢您这边如果说办理贷款成功的话才可以享受到进口的一个长途会员就是会放假上面会有打折', '客服:哦', '客服:如果说您这边办理成功以后每个月的话您还那个房子的款项', '客服:就是用座机还贷款了', '客服:这个还上了我可以每个月通过客网那边pp还进来', '客户:嗯嗯', '客服:那如果说后面您做出一段时间了这个房子不想再做做的话呢', '客服:您可以到时候他就是帮您做一个贷款结清', '客服:这个处理还款会操作的', '客服:到时候结清之后剩余的款项就不需要客户再去承担还款了所以款项这个金额公司偿还的', '客户:先生您的意思呢就是', '客户:比如我说的是', '客户:呃两个月的', '客户:我到时候我还交了押金押金是全额退了吗', '客服:那这个问题要问还款元这个跟我们贷款是没有关系的', '客服:我们这个基金', '客户:跟你核对信息吧您核对吧', '客服:好', '客服:那我们先确认一下您的身份证号码后四位数字是', '客户:八九四九', '客户:哎不对', '客户:就是我的手机号', '客户:零七五五八三', '客服:好您的房东请问导致后应该是多少钱一个月呢', '客户:呃一九八零', '客服:请问一下就说地址在杭州的哪个区呢', '客户:不上', '客服:好的我跟您再确认一下现在是否已了解办理的就是二十三个月的一个资金分期贷款业务了吗', '客户:嗯暂时了解了', '客服:刚才跟您核对一下您这个', '客服:办理的过程当中', '客服:是否有收到过物的胁迫关闭的情况吗', '客户:就扣扣微信没有', '客户:无脑的话', '客户:我我现在不清楚什么是正确的', '客户:所以我觉得应该也还好', '客服:他', '客户:跟我说', '客服:您说', '客户:嗯他是跟我说就是', '客户:嗯如果我两个月资金到了到时候不足的话', '客户:他们是可以把', '客户:咨询全额', '客户:但是我不知道最后是不是真的可以全额退', '客服:你说的这个的话您说的是否是押金的问题', '客户:对对对所以你这个问题你就是问吧', '客服:因为您先说一下如果我们这个问题需要得到您肯定答复才能做后续的确认的', '客户:如果说您没有这个人没有', '客服:你好', '客服:那您现在是确认办理途径分期贷款业务吗', '客户:对呀', '客服:好那就提交审核了结果出来之后短信通知您请您咨询留意一下', '客户:好谢谢', '客服:好不打扰了再见', '客户:嗯', '客户:嗯再见']
    text = ['客户:那个什么', '客服:喂', '您好张女士这边上海华瑞银行您现在通过我行申请的京客资金分期贷款需要跟您做一个电话核实方便吗', '客户:嗯嗯', '客服:请问您目前住在哪边', '客户:我在滨和家苑这边',
     '客服:啊好您的身份证后四位十', '客户:嗯等我看一下', '客户:嗯嗯', '客户:五二', '客户:二五二哎', '客服:恩好的啊每个月资金是多少呢', '客户:哎等等我我看一下啊因为我不太记得',
     '客户:之前我那个他发给我', '客户:稍等一下啊', '客户:哎', '客户:喂哎请您稍等您说', '客户:啊好的好的呃您有', '客服:之前有了解我申请的是二十三个月的话是资金被现在还业务吗啊好的这个地址是在上海市哪个区',
     '客服:呃嘉定区', '客户:恩好', '客服:您办理业务时是否有收到物的胁迫渭滨这些情况', '客户:没有', '客服:恩好之后跟您确认一下您现在确定要办理亲口资金分期贷款吗', '客户:嗯对的', '客服:恩',
     '客服:好那我这边给您做审批处理了审核结果您留意一下短信通知', '客户:恩好谢谢', '客服:恩不客气不打扰您了祝您生活愉快再见', '客户:恩好']

    text="##".join(text)
    user_info['text_type'] = 'paragraph'
    user_info['text'] = text
    data = json.dumps(user_info)
    headers = {'Content-Type': 'application/json'}
    # r = requests.post("http://10.0.12.112:6000/", headers=headers, data=data)
    # r = requests.post("http://10.0.12.113:3000/", headers=headers, data=data)
    r = requests.post("http://172.17.0.1:6000/", data=data)
    r = json.loads(r.text)
    print('time:' + r['time'])
    print('location:' + r['location'])
    print('person:' + r['person'])
    print('company:' + r['company'])
    print('ID:' + r['ID'])
    print('money:' + r['money'])
    print('state:' + r['state'])

    endtime = datetime.datetime.now()
    elapsed = (endtime - starttime)
    print(endtime)
    print("Time used:", elapsed)
    time_elapse = time.time() - s_time
    print ("实体识别耗时: {}s".format(time_elapse))



test_sentence()
#
# test_paragraph()
