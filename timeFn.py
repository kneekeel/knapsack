'''
    Computer Science 215: Design and Analysis of Algorithms
    Author: Nikhil Sodemba

    The purpose of this file is to run multiple tests for the 
    three algorithms: DP_Knapsack, breadthFirst_Knapsack, and 
    bestFirst_Knapsack. 

    Results of the following tests can be found in the write-up.
'''

import timeit

setup = '''
import random
from queue import PriorityQueue

def setGenerator(n, W):
    wt, val, idx = [] , [] , []
    for x in range(n):
        idx.append(x+1)
        wt.append(random.randint(1, W))
        val.append(random.randint(1, 10000))
    return wt, val, idx

def partition(wt_arr, val_arr, idx_arr, low,high):
    pivot = float(val_arr[low] / wt_arr[low])
    i = low
    j = high
    while(True):
        while(float(val_arr[i]/wt_arr[i]) > pivot):
            i += 1
        while(float(val_arr[j] /wt_arr[j]) < pivot):
            j -= 1
        if i < j:
            val_arr[i], val_arr[j] = val_arr[j], val_arr[i]
            wt_arr[i], wt_arr[j] = wt_arr[j], wt_arr[i]
            idx_arr[i], idx_arr[j] = idx_arr[j], idx_arr[i]
            i += 1
            j -= 1
        else:
            return j

def quickSort(wt_arr, val_arr, idx_arr, low, high): 
    if low < high: 
        pi = partition(wt_arr, val_arr, idx_arr, low, high)  
        quickSort(wt_arr, val_arr, idx_arr, low, pi) 
        quickSort(wt_arr, val_arr, idx_arr, pi+1, high) 

W = 20
n = 100
wt, val, idx = setGenerator(n, W)
quickSort(wt,val,idx,0,n-1)


def DP_Knapsack(W, wt, val, idx, n): 

    K = [[0 for x in range(W + 1)] for x in range(n + 1)] 
    optSolSet = []

  
    for i in range(n + 1): 
        for w in range(W + 1): 
            if i == 0 or w == 0: 
                K[i][w] = 0

            elif wt[i-1] <= w: 
                K[i][w] = max(val[i-1] + K[i-1][w-wt[i-1]],  K[i-1][w]) 

            else: 
                K[i][w] = K[i-1][w] 
    
    max_W = W
    tot_weight = 0

    for i in range(len(K)-1, -1, -1):
        if W == 0 or K[i][W] == 0:
            return optSolSet , K[n][max_W], tot_weight
        if K[i-1][W] == K[i][W]:
            i = i - 1
        else: 
            optSolSet.append(idx[i-1])
            tot_weight = tot_weight + wt[i-1]
            W = W - wt[i-1]
    


def bound(node, n, W, w, p):
    if node[2] >= W:
        return 0
    
    profit_bound = node[1]

    j = node[0] + 1
    totweight = float(node[2])
    
    while j < n and float(totweight + w[j]) <= W: 
        totweight = float(totweight + w[j])
        profit_bound = profit_bound + p[j]
        j = j + 1

    
    if j < n: 
        profit_bound = float(profit_bound + ((W-totweight)*p[j]/w[j]))

    return profit_bound 



def breadthFirst_Knapsack(n, p, w, W, idx):
    u = [None, None, None, None]
    v = [None, None, None, None]

    Q = [[]]
    
    optSolSet = []
    maxWeight = 0

    u[0] = -1
    u[1] = u[2] = 0

    Q.insert(0,u)  
    del Q[1]
    maxProfit = 0   


    while(len(Q) != 0):
        u = Q[0]   
        del Q[0]
        
        if u[0] == -1: 
            v[0] = 0

        if u[0] == n-1:
            continue

        v[0] = u[0] + 1
        v[2] = float(u[2] + w[v[0]])
        v[1] = u[1] + p[v[0]]    

        if (v[2] <= W and v[1] > maxProfit): 
            optSolSet.append(idx[v[0]])
            maxProfit = v[1]
            maxWeight = v[2]

        v[3] = bound(v,n,W,w,p)

        if v[3] > maxProfit: 
            Q.append(v)
        u[0] = v[0]
        u[3] = bound(u,n,W,w,p)
        if u[3] > maxProfit:
            Q.append(u)
        v = [None, None, None, None]
        u = [None, None, None, None]
    return maxProfit, maxWeight, optSolSet



def bestFirst_Knapsack(n, p, w, idx, W):
    pq = PriorityQueue()
    v = [None, None, None, None]
    u = [None, None, None, None]
    u[0] = -1
    u[1] = u[2] = 0

    maxProfit = 0
    maxWeight = 0
    optSet = []

    u[3] = bound(u,n,W,w,p)
    pq.put((-u[3], u))
    while not pq.empty():
        temp = pq.get() 
        u = temp[1]     
        if u[3] > maxProfit:     
            v[0] = u[0] + 1      
            v[1] = u[1] + p[v[0]]  
            v[2] = float(u[2] + w[v[0]])

            if v[2] <= W and v[1] > maxProfit: 
                optSet.append(idx[v[0]])
                maxProfit = v[1]
                maxWeight = v[2]

            v[3] = bound(v,n,W,w,p)
            if v[3] > maxProfit:
                pq.put((-v[3], v))
            u[0] = v[0]         
            u[3] = bound(u,n,W,w,p)     
            if u[3] > maxProfit: 
                pq.put((-u[3], u))
            v = [None, None, None, None]
            u = [None, None, None, None]
    return maxProfit , maxWeight , optSet
'''

# Driver code to test average execution time(s) 
dpKnapsack = timeit.Timer(stmt = "DP_Knapsack(W, wt, val, idx, n)", setup=setup)
print(dpKnapsack.timeit(100)/100)
breadthFirstKnapsack = timeit.Timer(stmt = "breadthFirst_Knapsack(n, val, wt, W, idx)", setup=setup)
print(breadthFirstKnapsack.timeit(100)/100)
bestFirstKnapsack = timeit.Timer(stmt = "bestFirst_Knapsack(n, val, wt, idx, W)", setup=setup)
print(bestFirstKnapsack.timeit(100)/100)
