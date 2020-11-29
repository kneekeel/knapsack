'''
    Computer Science 215: Design and Analysis of Algorithms
    Programming Project: 0-1 Knapsack Problem
    Author: Nikhil Sodemba


    Acknowledgement(s) :

        Quick Sort Algorithm taken from: https://www.geeksforgeeks.org/quick-sort/

            Modification(s) : 
            
                Algorithm sorts three arrays representing: weight, profit, and item #.

                Adjusted the algorithm to swap elements based on profit/weight ratios,
                in non-increasing order.
        
        Chapters 4 and 6 from: "Foundations of Algorithms, 5th Editition, by Richard E. Neapolitan".

            Modification(s) discussed in write-up.
        
'''

from queue import PriorityQueue
import random
import os

'''
    Partition Function: A utility function for the Quick Sort algorithm
'''
def partition(wt_arr, val_arr, idx_arr, low,high):
    pivot = float(val_arr[low] / wt_arr[low])
    i = low
    j = high
    while(True):
        # Ignore all the ratios lesser than the pivot ratio to right
        while(float(val_arr[i]/wt_arr[i]) > pivot):
            i += 1
        # Ignore all the ratios greater than the pivot ratio to left
        while(float(val_arr[j] /wt_arr[j]) < pivot):
            j -= 1
        # Swap the ratio lesser than pivot on left with a ratio greater than pivot on right
        if i < j:
            val_arr[i], val_arr[j] = val_arr[j], val_arr[i]
            wt_arr[i], wt_arr[j] = wt_arr[j], wt_arr[i]
            idx_arr[i], idx_arr[j] = idx_arr[j], idx_arr[i]
            i += 1
            j -= 1
        else:
            return j


'''
    Quick Sort algorithm, modified to swap elements with respect to 
    profit/weight ratios, in a non-increasing order.

    Function uses recursion and the partition (util. func.) to sort accordingly.

    Input(s):
        - Arrays are indexed 0 - n(-1), where n is the number of items
        wt_arr (weight), val_arr (profit), idx_arr (index), and low , high (integer)

    Return sorted (non-increasing order based on profit/weight ratios) wt_arr, 
        val_arr, and idx_arr. Where each index in the three arrays represents 
        one items weight, value, and item #. 
'''
def quickSort(wt_arr, val_arr, idx_arr, low, high): 
    if low < high: 

        pi = partition(wt_arr, val_arr, idx_arr, low, high)  
        # Separately sort elements before 
        # partition and after partition 
        quickSort(wt_arr, val_arr, idx_arr, low, pi) 
        quickSort(wt_arr, val_arr, idx_arr, pi+1, high) 


'''
    A Dynamic Programming algorithm for the 0-1 Knapsack Problem

    Input(s):

        Sorted arrays: wt, val, and idx (in nonincreasing order based on profit/weight ratios)
        W = integer value representing the size capacity of the Knapsack
        n = integer value representing the number of items

    Return(s):

        Optimal Solution Set -> array containing item's # in the optimal set.
        The Total Profit of the items in the optimal solution set
        The Total Weight of the items in the optimal solution set
'''
def DP_Knapsack(W, wt, val, idx, n): 
    K = [[0 for x in range(W + 1)] for x in range(n + 1)] 
    optSolSet = []  

    # Build table K[][]
    for i in range(n + 1): 
        for w in range(W + 1): 
            # Base case when there are # of items or weight = 0
            if i == 0 or w == 0: 
                K[i][w] = 0

            # If item can be added into the Knapsack, can be max of two cases:
                # 1): Current item value is included in the optimal subset
                # 2): The item is not included in the optimal subset
            elif wt[i-1] <= w: 
                K[i][w] = max(val[i-1] + K[i-1][w-wt[i-1]],  K[i-1][w]) 

            # Item #n-1 is considered as item n's weight exceeds the weight.
            else: 
                K[i][w] = K[i-1][w] 
    
    # Variable to store original value of W, used when alg.(below) reaches base case
    max_W = W
    tot_weight = 0
    # Traverse through rowws of K (descending)
    for i in range(len(K)-1, -1, -1):
        # Base case when W == 0 or K[i][W] == 0
        if W == 0 or K[i][W] == 0:
            return optSolSet , K[n][max_W], tot_weight
        # Check to see whether item should be included or not
        # If value of K[row-1][col] == K[row][col], item at row 
        # must be excluded from optimal subset
        if K[i-1][W] == K[i][W]:
            i = i - 1
        # Otherwise, the item is included in the optimal set
        else: 
            optSolSet.append(idx[i-1])
            tot_weight = tot_weight + wt[i-1]
            W = W - wt[i-1]


'''
    Bound Function: A utility function for the Best/Breadth First 
        Knapsack Algorithms.

    Input(s):
        
        Node = current node to be evaluated: type - array: [level, profit, weight, bound]
        W = integer value representing the size capacity of the Knapsack
        n = integer value representing the number of items
        w, p = respective weight and profit arrays (indexed 0-(n-1))

    Return(s):

        1). 0 if the weight overcomes the knapsack capacity (i.e., no need to calculate bound for that node)
        
        or, 

        2). Bound of that node, the algorithm follows the criteria located in write up, 
            at: 2.2.
'''
def bound(node, n, W, w, p):
    # If weight overcomes the knapsack capacity, return 0
    if node[2] >= W:
        return 0
    
    # initialize bound on profit by current profit
    profit_bound = node[1]

    # Start including items from index 1 more to current item index
    j = node[0] + 1
    totweight = float(node[2])
    
    # Checking index condition and knapsack capacity condition
    while j < n and float(totweight + w[j]) <= W: 
        totweight = float(totweight + w[j])
        profit_bound = profit_bound + p[j]
        j = j + 1

    
    # If k is not n, include last item partially for upper bound on profit
    if j < n: 
        profit_bound = float(profit_bound + ((W-totweight)*p[j]/w[j]))

    return profit_bound 


'''
    A Breadth-First, Branch and Bound Algorithm for the 0-1 Knapsack Problem

    Input(s):
        W = integer value representing the size capacity of the Knapsack
        n = integer value representing the number of items
        w, p, idx = respective weight, profit, index arrays (indexed 0-(n-1))

    Return(s): 

        Optimal Solution Set -> array containing item's # in the optimal set.
        The Total Profit of the items in the optimal solution set
        The Total Weight of the items in the optimal solution set
'''
def breadthFirst_Knapsack(n, p, w, W, idx):
    # Initialize nodes u, v 
    u = [None, None, None, None]
    v = [None, None, None, None]

    # Initialize Q to be empty
    Q = [[]]
    
    # Variable(s) for storing the optimal profit/weight
    optSolSet = []
    maxWeight = 0

    # Initiate Node u as 'dummy' node at start
    u[0] = -1
    u[1] = u[2] = 0

    Q.insert(0,u)   # Enqueue u in queue
    del Q[1]
    maxProfit = 0   # maxprofit = 0


    # Extract an item from 'tree' and compute profit of all
    # children of extracted item, updating value of maxProfit
    while(len(Q) != 0):
        # Dequeue first node from queue
        u = Q[0]   # Using del method instead of pop(...) due to program errors
        del Q[0]

        # If node is the starting node, assign level 0
        if u[0] == -1: 
            v[0] = 0

        # If there is nothing on next level
        if u[0] == n-1:
            continue

        # Else, increment level and compute profit of children node(s)
        v[0] = u[0] + 1
        # Taking current level's item add current level's weight and value 
        # to node u's weight and value
        v[2] = float(u[2] + w[v[0]])
        v[1] = u[1] + p[v[0]]    
        
        # If cumulated weight < W && profit > maxProfit, update maxProfit
        if (v[2] <= W and v[1] > maxProfit): 
            # Add current item at level to the optimal set
            optSolSet.append(idx[v[0]])
            maxProfit = v[1]
            maxWeight = v[2]

        # Get the upper bound on profit to decide to add v to Q or not.
        v[3] = bound(v,n,W,w,p)

        # If bound value > profit, then push into queue
        if v[3] > maxProfit: 
            Q.append(v)
        # Consider node u to be the case where v is not included 
        u[0] = v[0]
        u[3] = bound(u,n,W,w,p)
        if u[3] > maxProfit:
            Q.append(u)
        # Reset variables for next iteration to ensure that no 
        # data gets copied over to the next iteration.
        v = [None, None, None, None]
        u = [None, None, None, None]
    return maxProfit, maxWeight, optSolSet


'''
    A Depth-First, Branch and Bound Algorithm for the 0-1 Knapsack Problem

    Input(s):
        W = integer value representing the size capacity of the Knapsack
        n = integer value representing the number of items
        w, p, idx = respective weight, profit, index arrays (indexed 0-(n-1))

    Return(s): 

        Optimal Solution Set -> array containing item's # in the optimal set.
        The Total Profit of the items in the optimal solution set
        The Total Weight of the items in the optimal solution set
'''
def bestFirst_Knapsack(n, p, w, idx, W):
    # Initialize PQ to be empty
    pq = PriorityQueue()
    # Initialize nodes v and u
    v = [None, None, None, None]
    u = [None, None, None, None]
    # Initiate Node u as 'dummy' node at start
    u[0] = -1
    u[1] = u[2] = 0

    maxProfit = 0
    maxWeight = 0
    optSet = []

    u[3] = bound(u,n,W,w,p)
    # Insert with -ve bound, so the queue is prioritizing bound 
    pq.put((-u[3], u))
    while not pq.empty():
        temp = pq.get() # Remove node with best bound
        u = temp[1]     # Set node u to equal the values of (best bound) node
        if u[3] > maxProfit:     # Check if node is still promising
            v[0] = u[0] + 1      # Set v to the child that includes 
            v[1] = u[1] + p[v[0]]  # the next item
            v[2] = float(u[2] + w[v[0]])

            if v[2] <= W and v[1] > maxProfit: 
                optSet.append(idx[v[0]])
                maxProfit = v[1]
                maxWeight = v[2]

            v[3] = bound(v,n,W,w,p)
            if v[3] > maxProfit:
                pq.put((-v[3], v))
            u[0] = v[0]         # Set u to the child that does not
            u[3] = bound(u,n,W,w,p)     # include the next item
            if u[3] > maxProfit: 
                pq.put((-u[3], u))
            v = [None, None, None, None]
            u = [None, None, None, None]
    return maxProfit , maxWeight , optSet


'''
    Main Program to run the 0-1 Knapsack Problem with varying Algorithm(s)
'''
def mainKnapsack():
    # Global Variable(s)
    wt , val, idx = [] , [] , []
    W , n = 0 , 0

    # Potental Error(s)
    ERROR_ONE = 'The file doesn\'t contain the correct information to evaluate.'
    ERROR_TWO = 'The number of item\'s given doesn\'t match the actual number of items evaluated.'

    # Brief Introduction
    print("\n\nWelcome to Nikhil's 0-1 Knapsack Program.\n\nThis program is compatible with the following algorithms:\n")
    print("0: Dynamic Programming\t\t1: Breadth-First\t\t2: Best-First\n\nPlease follow the next set of instructions:\n")

    # You WILL have to change the dir path, to match the path on your local system
    dir_path = "/Users/nikhilsodemba/Documents/Comp Sci 215/knapsack_pp/"   # CHANGE DIRECTORY PATH HERE !!!
    # Note: if user specifies a non-existent file in directory, the program will terminate
    usr_file = input("Enter the file which you would like to use, alongside its filename extension:\t")
    print("\nEvaluating the given file to ensure compatability with program, please wait...\n")
    file = dir_path + usr_file
    reader = open(file, 'r')
    count = 0
    # Loop through all lines
    for line in reader:
        if count == 0: 
            n = int(line)
        elif count == 1:
            W = int(line)
        elif count >= 2: 
            values = line.split()
            # If the current line has more than 3 variables
            if len(values) > 3:
                print(ERROR_ONE)
                return ERROR_ONE
            # Else append the correspoding values into their respective arrays
            idx.append(int(values[0]))
            val.append(int(values[1]))
            wt.append(int(values[2]))
        count += 1
    
    # If the predicted size of items doesn't hold true, return ERROR_TWO
    if len(idx) != n:
        print(ERROR_TWO)
        return ERROR_TWO

    # Sort the respective arrays in order based on non-increasing, profit/weight ratios
    quickSort(wt,val,idx,0,n-1)

    alg_num = int(input("\nEnter: 0 for Dynamic Programming; 1 for Breadth-First; 2 for Best-First;\t"))
    
    print("\nAfter Sorting the Arrays:\nIndex Array:\n", idx, "\nProfit Array:\n", val, "\nWeight Array:\n", wt,"\n\n")
    
    # Dynamic Programming
    if alg_num == 0:
        optSet, tot_prof, tot_wt = DP_Knapsack(W, wt, val, idx, n)
        print("\nDynamic Programming Results...\n\nOptimal Solution Set (Item #):\n", optSet, "\nTotal Profit: ", tot_prof, "\t\tTotal Weight: ", tot_wt)
        return optSet, tot_prof, tot_wt
    # Breadth First
    elif alg_num == 1: 
        tot_prof , tot_wt, optSet = breadthFirst_Knapsack(n,val,wt,W,idx)
        print("\nBreadth First Results...\n\nOptimal Solution Set (Item #):\n", optSet, "\nTotal Profit: ", tot_prof, "\t\tTotal Weight: ", tot_wt)
        return optSet, tot_prof, tot_wt
    # Best First
    elif alg_num == 2: 
        tot_prof, tot_wt, optSet = bestFirst_Knapsack(n,val,wt,idx,W)
        print("\nBest First Results...\n\nOptimal Solution Set (Item #):\n", optSet, "\nTotal Profit: ", tot_prof, "\t\tTotal Weight: ", tot_wt)
        return optSet, tot_prof, tot_wt
    
    return

mainKnapsack()

