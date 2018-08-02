__author__ = 'LION'
#coding=utf-8
import urllib
import re
import logging
import functools
#单元测试 1 加载库
import unittest

'''
将对象属性转换化字符串
'''
def log_obj(obj):
    if hasattr(obj,'__dict__'):
        return '\n'.join(['%s:%s' % item for item in obj.__dict__.items()])
    #if hasattr(obj,'debug_dump'):
    #    return obj.debug_dump()
    else:
        return obj

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s[%(funcName)s:%(lineno)d][%(levelname)s]:%(message)s',
                #format='%(filename)s',
                datefmt='%a,%Y/%m/%d, %H:%M:%S')
                #datefmt='%a, %d %b %Y %H:%M:%S',
                #filename='myapp.log',
                #filemode='w')

#没有@functools.wraps(func)，被装饰的函数内部使用__name__的结果将会是wrapper
'''
@带参数的装饰函数
'''
def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        logging.debug('%s:----------start---------------' % func.__name__)
        for index,arg in enumerate(args):
            logging.debug('args[%s]=[%s]' % (index, log_obj(arg)) )
        ret = func(*args, **kw)
        logging.debug('%s:**********end with:[[%s]]************' % (func.__name__,ret) )
        return ret
    return wrapper
'''
@不带参数的装饰函数
'''
def logtext(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            logging.info('%s %s():' % (text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator


@log
def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

'''
单元测试 2 继承类
'''
Point = namedtuple('Point', ['x', 'y'])
class TestPoint(unittest.TestCase):
    def test_init(self):
        rec = Point(1,2)
        self.assertTrue(isinstance(rec, Point))
        self.assertEqual(rec.x, 1)
        self.assertEqual(rec.y, 2)

    def test_init_error(self):
        with self.assertRaises(TypeError):
            rec = Point('a',2,3)
'''
单元测试 3 运行
    if __name__ == '__main__':
        unittest.main()
或
    python3 -m unittest my_test #不要带文件后辍.py
'''