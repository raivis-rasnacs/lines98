import pygame
import random

pygame.init()
pygame.display.set_caption("Lines 98")
screen = pygame.display.set_mode([400,400])

colors = [(255, 0, 0),(0, 255, 0),(0, 0, 255)]

numOfBalls = 13
gameOver = False
ballSelected = False

ballsMap = [
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
]

class Ball():
    def __init__(self, **params):
        if len(params) > 0:
            self.position = ((params["x"]+25)/50)-1
            self.row = ((params["y"]+25)/50)-1
            self.color = params["color"]
        else:
            self.row = random.randrange(0, 8)
            self.position = random.randrange(0, 8)
            while ballsMap[self.row][self.position] != "":
                self.row = random.randrange(0, 8)
                self.position = random.randrange(0, 8)
            self.color = random.choice(colors)
        self.drawBall()

    def drawBall(self):
        centerPosX = ((self.position+1)*50)-25
        centerPosY = ((self.row+1)*50)-25
        print(centerPosX, centerPosY)
        pygame.draw.circle(screen, self.color, center=(centerPosX, centerPosY), radius=20)

    def setMap(self):
        global ballsMap
        ballsMap[self.row][self.position] = self.color

def drawLines():
    for i in range(1, 8):
        pygame.draw.line(screen, (88, 88, 88), (i*50, 0), (i*50, 400))
        pygame.draw.line(screen, (88, 88, 88), (0, i*50), (400, i*50))

def drawField():
    drawLines()
    for i in range(numOfBalls):
        myBall = Ball()
        #myBall.drawBall()
        myBall.setMap()
    pygame.display.update()
drawField()

def redrawField():
    screen.fill((0, 0, 0))
    drawLines()
    for i, row in enumerate(ballsMap):
        for j, color in enumerate(row):
            if color == (255, 0, 0) or color == (0, 255, 0) or color == (0, 0, 255):
                centerPosX = ((j+1)*50)-25
                centerPosY = ((i+1)*50)-25
                myBall = Ball(color=color, x=centerPosX, y=centerPosY)
                #myBall.drawBall()
    pygame.display.update()

def moveBall(posFrom, posTo):
    print(posTo)
    color = ballsMap[posFrom[0]][posFrom[1]]
    ballsMap[posFrom[0]][posFrom[1]] = ""
    ballsMap[posTo[0]][posTo[1]] = color
    checkForFives()

def checkForFives():
    # CHECKS ROWS
    for i, row in enumerate(ballsMap):
        for j in range(4):
            for color in colors:
                if row[j] == row[j+1] == row[j+2] == row[j+3] == row[j+4] == color:
                    row[j] = row[j+1] = row[j+2] = row[j+3] = row[j+4] = ""
                    break

    # CHECKS COLUMNS
    for i in range(8):
        for j in range(4):
            for color in colors:
                if ballsMap[j][i] == ballsMap[j+1][i] == ballsMap[j+2][i] == ballsMap[j+3][i] == ballsMap[j+4][i] == color:
                    ballsMap[j][i] = ballsMap[j+1][i] = ballsMap[j+2][i] = ballsMap[j+3][i] = ballsMap[j+4][i] = ""
                    break
    redrawField()

while gameOver == False:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            clickPos = pygame.mouse.get_pos()
            pos = clickPos[0]//50
            row = clickPos[1]//50
            if ballSelected == True:
                if ballsMap[row][pos] == "":
                    posTo = (row, pos)
                    ballSelected = False
                    moveBall(posFrom, posTo)
                else:
                    ballSelected = False
            else:
                if ballsMap[row][pos] != "":
                    ballSelected = True
                    posFrom = (row, pos)
                    print(posFrom)
                else:
                    ballSelected = False

pygame.QUIT