#Algorithm: hill climbing
import random
import numpy as np

def read_input():
    with open("tmp.txt", 'r') as f:
        data = f.read().strip().split('\n')
    N, M = map(int, data[0].split())
    d = list(map(int, data[1].split()))
    c = list(map(int, data[2].split()))
    K = int(data[3])
    conflict = {}
    for line in data[4:4 + K]:
        i, j = map(lambda x: int(x) - 1, line.split())
        conflict.setdefault(i, []).append(j)
        conflict.setdefault(j, []).append(i)
    return N, M, d, c, conflict

N, M, d, c, conflict = read_input()

def feasible(slot, room, cl, t_class, r_class):
    if d[cl] > c[room]:
        return False
    for other_cl in range(N):
        if other_cl != cl and t_class[other_cl] == slot:
            if other_cl in conflict.get(cl, []):
                return False
            if r_class[other_cl] == room:
                return False
    return True

def generate_initial_solution(N, M, d, c, conflict):
    t_class = [-1] * N
    r_class = [-1] * N
    max_slot = 0
    queue = list(range(N))  

    while queue:
        cl = queue.pop(0)
        assigned = False
        for slot in range(1, max_slot + 1):
            for room in range(M):
                if feasible(slot, room, cl, t_class, r_class):
                    t_class[cl], r_class[cl] = slot, room
                    assigned = True
                    break
            if assigned:
                break
        if not assigned:
            max_slot += 1
            for room in range(M):
                if feasible(max_slot, room, cl, t_class, r_class):
                    t_class[cl], r_class[cl] = max_slot, room
                    assigned = True
                    break
        if not assigned:
            t_class[cl], r_class[cl] = max_slot, 0

        for cnf in conflict.get(cl, []):
            if t_class[cnf] < 0 and cnf not in queue:
                queue.append(cnf)

    return t_class, r_class

def current_max_slot(t_class):
    return max(t_class)

def shake_solution(t_class, r_class, num_shakes=5):
    indices = random.sample(range(N), k=min(num_shakes, N))
    for cl in indices:
        for _ in range(20):  
            slot = random.randint(1, max(t_class) + 1)
            room = random.randint(0, M - 1)
            if feasible(slot, room, cl, t_class, r_class):
                t_class[cl] = slot
                r_class[cl] = room
                break

def local_search(N, M, conflict, iterations=100, max_restarts=6):
    best_t_class, best_r_class = None, None
    best_slot_usage_overall = 999
    restarts = 0

    while restarts < max_restarts:
        t_class, r_class = generate_initial_solution(N, M, d, c, conflict)
        if restarts == 0:
            best_t_class = t_class
            best_r_class = r_class
        best_slot_usage = 999
        no_improve_count = 0

        for it in range(iterations):
            max_slot_used = current_max_slot(t_class)
            classes_in_max_slot = [i for i in range(N) if t_class[i] == max_slot_used]
            if not classes_in_max_slot:
                best_slot_usage = max_slot_used - 1
                continue

            cl = random.choice(classes_in_max_slot)
            new_slot = random.randint(1, max_slot_used - 1) if max_slot_used > 1 else 1
            new_room = random.randint(0, M - 1)
            old_slot, old_room = t_class[cl], r_class[cl]

            if feasible(new_slot, new_room, cl, t_class, r_class):
                t_class[cl] = new_slot
                r_class[cl] = new_room
            
            new_usage = current_max_slot(t_class)
            if new_usage < best_slot_usage:
                best_t_class = t_class.copy()
                best_r_class = r_class.copy()
                best_slot_usage = new_usage
                no_improve_count = 0
            else:
                no_improve_count += 1
                t_class[cl] = old_slot
                r_class[cl] = old_room
            
            # Shake the solution if no improvement for a while
            if no_improve_count >= 50:
                shake_solution(t_class, r_class, num_shakes=5)
                no_improve_count = 0
            #print(f"Iteration {it}, current max slot usage: {current_max_slot(t_class)}")
            if no_improve_count >= 100:
                break

        if best_slot_usage < best_slot_usage_overall:
            best_slot_usage_overall = best_slot_usage
            best_t_class = t_class
            best_r_class = r_class

        restarts += 1
    #print("Overall best slot usage found:", best_slot_usage_overall)
    return best_t_class, best_r_class, best_slot_usage_overall

best_t_class, best_r_class, best_slot_usage_overall = local_search(N, M, conflict)
for i in range(N):
    print(i + 1, best_t_class[i], best_r_class[i] + 1)
print(best_slot_usage_overall)
