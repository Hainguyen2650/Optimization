Given a network G = (V,E). Each edge (i,j) has length c(i,j).
Find two edge-disjoint paths from 1 to n (two paths that do not have common edges) such that the sum of lengths of the two paths is minimal.

Input
Line 1: contains 2 positive integers n and m (1 <= n,m <= 30)
Line i+1 (i = 1, 2, . . ., m): contains 3 positive integers u, v, c in which w is the length of the edge(u,v)

Output
Write the sum of lengths of thw two edge-disjoint paths found, or write NOT_FEASIBLE if no solution found.

Example
Input
10 18
1 2 2
1 3 3
1 4 6
2 4 8
2 5 5
3 4 1
3 6 7
4 5 9
4 6 3
5 8 9
5 9 1
6 7 4
6 8 4
7 8 8
7 10 4
8 9 5
8 10 5
9 10 3


Output 
26