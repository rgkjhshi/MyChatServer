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


# from multiprocessing import Manager

from router import Router
from package import Package

######################################################################
# 连接 
######################################################################
class Connection(object):
    def __init__(self, stream, address):
        self._stream = stream
        self._address = address
        self._stream.set_close_callback(self.on_close)            # 继承自IOStream，连接关闭时的回调函数
        self.read_message()

    # 读取数据
    def read_message(self):
        r"""
        参数中的stream为IOStream对象，有四个常用方法:
        class IOStream(object):
            def read_until(self, delimiter, callback): 
            def read_bytes(self, num_bytes, callback, streaming_callback=None): 
            def read_until_regex(self, regex, callback): 
            def read_until_close(self, callback, streaming_callback=None): 
            def write(self, data, callback=None):
        """
        self._stream.read_until_regex(r'"end"\s*:\s*"end"\s*}', self.handle_message)  # 读取完指定内容后，交给处理函数

    # 处理函数
    def handle_message(self, data):
        package = Package.decodePackage(data)
        Router.routePackage(self , package)
        # 处理完毕后，继续读取内容
        self.read_message()

    # 发送信息
    def send_message(self, data):
        self._stream.write(data)

    # 连接断开时的回调
    def on_close(self):
        print "A user has left the chat room.", self._address
        self._stream.close()

