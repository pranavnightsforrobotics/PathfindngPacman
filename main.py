#   Imports
import pygame
import random
pygame.init()
pygame.font.init()
run = True
close = False

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


#   ScreenBitMap Stuff
screenBitMap = []
for x in range(800):
    lengthElements = []
    for y in range(400):
        lengthElements.append(True)
    screenBitMap.append(lengthElements)

mapFile = open("wallMap.txt", "r")
mapFileFinal = mapFile.read()
mapLineArray = mapFileFinal.split("#", 3)
mapLineArray[len(mapLineArray)-1] = mapLineArray[len(mapLineArray)-1].strip("#")

for mapLine in mapLineArray:
    lineArray = mapLine.split()
    print(lineArray)
    pygame.draw.rect(screen, wallColor, pygame.Rect(int(lineArray[0]), int(lineArray[1]), int(lineArray[2]), int(lineArray[3])), 0)
    for x in range(int(lineArray[2])):
        for y in range(int(lineArray[3])):
            screenBitMap[int(lineArray[0]) + x - 1 ][int(lineArray[1]) + y - 1] = False

#   Movement and Basic Pacman Stuff
pacmanCurrentX = 100
pacmanCurrentY = 100
pacmanXVel = 10
pacmanYVel = 10
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
    if(wantedDir == 0):
        for xPos in range(20):
            for yPos in range(20):
                if(not screenBitMap[currentX + xVel + xPos - 1][currentY + yPos -1]):
                    return [currentX, currentY, currentDir]
        return [currentX + xVel, currentY, wantedDir]
    elif(wantedDir == 90):
        for xPos in range(20):
            for yPos in range(20):
                if(not screenBitMap[currentX + xPos - 1][currentY - yVel + yPos -1]):
                    return [currentX, currentY, currentDir]
        return [currentX, currentY - yVel, wantedDir]
    elif(wantedDir == 180):
        for xPos in range(20):
            for yPos in range(20):
                if(not screenBitMap[currentX - xVel + xPos - 1][currentY + yPos -1]):
                    return [currentX, currentY, currentDir]
        return [currentX - xVel, currentY, wantedDir]
    elif(wantedDir == 270):
        for xPos in range(20):
            for yPos in range(20):
                if(not screenBitMap[currentX + xPos - 1][currentY + yVel + yPos -1]):
                    return [currentX, currentY, currentDir]
        return [currentX, currentY+ yVel, wantedDir]
    else:
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

#   Ghost Class
class Ghost:

    ghostHeight = 20
    ghostWidth = 20
    ghostXVel = 10
    ghostYVel = 10

    def __init__(self, xPos, yPos, color, dir):
        self.xPos = xPos
        self.yPos = yPos
        self.color = color
        self.dir = dir
        self.wantedDir = dir
        self.pastX = xPos - 20
        self.pastY = yPos - 20
    
    def dislayGhost(self):
        if((self.wantedDir == self.dir) and ( (self.xPos == self.pastX) and (self.yPos == self.pastY))):
            self.pos = canMove(self.wantedDir, self.dir, self.xPos, self.yPos, self.ghostXVel, self.ghostYVel)
            self.xPos = self.pos[0]
            self.yPos = self.pos[1]
            self.dir = self.pos[2]
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
    
    def calculateMovements(self):
        self.pastX = self.xPos
        self.pastY = self.yPos
        if(abs(self.xPos - pacmanCurrentX) > abs(self.yPos - pacmanCurrentY)):
            if(self.xPos - pacmanCurrentX > 0):
                self.wantedDir = 180
            else:
                self.wantedDir = 0
        else:
            if(self.yPos - pacmanCurrentY > 0):
                self.wantedDir = 90
            else:
                self.wantedDir = 270
        self.pos = canMove(self.wantedDir, self.dir, self.xPos, self.yPos, self.ghostXVel, self.ghostYVel)
        self.xPos = self.pos[0]
        self.yPos = self.pos[1]
        self.dir = self.pos[2]


        
redGhost = Ghost(200, 200, "Red", 0)
#blueGhost = Ghost(300, 200, "Blue", 90)
#pinkGhost = Ghost(200, 300, "Pink", 180)
#yellowGhost = Ghost(300, 300, "Yellow", 270)

def ghostFunctions():
    redGhost.calculateMovements()
    #blueGhost.calculateMovements()
    #yellowGhost.calculateMovements()
    #pinkGhost.calculateMovements()
    redGhost.dislayGhost()
    #blueGhost.dislayGhost()
    #yellowGhost.dislayGhost()
    #pinkGhost.dislayGhost()
    
    
while run:
    pygame.time.delay(80)
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
    if(keys[pygame.K_e]):
        close = True
        endScreen()

    pos = canMove(pacmanWantedDir, pacmanDir, pacmanCurrentX, pacmanCurrentY, pacmanXVel, pacmanYVel)
    pacmanCurrentX = pos[0]
    pacmanCurrentY = pos[1]
    pacmanDir = pos[2]
    if(runner % 2 == 0):
        ghostFunctions()
    if(not close):
        displayPacman()
    
    switchToClosed = not switchToClosed
    runner += 1
    pygame.display.update()

pygame.quit()

"""
Test a dummy ghost class with random movement using bitmap and figure out how to do death
Then use basic greater than and less than logic to determine ideal path
"""