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

from tornado.tcpserver import TCPServer
from tornado.ioloop  import IOLoop

import db
from connection import Connection
######################################################################
# ChatServer 继承TCPServer 
######################################################################
class ChatServer(TCPServer):
    r"""
    可通过下面三种方式启动 `ChatServer` :

    1. `listen`: simple single-process::

            server = ChatServer()
            server.listen(8888)
            IOLoop.instance().start()

    2. `bind`/`start`: simple multi-process::

            server = ChatServer()
            server.bind(8888)
            server.start(1)          # 若<=0或者为None，则使用系统允许的最大进程数；若>1,则按给定的进程数
            IOLoop.instance().start()

    3. `add_sockets`: advanced multi-process::

            sockets = bind_sockets(8888)
            tornado.process.fork_processes(0)
            server = ChatServer()
            server.add_sockets(sockets)
            IOLoop.instance().start()
    """

    # 覆盖 TCPServer 的方法，否则会抛 NotImplementedError 异常
    def handle_stream(self, stream, address):
        print "New connection :", address, stream
        Connection(stream, address)


######################################################################
#  测试
######################################################################
if __name__ == '__main__':
    print "ChatServer start ..."
    db.create_engine('root', 'root', 'shisong')     # 数据库连接，其上下文对象时线程独立的
    server = ChatServer()
    server.bind(8000)
    server.start(1)                                 # 由于还没找到办法让多进程共享connections变量，所以目前只能使用单进程
    IOLoop.instance().start()

