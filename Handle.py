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


from Package import *
import db

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
        pass

    def loginHandler(self, package):
        username = package.username
        password = package.password
        sql = "select * from ofUser where username=? and password=? "
        res = db.select_one(sql, username, password)
        reply = LoginReplyPackage()
        if res is None :
            reply.status = 0

        self._connection.send_message(str(reply))

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
        pass

    def errorHandler(self, package):
        pass
