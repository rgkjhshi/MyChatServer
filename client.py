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

import socket
import time


HOST = '127.0.0.1'    # The remote host
PORT = 8000           # The same port as used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
s.connect((HOST, PORT))

offlineMessage = """
    {
        "action"   : "chatmessage",
        "fromID"   : "test01@qq.com",
        "toID"     : "313832830@qq.com",
        "message"  : "哈哈哈哈大侠啊谁来的快放假啊；士大夫",
        "end"      : "end"
    }
    """
register = """
    {
        "action"   : "register",
        "username" : "test01@qq.com",
        "password" : "shisong",
        "name"     : "石松",
        "gender"   : 0,
        "end"      : "end"
    }
    """
login = """
    {
        "action"   : "login",
        "username" : "313832830@qq.com",
        "password" : "shisong",
        "end"      : "end"
    }
    """
data2='''{"action" : "regisger", "username" : "test01@qq.com", "password" : "shisong", "name" : "石松", "gender" : 0, "end" : "end"}'''


s.sendall(login)
print 'send:', login
time.sleep(1)  
data = s.recv(1024)
print 'Received', data # repr(data)

time.sleep(1)  
s.close()  