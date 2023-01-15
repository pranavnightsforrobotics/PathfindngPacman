import math

def caluclateHeuristic(a, b):
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    return(math.sqrt(dx * dx + dy * dy))

size = (width, height) = 800, 400

cols, rows = 40, 40

grid = []
openSet, closeSet = [], []
path = []

w = width//cols
h = height//rows

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbors = []
        self.prev = None
        self.wall = False
        self.g = 0
        self.f = 1000


    def addNeighbors(self, grid):
        if self.x < cols - 1:
            self.neighbors.append(grid[self.x+1][self.y])
        if self.x > 0:
            self.neighbors.append(grid[self.x-1][self.y])
        if self.y < rows - 1:
            self.neighbors.append(grid[self.x][self.y+1])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y-1])

def createWall(x, y):
    grid[x][y].wall = True

for x in range(cols):
    arr = []
    for y in range(rows):
        arr.append(Node(x, y))
    grid.append(arr)

for i in range(cols):
    for j in range(rows):
        grid[i][j].addNeighbors(grid)

def aStar(ghostPos, pacPos):
    start = grid[ghostPos[0]][ghostPos[1]]
    goal = grid[pacPos[0]][pacPos[1]]
    cur = start
    cur.f = caluclateHeuristic([cur.x, cur.y], [goal.x, goal.y])
    openSet.append(start)
    iter = 0
    while(cur != goal):
        curF = 1000
        for neighbors in cur.neighbors:
            iter+= 1
            if(neighbors in closeSet or neighbors.wall):
                continue
            else:
                neighbors.g = cur.g + 1
                neighbors.h = caluclateHeuristic([neighbors.x, neighbors.y], [goal.x, goal.y])
                neighbors.f = neighbors.g + neighbors.h
                if(curF > neighbors.f):
                    best = neighbors
                    curF = neighbors.f
        if(best != cur):
            openSet.append(best)
        best.prev = cur
        #print(cur.x, cur.y)
        openSet.remove(cur)
        closeSet.append(cur)
        if(openSet != []):
            cur = openSet[0]
    
    while(cur.prev != None):
        path.append(cur.prev)
        cur = cur.prev
    
    print(iter)
    return path


createWall(4, 5)
createWall(4, 4)
p = aStar([0, 0], [21, 21])

for j in p:
    print(j.x, j.y)

def aStar(ghostPos, pacPos):
    start = grid[ghostPos[0]][ghostPos[1]]
    goal = grid[pacPos[0]][pacPos[1]]
    cur = start
    cur.f = caluclateHeuristic([cur.x, cur.y], [goal.x, goal.y])
    openSet.append(start)
    iter = 0
    while(cur != goal):
        curF = 1000
        for neighbors in cur.neighbors:
            iter+= 1
            if(neighbors in closeSet or neighbors.wall):
                continue
            else:
                neighbors.g = cur.g + 1
                neighbors.h = caluclateHeuristic([neighbors.x, neighbors.y], [goal.x, goal.y])
                neighbors.f = neighbors.g + neighbors.h
                if(curF > neighbors.f):
                    best = neighbors
                    curF = neighbors.f
        if(best != cur):
            openSet.append(best)
        best.prev = cur
        #print(cur.x, cur.y)
        openSet.remove(cur)
        closeSet.append(cur)
        if(openSet != []):
            cur = openSet[0]
    
    while(cur.prev != None):
        path.append(cur.prev)
        cur = cur.prev
    
    print(iter)
    return path

