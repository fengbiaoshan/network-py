#!/usr/bin/env python
# coding:utf-8

#Author: Mi Zhangpeng

import requests
import json
import threading

# 字典allusers用于存储 由 索引名和openID构成的键值对
# 微信关注‘测试号’时，会生成openID用于与对应微信账号通讯
# 索引名 是为了便于自己识别和管理而对openID起的别名
allusers = {'昵称':'对应编号'}

def usersto(users = None):
    if users == None:
        return allusers['昵称']
    elif users == "All":
        return ','.join(set(allusers.values()))
    else:
        if isinstance(users,list):
            usersinfo = []
            for user in users:
                usersinfo.append(allusers[user])
            return ','.join(set(usersinfo))
        else:
            print "'users' must be a list!"
            return

def json_post_data_generator(content='Hi!你好！',users = None):
    msg_content = {}
    msg_content['content'] = content
    post_data = {}
    post_data['text'] = msg_content
    post_data['touser'] = "%s" % usersto(users)
    post_data['toparty'] = ''
    post_data['msgtype'] = 'text'
    post_data['agentid'] = '9'
    post_data['safe'] = '0'
    #由于字典格式不能被识别，需要转换成json然后在作post请求
    #注：如果要发送的消息内容有中文的话，第三个参数一定要设为False
    return json.dumps(post_data,False,False)

# 需将此处的APPID,APPSECRET换为自己‘测试号管理’页面内显示的内容
def appInfos():
    APPID = "****************"
    APPSECRET = "******************"
    return (APPID,APPSECRET)

def get_token_info():
    APPInfo = appInfos()
    r = requests.get("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % APPInfo)
    #print "Accessing %s" %r.url
    js =  r.json()
    if "errcode" not in js:
        access_token = js["access_token"]
        expires_in = js["expires_in"]
    else:
        print "Can not get the access_token"
        print js
        quit()
    return access_token,expires_in

post_url_freshing = ['']

def post_url():
    access_token,expires_in = get_token_info()
    print "token expires_in:%s" % expires_in
    timer = threading.Timer((expires_in-200),post_url)
    timer.start()
    post_url_freshing[0] = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s' %access_token

post_url()

def sender(text_str,user_lis = None):
    posturl = post_url_freshing[0]
    post_data = json_post_data_generator(content=text_str,users = user_lis)
    r = requests.post(posturl,data=post_data)
    result = r.json()
    if result["errcode"] == 0:
        print "Sent successfully"
    else:
        print result["errmsg"]

if __name__ == "__main__":
    text_str = "你好"
    user_lis = None
    sender(text_str,user_lis)
