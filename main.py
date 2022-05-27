import pygame
import random

pygame.init()
pygame.display.set_caption("Lines 98")
screen = pygame.display.set_mode([400,400])

colors = [(255, 0, 0),(0, 255, 0),(0, 0, 255)]

numOfBalls = 20
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
            self.setMap()
        self.drawBall()

    def drawBall(self):
        centerPosX = ((self.position+1)*50)-25
        centerPosY = ((self.row+1)*50)-25
        pygame.draw.circle(screen, self.color, center=(centerPosX, centerPosY), radius=20)

    def setMap(self):
        global ballsMap
        ballsMap[self.row][self.position] = self.color

def newGame():
    global drawLines
    def drawLines():
        for i in range(1, 8):
            pygame.draw.line(screen, (88, 88, 88), (i*50, 0), (i*50, 400))
            pygame.draw.line(screen, (88, 88, 88), (0, i*50), (400, i*50))

    def drawField():
        drawLines()
        for i in range(numOfBalls):
            Ball()
        pygame.display.update()
    drawField()
newGame()

def redrawField():
    screen.fill((0, 0, 0))
    drawLines()
    for i, row in enumerate(ballsMap):
        for j, color in enumerate(row):
            if color == (255, 0, 0) or color == (0, 255, 0) or color == (0, 0, 255):
                centerPosX = ((j+1)*50)-25
                centerPosY = ((i+1)*50)-25
                Ball(color=color, x=centerPosX, y=centerPosY)
    pygame.display.update()

def moveBall(posFrom, posTo):
    color = ballsMap[posFrom[0]][posFrom[1]]
    ballsMap[posFrom[0]][posFrom[1]] = ""
    ballsMap[posTo[0]][posTo[1]] = color
    if checkForFives() == False:
        moreBalls(3)
    redrawField()
    isFieldFull()

def moreBalls(amount):
    freeSpaces = []
    for i, row in enumerate(ballsMap):
        for j, ball in enumerate(row):
            if ball == "":
                freeSpaces.append((i, j))

    freeSpacesToFill = []

    if len(freeSpaces) < 3:
        amount = len(freeSpaces)

    for i in range(amount):
        space = random.choice(freeSpaces)
        freeSpacesToFill.append(space)
        freeSpaces.remove(space)

    for space in freeSpacesToFill:
        ballsMap[space[0]][space[1]] = random.choice(colors)

def checkForFives():
    
    def updateMap(direction):
        if direction == "horizontally":
            for each in fiveInRow:
                ballsMap[each[0]][each[1]] = ""
        elif direction == "vertically":
            for each in fiveInRow:
                switchedBallsMap[each[0]][each[1]] = ""

            for i, row in enumerate(switchedBallsMap):
                for j, ball in enumerate(row):
                    ballsMap[j][i] = ball

    # CHECKS ROWS
    for i, row in enumerate(ballsMap):
        if row.count("") > 3:
            continue
        
        fiveInRow = []
        for j, ball in enumerate(row):
            if ball != "" and not j > 3:
                previousColor = ball
                fiveInRow.append((i, j))
                firstBallIndex = j
                break
        else:
            continue

        for k in range(firstBallIndex+1, 8):
            if row[k] == previousColor:
                fiveInRow.append((i, k))
                if k == 7: 
                    if len(fiveInRow) >= 5:
                        updateMap("horizontally")
                    fiveInRow = []
            else:
                if len(fiveInRow) >= 5:
                    updateMap("horizontally")
                fiveInRow = [(i, k)]
            if row[k] != "":
                previousColor = row[k]
            else:
                previousColor = "none"

    switchedBallsMap = [
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
    ]

    # SWITCHES ROWS AND COLS
    for i, row in enumerate(ballsMap):
        for j, ball in enumerate(row):
            switchedBallsMap[j][i] = ball

    # CHECKS ROWS
    for i, row in enumerate(switchedBallsMap):
        if row.count("") > 3:
            continue
        
        fiveInRow = []
        for j, ball in enumerate(row):
            if ball != "" and not j > 3:
                previousColor = ball
                fiveInRow.append((i, j))
                firstBallIndex = j
                break
        else:
            continue

        for k in range(firstBallIndex+1, 8):
            if row[k] == previousColor:
                fiveInRow.append((i, k))
                if k == 7: 
                    if len(fiveInRow) >= 5:
                        updateMap("vertically")
                    fiveInRow = []
            else:
                if len(fiveInRow) >= 5:
                    updateMap("vertically")
                fiveInRow = [(i, k)]
            if row[k] != "":
                previousColor = row[k]
            else:
                previousColor = "none"

def isFieldFull():
    global gameOver
    breakFlag = False
    for row in ballsMap:
        for ball in row:
            if ball == "":
                breakFlag = True
                break
        if breakFlag == True:
            break
    else:
        gameOver = True
        pygame.quit()

# EVENT LOOP
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
                else:
                    ballSelected = False