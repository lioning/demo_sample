#!/usr/bin/env python
class SolutionReverseFaster(object):
    def countArrangement(self, N):
        cache = {}
        def helper(i, X):
            #print ("X=")
            if i == 1:
                return 1
            key = (i, X)
            if key in cache:
                return cache[key]
            total = 0
            for j in range(len(X)):
                if X[j] % i == 0 or i % X[j] == 0:
                    #print ("i=%s, j=%s" %(i,j))
                    total += helper(i - 1, X[:j] + X[j + 1:])
            cache[key] = total
            return total

        return helper(N, tuple(range(1, N + 1)))

class Solution:
    def countArrangement(self, N):
        """
        :type N: int
        :rtype: int
        """
        memory = dict()
        def solve(idx, nums):
            if not nums: return 1
            key = idx, tuple(nums)
            if key in memory:return memory[key]
            
            res = 0
            for i, n in enumerate(nums):
                if n % idx == 0 or idx % n == 0:
                    res += solve(idx+1, nums[:i]+nums[i+1:])
            memory[key] = res 
            return res 
        return solve(1, list(range(1, N+1)))


import sys
N = int(sys.argv[1])

s = SolutionReverseFaster()

print ("reverse count:%s" %(s.countArrangement(N)))

s = Solution()
print ("normal count:%s" %(s.countArrangement(N)))
