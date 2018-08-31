__author__ = 'LION'
#coding=utf-8
import urllib
import re
import logging
import functools
#单元测试 1 加载库
import unittest

'''
将对象__dict__属性转换化字符串
'''
def dump(obj):
    if hasattr(obj,'__dict__'):
        return '\n'.join(['%s:%s' % item for item in obj.__dict__.items()])
    else:
        return obj

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s[%(funcName)s:%(lineno)d][%(levelname)s]:%(message)s',
                datefmt='%a,%Y/%m/%d, %H:%M:%S')
                #datefmt='%a, %d %b %Y %H:%M:%S',
#format 支持的变量
#    文件名 %(filename)s
#指定日志文件名和打开模式
                #filename='myapp.log',
                #filemode='w')
#高亮绿色字的函数名
#format='\033[1;32m%(funcName)s\033[0m',

#带颜色的显示
#    命令 \033[ 开始，后接操作代码。操作颜色的操作代码以 m 结尾。多个操作代码间用 ; 分隔，且只能最后一个代码以 m 结尾。
#        如，\033[31m 表示红色字，\033[01;31m 表示高亮红色字，\033[0m 表示关闭属性设置


#没有@functools.wraps(func)，被装饰的函数内部使用__name__的结果将会是wrapper
'''
@不指定打印内容的调试装饰函数
用此方法装饰的函数，执行前将打印参数列表，结束后将打印返回值
'''
def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        logging.debug('%s:----------start---------------' % func.__name__)

        for i,arg in enumerate(args):
            logging.debug('args[%s]=[%s]' % (i, dump(arg)) )
            
        ret = func(*args, **kw)
        logging.debug('%s:**********end with:[[%s]]************' % (func.__name__,ret) )
        return ret
    return wrapper
'''
@指定打印内容的调试装饰函数
用此方法装饰的函数，执行前将打印指定内容，结束后将打印返回值
'''
def logtext(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            logging.info('%s: %s()' % (func.__name__, text))
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