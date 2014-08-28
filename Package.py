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
import types

####################################################################################
# 接收包协议
####################################################################################
# 所有包的父类
class Package(object):

    def __init__(self):
        self.action = ''
        self.end = 'end'

    def parser(self, datas):
        for (k , v) in datas.items():                                        # datas里的属性
            try:
                if  type(self.__getattribute__(k)) is not types.NoneType:    # 若Package也有该属性并且不时None，则更新其值。
                    self.__setattr__(k, v)
            except AttributeError:                                           # 若没有该属性，抛出AttributeError，捕捉到之后不作处理
                pass                                                         # 相当于有该属性则更新，没有则不处理

    def __str__(self):
        return "%s" % self.__dict__

# 普通请求包
# 注册
class RegisterPackage(Package):
    """
    {
        "action"   : "regisger",
        "username" : "tom@126.com",
        "password" : "********",
        ...
        "end"      : "end"
    }
    """
    def __init__(self):
        super(RegisterPackage, self).__init__()

        self.username = ''
        self.password = ''

# 登录
class LoginPackage(Package):
    """
    {
        "action"   : "login",
        "username" : "michael@126.com",
        "password" : "********",
        "end"      : "end"
    }
    """
    def __init__(self):
        super(LoginPackage, self).__init__()

        self.username = ''
        self.password = ''

# 添加好友申请
class AddFriendRequestPackage(Package):
    """
    {
        "action"     : "addfriendRequest",
        "username"   : "michael@126.com",
        "friendname" : "tom@126.com",
        "message"    : "Hello!",
        "end"        : "end"
    }
    """
    def __init__(self):
        super(AddFriendRequestPackage, self).__init__()

        self.username = ''            # 发起人
        self.friendname = ''          # 要加的人
        self.message = ''

# 对好友请求的回应，这个包主要用在客户端
class AddFriendResponsePackage(Package):
    """
    {
        "action"     : "addfriendResponse",
        "username"   : "michael@126.com",
        "friendname" : "tom@126.com",
        "status"     : 0
        "message"    : "Hello!",
        "end"        : "end"
    }
    """
    def __init__(self):
        super(AddFriendRequestPackage, self).__init__()

        self.username = ''           # 申请的发起人
        self.friendname = ''         # 回复的人
        self.status = 0              # 是否同意用数字1和0表示，1表示同意，默认为0
        self.message = ''

# 删除好友
class DeleteFriendPackage(Package):
    """
    {
        "action"     : "deletefriend",
        "username"   : "michael@126.com",
        "friendname" : "tom@126.com",
        "end"        : "end"
    }
    """
    def __init__(self):
        super(DeleteFriendPackage , self).__init__()

        self.username = ''
        self.friendname = ''


# 获取好友列表
class GetRosterPackage(Package):
    """
    {
        "action"     : "getroster",
        "username"   : "michael@126.com",
        "end"        : "end"
    }
    """
    def __init__(self):
        super( GetRosterPackage, self ).__init__()

        self.username = ''

# 获取用户详细信息
class GetUserInfoPackage(Package):
    """
    {
        "action"     : "getuserinfo",
        "username"   : "michael@126.com",
        "end"        : "end"
    }
    """
    def __init__(self):
        super(GetUserInfoPackage , self).__init__()

        self.username = ''

# 聊天信息
class ChatMessagePackage(Package):
    """
    {
        "action"     : "chatmessage",
        "fromuser"       : "michael@126.com",
        "touser"         : "tom@126.com",
        "message"    : "hello",
        "end"        : "end"
    }
    """
    def __init__(self):
        super (ChatMessagePackage , self).__init__()

        self.fromuser = ''
        self.touser = ''
        self.message = ''


####################################################################################
# 应答包协议
####################################################################################
# 错误
class ErrorPackage(Package):
    """
    {
        "action"   : "error",
        "username" : "tom@126.com",
        "message"  : "404:not found"
        "end"      : "end"
    }
    """
    def __init__(self):
        super(ErrorPackage, self).__init__()

        self.username = ''
        self.message  = ''


# 所有需要回应的包的父类
class ReplyPackage(Package):
    """
    {
        "action"   : "reply",
        "type"     : "addFriend"
        "status"   : 1
        "message"  : ""
        子类自行扩展...
        "end"      : "end"
    }
    """
    def __init__(self):
        super(ReplyPackage, self).__init__()

        self.action = 'reply'
        self.type = ''
        self.status = 1    # 所有应答包，数字1表示正确，0表示错误，默认为1
        self.message = ''


# 注册反馈
class RegisterReplyPackage(ReplyPackage):
    """
    {
        "action"   : "reply",
        "type"     : "register"
        "status"   : 1
        "message" : ""
        "end"      : "end"
    }
    """
    def __init__(self):
        super(RegisterReplyPackage, self).__init__()

        self.type = 'register'

# 登录反馈
class LoginReplyPackage(ReplyPackage):
    """
    {
        "action"   : "reply",
        "type"     : "login"
        "status"   : 1
        "message"  : ""
        "end"      : "end"
    }
    """
    def __init__(self):
        super(LoginReplyPackage, self).__init__()

        self.type = 'login'

# 获取好友列表反馈
class GetRosterPackage(ReplyPackage):
    """
    {
        "action"   : "reply",
        "type"     : "getRoster"
        "status"   : 1
        "message" : ""
        "end"      : "end"
    }
    """
    def __init__(self):
        super(GetRosterPackage, self).__init__()

        self.type = 'getRoster'

# 获取用户详细信息反馈
class GetUserInfoPackage(ReplyPackage):
    """
    {
        "action"   : "reply",
        "type"     : "getUserInfo"
        "status"   : 1
        "message" : ""
        "end"      : "end"
    }
    """
    def __init__(self):
        super(GetUserInfoPackage, self).__init__()

        self.type = 'getUserInfo'

# 下面这两个比较特殊，不是发给当前用户，而是发给对方用户
# 对好友申请的反馈，应该反馈给被加的人
class AddFriendRequestReplyPackage(ReplyPackage):
    """
    {
        "action"     : "reply",
        "type"       : "addFriendRequest"
        "status"     : 1
        "message"    : "加好友的附加消息"
        "username"   : ""
        "friendname" : ""
        "end"        : "end"
    }
    """
    def __init__(self):
        super(AddFriendRequestReplyPackage, self).__init__()

        self.username = ''            # 发起人的账号
        self.friendname = ''          # 被加的人
        self.status = None            # status在这里没有意义

# 好友申请回应的反馈，应该反馈给发起好友申请的人
class AddFriendResponseReplyPackage(ReplyPackage):
    """
    {
        "action"     : "reply",
        "type"       : "addFriendResponse"
        "status"     : 1
        "message"    : "回应的附加消息"
        "username"   : ""
        "friendname" : ""
        "end"        : "end"
    }
    """
    def __init__(self):
        super(AddFriendResponseReplyPackage, self).__init__()

        self.username = ''           # 申请的发起人
        self.friendname = ''         # 回复的人
        self.status = 0              # 是否同意用数字1和0表示，1表示同意，默认为0

