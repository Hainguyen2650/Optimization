import numpy as np



datapath = 'testcase.txt'
with open (datapath, 'r') as f:
    data = f.read().strip().split('\n')

n = int(data[0])
c = []
for i in range(1, n+1):
    c.append(list(map(int, data[i].split())))


print(c)

def chooseCity(cur, visited, distancesMatrix, pheromone, alpha, beta):
    global n
    probalities = []
    for next in range(n):
        if next not in visited:
            pheromoneLvl = pheromone[cur][next] ** alpha
            heuristic = (1 / distancesMatrix[cur][next]) ** beta
            probalities.append(pheromoneLvl * heuristic)
        else:
            probalities.append(0)

    total = sum(probalities)
    if total == 0:
        probalities = [1 if ct not in visited else 0 for ct in range(n)]
        total = sum(probalities)

    probalities = [ele / total for ele in probalities]
    return int(np.random.choice(range(n), p=probalities))

def generateInitialSolution(distancesMatrix, antNumber, pheromone, alpha, beta):
    sol = []
    global n
    for _ in range(antNumber):
        path = []
        cur = np.random.randint(0,n-1)
        path.append(cur)

        while len(path) < n:
            next = chooseCity(cur, path, distancesMatrix, pheromone, alpha, beta)
            path.append(next)
            cur = next

        path.append(path[0])
        sol.append(path)

    return sol
    
def updatePheromone(pheromone, sol, distancesMatrix, evaporateRate, pheromoneDepth):
    pheromone *= (1-evaporateRate)

    for path in sol:
        cost = Cost(path, distancesMatrix)
        for i in range(len(path)-1):
            pheromone[path[i]][path[i+1]] += pheromoneDepth/cost
            pheromone[path[i+1]][path[i]] += pheromoneDepth/cost
            
    

def Cost(path, distancesMatrix):
    return sum(distancesMatrix[path[i]][path[i+1]] for i in range(len(path)-1))

def Optimize(distancesMatrix, antNumber, maxIter = 100, alpha = 1, beta = 3.5, evaporateRate = 0.5, pheromoneDepth = 1, bestPath = None):
    global n
    pheromone = np.ones((n,n))/n
    #print(pheromone)
    #print(bestPath)
    bestCost = 1e9 if bestPath == None else Cost(bestPath, distancesMatrix)

    stopCount = 0
    upperBound = 50

    for iter in range(maxIter):
        sol = generateInitialSolution(distancesMatrix, antNumber, pheromone, alpha, beta)
        updatePheromone(pheromone, sol, distancesMatrix, evaporateRate, pheromoneDepth)
        #print(sol)
        improved = False
        for path in sol:
            #print('path: ', path)
            cost = Cost(path, distancesMatrix)
            if cost < bestCost:
                bestCost = cost
                bestPath = path
                improved = True

        if improved:
            stopCount = 0
        else:
            stopCount += 1

        if stopCount > upperBound:
            break
    print('bestpath: ',bestPath)
    print('bestCost: ', bestCost)
    return bestCost, bestPath



bestCost, bestPath = Optimize(c,n)
print("first solution: ", bestPath, bestCost)
for i in range(10):
    #print(i)
    bestCost, bestPath = Optimize(c,n, bestPath = bestPath)

for i in bestPath[:n]:
    print(i, end = ' ')
print()
print(bestCost)