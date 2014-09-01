#!/usr/bin/env python
# -*- coding: utf-8 -*-

#                       _ooOoo_ 
#                      o8888888o 
#                      88" . "88 
#                      (| -_- |) 
#                      O\  =  /O 
#                   ____/`---'\____ 
#                 .'  \\|     |//  `. 
#                /  \\|||  :  |||//  \ 
#               /  _||||| -:- |||||-  \ 
#               |   | \\\  -  /// |   | 
#               | \_|  ''\---/''  |   | 
#               \  .-\__  `-`  ___/-. / 
#             ___`. .'  /--.--\  `. . __ 
#          ."" '<  `.___\_<|>_/___.'  >'"". 
#         | | :  `- \`.;`\ _ /`;.`/ - ` : | | 
#         \  \ `-.   \_ __\ /__ _/   .-` /  / 
#    ======`-.____`-.___\_____/___.-`____.-'====== 
#                       `=---=' 
#    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ 
#                  佛祖镇楼                  BUG辟易
#        佛曰:
#                  写字楼里写字间，写字间里程序员；
#                  程序人员写程序，又拿程序换酒钱。
#                  酒醒只在网上坐，酒醉还来网下眠；
#                  酒醉酒醒日复日，网上网下年复年。
#                  但愿老死电脑间，不愿鞠躬老板前；
#                  奔驰宝马贵者趣，公交自行程序员。
#                  别人笑我忒疯癫，我笑自己命太贱；
#                  不见满街漂亮妹，哪个归得程序员？

__author__ = 'Michael King'


import db
from package import *


# 多线程共享的变量
# 再主程序中用multiprocessing模块的Manager().dict()对其进行初始化
# connections = Manager().dict()
# 上述方法不太实用，因为没有办法把它作为参数传给TCPserver，因此只能用但进程了，通过全局变量共享connections
connections = dict()

class Handler(object):

    def __init__(self , connection):
        super(Handler , self).__init__()

        self._connection = connection

    # 反馈包，直接发出去
    def replyHandler(self, package):
        pass

    # 加好友的反馈特殊处理
    def addFriendRequestReplyHandler(self, package):
        pass

    def addFriendResponseReplyHandler(self, package):
        pass

    # 普通包，处理
    def registerHandler(self, package):
        registerReply = RegisterReplyPackage()   # 创建回复包
        username = package.username      # 回复包的字段设置
        password = package.password
        name = package.name
        gender = package.gender
        sql = "select * from `ofUser` where username=? "
        res = db.select_one(sql, username)  # 查询数据库是否已经被注册过了
        if res is not None :                # 被注册过，status设为失败，并设置已被注册的信息
            registerReply.status = 0
            registerReply.message = '该邮箱已被注册'
        else :                              # 未被注册过，status设置为成功，并将新用户插入数据库
            table = "ofUser"
            kw = {"username":username, "password":password, "name":name, "gender":gender}
            res = db.insert(table, **kw)
            registerReply.status = 1
            registerReply.message = '注册成功'
        data = json.dumps(registerReply , cls= ComplexEncoder, ensure_ascii=False)     # 把python对象编码成json格式的字符串
        self._connection.send_message(data)  # 向客户端发送回应信息


    def loginHandler(self, package):
        loginReply = LoginReplyPackage()   # 创建回复包
        username = package.username
        password = package.password
        global connections            # 进程共享的变量
        sql = "select * from `ofUser` where username=? and password=? "
        res = db.select_one(sql, username, password)   # 查询数据库，看用户名和密码是否正确
        if res is None :              # 未找到，则用户名或密码不对，设置status为失败
            loginReply.status = 0
        else:                         # 找到，则用户名密码正确；此时可以确保本次登录成功。但除此之外，还需验证是否已经登录过了
            if connections.has_key(username):   # 若已登录过，需先强制之前的登录离线
                errPackage = ErrorPackage()                 # 准备错误信息包
                errPackage.message = '该账号已在其他设备上登录' # 设定错误信息
                errData = json.dumps(errPackage , cls= ComplexEncoder, ensure_ascii=False)     # 把python对象编码成json格式的字符串
                old_connection = connections.pop(username)  # 从connections中删除
                old_connection.send_message(errData)
                # 这里并不直接断开连接，因为由于网络延迟，可能信息还未发送到客户端，若在此直接断开，客户端就无法收到信息了。这就要求客户端收到错误信息时，主动断开
            # 将新的TCP连接记录在connections中
            connections.update({username:self._connection})
        # 返回登录结果信息包
        data = json.dumps(loginReply , cls= ComplexEncoder, ensure_ascii=False)     # 把python对象编码成json格式的字符串
        print "in handler:", type(data)
        print data
        self._connection.send_message(data)  # 向客户端发送登录回应信息
        if loginReply.status :  # 若登录成功，还得检查是否有离线消息，如果有需要经离线消息发送给用户
            sql = "select * from `ofOffline` where toID=? "
            items = db.select(sql, username)   # 查询数据库，得到该用户的离线消息(可能多条)
            for item in items:
                data = item['data'].encode('utf8')
                print "in handler for:", type(data)
                print data
                self._connection.send_message(data)  # 向客户端发送离线消息
                db.update('delete from `ofOffline` where ID=? ', item['ID'])

    def addFriendRequestHandler(self, package):
        pass

    def addFriendResponseHandler(self, package):
        pass

    def deleteFriendHandler(self, package):
        pass

    def getRosterHandler(self, package):
        pass

    def getUserInfoHandler(self, package):
        pass

    def chatMessageHandler(self, package):
        toID   = package.toID
        # 要发送的数据
        data = json.dumps(package , cls= ComplexEncoder, ensure_ascii=False)     # 把python对象编码成json格式的字符串
        # 判断toID是否在线
        if connections.has_key(toID):   # 在线，直接转发
            to_connection = connections.get(toID)
            # 直接将发过来的聊天包转发给toID
            to_connection.send_message(data)
        else :  # 不在线，保存到数据库
            table = "ofOffline"
            kw = {"fromID":package.fromID, "toID":package.toID, "data":data }
            db.insert(table, **kw)

    def errorHandler(self, package):
        pass
