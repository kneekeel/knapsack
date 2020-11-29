# 0-1 Knapsack Project: User Handbook

## Created by: Nikhil Sodemba

### Refer to this project for educational purposes only

See the
[0-1 Knapsack](http://www.cs.kzoo.edu/cs215/HW/Knapsack/knapsack.html)
for the instructions for this assignment, coding tips, links to helpful
documents, and submission requirements.

### Welcome to the 0-1 Knapsack Program

This program is intended to utilize the three algorithms: dynamic programming, breadth-first, and best-first (depth); to solve the famous 0-1 Knapsack Problem.

In 0-1 Knapsack, items cannot be broken which means the thief should take the item as a whole or should leave it. There are three algorithms which are discussed in detail in the write-up/under the respective file.

All three algorithms can be found under the file 'knapsackPP.py' under the same directory, alongside their respective function declarations and in-depth comments.

The program will read in a file which has: the number of items in set, capacity of the knapsack evaluated, and the respective item number alongside respective item profit and weight. The program is user friendly, it will ask the user to input the file name they would like to test.

**How to run the program:**

- User will have to run the 'knapsackPP.py' file and simply follow the instructions provided, Note that the program is suspectible to errors and will terminate when error criteria has been met.

**NOTE FOR USERS:**

- In the 'knapsackPP.py' file, there is the main function 'mainKnapsack()' where, on line 334 there is a variable 'dir_path', ensure that this path is the correct path for your directory on your local machine. Ensure that the input you give for the file name has the file extension alongside it and remember that the program is case-sensitive, in other words, the input must match the file name EXACTLY!

- The file which is evaluated must match the criteria's provided in the project [documentation](http://www.cs.kzoo.edu/cs215/HW/Knapsack/knapsack.html).

- The items are sorted, using a manipulated Quick Sort algorithm, based on non-increasing proft/weight ratio order.

- The best and breath first algorithms will not always produce the actual optimal solution set, but will produce the actual (maximum) total profit and weight.

**Files Inclusive of Original Program:**

- knapsackPP.py - contains all three algorithms to solve the 0-1 Knapsack Problem, the manipulated QuickSort algorithm and the mainKnapsack() function needed to stimulate the program.

- timeFn.py - contains the code which I used to test the empircal results found in the write-up.

- sample.txt - Original File given by instructor, contains the information needed for the 0-1 Knapsack Problem.

- example5-6.txt - Set of items taken from Example 5.6 from "*Foundations of Algorithms, 5th Editition, by Richard E. Neapolitan*"

- error_one.txt - The file which has more than 3 variables for an item, i.e., 1 10 2 20. The purpose of this file is to ensure error-handling.

- error_two.txt - The file which has not equal set of items when compared to the value of n (line 1 from file). The purpose of this file is to ensure error-handling.
