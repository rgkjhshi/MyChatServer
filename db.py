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

'''
Database operation module.
'''

import time, functools, threading, logging

# Dict object:

class Dict(dict):
    '''
    Simple dict but support access as x.y style.

    >>> d1 = Dict()
    >>> d1['x'] = 100
    >>> d1.x
    100
    >>> d1.y = 200
    >>> d1['y']
    200
    >>> d2 = Dict(a=1, b=2, c='3')
    >>> d2.c
    '3'
    >>> d2['empty']
    Traceback (most recent call last):
        ...
    KeyError: 'empty'
    >>> d2.empty
    Traceback (most recent call last):
        ...
    AttributeError: 'Dict' object has no attribute 'empty'
    >>> d3 = Dict(('a', 'b', 'c'), (1, 2, 3))
    >>> d3.a
    1
    >>> d3.b
    2
    >>> d3.c
    3
    '''
    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

# 自定义异常
class DBError(Exception):
    pass

class MultiColumnsError(DBError):
    pass

# 类定义，数据库连接的上下文，local对象，每个线程的内容都不一样
class _DbCtx(threading.local):
    '''
    Thread local object that holds connection info.
    '''
    def __init__(self):
        self.connection = None
        self.transactions = 0

    def is_init(self):
        return not self.connection is None

    def init(self):
        self.connection = engine.connect()
        # logging.info('open connection <%s>...' % hex(id(self.connection)))
        self.transactions = 0

    def cleanup(self):
        if self.connection:
            # logging.info('close connection <%s>...' % hex(id(self.connection)))
            self.connection.close()
            self.connection = None

    def cursor(self):
        if self.connection is None:
            self.init()
        return self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

# thread-local db context:
_db_ctx = _DbCtx()

# global engine object:
# engine 本身就是
engine = None

# 类定义
class _Engine(object):

    def __init__(self, connect):
        self._connect = connect

    def connect(self):
        return self._connect()

# 对外函数
def create_engine(user, passwd, db, host='127.0.0.1', port=3306, **kw):
    import MySQLdb
    global engine
    if engine is not None:
        raise DBError('Engine is already initialized.')
    params = dict(user=user, passwd=passwd, db=db, host=host, port=port)
    defaults = dict(use_unicode=True, charset='utf8', autocommit=False)
    for k, v in defaults.iteritems():
        params[k] = kw.pop(k, v)
    params.update(kw)
    engine = _Engine(lambda: MySQLdb.connect(**params))
    # test connection...
    # logging.info('Init mysql engine <%s> ok.' % hex(id(engine)))

# 类定义, 用于with
class _ConnectionCtx(object):
    '''
    _ConnectionCtx object that can open and close connection context. _ConnectionCtx object can be nested and only the most 
    outer connection has effect.

    with connection():
        fun()
        with connection():
            fun()
    '''
    def __enter__(self):
        global _db_ctx
        self.should_cleanup = False     # 刚进来先置为False，然后只在初始化的时候改为True，这样在嵌套的时候
        if not _db_ctx.is_init():
            _db_ctx.init()
            self.should_cleanup = True  # 放在 if 里面，是为了在有嵌套发生时，只有最外层（未初始化过）才会生效
        return self

    def __exit__(self, exctype, excvalue, traceback):
        global _db_ctx
        if self.should_cleanup:
            _db_ctx.cleanup()

# 对外接口，通过 with 调用
def connection():
    '''
    Return _ConnectionCtx object that can be used by 'with' statement:

    with connection():
        fun()
    '''
    return _ConnectionCtx()
# 对外接口，通过 装饰器 调用
def with_connection(func):
    '''
    Decorator for reuse connection.

    @with_connection
    def foo(*args, **kw):
        f1()
        f2()
        f3()
    '''
    @functools.wraps(func)
    def _wrapper(*args, **kw):
        with _ConnectionCtx():
            return func(*args, **kw)
    return _wrapper

class _TransactionCtx(object):
    '''
    _TransactionCtx object that can handle transactions.

    with _TransactionCtx():
        fun()
    '''

    def __enter__(self):
        global _db_ctx
        self.should_cleanup = False                        # 
        if not _db_ctx.is_init():
            # needs open a connection first:
            _db_ctx.init()
            self.should_cleanup = True
        _db_ctx.transactions = _db_ctx.transactions + 1    # 每次嵌套都需要＋1
        # logging.info('begin transaction...' if _db_ctx.transactions==1 else 'join current transaction...')
        return self

    def __exit__(self, exctype, excvalue, traceback):
        global _db_ctx
        _db_ctx.transactions = _db_ctx.transactions - 1
        try:
            if _db_ctx.transactions==0:
                if exctype is None:
                    self.commit()
                else:
                    self.rollback()
        finally:
            if self.should_cleanup:
                _db_ctx.cleanup()

    def commit(self):
        global _db_ctx
        try:
            _db_ctx.commit()
            # logging.info('commit ok.')
        except:
            _db_ctx.rollback()
            raise

    def rollback(self):
        global _db_ctx
        _db_ctx.rollback()
        logging.warning('rollback.')

def transaction():
    '''
    Create a transaction object so can use with statement:

    with transaction():
        fun()
    '''
    return _TransactionCtx()

def with_transaction(func):
    '''
    A decorator that makes function around transaction.

    @with_transaction
    def foo(*args, **kw):
        f1()
        f2()
        f3()
    '''
    @functools.wraps(func)
    def _wrapper(*args, **kw):
        with _TransactionCtx():
            return func(*args, **kw)
    return _wrapper

def _select(sql, first, *args):      # first 布尔类型，表示是否只有一行
    ' execute select SQL and return unique result or list results.'
    global _db_ctx
    cursor = None
    sql = sql.replace('?', '%s')     #  使用占位符"?"可以有效避免sql注入攻击
    # logging.info('SQL: %s, ARGS: %s' % (sql, args))
    try:
        cursor = _db_ctx.cursor()
        cursor.execute(sql, args)
        if cursor.description:
            names = [x[0] for x in cursor.description]  # 得到select语句执行结果的每一列的名字列表
        if first:
            values = cursor.fetchone()
            if not values:
                return None
            return Dict(names, values)                      # 若返回一行，返回的是一个字典，键为列的描述
        return [Dict(names, x) for x in cursor.fetchall()]  # 若返回多行，返回的是一个列表，列表的元素为一个字典，字典的键为列的描述
    finally:
        if cursor:
            cursor.close()


@with_connection
def select_one(sql, *args):
    '''
    Execute select SQL and expected one result. 
    If no result found, return None.
    If multiple results found, the first one returned.

    >>> u1 = dict(id=100, name='Alice', email='alice@test.org', passwd='ABC-12345', last_modified=time.time())
    >>> u2 = dict(id=101, name='Sarah', email='sarah@test.org', passwd='ABC-12345', last_modified=time.time())
    >>> insert('user', **u1)
    1L
    >>> insert('user', **u2)
    1L
    >>> u = select_one('select * from user where id=?', 100)
    >>> u.name
    u'Alice'
    >>> select_one('select * from user where email=?', 'abc@email.com')
    >>> u2 = select_one('select * from user where passwd=? order by email', 'ABC-12345')
    >>> u2.name
    u'Alice'
    '''
    return _select(sql, True, *args)

@with_connection
def select_int(sql, *args):
    '''
    Execute select SQL and expected one int and only one int result. 

    >>> n = update('delete from user')
    >>> u1 = dict(id=96900, name='Ada', email='ada@test.org', passwd='A-12345', last_modified=time.time())
    >>> u2 = dict(id=96901, name='Adam', email='adam@test.org', passwd='A-12345', last_modified=time.time())
    >>> insert('user', **u1)
    1L
    >>> insert('user', **u2)
    1L
    >>> select_int('select count(*) from user')
    2L
    >>> select_int('select count(*) from user where email=?', 'ada@test.org')
    1L
    >>> select_int('select count(*) from user where email=?', 'notexist@test.org')
    0L
    >>> select_int('select id from user where email=?', 'ada@test.org')
    96900L
    >>> select_int('select id, name from user where email=?', 'ada@test.org')
    Traceback (most recent call last):
        ...
    MultiColumnsError: Expect only one column.
    '''
    d = _select(sql, True, *args)
    if len(d)!=1:
        raise MultiColumnsError('Expect only one column.')
    return d.values()[0]

@with_connection
def select(sql, *args):
    '''
    Execute select SQL and return list or empty list if no result.

    >>> u1 = dict(id=200, name='Wall.E', email='wall.e@test.org', passwd='back-to-earth', last_modified=time.time())
    >>> u2 = dict(id=201, name='Eva', email='eva@test.org', passwd='back-to-earth', last_modified=time.time())
    >>> insert('user', **u1)
    1L
    >>> insert('user', **u2)
    1L
    >>> L = select('select * from user where id=?', 900900900)
    >>> L
    []
    >>> L = select('select * from user where id=?', 200)
    >>> L[0].email
    u'wall.e@test.org'
    >>> L = select('select * from user where passwd=? order by id desc', 'back-to-earth')
    >>> L[0].name
    u'Eva'
    >>> L[1].name
    u'Wall.E'
    '''
    return _select(sql, False, *args)

@with_connection
def _update(sql, *args):
    global _db_ctx
    cursor = None
    sql = sql.replace('?', '%s')
    # logging.info('SQL: %s, ARGS: %s' % (sql, args))
    try:
        cursor = _db_ctx.cursor()
        cursor.execute(sql, args)
        r = cursor.rowcount
        if _db_ctx.transactions==0:
            # no transaction enviroment:
            # logging.info('auto commit')
            _db_ctx.commit()
        return r
    finally:
        if cursor:
            cursor.close()

def insert(table, **kw):
    '''
    Execute insert SQL.

    >>> u1 = dict(id=2000, name='Bob', email='bob@test.org', passwd='bobobob', last_modified=time.time())
    >>> insert('user', **u1)
    1L
    >>> u2 = select_one('select * from user where id=?', 2000)
    >>> u2.name
    u'Bob'
    >>> insert('user', **u2)
    Traceback (most recent call last):
      ...
    IntegrityError: (1062, "Duplicate entry '2000' for key 'PRIMARY'")
    '''
    cols, args = zip(*kw.iteritems())
    sql = 'insert into `%s` (%s) values (%s)' % (table, ','.join(['`%s`' % col for col in cols]), ','.join(['?' for i in range(len(cols))]))
    return _update(sql, *args)

def update(sql, *args):
    r'''
    Execute update SQL.

    >>> u1 = dict(id=1000, name='Michael', email='michael@test.org', passwd='123456', last_modified=time.time())
    >>> insert('user', **u1)
    1L
    >>> u2 = select_one('select * from user where id=?', 1000)
    >>> u2.email
    u'michael@test.org'
    >>> u2.passwd
    u'123456'
    >>> update('update user set email=?, passwd=? where id=?', 'michael@example.org', '654321', 1000)
    1L
    >>> u3 = select_one('select * from user where id=?', 1000)
    >>> u3.email
    u'michael@example.org'
    >>> u3.passwd
    u'654321'
    >>> update('update user set passwd=? where id=?', '***', '123\' or id=\'456')
    0L
    '''
    return _update(sql, *args)

if __name__=='__main__':
    logging.basicConfig(level=logging.DEBUG)
    create_engine('root', 'root', 'test')
    update('drop table if exists user')
    update('create table user (id int primary key, name varchar(20), email varchar(50), passwd varchar(20), last_modified real)')
    import doctest
    doctest.testmod()