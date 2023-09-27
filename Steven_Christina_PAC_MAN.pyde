import copy 
import random
import pickle


def setup():
    global gameGrid, PAC, dirInput, timer, GHOST1, GHOST2, changePath, dots, escapeMode
    global G1, G2, scattertime, flashtime, blueOff, died1, died2, player, pausetime, paused, mousePress, time, mode, scrollinc
    global pinky, bluey, scattery, pac, mouth, mcycle, boxoutline, Uinput, scoreL, invalidn, invalidc, win
    global saveEntered, saveName, directory, wrongfile, themecolour, theme, tick, scrollbarlen, upcycle, slide, minput, multiplayer
    
    pinky = loadImage("PINKY.png")
    pinky.resize(0, width/12)
    
    bluey = loadImage("BLUEY.png")
    bluey.resize(0, width/12)
    
    scattery = loadImage("SCATTER.png")
    scattery.resize(0, width/12)
    
    pac = [0, 0, 0, 0] 
    pac[0] = loadImage("PAC0R.png")
    pac[0].resize(0, 50)
    
    pac[1] = loadImage("PAC1R.png")
    pac[1].resize(0, 50)
    
    pac[2] = loadImage("PAC2R.png")
    pac[2].resize(0, 50)
    
    pac[3] = loadImage("PAC3.png")
    pac[3].resize(0, 50)
    
    textFont(createFont("PressStart2P-Regular.ttf", 20))
    textAlign(LEFT, CENTER)
    textSize(20)
    
    gameGrid = \
    [1, 1, 1, 0, 1, 1, 0, 1, 0, 1],\
    [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],\
    [1, 0, 0, 0, 1, 1, 0, 0, 0, 1],\
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],\
    [1, 1, 1, 0, 1, 0, 1, 1, 1, 1],\
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0],\
    [1, 1, 0, 1, 1, 0, 1, 1, 0, 1],\
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],\
    [1, 0, 0, 0, 0, 1, 0, 1, 0, 1],\
    [1, 1, 1, 0, 1, 1, 0, 1, 0, 1]
    
    size(1000, 1000) 
    
    scrollinc = 0 
    scoreL = []
    mode = 5
    mousePress = False
    
    boxoutline = [False, False, False]
    Uinput = "" 
    invalidn = False
    invalidc = False
    
    player = Player("")

    saveEntered =  False
    saveName =  "pacman"    
    directory =  sketchPath("") + "scores" 
    wrongfile = False
    theme = [[0, 0, 0, 80, 80, 80],[90, 107, 81, 61, 66, 58], [9, 24, 143, 190, 197, 247]]
    themecolour = theme[0]
    time = 0 
    
    tick = "_"
    scrollbarlen = height - height/6 - height/12.0
    timer = millis()
    mcycle = 0
    upcycle = True
    slide = 4
    
    multiplayer = False
    
    
def totalRESET(): 
    
    # resets the entire game after the player has clicked to start a new round
    
    global gameGrid, PAC, dirInput, timer, GHOST1, GHOST2, pactime, changePath, dots, dotTemplate, escapeMode
    global G1, G2, scattertime, flashtime, blueOff, died1, died2, font, player, pausetime, paused, mousePress, time, mode, scrollinc, scoreList
    global pinky, bluey, scattery, pac, mouth, mcycle, upcycle, win, slide, pGHOST, minput
    
    mouth = millis()
    mcycle = 0
    upcycle = True
    
    dots = []
    for row in gameGrid: 
        dotrow = []
        for block in row: 
            if block == 1: 
                dotrow.append(0)
            elif block == 0: 
                dotrow.append(1)
        dots.append(dotrow)
                
    PAC = PacMan(1, 1, 1, 0)
    
    dots = makeCherry(3)
    
    GHOST1 = Ghost(8, 7)
    GHOST1.drawPath(gameGrid, PAC, 0) 
    G1 = Corner([[1, 8], [1, 1], [8, 2], [8, 7]]) 
    
    
    GHOST2 = Ghost(1, 8) 
    GHOST2.drawPath(gameGrid, PAC, 1) 
    G2 = Corner([[8, 2], [8, 7], [8, 2], [8, 7]])
    
    slide = 4
    dirInput = 0
    timer = millis()
    scattertime = millis()
    flashtime = millis()
    blueOff = False 
    
    changePath = 0
    escapeMode = False
    
    died1 = False
    died2 = False
    
    pausetime = 0
    paused = False 
    win = False
    
    time = millis() - pausetime
    pGHOST = pGhost(8, 7, 1, 1)
    minput = [0, 0]
    
    
def resetGame():
    
    # resets the positions of the player and ghosts after player has been eaten
    global gameGrid, PAC, dirInput, timer, GHOST1, GHOST2, pactime, dots, dotTemplate, escapeMode, G1, G2, scattertime, flashtime, pGHOST
    
    PAC = PacMan(1, 1, 1, 0)
    
    GHOST1 = Ghost(8, 7)
    GHOST1.drawPath(gameGrid, PAC, 0) 
    G1 = Corner([[1, 8], [1, 1], [8, 2], [8, 7]]) 
    
    GHOST2 = Ghost(1, 8) 
    GHOST2.drawPath(gameGrid, PAC, 1) 
    G2 = Corner([[8, 2], [8, 7], [8, 7], [8, 2]])
    
    dirInput = 0
    timer = millis()
    scattertime = millis()
    flashtime = millis()
    escapeMode = False
    
    pGHOST = pGhost(8, 7, 1, 1)
        
class Player():
     
    def __init__(self, name):
        self.name = name 
        self.score = 0
        self.lives = 3
    
    def captured(self): 
        self.score -= 50
        self.lives -= 1
    
    def dots(self):
        self.score += 10
    
    def ghost(self): 
        self.score += 100
        
    
class PacMan():
    
    def __init__(self, locationx, locationy, speed, direction): 
        self.lx = locationx
        self.ly = locationy
        self.px = locationx
        self.py = locationy
        self.sp = speed 
        self.dir = direction
    
    def changeLocation(self, dirInput): 
        self.px = self.lx 
        self.py = self.ly
        self.dir = dirInput
        
        #direction needed
        if dirInput == 0: 
            print("right")
            if self.lx + 1 <= 9: 
                if gameGrid[self.ly][self.lx + 1] != 1: 
                    self.lx = self.lx + self.sp ## for now
            else:
                self.lx = 0 
        if dirInput == 1: 
            print("left")
            if self.lx - 1 >= 0: 
                if gameGrid[self.ly][self.lx - 1] != 1:
                    self.lx = self.lx - self.sp
            else: 
                self.lx = 9
        if dirInput == 2: 
            print("up")
            if self.ly - 1 >= 0: 
                if gameGrid[self.ly - 1][self.lx] != 1:
                    self.ly = self.ly - self.sp
            else:
                self.ly = 9
        if dirInput == 3:
            print("down")
            if self.ly + 1 <= 9: 
                if gameGrid[self.ly + 1][self.lx] != 1:
                    self.ly = self.ly + self.sp
            else:
                self.ly = 0
            
class Corner(): 
    
    # when the ghosts are in escapeMode, they are assigned four corners to go to, just like the real game.
    # when ghost has reached one of the corners, it travels to the other corners. If those have been reached, the list resets
    # ghost travels back to first corner. (unlikely as escapeMode total time possible is 21 seconds)
    
    def __init__(self, corner): 
        self.corner = corner
        self.n = 0
        self.lx = self.corner[self.n][0]
        self.ly = self.corner[self.n][1]
        
    def next(self): 
        self.n += 1 

        self.lx = self.corner[self.n][0]
        self.ly = self.corner[self.n][1]
        
    def reset(self):
        self.n = 0
        self.lx = self.corner[self.n][0]
        self.ly = self.corner[self.n][1]
        
        
class Ghost():
    
    def __init__(self, ax, ay):
        self.lx = ax
        self.ly = ay
        self.ax = ax
        self.ay = ay

        self.onPath = []
        self.toPath = []
        self.finishPath = []

        self.followPath = []

    def drawPath(self, gameGrid, PAC, choosePath):
        endRecursion = False
        pathEnded = False

        while not endRecursion:
            # print(self.onPath)

            if len(self.toPath) == 0 and len(self.finishPath) > 0:
                endRecursion = True
                break

            if pathEnded:
                self.onPath = self.toPath.pop(0)
                self.lx, self.ly = self.onPath[-1]
                pathEnded = False
                # if dead end
            else:
                self.onPath.append([self.lx, self.ly])

            if PAC.lx == self.lx and PAC.ly == self.ly:
                self.finishPath.append(self.onPath)
                pathEnded = True
                continue

            possibleDir = self.checkPossible(gameGrid)

            if len(possibleDir) < 1:
                pathEnded = True
                continue

            elif len(possibleDir) == 1:
                self.lx = possibleDir[0][0]
                self.ly = possibleDir[0][1]

            elif len(possibleDir) > 1:
                newdir = possibleDir.pop(0)
                self.lx = newdir[0]
                self.ly = newdir[1]

                for possiblePath in possibleDir:

                    newpath = []
                    for item in self.onPath: newpath.append(item)
                    newpath.append(possiblePath)

                    self.toPath.append(newpath)

                #print(self.toPath, 'toPath')

        self.finishPath = doubleSort(self.finishPath)
        if len(self.finishPath) > choosePath:     
            self.followPath = self.finishPath[choosePath]
        else: 
            print("YES")
            self.followPath = self.finishPath[0]
    

    def checkPossible(self, gameGrid):
        possibleDir = []
                    
        if self.lx + 1 <= 9:
            if gameGrid[self.ly][self.lx + 1] == 0 and [self.lx + 1, self.ly] not in self.onPath:
                possibleDir.append([self.lx + 1, self.ly])
        # else:
        #     if gameGrid[self.ly][0] == 0 and [0, self.ly] not in self.onPath:
        #         possibleDir.append([0, self.ly])

            # right
        if self.lx - 1 >= 0:
            if gameGrid[self.ly][self.lx - 1] == 0 and [self.lx - 1, self.ly] not in self.onPath:
                possibleDir.append([self.lx - 1, self.ly])
        # else:
        #     if gameGrid[self.ly][9] == 0 and [9, self.ly] not in self.onPath:
        #         possibleDir.append([9, self.ly])
            # left
        if self.ly - 1 >= 0:
            if gameGrid[self.ly - 1][self.lx] == 0 and [self.lx, self.ly - 1] not in self.onPath:
                possibleDir.append([self.lx, self.ly - 1])
        # else:
        #     if gameGrid[9][self.lx] == 0 and [self.lx, 9] not in self.onPath:
        #         possibleDir.append([self.lx, 9])
            # up
        if self.ly + 1 <= 9:
            if gameGrid[self.ly + 1][self.lx] == 0 and [self.lx, self.ly + 1] not in self.onPath:
                possibleDir.append([self.lx, self.ly + 1])
        # else:
        #     if gameGrid[0][self.lx] == 0 and [self.lx, 0] not in self.onPath:
        #         possibleDir.append([self.lx, 0])

        return possibleDir

class pGhost():
    
    def __init__(self, ax, ay, dir, sp): 
        self.ax = ax 
        self.ay = ay 
        self.sp = sp
        self.dir = dir
    
    def checkEat(self, PAC, player): 
        if PAC.lx == self.ax and PAC.ly == self.ay: 
            return True
            
    def changeLocation(self, minput): 
        self.px = self.ax 
        self.py = self.ay
        self.dir = minput
        
        if self.dir == 0: 
            print("right")
            if self.ax + 1 <= 9: 
                if gameGrid[self.ay][self.ax + 1] != 1: 
                    self.ax = self.ax + self.sp ## for now
            else:
                self.ax = 0 
        if self.dir == 1: 
            print("left")
            if self.ax - 1 >= 0: 
                if gameGrid[self.ay][self.ax - 1] != 1:
                    self.ax = self.ax - self.sp
            else: 
                self.ax = 9
        if self.dir == 2: 
            print("up")
            if self.ay - 1 >= 0: 
                if gameGrid[self.ay - 1][self.ax] != 1:
                    self.ay = self.ay - self.sp
            else:
                self.ay = 9
        if self.dir == 3:
            print("down")
            if self.ay + 1 <= 9: 
                if gameGrid[self.ay + 1][self.ax] != 1:
                    self.ay = self.ay + self.sp
            else:
                self.ay = 0
        
def doubleSort(targetSort):
    # bubble sorts list from smallest to biggest
    
    n = len(targetSort)

    for i in range(1, n):
        isSorted = True
        for j in range(0, n - i):
            if len(targetSort[j]) > len(targetSort[j + 1]):
                targetSort[j], targetSort[j + 1] = targetSort[j + 1], targetSort[j]
                isSorted = False
        if isSorted:
            break

    return targetSort

def buildBox(x1,  y1,  scoreList,  rank,  displayText):
    # builds the box for the leaderboard
    
    wid =  width/2 - width/20
    hei =  height/12
    x2 =  x1 + wid 
    y2 =  y1 + hei
    
    strokeWeight(3)
    stroke(250, 255, 181)
    noFill()
    rectMode(CORNER)
    rect(x1,  y1,  wid,  hei)
    
    textAlign(CENTER,  CENTER)
    textSize(25)
    fill(250, 255, 181)
    
    if displayText: 
        text(scoreList[rank]["name"],  (x1 + x2)/2,  (y1 + y2)/2)
    else: 
        text(scoreList[rank]["score"],  (x1 + x2)/2,  (y1 + y2)/2)
        
                
def draw(): 
    global mode, mousePress    
    
    if mode == 0: 
        STARTSCREEN()
    elif mode == 1: 
        GAMEMODE()
    elif mode == 2:
        SCOREBOARD()
    elif mode == 3: 
        SETUPGAME()
    elif mode == 4: 
        GAMEOVER()
    elif mode == 5: 
        INPUTFILE()
    elif mode == 6:
        SCORESAVE()
    elif mode == 7: 
        HELPPAGE()
    elif mode == 8: 
        COUNTDOWN()
    elif mode == 9: 
        MGAMEMODE()
        
    mousePress = False
        
def GAMEMODE():
    # the function called when player starts game
    
    global gameGrid, dirInput, PAC, timer, GHOST1, GHOST2, changePath, escapeMode, G1, G2, scattertime, flashtime, blueOff, died1, died2, player
    global paused, pinky, dots, win, theme, themecolour
    # global pactime, dx, dy
    
    background(themecolour[0], themecolour[1], themecolour[2])
    stroke(250, 255, 181)
    strokeWeight(6)
    drawWall()
        
        
    if millis() - timer > 550 and not paused: 
            
        timer = millis()
        PAC.changeLocation(dirInput)  
        
        if not escapeMode: 
            if checkDots(): 
                escapeMode = True
                scattertime = millis() 
                
                GHOST1 = scatter(GHOST1, G1)
                GHOST2 = scatter(GHOST2, G2)
                
                died1 = False
                died2 = False
        else: 
             if checkDots(): 
                scattertime = millis() 
                
        checkCapture()
                
        if escapeMode: 
            if millis() - scattertime > 6500: 
                escapeMode = False
                G1.reset()
                G2.reset()
                died1 = False
                died2 = False
                
                GHOST1 = Ghost(GHOST1.ax, GHOST1.ay) 
                GHOST1.drawPath(gameGrid, PAC, 0)
                GHOST1.followPath.pop(0)
    
                GHOST2 = Ghost(GHOST2.ax, GHOST2.ay) 
                GHOST2.drawPath(gameGrid, PAC, changePath)
                GHOST2.followPath.pop(0)
            else:       
                if len(GHOST1.followPath) == 0: 
                    G1.next()
                    GHOST1 = scatter(GHOST1, G1)
                if len(GHOST2.followPath) == 0: 
                    G2.next()
                    GHOST2 = scatter(GHOST2, G2)
        else:
            GHOST1 = Ghost(GHOST1.ax, GHOST1.ay) 
            GHOST1.drawPath(gameGrid, PAC, 0)
            GHOST1.followPath.pop(0)

            GHOST2 = Ghost(GHOST2.ax, GHOST2.ay) 
            GHOST2.drawPath(gameGrid, PAC, changePath)
            GHOST2.followPath.pop(0)
            
        if not checkCapture():
            if not died1: 
                coor = GHOST1.followPath.pop(0)
                GHOST1.ax = coor[0]
                GHOST1.ay = coor[1]
                
            if not died2: 
                coor = GHOST2.followPath.pop(0)
                GHOST2.ax = coor[0]
                GHOST2.ay = coor[1]
        checkCapture()

    drawDots()
    drawPAC()
    
    if millis() - scattertime > 3000 and escapeMode:
        if millis() - flashtime > 250: 
            flashtime = millis()
            if blueOff: 
                blueOff = False
            else: 
                blueOff = True
        if not blueOff: 
            drawGHOST(GHOST1, 1)
            drawGHOST(GHOST2, 2)
    else: 
        drawGHOST(GHOST1, 1)
        drawGHOST(GHOST2, 2)

    if GHOST1.ax == GHOST2.ax and GHOST1.ay == GHOST2.ay:
        changePath = 1
    else: 
        changePath = 0
        
    drawInfo()
    strokeWeight(4)
    
    if player.lives < 0: 
        endGame((millis() - time)/1000)
        win = False
    if isGameFinish(dots): 
        endGame((millis() - time)/1000) 
        win = True
        
        
def MGAMEMODE(): 
    # multiplayer game mode, when not against AI but another person controlling the ghost
    
    global gameGrid, dirInput, PAC, timer, pGHOST, escapeMode, scattertime, flashtime, blueOff, died1, player
    global paused, dots, win, theme, themecolour, minput
    
    background(themecolour[0], themecolour[1], themecolour[2])
    stroke(250, 255, 181)
    strokeWeight(6)
    drawWall()
    
    if millis() - timer > 550 and not paused: 
            
        timer = millis()
        PAC.changeLocation(minput[0]) 
        if pGHOST.checkEat(PAC, player):
            resetGame()
            player.lives -= 1
            player.score -= 50
            
        pGHOST.changeLocation(minput[1]) 
        
        if pGHOST.checkEat(PAC, player): 
            resetGame()
            player.lives -= 1
            
        if not escapeMode: 
            if checkDots(): 
                escapeMode = True
                scattertime = millis() 
        else: 
             if checkDots(): 
                scattertime = millis() 
    
        if escapeMode: 
            if pGHOST.checkEat(PAC, player) and not died1: 
                pGHOST.ax, pGHOST.ay = 8, 7
                player.score += 150 
                died1 = True
                
            if millis() - scattertime > 6500: 
                escapeMode = False
            
    drawDots()
    drawPAC()
    
    if millis() - scattertime > 3000 and escapeMode:
        if millis() - flashtime > 250: 
            flashtime = millis()
            if blueOff: 
                blueOff = False
            else: 
                blueOff = True
        if not blueOff: 
            drawGHOST(pGHOST, 1)
    else: 
        drawGHOST(pGHOST, 1)
        
    drawInfo()
    strokeWeight(4)
    
    if player.lives < 0: 
        endGame((millis() - time)/1000)
        win = False
    if isGameFinish(dots): 
        endGame((millis() - time)/1000) 
        win = True
        
    
def STARTSCREEN():
    # the screen that is displayed with option to play and view leaderboard
    
    global mode, mousePress, scoreL, timer, mouth, scrollinc, multiplayer
    
    background(39, 32, 66)
    fill(250, 255, 181)
    strokeWeight(0)
    textAlign(CENTER, CENTER)
    textSize(80)
    text("PAC-MAN", width/2, height*3/10)

    if width/2 - width/5 < mouseX < width/2 + width/5 and height*2/3 - height/36 < mouseY < height*2/3 + height/36:
        fill(250, 200, 215)
        if mousePress == True:
            mousePress = False
            multiplayer = False
            Uinput = ""
            mode = 3
    else:
        fill(190, 145, 165)
        
    rectMode(CORNERS)
    rect(width/2 - width/5, height*2/3 + height/36, width/2 + width/5, height*2/3 - height/36)
    fill(255, 245, 215)
    textSize(20)
    text("START GAME", width/2, height*2/3)
    
    if width/2 - width/5 < mouseX < width/2 + width/5 and height*2/3 - height/36 - height/9 < mouseY < height*2/3 + height/36 - height/9:
        fill(250, 200, 215)
        if mousePress == True:
            mousePress = False
            scoreL = sorting(scoreL)
            mode = 2
            timer = millis()
    else:
        fill(190, 145, 165)
        
    rectMode(CORNERS)
    rect(width/2 - width/5, height*2/3 + height/36 - height/9, width/2 + width/5, height*2/3 - height/36 - height/9)
    fill(255, 245, 215)
    textSize(20)
    text("LEADERBOARD", width/2, height*2/3 - height/9)
    
    if width/2 - width/5 < mouseX < width/2 + width/5 and height*2/3 - height/36 + height/9 < mouseY < height*2/3 + height/36 + height/9:
        fill(250, 200, 215)
        if mousePress == True:
            mousePress = False
            multiplayer = True
            Uinput = ""
            mode = 3
    else:
        fill(190, 145, 165)
        
    rectMode(CORNERS)
    rect(width/2 - width/5, height*2/3 + height/36 + height/9, width/2 + width/5, height*2/3 - height/36 + height/9)
    fill(255, 245, 215)
    textSize(20)
    text("MULTIPLAYER", width/2, height*2/3 +  height/9)
    
    rectMode(CORNER)
    fill(200, 70, 70)
    rect(10*width/12, 11*height/12, width/12 + width/18, height/16)
    if 10*width/12 < mouseX < 10*width/12 + width/12 + width/18 and 11*height/12 < mouseY < 11*height/12 + height/16: 
        fill(150, 30, 30)
        if mousePress: 
            mode = 6
            timer = millis()
    rect(10*width/12 + width/96, 11*height/12 + height/96, width/12 + width/18 - 2*width/96, height/16 - 2*width/96)
    
    textAlign(LEFT, CENTER)
    fill(255, 255, 255)
    text("EXIT", 10*width/12 + 3*width/96, 11*height/12 + height/32)
    
    rectMode(CORNER)
    fill(83, 110, 73)
    rect(width/36, 11*height/12, width/12 + width/18, height/16)
    if width/36 < mouseX < width/18 + width/12 + width/36 and 11*height/12 < mouseY < 11*height/12 + height/16: 
        fill(60, 69, 57)
        if mousePress: 
            mode = 7
            mouth = millis()
    rect(width/36 + width/96, 11*height/12 + height/96, width/12 + width/18 - 2*width/96, height/16 - 2*width/96)
    
    textAlign(LEFT, CENTER)
    fill(255, 255, 255)
    text("HELP", width/36 + 3*width/96, 11*height/12 + height/32)
    
    
def SCOREBOARD():
    # the leaderboard, ranked from highest score to lowest score. left side is player name, right side is score
    
    global player, mode, scrollinc, scoreL, Uinput, tick, timer, scrollbarlen
    background(39, 32, 66)
    fill(250, 255, 181)
    strokeWeight(6)
    
    nameFound = searchScore()
    
    if len(Uinput) == 0: 
        scoreInput = scoreL
    else: 
        scoreInput = nameFound

    if millis() - timer > 500: 
        timer = millis() 
        if tick == "_":
            tick = " "
        else: 
            tick = "_"
            
    heiinc =  height/10
    titlepos =  height/12.0
    increm = -len(scoreInput)*heiinc*scrollinc
    
    hei =  height/6 + height/12 + increm
    
    for i in range(len(scoreInput)):
        displayText = True
        buildBox(50, hei, scoreInput, i, displayText) 
        hei =  hei + heiinc
 
    hei =  height/6 + height/12 + increm
    
    for k in range(len(scoreInput)):
        displayText = False
        buildBox(width/2, hei, scoreInput, k, displayText) 
        hei = hei + heiinc
        
    if keyPressed and key == ENTER:
        mode =  0    
        
    rectMode(CORNER)
    fill(39, 32, 66)
    noStroke()
    rect(0, 0, width, height/6 + height/12)

    textAlign(CENTER,  CENTER)
    textSize(45)
    fill(250, 255, 181)
    text("LEADERBOARD",  width/2,  titlepos)
    textSize(30)
    text(Uinput + tick,  width/2,  titlepos + height/9)
    textSize(15)
    fill(200, 205, 131)
    text("TYPE TO SEARCH USERNAME / ENTER TO QUIT TO MENU",  width/2,  titlepos + height/24)
    
    fill(250, 255, 181)
    rect(width - width/24, (height - scrollbarlen) + scrollinc*scrollbarlen, width/24 - width/96, height/12)

def COUNTDOWN(): 
    # counts down from 3 to start the start of the game 
    
    global mode, timer, slide, multiplayer
    background(0)
    
    fill(250, 255, 181)
    textSize(50)
    textAlign(CENTER,  CENTER)
    if slide == 4 or slide == 3: 
        text("ARE YOU READY", width/2, height/2)
    else: 
        text(slide + 1, width/2, height/2)
        
    if millis() - timer > 1000: 
        timer = millis()
        slide -= 1
        
    if slide < 0: 
        timer = millis()
        if multiplayer: 
            mode = 9
        else:
            mode = 1
        textSize(20)

    
def HELPPAGE():
    # contains the rules of the game, quick explanation of everything
    
    global mode, pac, pinky, bluey, mouth, mcycle, upcycle
    background(39, 32, 66)
    stroke(250, 255, 181)
    strokeWeight(6)
    imageMode(CORNER)
    
    if millis() - mouth > 200: 
        mouth = millis() 
        if upcycle: 
            mcycle += 1
            if mcycle == 3: 
                upcycle = False
        else: 
            mcycle -= 1
            if mcycle == 0: 
                upcycle = True 
    
    image(pac[mcycle], width/18, height/5, width/6, height/6)
    fill(200,200,200)
    circle(width/18 + 3*width/12, height/5 + height/12, width/20)
    fill(255,105,180)
    circle(width/18 + 4*width/12, height/5 + height/12, width/20)
    
    image(pinky, width/18, 2*height/5 + height/12, width/6, height/6)
    image(bluey, width/18 + width/6 + width/18, 2*height/5 + height/12, width/6, height/6)
    
    fill(250, 255, 181)
    textSize(20)
    text("YOUR OBJECTIVE IS TO EAT ALL THE WHITE DOTS \nWITHOUT GETTING KILLED BY THE GHOSTS. \n\nCHERRIES WILL SCATTER AWAY THE GHOSTS FOR 7 \nSECONDS. IN THIS TIME YOU MAY EAT THE \nGHOST AND DOTS.", width/18, height*4/5)
    
    strokeWeight(0)
    rectMode(CORNER)
    fill(200, 70, 70)
    rect(10*width/12, 11*height/12, width/12 + width/18, height/16)
    if 10*width/12 < mouseX < 10*width/12 + width/12 + width/18 and 11*height/12 < mouseY < 11*height/12 + height/16: 
        fill(150, 30, 30)
        if mousePress: 
            mode = 0
            timer = millis()
    rect(10*width/12 + width/96, 11*height/12 + height/96, width/12 + width/18 - 2*width/96, height/16 - 2*width/96)
    
    textAlign(LEFT, CENTER)
    fill(255, 255, 255)
    text("BACK", 10*width/12 + 3*width/96, 11*height/12 + height/32)
    
def SETUPGAME():
    # ability for player to choose/type a username and choose a theme for the game
    
    global mode, theme, themecolour, mousePress, boxoutline, Uinput, invalidn, invalidc, player, timer, tick, multiplayer
    
    background(47, 56, 82)
    
    if millis() - timer > 500: 
        timer = millis() 
        if tick == "_":
            tick = " "
        else: 
            tick = "_"
            
    textAlign(CENTER, CENTER)
    textSize(60)
    fill(250, 255, 181)
    text("CUSTOMISE", width/2, height/6)
    textAlign(LEFT, CENTER)
    textSize(20)
    text("SELECT YOUR THEME", 2*width/12, 4*height/12)
    text("CHOOSE YOUR NICKNAME", 2*width/12, 9*height/12)
    
    rectMode(CORNER)
    
    if mousePress and 5*height/12 < mouseY < 5*height/12 + height/6: 
        if 2*width/12 < mouseX < 2*width/12 + width/6:
            boxoutline = [True, False, False] 
        if 5*width/12 < mouseX < 5*width/12 + width/6:
            boxoutline = [False, True, False] 
        if 8*width/12 < mouseX < 8*width/12 + width/6:
            boxoutline = [False, False, True] 
 
    textAlign(CENTER, CENTER)        
    if boxoutline[0]:
        strokeWeight(8)
        stroke(250, 255, 181)
        textSize(24)
    fill(0)
    rect(2*width/12, 5*height/12, width/6, height/6)
    fill(250, 255, 181)
    text("MIDNIGHT", 2*width/12 + width/12, 5*height/12 + height/6 + height/24)
    strokeWeight(0)
    textSize(20)
    
    if boxoutline[1]:
        strokeWeight(8)
        stroke(250, 255, 181)
        textSize(24)
    fill(90, 107, 81)
    rect(5*width/12, 5*height/12, width/6, height/6)
    fill(250, 255, 181)
    text("COPPICE", 5*width/12 + width/12, 5*height/12 + height/6 + height/24)
    strokeWeight(0)
    textSize(20)
    
    if boxoutline[2]:
        strokeWeight(8)
        stroke(250, 255, 181)
        textSize(24)
    fill(9, 24, 143)
    rect(8*width/12, 5*height/12, width/6, height/6)
    fill(250, 255, 181)
    text("MARINE", 8*width/12 + width/12, 5*height/12 + height/6 + height/24)
    strokeWeight(0)
    textSize(20)
       
    textAlign(LEFT, CENTER)    
    text(Uinput + tick, 2*width/12, 10*height/12)
    
    rectMode(CORNER)
    fill(151, 194, 183) 
    stroke(250, 255, 181)
    strokeWeight(3)
    rect(8*width/12, 10*height/12, width/12 + width/18, height/16)
    if 8*width/12 < mouseX < 8*width/12 + width/12 + width/18 and 10*height/12 < mouseY < 10*height/12 + height/16: 
        fill(94, 140, 128)
        if mousePress: 
            if checkUinput(Uinput) and True in boxoutline and len(Uinput) > 0: 
                totalRESET()
                mode = 8
                invalidc = False
                invalidn = False
                player = Player(Uinput)
                Uinput = ""
                themecolour = theme[boxoutline.index(True)]
                boxoutline = [False, False, False] 
            elif True not in boxoutline: 
                invalidc = True 
            else:
                invalidn = True 
    
    rect(8*width/12 + width/96, 10*height/12 + height/96, width/12 + width/18 - 2*width/96, height/16 - 2*width/96)
    
    if invalidn: 
        fill(230, 104, 85)
        text("NAME ALREADY TAKEN", 2*width/12, 10*height/12 + height/24)
    if invalidc: 
        fill(230, 104, 85)
        text("PLEASE PICK THEME", 2*width/12, 10*height/12 + 2*height/24)
        
    textAlign(LEFT, CENTER)
    fill(255, 255, 255)
    text("NEXT", 8*width/12 + 3*width/96, 10*height/12 + height/32)
    
    fill(200, 70, 70)
    rect(10*width/12, 10*height/12, width/12 + width/18, height/16)
    if 10*width/12 < mouseX < 10*width/12 + width/12 + width/18 and 10*height/12 < mouseY < 10*height/12 + height/16: 
        fill(150, 30, 30)
        if mousePress: 
            mode = 0
    rect(10*width/12 + width/96, 10*height/12 + height/96, width/12 + width/18 - 2*width/96, height/16 - 2*width/96)
    
    textAlign(LEFT, CENTER)
    fill(255, 255, 255)
    text("BACK", 10*width/12 + 3*width/96, 10*height/12 + height/32)
    
    strokeWeight(0)

    mousePress = False

def GAMEOVER():
    # a timed display shown to player when the game ends, either from running out of lives or capturing all the dots
    
    global win, scoreL, mode, timer, themecolour, theme, pausetime, time
    
    themecolour = theme[0]
    background(39, 32, 66)
    textAlign(CENTER, CENTER)
    textSize(60)
    fill(250, 255, 181)
    
    if win: 
        text("YOU WIN", width/2, height/6)
    else: 
        text("GAME OVER", width/2, height/6)
    
    textAlign(LEFT, CENTER) 
    textSize(30)   
    text("YOUR SCORE " + str(scoreL[-1]["score"]), width/6, 6*height/12)
    text("YOUR TIME " + str(scoreL[-1]["time"]), width/6, 5*height/12)
    
    pausetime = millis() - time
    
    if millis() - timer > 5000: 
        mode = 0 
                     
                                                           
def checkUinput(Uinput): 
    # checks if the username inputted by player has already been taken before
    
    global scoreL
    
    for d in scoreL: 
        if Uinput == d["name"]:
            return False
    return True
  
              
def endGame(time): 
    # appends player name and player score to scoreL, then the game ended screen is shown  
    
    global scoreL, player, mode, timer, Uinput
    p = dict(name = player.name, score = player.score, time = time)    
    scoreL.append(p)                        
    
    mode = 4    
    timer = millis()
            
                                                                                                                                                                                                                                                                                                                                                                                                            
def checkCapture(): 
    # checks if the player has captured the ghost in escapeMode and if the ghost has captured the player regularly
    
    global GHOST1, GHOST2, died1, died2, player
    
    capture = False
    if GHOST1.ax == PAC.lx and GHOST1.ay == PAC.ly: 
        if escapeMode: 
            if not died1: 
                GHOST1 = Ghost(8, 7)
                player.ghost()
                died1 = True 
        else: 
            player.captured()
            resetGame()
            capture = True
        
    if GHOST2.ax == PAC.lx and GHOST2.ay == PAC.ly: 
        if escapeMode: 
            if not died2:
                GHOST2 = Ghost(1, 8) 
                player.ghost()
                died2 = True
        else: 
            player.captured()
            resetGame()
            capture = True
    
    return capture
            
        
def scatter(GHOST, G): 
    # if escapeMode is activated, GHOSTS scatter 
    
    GHOST = Ghost(GHOST.ax, GHOST.ay)
    GHOST.drawPath(gameGrid, G, 0)
    
    return GHOST

def drawInfo(): 
    # displays the amount of lives the player has, the score, the time, and the ability to quit anytime
    global player, paused, pausetime, mousePress, time, mode

    
    textAlign(LEFT, CENTER)
    fill(255, 255, 255)
    text("SCORE  " + str(player.score), width/12, height/12 - height/24)
    
    textAlign(RIGHT, CENTER)
    text("LIVES  " + str(player.lives), 11*width/12, height/12 - height/24)
    
    textAlign(LEFT, CENTER)
    if not paused: 
        text("TIME  " + str((millis() - time)/1000), width/12, height - height/24)
    else: 
        text("TIME  " + str(pausetime/1000), width/12, height - height/24)
       
    rectMode(CORNERS)
    fill(200, 70, 70) 
    rect(9*width/12 + width/24, height - height/96, 9*width/12 + width/24 + width/6, 11*height/12 + height/96)
    if 9*width/12 + width/24 < mouseX < 9*width/12 + width/24 + width/6 and 11*height/12 + height/96 < mouseY < height - height/96: 
        fill(150, 30, 30)
        if mousePress: 
            if paused: 
                paused = False
                time = millis() - pausetime
            else: 
                paused = True 
                pausetime = millis() - time
            
            mousePress = False
    else: 
        fill(200, 70, 70) 
        
    rect(9*width/12 + width/24 + width/96, height - height/96 - width/96, 9*width/12 + width/24 + width/6 - width/96, 11*height/12 + height/96 + width/96)
    textAlign(RIGHT, CENTER)
    fill(255, 255, 255)
    text("QUIT", 11*width/12, height - height/24)
 
    if paused: 
        rectMode(CORNERS)
        
        if 4*width/12 < mouseX < 8*width/12 and 4.5*height/12 < mouseY < 7.5*height/12: 
            fill(81, 76, 110)
            if mousePress: 
                mode = 0 
                paused = False
                mousePress = False
                pausetime = millis() - time
        else: 
            fill(46, 41, 71)
            
        rect(4*width/12, 7.5*height/12, 8*width/12, 4.5*height/12)
        
        textAlign(CENTER, CENTER)
        fill(255)
        text("DO YOU REALLY " + "\n" + "WANT TO QUIT?", 6*width/12, 6*height/12)
    
def drawDots(): 
    # displays the white dots for the player to eat, as well as the red cherries
    
    global dots, PAC
    
    shapeMode(CENTER) 
    
    for i in range (len(dots)): 
        for j in range (len(dots[i])): 
            if dots[i][j] == 1: 
                xc = ( (j + 0.5 + 1)/ 12 )*width
                yc = ( (i + 0.5 + 1)/ 12 )*height
                
                fill(200,200,200)
                circle(xc, yc, 25) 
            if dots[i][j] == 2: 
                xc = ( (j + 0.5 + 1)/ 12 )*width
                yc = ( (i + 0.5 + 1)/ 12 )*height
                
                fill(255,105,180)
                circle(xc, yc, 25) 
            
        
def isGameFinish(dots):  
    # checks if the game is finished, game is finished if there are no more dots left
    
    for row in dots: 
        for block in row: 
            if block == 1: 
                return False
    return True

                  
                              
def checkDots(): 
    # chhecks if the player is currently on a dot. checks if player has captured a cherry, thereby 
    # activating escapeMode
    global dots, PAC, player
    
    if dots[PAC.ly][PAC.lx] == 1: 
        dots[PAC.ly][PAC.lx] = 0
        player.dots()
        return False
        
    elif dots[PAC.ly][PAC.lx] == 2: 
        dots[PAC.ly][PAC.lx] = 0 
        return True
        
      
def makeCherry(numCherry):
    # randomly generates three cherries on the game board in the beginning of game. makes sure the cherries are not
    # on the same location as where the player is standing
     
    global dots, gameGrid
    global PAC
    
    for i in range(numCherry): 
        blocky = random.randint(0, len(gameGrid) - 1)
        blockx = random.randint(0, len(gameGrid) - 1)
        
        while dots[blocky][blockx] == 0 or PAC.lx == blockx or PAC.ly == blocky: 
            blocky = random.randint(0, len(gameGrid) - 1)
            blockx = random.randint(0, len(gameGrid) - 1)
            
        dots[blocky][blockx] = 2
    
    dotTemplate = dots 
    
    return dotTemplate
          
    
def drawPAC():
    # draws pacman and its animations
    
    global gameGrid, PAC, pac, mouth, mcycle, upcycle
    
    if millis() - mouth > 100: 
        mouth = millis() 
        if upcycle: 
            mcycle += 1
            if mcycle == 3: 
                upcycle = False
        else: 
            mcycle -= 1
            if mcycle == 0: 
                upcycle = True 

    
    xc = ( (PAC.lx + 0.5 + 1)/ 12 )*width
    yc = ( (PAC.ly + 0.5 + 1)/ 12 )*height
    
    imageMode(CENTER)
    if PAC.dir == 0: 
        pushMatrix()
        translate(xc, yc)
        rotate(radians(0))
        image(pac[mcycle], 0, 0)
        popMatrix()
    elif PAC.dir == 1: 
        pushMatrix()
        translate(xc, yc)
        rotate(radians(180))
        image(pac[mcycle], 0, 0)
        popMatrix()
    elif PAC.dir == 2: 
        pushMatrix()
        translate(xc, yc)
        rotate(radians(270))
        image(pac[mcycle], 0, 0)
        popMatrix()
    elif PAC.dir == 3:
        pushMatrix()
        translate(xc, yc)
        rotate(radians(90))
        image(pac[mcycle], 0, 0)
        popMatrix()
        
    
def drawGHOST(GHOST, co):
    # draws the two ghosts, and its scatter (blue) form in escapeMode 
    # two different colour of ghosts
    
    global gameGrid, escapeMode, pinky, bluey, scattery
    
    shapeMode(CENTER)
    xc = ( (GHOST.ax + 0.5 + 1)/ 12 )*width
    yc = ( (GHOST.ay + 0.5 + 1)/ 12 )*height
    
    if escapeMode: 
        imageMode(CENTER)
        image(scattery, xc, yc, 50, 50)
    elif co == 1: 
        fill(255,185,240)
        imageMode(CENTER)
        image(pinky, xc, yc, 50, 50)
    elif co == 2: 
        imageMode(CENTER)
        image(bluey, xc, yc, 50, 50)
    
                            
def drawWall(): 
    # draws the walls in the game
    
    global gameGrid, themecolour
    rectMode(CORNER)
    
    row = (width/12)
    col = (height/12)
    
    for i in gameGrid: 
        for j in i:
            if j == 1: 
                fill(themecolour[3], themecolour[4], themecolour[5])
                rect(row, col, width/12, height/12)
            row += width/12
        row = width/12
        col += height/12

def SCORESAVE():
    # prompt shown at the end, when player presses exit on the program. 
    # prompts player to save to a file. if file does not exist, game will attempt to create it.
    global saveName,  saveEntered, scoreL, tick, timer 
    background(39, 32, 66)
    
    if millis() - timer > 500: 
        timer = millis() 
        if tick == "_":
            tick = " "
        else: 
            tick = "_"
            
    textAlign(CENTER,  CENTER)
    textSize(30)
    fill(250, 255, 181)
    text("INPUT SAVE GAME FILE: ",  width/2,  height*2/4)
    
    textSize(15)
    text(saveName + tick,  width/2,  height*2/4 + 40)
        
    if saveEntered:
        address =  os.path.join(directory,  saveName + ".txt")
    
        with open(address, 'wb') as file:
            pickle.dump(scoreL,  file)
        
        delay(500)
        exit()
        
        
def INPUTFILE():
    # prompt shown before game starts to retrieve scoreboard from preexisting savegame. 
    
    global directory, wrongfile, mode, saveName, saveEntered, scoreL, tick, timer
    
    background(39, 32, 66)
    textAlign(CENTER,  CENTER)
    textSize(30)
    fill(250, 255, 181)
    
    if millis() - timer > 500: 
        timer = millis() 
        if tick == "_":
            tick = " "
        else: 
            tick = "_"
            
    if not wrongfile:
        text("ENTER SAVE GAME: ",  width/2,  height*2/4)
    else: 
        text("ENTER SAVE GAME FULL PATH: ",  width/2,  height*2/4)
        
    textSize(15)
    text(saveName + tick,  width/2,  height*2/4 + 40)
    
    if saveEntered: 
        try:
            if not wrongfile:
                fileaddress =  os.path.join(directory,  saveName + ".txt")
                with open(fileaddress,  'rb') as f:
                    scoreL =  pickle.load(f)
            else: 
                with open(saveName,  'rb') as f:
                    scoreL =  pickle.load(f)
            scoreL = list(scoreL)
            mode =  0
            saveEntered = False
        except: 
            saveEntered =  False
            saveName = ""
            wrongfile =  True    
                
    
def sorting(scoreL):
    # sorts the scoreL from largest to smallest scores
    
    n =  len(scoreL)

    for i in range(1,  n):
        isSorted =  True
        for j in range(0,  n - i):
            if scoreL[j]["score"] < scoreL[j + 1]["score"]:
                scoreL[j],  scoreL[j + 1] =  scoreL[j + 1],  scoreL[j]
                isSorted =  False
        if isSorted:
            break
    return scoreL


def searchScore(): 
    # searches the dictionary of scoreL for the username of a player
    global scoreL, Uinput
    
    nameFound = [] 
    
    for i in range(len(scoreL)):
        if Uinput in scoreL[i]["name"]: 
            nameFound.append(scoreL[i])
            
    return nameFound


def keyReleased():
    # controls direction of player, multiplayer, input of file, input of username, and search of player in leaderboard
    global dirInput, mode, Uinput
    global saveName,  saveEntered, minput
    
    wordBank = "abcdefghijklmnopqrstuvwyxz1234567890_!?*^-." 
    
    if mode == 1:
        if key == "d":
            dirInput = 0
        elif key == "a":
            dirInput = 1
        elif key == "w":
            dirInput = 2
        elif key == "s":
            dirInput = 3
            
        if key == CODED: 
            if keyCode == RIGHT:
                dirInput = 0
            elif keyCode == LEFT:
                dirInput = 1
            elif keyCode == UP:
                dirInput = 2
            elif keyCode == DOWN:
                dirInput = 3
                
    if mode == 3 or mode == 2: 
        if key != CODED:
            if key == BACKSPACE: 
                Uinput = Uinput[:-1]
            elif len(Uinput) < 16:
                if key in wordBank or key in wordBank.upper():
                    Uinput = Uinput + key
    if mode == 6 or mode == 5: 
        if key != CODED:
            if key == BACKSPACE: 
                saveName = saveName[:-1]
            elif key == ENTER: 
                saveEntered = True 
            elif len(Uinput) < 8:
                if key in wordBank or key in wordBank.upper():
                    saveName = saveName + key
    if mode == 9: 
        if key == "d":
            minput[0] = 0
        elif key == "a":
            minput[0] = 1
        elif key == "w":
            minput[0] = 2
        elif key == "s":
            minput[0] = 3
            
        if key == CODED: 
            if keyCode == RIGHT:
                minput[1] = 0
            elif keyCode == LEFT:
                minput[1] = 1
            elif keyCode == UP:
                minput[1] = 2
            elif keyCode == DOWN:
                minput[1] = 3
        
def mouseReleased(): 
    global mousePress
    
    mousePress = True 
    
def mouseDragged():
    # used for scrolling in leaderboard
    
    global mode, scrollinc, scoreL, scrollbarlen
    
    if mode == 2: 
        if 0 <= scrollinc - (pmouseY - mouseY)*1.0/scrollbarlen <= 1 - (height/9.0)/height:
            scrollinc -= (pmouseY - mouseY)*1.0/scrollbarlen

    
    
    
        
    
