#Algorithm: Ant colony optimization + Simulated annealing
import numpy as np
import time
start = time.time()
data_file = "tmp.txt"
def read_input():
    with open(data_file, 'r') as f:
        data = f.read().strip().split('\n')
    
    N, M = map(int, data[0].split())
    d = np.array(list(map(int, data[1].split())))
    c = np.array(list(map(int, data[2].split())))
    K = int(data[3])
    conflict = np.ones(shape=(N,N), dtype=bool)

    for line in data[4:4 + K]:
        c1, c2 = map(lambda x: int(x) - 1, line.split())
        conflict[c1,c2] = False
        conflict[c2,c1] = False
    
    return N, M, d, c, conflict
N,M, classes, rooms, conflict = read_input()

r_class = np.zeros(N, dtype=int)
def AntColonyAlg(vapor_rate=0.9, significant_rate=4, DELTA_PHER=5, RATE_UNCHANGE=0.3, MAX_INTERATION=1000):
    x = [(classes<=rooms[r]).astype(int) for r in range(M)]
    min_value = 1e9
    for interation in range(MAX_INTERATION):
        t_class = np.zeros(N, dtype=int)
        t_room = np.zeros(M, dtype=int)
        conflict_time = {}
        path = [np.zeros(N) for r in range(M)]
        while 0 in t_class:
            choose_r = np.random.choice(np.arange(M)[t_room==t_room.min()])
            t_room[choose_r] += 1
            cur_timeslot = t_room[choose_r]
            conflict_time[cur_timeslot] = conflict_time.get(cur_timeslot, np.ones(N, dtype=bool))

            idx = (t_class==0)&conflict_time[cur_timeslot]
            heuristic = np.power(classes[idx],significant_rate)*x[choose_r][idx]
            if heuristic.sum()!=0:
                choose_c = np.random.choice(np.arange(N)[idx], p= heuristic/heuristic.sum())
                conflict_time[cur_timeslot] = conflict_time[cur_timeslot]&(conflict[choose_c])
                t_class[choose_c] = cur_timeslot
                r_class[choose_c] = choose_r
                path[choose_r][choose_c] = 1

        if  min_value > t_room.max():
            delta_pher = DELTA_PHER
            save_timeslot = tuple(t_class)
            save_classtoroom = tuple(r_class)
            min_value = t_room.max()
        elif min_value >= t_room.max()/np.random.uniform(1,1.5*pow(2,-20*(interation/MAX_INTERATION))+1):
            delta_pher = RATE_UNCHANGE*DELTA_PHER
        else:
            delta_pher = 0

        for r in range(M):
            x[r] = np.power(x[r], vapor_rate) + path[r]*delta_pher

    return min_value, save_timeslot, save_classtoroom

min_,t,r = AntColonyAlg(DELTA_PHER=classes.max()*0.5, vapor_rate=0.5)
#print(min_)

for i in range(N):
    print(f"{i+1} {t[i]} {r[i]+1}")

stop = time.time()
print('Time: ', stop - start)