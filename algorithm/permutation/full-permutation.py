#!/usr/bin/env python
# -*- coding: utf-8 -*-  
import logging
import copy
import unittest
import functools

'''
全排列生成算法
以元素分治、算法2基于位置的辅助空间算法效率相当，交换位置节省空间的算法最快，大约快 30% 到 40%

以元素分治算法比较挫，beatiful permutation 问题中生成的中间过程中无法筛选，只能先生成全排列，效率低下
logging 打印对时间的影响非常大，本文件的影响系数在12左右
'''

logging.basicConfig(level=logging.ERROR,
                format='%(asctime)s[\033[1;32m%(funcName)s\033[0m:%(lineno)d][%(levelname)s]:%(message)s',
                datefmt='%a,%Y/%m/%d, %H:%M:%S')

def dump(obj):
    if hasattr(obj,'__dict__'):
        return '\n'.join(['%s:%s' % item for item in obj.__dict__.items()])
    else:
        return obj

def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        logging.debug('%s:----------start---------------' % func.__name__)

        for i,arg in enumerate(args):
            logging.debug('args[%s]=[--%s--]' % (i, dump(arg)) )
            
        ret = func(*args, **kw)
        logging.debug('%s:**********end with:[[--%s--]]************' % (func.__name__,ret) )
        return ret
    return wrapper


class FullPermutationLocation:
    '''
    生成无重复元素全排列。利用辅助空间
    当层递归确定当前位置的元素，遍历可选元素 src_seq []，不能选择已使用元素 used []，放到目标序列上 target_seq []
    到达最后一个位置时即已生成一个序列
    '''
    def __init__(self, seq):
        self.src_seq = seq
        self.used    = {}
        self.target_seq = []
        self.permutaions= []
    
    def get_permutation_yiled(self):
        return list(self.full_permutation_yiled(0, len(self.src_seq) ))

    def full_permutation_yiled(self, location, uplimit):
        '''
        location 当前生成序列中哪个位置的值，从1开始
        '''
        #logging.debug("full_permutation:----------start---------------")
        #logging.debug("location:%s" % (location))
        #logging.debug("uplimit:%s" % (uplimit))
        #logging.debug("src_seq:%s" % (self.src_seq))
        #logging.debug("used:%s" % (self.used))
        #logging.debug("target_seq:%s" % (self.target_seq))


        if (location >= uplimit):
            assert (len(self.target_seq) == len(self.src_seq))
            #logging.debug("yiled>>>>>>>>>>target_seq:%s" % (self.target_seq))
            yield self.target_seq[:]
            return

        for src in self.src_seq:
            #logging.debug("src:%s, used.get(src)=%s" % (src, self.used.get(src, False)))
            if self.used.get(src, False):
                continue
            
            self.target_seq.append(src)
            self.used[src] = True
            assert(self.target_seq[location])

            yield from self.full_permutation_yiled( location +1, uplimit)
            #next_location_func = self.full_permutation( location +1, uplimit)
            #for i in next_location_func:
                #yield i

            self.used[src] = False
            del self.target_seq[location]

    def get_permutation(self):
        self.full_permutation(0, len(self.src_seq))
        return self.permutaions

    def full_permutation(self, location, uplimit):
        '''
        location 当前生成序列中哪个位置的值，从1开始
        '''
        #logging.debug("full_permutation:----------start---------------")
        #logging.debug("location:%s" % (location))
        #logging.debug("uplimit:%s" % (uplimit))
        #logging.debug("src_seq:%s" % (self.src_seq))
        #logging.debug("used:%s" % (self.used))
        #logging.debug("target_seq:%s" % (self.target_seq))


        if (location >= uplimit):
            assert (len(self.target_seq) == len(self.src_seq))
            #logging.debug("yiled>>>>>>>>>>target_seq:%s" % (self.target_seq))
            self.permutaions.append(self.target_seq[:])
            return

        for src in self.src_seq:
            #logging.debug("src:%s, used.get(src)=%s" % (src, self.used.get(src, False)))
            if self.used.get(src, False):
                continue
            
            self.target_seq.append(src)
            self.used[src] = True
            assert(self.target_seq[location])

            self.full_permutation( location +1, uplimit)

            self.used[src] = False
            del self.target_seq[location]

class FullPermutationSwap:
    '''
    位置交换，即可省去目标序列空间，已用标记空间
    交换 swap
    当层递归确定当前位置的元素：当前位置后的每个元素都与当前元素交换（前面的已经被使用）
    到达最后一个位置时即已生成一个序列
    '''
    def __init__(self, seq):
        self.src_seq = seq
        self.permutaions= []

    def get_permutation(self):
        self.full_permutation(0, len(self.src_seq))
        return self.permutaions

    def full_permutation(self, location, uplimit):
        '''
        location 当前生成序列中哪个位置的值，从1开始
        '''
        #logging.debug("full_permutation:----------start---------------")
        #logging.debug("***location:%s" % (location))
        #logging.debug("uplimit:%s" % (uplimit))
        #logging.debug("src_seq:%s" % (self.src_seq))

        if (location >= uplimit):
            #logging.debug("yiled>>>>>>>>>>target_seq:%s" % (self.src_seq))
            self.permutaions.append(self.src_seq[:])
            return

        for cur in range(location, uplimit):
            #logging.debug("cur:%s" % (cur))

            (self.src_seq[cur], self.src_seq[location]) =  (self.src_seq[location], self.src_seq[cur])
            #logging.debug("swap 1 src_seq:%s" % (self.src_seq))

            self.full_permutation( location +1, uplimit)

            #为什么要再交换回来？原因是下一层递归调用在返回前没有交换回来的话，当前 FOR 循环无法正确完整地遍历 src_seq
            (self.src_seq[cur], self.src_seq[location]) =  (self.src_seq[location], self.src_seq[cur])
            #logging.debug("swap 2 src_seq:%s" % (self.src_seq))

class FullPermutationOwn:
    '''
    分治，删除首元素得到长度为 N-1 的子序列，并递归生成子序列的全排列，再将所有排列与首元素合并，得到完整序列的全排列
    '''
    def __init__(self, seq):
        self.src_seq = seq
        self.permutaions= []

    def get_permutation(self):
        self.full_permutation(self.src_seq)
        return self.permutaions

    def single_arrage_plus_one(self, arr, ele):
        '''
        将 ele 插入到排列 arr 中的任一位置（包括头尾）得到一个新排列，并将所有的新排列返回
        '''
        new_arrs = []

        for index,e in enumerate(arr):
            new_arrs.append(arr[0:index] + [ele] + arr[index:] )
        #尾部
        new_arrs.append(arr + [ele])

        return new_arrs


    def full_permutation(self, arr):
        #logging.debug("arr:\t%s" % (arr))

        new_arr = []

        if not arr:
            return new_arr
        if len(arr) == 1:
            new_arr.append(arr)
            #logging.debug("all_arr:%s" % (new_arr))
            return new_arr

        ele = arr[0]
        sub_arr = arr[1:]
        sub_all_arr = self.full_permutation(sub_arr)

        for sa_arr in sub_all_arr:
            new_arr.extend(self.single_arrage_plus_one(sa_arr, ele))

        #logging.debug("all_arr:%s" % (new_arr))
        return new_arr

class TestFullPermutationOwn(unittest.TestCase):
    def test_full_permutation(self, N=3):
        #N = 9
        fm = FullPermutationLocation(list(range(1,N+1)))
        perms = fm.get_permutation()
        print ("[Own]count:%s" %(len(perms)))
        #print ("permutation:%s" %(perms))

class TestFullPermutationLocation(unittest.TestCase):
    def test_full_permutation(self, N=3):
        #N = 9
        fm = FullPermutationLocation(list(range(1,N+1)))
        perms = fm.get_permutation()
        print ("[Location]count:%s" %(len(perms)))
        #print ("permutation:%s" %(perms))
        
    
class TestFullPermutationSwap(unittest.TestCase):

    def test_full_permutation(self, N=3):
        #N = 3
        fm = FullPermutationSwap(list(range(1,N+1)))
        perms = fm.get_permutation()
        print ("[Swap]count:%s" %(len(perms)))
        #print ("permutation:%s" %(perms))

if __name__ == '__main__':
    #unittest.main()
    import sys
    reverse_yield = sys.argv[1]
    N = int(sys.argv[2])

    if reverse_yield == '1':
        #N = 15
        t = TestFullPermutationSwap()
        t.test_full_permutation (N)
    elif reverse_yield == '2':
        #N = 15
        t = TestFullPermutationLocation()
        t.test_full_permutation (N)
    else:
        #N = 15
        t = TestFullPermutationOwn()
        t.test_full_permutation (N)