#   Imports
import pygame
import math
pygame.init()
pygame.font.init()
run = True
close = False

updateCycle = 55

#   Title and space
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Pacman but Better")

wallColor = (209,31,206)



#   End Screen Stuff
endScreenFont = pygame.font.SysFont("javanesetext", 50)

endScreenText = endScreenFont.render("Game Over", True, (255, 255, 0))

def endScreen():
    pygame.draw.rect(screen, (0,0,0), pygame.Rect(0, 0, 800, 400))
    screen.blit(endScreenText, ((800 - endScreenText.get_width()) // 2, (400 - endScreenText.get_height()) //2))

#   PathFinding Classes and Methods
size = (width, height) = 800, 400

cols, rows = 40, 20
reasonable = 800
grid = []


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
        self.h = 0
        self.reset = True


    def addNeighbors(self, grid):
        if self.x < cols - 1:
            self.neighbors.append(grid[self.x+1][self.y])
        if self.x > 0:
            self.neighbors.append(grid[self.x-1][self.y])
        if self.y < rows - 1:
            self.neighbors.append(grid[self.x][self.y+1])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y-1])

for x in range(cols):
    arr = []
    for y in range(rows):
        arr.append(Node(x, y))
    grid.append(arr)

for i in range(cols):
    for j in range(rows):
        grid[i][j].addNeighbors(grid)

def createWall(x, y):
    grid[x][y].wall = True
    grid[x][y].reset = False

def caluclateHeuristic(a, b):
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    return(math.sqrt(dx * dx + dy * dy))

def aStar(ghostPos, pacPos, build):
    vis = []
    opset = [grid[ghostPos[0]][ghostPos[1]]]
    cur = grid[ghostPos[0]][ghostPos[1]]
    goal = grid[pacPos[0]][pacPos[1]]
    best = 0
    ver = False
    while cur != goal:
        cur = opset[best]
        for neighbor in cur.neighbors:
            if neighbor not in vis and not neighbor.wall:
                tempG = cur.g + 1

                newPath = False
                if neighbor in opset:
                    if tempG < neighbor.g:
                        neighbor.g = tempG
                        newPath = True
                else:
                    neighbor.g = tempG
                    newPath = True
                
                if newPath:
                    neighbor.h = caluclateHeuristic([neighbor.x, neighbor.y], [goal.x, goal.y])
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.prev = cur
                if neighbor not in opset:
                    opset.append(neighbor)
        opset.remove(cur)
        vis.append(cur)
        bestF = 1000
        for i, n in enumerate(opset):
            if n.f < bestF:
                best = i
                bestF = n.f
        
        if(best > len(opset) -1):
            ver = True
            break

    path = []
    while(cur.prev != None):
        path.append(cur.prev)
        if(build):
            cur.prev.wall = True
        cur = cur.prev
    
    for x in range(cols):
        for y in range(rows):
            grid[x][y].f = 1000
            grid[x][y].g = 0
            grid[x][y].h = 0
            grid[x][y].prev = None
            if(not build and grid[x][y].reset):
                grid[x][y].wall = False
    if len(path) >= 2:
        if(ver):
            minF = path[-2]
            for x in range(len(path)):
                if(path[-x].g == 1):
                    tempF = path[-x]
                    if(tempF.h < minF.h):
                        minF = tempF
            return minF
        else:
            return path[-2]
    else:
        return True
    

#   ScreenBitMap Stuff
screenBitMap = []
for x in range(800):
    lengthElements = []
    for y in range(400):
        lengthElements.append(True)
    screenBitMap.append(lengthElements)

mapFile = open("wallMap.txt", "r")
mapFileFinal = mapFile.read()
mapLineArray = mapFileFinal.split("#", 73)
mapLineArray[len(mapLineArray)-1] = mapLineArray[len(mapLineArray)-1].strip("#")

for mapLine in mapLineArray:
    lineArray = mapLine.split()
    pygame.draw.rect(screen, wallColor, pygame.Rect(int(lineArray[0]), int(lineArray[1]), int(lineArray[2]), int(lineArray[3])), 0)
    for x in range(int(lineArray[2])):
        for y in range(int(lineArray[3])):
            screenBitMap[int(lineArray[0]) + x - 1 ][int(lineArray[1]) + y - 1] = False
            if (x == 0 and y == 0):
                createWall(int(lineArray[0]) // 20, int(lineArray[1]) // 20)
                reasonable -= 1
            elif (x % 20 == 0 and y % 20 == 0):
                createWall((x + int(lineArray[0])) // 20, (y + int(lineArray[1])) // 20)
                reasonable -= 1

#   Movement and Basic Pacman Stuff
pacmanCurrentX = 300
pacmanCurrentY = 240
pacmanXVel = 20
pacmanYVel = 20
pacmanPastX = 0
pacmanPastY = 0
pos = [100, 100, 0]
movementStarted = False
moving = False
pacmanDir = 0
pacmanWantedDir = 0
switchToClosed = False
runner = 0

#   Configuring all image of blankness and pacman
clearSpriteImage = pygame.image.load("clearImage.png")
clearSpriteSmall = pygame.transform.scale(clearSpriteImage, (20, 20))
pacmanSpriteImageOpen = pygame.image.load("pacman.png")
pacmanSpriteImageClosed = pygame.image.load("closedPacman.png")
pacmanSpriteSmallRightOpen = pygame.transform.scale(pacmanSpriteImageOpen, (20, 20)) 
pacmanSpriteSmallClosed = pygame.transform.scale(pacmanSpriteImageClosed, (20, 20))
pacmanSpriteSmallLeftOpen = pygame.transform.rotate(pacmanSpriteSmallRightOpen, 180)
pacmanSpriteSmallDownOpen = pygame.transform.rotate(pacmanSpriteSmallRightOpen, 270)
pacmanSpriteSmallUpOpen = pygame.transform.rotate(pacmanSpriteSmallRightOpen, 90)

#   Displaying Pacman Based on Orientation
def displayPacman():
    screen.blit(clearSpriteSmall, (pacmanPastX, pacmanPastY))
    if(switchToClosed):
        screen.blit(pacmanSpriteSmallClosed, (pacmanCurrentX, pacmanCurrentY))
    else:
        if(pacmanDir == 0):
            screen.blit(pacmanSpriteSmallRightOpen, (pacmanCurrentX, pacmanCurrentY))
        elif(pacmanDir == 90):
            screen.blit(pacmanSpriteSmallUpOpen, (pacmanCurrentX, pacmanCurrentY))
        elif(pacmanDir == 180):
            screen.blit(pacmanSpriteSmallLeftOpen, (pacmanCurrentX, pacmanCurrentY))
        elif(pacmanDir == 270):
            screen.blit(pacmanSpriteSmallDownOpen, (pacmanCurrentX, pacmanCurrentY))


#   Deciding how to move for all characters
def canMove(wantedDir, currentDir, currentX, currentY, xVel, yVel):
    canWant = True
    canCur = True
    for xPos in range(20):
        for yPos in range(20):
            if(wantedDir == 0 or currentDir == 0):
                if(not screenBitMap[currentX + xVel + xPos - 1][currentY + yPos - 1]):
                    if(wantedDir == 0):
                        canWant = False
                    if(currentDir == 0):
                        canCur = False
            if(wantedDir == 90 or currentDir == 90):
                if(not screenBitMap[currentX + xPos - 1][currentY - yVel + yPos - 1]):
                    if(wantedDir == 90):
                        canWant = False
                    if(currentDir == 90):
                        canCur = False

            if(wantedDir == 180 or currentDir == 180):
                if(not screenBitMap[currentX - xVel + xPos - 1][currentY + yPos - 1]):
                    if(wantedDir == 180):
                        canWant = False
                    if(currentDir == 180):
                        canCur = False
            
            if(wantedDir == 270 or currentDir == 270):
                if(not screenBitMap[currentX + xPos - 1][currentY + yVel + yPos - 1]):
                    if(wantedDir == 270):
                        canWant = False
                    if(currentDir == 270):
                        canCur = False
            
    if(canWant == True):
        if(wantedDir == 0):
            return [currentX + xVel, currentY, wantedDir]
        elif(wantedDir == 90):
            return [currentX, currentY - yVel, wantedDir]
        elif(wantedDir == 180):
            return [currentX - xVel, currentY, wantedDir]
        elif(wantedDir == 270):
            return [currentX, currentY + yVel, wantedDir]
    elif(canCur == True):
        if(currentDir == 0):
            return [currentX + xVel, currentY, currentDir]
        elif(currentDir == 90):
            return [currentX, currentY - yVel, currentDir]
        elif(currentDir == 180):
            return [currentX - xVel, currentY, currentDir]
        elif(currentDir == 270):
            return [currentX, currentY + yVel, currentDir]
    return [currentX, currentY, currentDir]

#   Creating all Ghost Images
redLeftGhostImage = pygame.image.load("redLeftGhost.png")
redRightGhostImage = pygame.image.load("redRightGhost.png")
redDownGhostImage = pygame.image.load("redDownGhost.png")
redUpGhostImage = pygame.image.load("redUpGhost.png")

blueLeftGhostImage = pygame.image.load("blueLeftGhost.png")
blueRightGhostImage = pygame.image.load("blueRightGhost.png")
blueDownGhostImage = pygame.image.load("blueDownGhost.png")
blueUpGhostImage = pygame.image.load("blueUpGhost.png")

yellowLeftGhostImage = pygame.image.load("yellowLeftGhost.png")
yellowRightGhostImage = pygame.image.load("yellowRightGhost.png")
yellowDownGhostImage = pygame.image.load("yellowDownGhost.png")
yellowUpGhostImage = pygame.image.load("yellowUpGhost.png")

pinkLeftGhostImage = pygame.image.load("pinkLeftGhost.png")
pinkRightGhostImage = pygame.image.load("pinkRightGhost.png")
pinkDownGhostImage = pygame.image.load("pinkDownGhost.png")
pinkUpGhostImage = pygame.image.load("pinkUpGhost.png")

redLeftGhost = pygame.transform.scale(redLeftGhostImage, (20, 20))
redRightGhost = pygame.transform.scale(redRightGhostImage, (20, 20))
redDownGhost = pygame.transform.scale(redDownGhostImage, (20, 20))
redUpGhost = pygame.transform.scale(redUpGhostImage, (20, 20))

blueLeftGhost = pygame.transform.scale(blueLeftGhostImage, (20, 20))
blueRightGhost = pygame.transform.scale(blueRightGhostImage, (20, 20))
blueDownGhost = pygame.transform.scale(blueDownGhostImage, (20, 20))
blueUpGhost = pygame.transform.scale(blueUpGhostImage, (20, 20))

yellowLeftGhost = pygame.transform.scale(yellowLeftGhostImage, (20, 20))
yellowRightGhost = pygame.transform.scale(yellowRightGhostImage, (20, 20))
yellowDownGhost = pygame.transform.scale(yellowDownGhostImage, (20, 20))
yellowUpGhost = pygame.transform.scale(yellowUpGhostImage, (20, 20))

pinkLeftGhost = pygame.transform.scale(pinkLeftGhostImage, (20, 20))
pinkRightGhost = pygame.transform.scale(pinkRightGhostImage, (20, 20))
pinkDownGhost = pygame.transform.scale(pinkDownGhostImage, (20, 20))
pinkUpGhost = pygame.transform.scale(pinkUpGhostImage, (20, 20))

ghostList = (redRightGhost, redUpGhost, redDownGhost, redLeftGhost, blueRightGhost, blueUpGhost, blueLeftGhost, blueDownGhost, yellowRightGhost, yellowUpGhost, yellowLeftGhost, yellowDownGhost, pinkRightGhost, pinkUpGhost, pinkLeftGhost, pinkDownGhost, clearSpriteSmall)

#   Ghost Class and Functions
class Ghost:

    ghostHeight = 20
    ghostWidth = 20
    ghostXVel = 20
    ghostYVel = 20
    path = []

    def __init__(self, xPos, yPos, color, dir):
        self.xPos = xPos
        self.yPos = yPos
        self.color = color
        self.dir = dir
        self.wantedDir = dir
        self.pastX = xPos
        self.pastY = yPos
    
    def dislayGhost(self):
        
        if(self.color == "Red"):
            self.value = 0
        elif(self.color == "Blue"):
            self.value = 4
        elif(self.color == "Yellow"):
            self.value = 8
        elif(self.color == "Pink"):
            self.value = 12
        
        if(self.dir == 0):
            self.value += 0
        elif(self.dir == 90):
            self.value += 1
        elif(self.dir == 180):
            self.value += 2
        elif(self.dir == 270):
            self.value += 3

        if(self.pastX != self.xPos or self.pastY != self.yPos):
            screen.blit(ghostList[16], (self.pastX, self.pastY))
        screen.blit(ghostList[self.value], (self.xPos, self.yPos))
    
    def calculateMovements(self, build):
        global pacmanCurrentX
        global pacmanCurrentY
        self.pastX = self.xPos
        self.pastY = self.yPos
        self.target = aStar([self.xPos // 20, self.yPos // 20], [pacmanCurrentX // 20, pacmanCurrentY // 20], build)
        
        if(self.target != True):
            self.xPos = self.target.x * 20
            self.yPos = self.target.y * 20
        


        
redGhost = Ghost(60, 60, "Red", 0)
blueGhost = Ghost(60, 340, "Blue", 90)
pinkGhost = Ghost(740, 20, "Pink", 180)
yellowGhost = Ghost(740, 360, "Yellow", 270)

ghosts = [redGhost, blueGhost, pinkGhost, yellowGhost]

def ghostFunctions():
    yellowGhost.calculateMovements(False)
    blueGhost.calculateMovements(True)
    redGhost.calculateMovements(False)
    pinkGhost.calculateMovements(False)
    redGhost.dislayGhost()
    blueGhost.dislayGhost()
    yellowGhost.dislayGhost()
    pinkGhost.dislayGhost()

#   What to do at death
def end():
    if(redGhost.target == True or blueGhost.target == True or yellowGhost.target == True or pinkGhost.target == True):
        if(yellowGhost.target == True):
            if(caluclateHeuristic([yellowGhost.xPos, yellowGhost.yPos], [pacmanCurrentX, pacmanCurrentY]) < 21):
                pass
            else:
                print(caluclateHeuristic([yellowGhost.xPos, yellowGhost.yPos], [pacmanCurrentX, pacmanCurrentY]))
                return False

        if(redGhost.target == True):
            if(caluclateHeuristic([redGhost.xPos, redGhost.yPos], [pacmanCurrentX, pacmanCurrentY]) < 21):
                pass
            else:
                print(caluclateHeuristic([redGhost.xPos, redGhost.yPos], [pacmanCurrentX, pacmanCurrentY]))
                return False

        redGhost.dislayGhost()
        blueGhost.dislayGhost()
        yellowGhost.dislayGhost()
        pinkGhost.dislayGhost()
        return True
    return False

#   All Fruit stuff
fruitImage = pygame.image.load("fruit.png")

fruitSmall = pygame.transform.scale(fruitImage, (20, 20))

class fruit:
    def __init__(self, xPos, yPos, wall):
        self.xPos = xPos
        self.yPos = yPos
        self.eaten = wall
    
    def display(self):
        for ghost in ghosts:
            if(self.xPos == ghost.xPos and self.yPos == ghost.yPos):
                break
            elif(self.xPos == pacmanCurrentX and self.yPos == pacmanCurrentY):
                break
            elif(self.eaten == True):
                break
            else:
                screen.blit(fruitSmall, (self.xPos,self.yPos))

fruits = []
for x in range(0, 800, 20):
    arr = []
    for y in range(0, 400, 20):
        arr.append(fruit(x, y, grid[x//20][y//20].wall))
    fruits.append(arr)

for x in fruits:
    for y in x:
        y.display()

def displayFruits(resetArr, atePos):
    for pos in resetArr:
        fruits[pos[0]//20][pos[1]//20].display()
    fruits[atePos[0]//20][atePos[1]//20].eaten = True

#   Actual Run loop
while run:
    resetArr = []
    pygame.time.delay(updateCycle)
    pacmanPastX = pacmanCurrentX
    pacmanPastY = pacmanCurrentY
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            run = False 
    keys = pygame.key.get_pressed()

    if(keys[pygame.K_w]):
        pacmanWantedDir = 90
    
    elif(keys[pygame.K_a]):
        pacmanWantedDir = 180
    
    elif(keys[pygame.K_s]):
        pacmanWantedDir = 270
    
    elif(keys[pygame.K_d]):
        pacmanWantedDir = 0

    if(keys[pygame.K_q]):
        break
        
    if(not close):
        resetArr = [[redGhost.pastX, redGhost.pastY], [blueGhost.pastX, blueGhost.pastY], [pinkGhost.pastX, pinkGhost.pastY], [yellowGhost.pastX, yellowGhost.pastY]] 
        displayFruits(resetArr, [pacmanCurrentX, pacmanCurrentY])
        if(runner % 2 == 0):
            switchToClosed = not switchToClosed
            pos = canMove(pacmanWantedDir, pacmanDir, pacmanCurrentX, pacmanCurrentY, pacmanXVel, pacmanYVel)
            pacmanCurrentX = pos[0]
            pacmanCurrentY = pos[1]
            pacmanDir = pos[2]
            displayPacman()
        if(runner % 3 == 0):
            ghostFunctions()
            if(end()):
                runner = -20
                close = True
    
    
    if(runner == -1):
        endScreen()
    runner += 1
    pygame.display.update()

pygame.quit()