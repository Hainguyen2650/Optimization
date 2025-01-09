There are N classes 1, 2, . . ., N that need to be scheduled for the final exam. Each class must be assigned to a time-slot and a room.
There are M rooms 1, 2, …, M that can be used for scheduling the exam. Each room i has capacity c(i) (number of places of the room)
Each day is divided into 4 slots 1, 2, 3, 4.
Each class i has number of students d(i) (i = 1,..., N).
Among N classes, there are K pairs of classes (i, j) in which class i and class j have the same student participating in the exam. 
It means that these 2 classes cannot be scheduled in the same time-slot.
Objective: Compute the exam time-table such that the number of days used is minimal.

A solution is represented by 2 array s and r in which s[i] is the start slot and r[i] is the room of course i
Input
Line 1: contains N, M
Line 2: contains d1, d2, …, dN
Line 3: contains c1, c2, …, cM
Line 4: contains K
Line 4 + k (k = 1,…, K): contains 2 integers i and j (2 courses having a same student registerd,  these courses cannot be scheduled in the same slot)
Output
Each line i ( i = 1, 2, . . ., N): contains 3 integer i, s[i], and r[i] 

Example

Input
10 3
72 77 71 71 53 45 53 53 66 70 
79 53 70 
16
1 2
1 3
1 8
1 10
2 5
2 9
3 6
3 9
4 10
5 8
5 10
7 8
7 9
7 10
8 9
9 10

Output
1 1 1
2 2 1
3 3 1
4 4 1
5 1 2
6 1 3
7 2 2
8 3 2
9 4 3
10 3 3
