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


import json
from package import *
from handle import Handler

class Router(object):

    ####################################################################################
    # 包的分发路由表
    ####################################################################################
    @staticmethod
    def routePackage(connection , package):

        # Reply包
        if isinstance(package, ReplyPackage):
            # 添加好友的回应要单独处理
            if isinstance(package, AddFriendRequestReplyPackage):
                Handler(connection).addFriendRequestReplyHandler(package)

            elif isinstance(package, AddFriendResponseReplyPackage):
                Handler(connection).addFriendResponseReplyHandler(package)
                
            else :
                Handler(connection).replyHandler(package)

        # 正常的请求包
        elif isinstance(package, RegisterPackage):
            Handler(connection).registerHandler(package)

        elif isinstance(package, LoginPackage):
            Handler(connection).loginHandler(package)

        elif isinstance(package, AddFriendRequestPackage):
            Handler(connection).addFriendRequestHandler(package)

        elif isinstance(package, AddFriendResponsePackage):
            Handler(connection).addFriendResponseHandler(package)

        elif isinstance(package, DeleteFriendPackage):
            Handler(connection).deleteFriendHandler(package)

        elif isinstance(package, GetRosterPackage):
            Handler(connection).getRosterHandler(package)

        elif isinstance(package, GetUserInfoPackage):
            Handler(connection).getUserInfoHandler(package)

        elif isinstance(package, ChatMessagePackage):
            Handler(connection).chatMessageHandler(package)
        # 错误的请求包
        else :
            Handler(connection).errorHandler(package)
