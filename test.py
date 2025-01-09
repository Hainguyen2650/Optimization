a = '1 18 45 23 11 48 24 50 26 22 28 19 25 4 30 41 3 34 13 20 35 49 9 6 47 39 32 44 37 10 7 27 17 33 36 42 16 43 21 15 46 38 29 5 14 12 31 2 40 8'
b = list(map(int, a.split()))
datapath = 'testcase.txt'
with open (datapath, 'r') as f:
    data = f.read().strip().split('\n')

n = int(data[0])
c = []
for i in range(1, n+1):
    c.append(list(map(int, data[i].split())))

import numpy as np
print(len(b))

print(sum(c[b[i]-1][b[i+1]-1] for i in range(len(b)-1)))