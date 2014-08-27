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
        self.end = ''

    def parser(self, datas):
        for (k , v) in datas.items():
            try:
                if  type(self.__getattribute__(k)) is not types.NoneType:    # 得到自己已有的属性，然后重新赋值
                    self.__setattr__(k, v)
            except AttributeError:
                pass

    def __str__(self):
        return "%s" % self.__dict__
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
        "action"     : "addfriendrequest",
        "username"   : "michael@126.com",
        "friendname" : "tom@126.com",
        "message"    : "Hello!",
        "end"        : "end"
    }
    """
    def __init__(self):
        super(AddFriendRequestPackage, self).__init__()

        self.username = ''
        self.friendname = ''
        self.message = ''

# 同意或者拒绝添加好友申请
class AddFriendStatusPackage(Package):
    """
    {
        "action"     : "addfriendstatus",
        "username"   : "michael@126.com",
        "friendname" : "tom@126.com",
        "agree"      : 1,   or 0
        "end"        : "end"
    }
    """
    def __init__(self):
        super(AddFriendStatusPackage , self).__init__()

        self.username = ''
        self.friendname = ''
        self.agree = 0

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


# 获取好友列表请求
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
#发送协议
####################################################################################

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj,'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)



class SendToClientPackageRegister(object):

    def __init__(self):
        pass


class SendToClientPackageUser(object):

    def __init__(self , uid, username , sex , description , online = False):

        self.uid = uid
        self.username = username
        self.sex = sex
        self.description = description
        self.online = online


    def reprJSON(self):

        return dict(
            uid = self.uid,
            username = self.username,
            sex = self.sex,
            description = self.description,
            online = self.online,
        )



class SendToClientAddFriend(object):
    """
    添加好友，状态返回
    """
    def __init__(self):
        super(SendToClientAddFriend , self).__init__()
        pass



class SendToClientAddFriendStatusReuest(object):
    """
    添加好友状态返回
    """

    def __init__(self , fromid, toid, username , sex, description, agree):

        self.fromid = fromid
        self.toid = toid
        self.username = username
        self.sex = sex
        self.description = description
        self.agree = agree

    def reprJSON(self):

        return dict(

            fromid = self.fromid,
            toid = self.toid,

            username = self.username,
            sex = self.sex,
            description = self.description,

            agree = self.agree,

        )



class SendToClientPackageRecvAddFriendRequest(object):
    """
    发送有人申请添加消息
    """

    def __init__(self, fromid, username, toid, sex , description, msg, date):

        self.fromid = fromid
        self.toid = toid

        self.username = username
        self.sex = sex
        self.description = description

        self.msg = msg
        self.senddate = date

    def reprJSON(self):

        return dict(
            fromid = self.fromid,
            toid = self.toid,

            username = self.username,
            sex = self.sex,
            description = self.description,

            msg = self.msg,
            senddate = self.senddate.strftime("%Y-%m-%d %H:%M:%S"),
        )



class SendToClientPackageChatMessage(object):

    def __init__(self , fromid = 0, toid = 0, chatmsg = ''):

        self.fromid = fromid
        self.toid = toid
        self.chatmsg = chatmsg

    def reprJSON(self):

        return dict(fromid = self.fromid , toid = self.toid, chatmsg = self.chatmsg)



class SendToClientPackageOfflineChatMessage(object):

    def __init__(self , fromid , toid, msg , senddate):

        self.fromid = fromid
        self.toid = toid
        self.chatmsg = msg
        self.senddate = senddate

    def reprJSON(self):

        return dict(
            fromid = self.fromid,
            toid = self.toid,
            chatmsg = self.chatmsg,
            senddate = self.senddate.strftime("%Y-%m-%d %H:%M:%S"),
        )


class SendToClientUserOnOffStatus(object):
    """
    用户上线下线消息
    """

    def __init__(self , uid, username , sex , description , online):

        self.uid = uid
        self.username = username
        self.sex = sex
        self.description = description
        self.online = online


    def reprJSON(self):

        return dict(
            uid = self.uid,
            username = self.username,
            sex = self.sex,
            description = self.description,
            online = self.online,
        )


class SendToClientPackage(object):

    def __init__(self , action):

        super(SendToClientPackage , self).__init__()

        self.status = 0
        self.errcode = 0

        self.obj = None
        self.action = action

    def reprJSON(self):
        return dict(datas = self.obj, action = self.action , status = self.status, errcode = self.errcode)
 
