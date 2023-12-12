# Pongtato

# Global Variables
gameState=0
TITLE_STATE=0
PLAY_STATE=1
GAME_OVER_STATE=2
STORE_PAGE = 3

enemyBallList=[]
INITIAL_BALL_SIZE = 60
BALL_IMPACT_DECAY = 0.95
BALL_SIZE_DECAY = -0.02

# Variables here would need to reset after a match
playerExp = 0
playerLevel = 1
expToNextLevel = 2
expIncrement = 3
enemyHP = 1
SpawnedEnemies = 0
playerBallSize = 60
playerBallPenPower = 1
playerBallStock = 5
enemyRespawnInterval = 30
ballReplenishInterval = 360
remainReplenishInterval = 360
currentScore = 0

playerBallList=[]

paddlePosX=0
paddlePosY=0
paddleWidth=120
paddleHeight=20

# Possible Upgrade List
upgradeList = ["Ball Size increase", 
             "Paddle Width increase", 
             "Ball Penetration Power + 1", 
             "Ball Stock + 3", 
             "Enemies Refresh Frequency Decrease"]

currentStoreList = []

#____________Main Functions___________#
def setup():
    global paddlePosX,paddlePosY,paddleWidth,paddleHeight
    size(960,480)
    background(0)
    textSize(32)

def draw():
    background(0)
    if gameState==TITLE_STATE:
        drawTitleScreen()
    elif gameState==PLAY_STATE:
        drawPlayScreen()
    elif gameState==GAME_OVER_STATE:
        drawGameOverScreen()
    elif gameState == STORE_PAGE:
        drawStorePage()

#__________Sub Draw Functions___________#

def drawTitleScreen():
    textSize(64)
    textAlign(CENTER)
    text("Pongtato",width/2,height/2)

    # textSize(32)
    # textAlign(LEFT)
    # text("Today's Date:"+str(month())+"-"+str(day())+"-"+str(year()),20,40)
    # textAlign(RIGHT)
    # text(str(hour())+":"+nf(minute(),2)+":"+nf(second(),2),width-20,40)
    # textAlign(CENTER)
    textSize(30)
    text("Press P to Start",width/2,height*2/3)
    
def drawPlayScreen():
    updatePaddle()
    enemySpawnController()
    resetBallCollision()
    UpdatePlayerBalls()
    UpdateEnemyBalls()
    updatePlayerExp()
    updateAutoReplenish()
    drawUI()
        
def drawGameOverScreen():
    global objects
    fill(255)
    textAlign(CENTER, CENTER)
    textSize(60)
    text("GAME OVER",width/2,height/2)
    textSize(30)
    text("Your Score is: " + str(currentScore), width/2, height/2 - 100)
    text("Press P to go Main Menu", width/2, height/2 + 100)
    objects=[]
    
def drawStorePage():
    global upgradeList, currentStoreList, gameState
    tempY = 30
    tempYInc = 160
    for i in range(3):
        if buttonCreation(100, tempY + tempYInc * i, 760, 100, upgradeList[currentStoreList[i]]):
            applyUpgrade(currentStoreList[i])
            gameState = PLAY_STATE
        else:
            pass

#______________Helper Functions____________#
def updatePaddle():
    global paddlePosY,paddlePosX 
    paddlePosX=mouseX
    paddlePosY=height
    rectMode(CENTER)
    fill(255)
    rect(paddlePosX,paddlePosY,paddleWidth,paddleHeight)
    
def enemySpawnController():
    global enemyHP, SpawnedEnemies
    if SpawnedEnemies / 10 > enemyHP:
        enemyHP += 1
    if frameCount % enemyRespawnInterval == 0:            
        startPos=PVector(random(0,width), 30)
        tempVel=PVector(random(0,1), random(0,2))
        tempColor=color(random(120, 255), random(120, 255), random(120, 255))
        newEnemyBall=EnemyBall(startPos,tempVel,INITIAL_BALL_SIZE,tempColor,enemyHP)
        enemyBallList.append(newEnemyBall)
        SpawnedEnemies += 1        

def applyUpgrade(upgradeNum):
    global playerBallSize, paddleWidth, playerBallPenPower, enemyRespawnInterval, playerBallStock
    if upgradeNum == 0:
        playerBallSize += 20
    elif upgradeNum == 1:
        paddleWidth += 40
    elif upgradeNum == 2:
        playerBallPenPower += 1
    elif upgradeNum == 3:
        playerBallStock += 3
    elif upgradeNum == 4:
        enemyRespawnInterval += 5
    else:
        pass

def keyPressed():
    global gameState,startTime
    if key =="p" or key=="P":
        if gameState==TITLE_STATE:
            gameState=PLAY_STATE
            startTime=millis()
        # elif gameState==PLAY_STATE:
        #     gameState=GAME_OVER_STATE                
        elif gameState==GAME_OVER_STATE:
            gameState=TITLE_STATE
            resetGameConst()
            
    if key==" ":
        global playerBallStock
        if playerBallStock >= 1:
            startPos=PVector(mouseX, height - playerBallSize / 2 - paddleHeight)
            tempVel=PVector(random(0,4), random(0,10))
            tempColor=color(random(120, 255), random(120, 255), random(120, 255))
            tempVel.normalize().mult(11)
            # tempVel2=PVector(random(10,10), random(4,4))        
            newPlayerBall=PlayerBall(startPos,tempVel, playerBallSize, tempColor,1)       
            playerBallList.append(newPlayerBall)
            playerBallStock -= 1 
        
def UpdateEnemyBalls():
    global gameState,enemyBallList,playerBallList
    for ball in enemyBallList:
        ball.update()    
        ball.render()
        if ball.rad<0:            
            enemyBallList.remove(ball)
        if ball.collision(paddlePosX,paddlePosY,paddleWidth,paddleHeight):
            enemyBallList=[]
            playerBallList=[]
            gameState=GAME_OVER_STATE
            
def UpdatePlayerBalls():
    for playerBall in playerBallList:
        playerBall.EnemyCollision()
        playerBall.update()    
        playerBall.render()
        playerBall.collision(paddlePosX,paddlePosY,paddleWidth,paddleHeight)
            
def updatePlayerExp():
    global playerExp, playerLevel, expToNextLevel, expIncrement, gameState, playerBallStock
    if playerExp >= expToNextLevel:
        playerExp = 0
        playerLevel += 1
        expToNextLevel += expIncrement
        expIncrement += 1
        gameState = STORE_PAGE
        playerBallStock += 1
        storeSetup()

def updateAutoReplenish():
    global ballReplenishInterval, playerBallStock, remainReplenishInterval
    if remainReplenishInterval <= 0:
        playerBallStock += 1
        remainReplenishInterval = ballReplenishInterval
    else:
        remainReplenishInterval -= 1
    
def storeSetup():
    global currentStoreList, mouseClickPasser
    mouseClickPasser = False
    currentStoreList = []
    for i in range(3):
        # TODO: check repetition of elements
        tempInt = int(random(0, len(upgradeList)))
        currentStoreList.append(tempInt)

def resetGameConst():
    global currentScore, remainReplenishInterval, ballReplenishInterval, playerExp, playerLevel, expToNextLevel, enemyHP, SpawnedEnemies, playerBallSize, playerBallPenPower, playerBallStock, enemyRespawnInterval, paddleWidth
    playerExp = 0
    playerLevel = 1
    expToNextLevel = 2
    enemyHP = 1
    SpawnedEnemies = 0
    playerBallSize = 60
    playerBallPenPower = 1
    playerBallStock = 5
    enemyRespawnInterval = 30
    ballReplenishInterval = 360
    remainReplenishInterval = 360
    paddleWidth=120
    currentScore = 0

def offScreen(vector, rad):
    rad /= 2
    if vector.x - rad < 0:
        return 1 # N
    elif vector.y + rad > height:
        return 2 # E
    elif vector.x + rad > width:
        return 3 # S
    elif vector.y - rad < 0:
        return 4 # W
    return 0    

def reflect(ball1, ball2):
    normal = PVector.sub(ball1.pos, ball2.pos)
    normal.normalize()
    
    dot = 2 * ball1.vel.dot(normal)
    ball1.vel.sub(PVector.mult(normal, dot))
    
    normal = PVector.mult(normal, -1)
    dot2 = 2 * ball2.vel.dot(normal)
    ball2.vel.sub(PVector.mult(normal, dot2))
    
def resetBallCollision():
    for enemyBall in enemyBallList:
        enemyBall.collidedThisFrame = False
    for playerBall in playerBallList:
        playerBall.collidedThisFrame = False
        
def buttonCreation(posX, posY, sizeX, sizeY, tempText):
    global mouseClickPasser
    rectMode(CORNER)
    textAlign(CENTER,CENTER)
    if (mouseX < posX + sizeX) and (mouseX > posX) and (mouseY < posY + sizeY) and (mouseY > posY):
        fill(200, 200, 250)
        rect(posX, posY, sizeX, sizeY)
        fill(40)
        textSize(30)
        text(tempText, posX + 0.5 * sizeX, posY + 0.5 * sizeY)
        if mouseClickPasser:
            mouseClickPasser = False
            return True
    else:
        fill(100, 100, 130)
        rect(posX, posY, sizeX, sizeY)
        fill(250)
        textSize(20)
        text(tempText, posX + 0.5 * sizeX, posY + 0.5 * sizeY)
    return False

def mouseClicked():
    global mouseClickPasser
    mouseClickPasser = True

#______________Render UIs_____________#
def drawUI():
    drawExpBar()
    drawRemainingBalls()
    drawReplenishBar()
    drawScore()
    # drawTime()
    
def drawExpBar():
    fill(100, 100, 255, 80)
    expPercentage = float(playerExp) / expToNextLevel
    rectMode(CORNER)
    rect(0, 0, expPercentage * width, 30) 
    fill(255)
    textAlign(LEFT)
    textSize(30)
    text("level: " + str(playerLevel), 80, 30)
    
def drawRemainingBalls():
    textAlign(LEFT)
    textSize(30)
    text("Remaining Balls: " + str(playerBallStock), 380, 30)

def drawTime():
    offsetTime=millis()-startTime
    seondsString=str(offsetTime/1000)
    middleString=str((offsetTime%1000-(offsetTime%100))/100)
    millisecondsString=nf(offsetTime%100,2)
    offsetString=seondsString+":"+middleString+":"+millisecondsString
    textAlign(CENTER)
    fill(255)
    text(offsetString+"\n"+str(offsetTime),width/2,height/2)
    
def drawReplenishBar():
    fill(100, 255, 100, 80)
    rectMode(CORNER)
    tempBar = float(remainReplenishInterval) / ballReplenishInterval
    rect(0, 30, tempBar * width, 10)
    
def drawScore():
    textAlign(RIGHT)
    textSize(30)
    fill(255)
    text("Score: " + str(currentScore), width - 100, 30)

#__________EnemyBall Class_________#
class EnemyBall:
    def __init__(self,tempPos,tempVel,tempSize,tempColor,enemyHP):
        self.pos=tempPos
        self.vel=tempVel
        self.rad=tempSize
        self.col=tempColor
        self.enemyHP=enemyHP
        self.colliedThisFrame=False
        
    def update(self):
        global playerExp, currentScore
        self.pos+= self.vel         

        whichWall = offScreen(self.pos, self.rad)
        if whichWall > 0:    
            self.rad *= BALL_IMPACT_DECAY
            if whichWall == 1 or whichWall == 3:
                self.vel.rotate(PI - 2*self.vel.heading())
            else:
                self.vel.rotate(-2 * self.vel.heading())
                
        if self.rad > 0:
            if self.rad > INITIAL_BALL_SIZE/4:
                self.rad += BALL_SIZE_DECAY
            else:
                self.rad += BALL_SIZE_DECAY * 10
        if self.colliedThisFrame==True:
                self.enemyHP-=1
                self.colliedThisFrame=False
        if self.enemyHP <= 0:
            enemyBallList.remove(self)
            playerExp += 1
            currentScore += enemyHP * 1000
            
    def render(self):
        pushStyle()
        fill(0,0,0,0)
        stroke(self.col, 255 * self.rad/float(INITIAL_BALL_SIZE))
        ellipse(self.pos.x, self.pos.y, self.rad, self.rad)
        fill(self.col)
        text(self.enemyHP,self.pos.x,self.pos.y)
        popStyle()

    def collision(self,paddlePosX,paddlePosY,paddleWidth,paddleHeight):
        if self.pos.x> paddlePosX-paddleWidth/2 and self.pos.x<paddlePosX+paddleWidth/2:
            if self.pos.y + self.rad / 2 >paddlePosY - paddleHeight / 2 and self.pos.y + self.rad / 2< paddlePosY + paddleHeight / 2:
                return True
            return False
#_________Player Ball__________#
class PlayerBall(EnemyBall):
    def update(self):
        self.pos += self.vel #/10.0        
        whichWall = offScreen(self.pos, self.rad)
        if whichWall > 0:     
            if whichWall == 1 or whichWall == 3:
                self.vel.rotate(PI - 2*self.vel.heading())
            elif whichWall == 4:
                self.vel.rotate(-2*self.vel.heading())
            else:
                playerBallList.remove(self)
                   
    def render(self):
        pushStyle()
        fill(255)
        circle(self.pos.x, self.pos.y, self.rad)    
        fill(self.col)
        text(self.enemyHP,self.pos.x,self.pos.y)
        popStyle()
        
    def collision(self,paddlePosX,paddlePosY,paddleWidth,paddleHeight):
        if self.pos.x>paddlePosX-paddleWidth/2 - self.rad / 3 and self.pos.x<paddlePosX+paddleWidth/2 + self.rad / 3:
            if self.pos.y + self.rad / 2 >paddlePosY - paddleHeight / 2 and self.pos.y + self.rad / 2< paddlePosY + paddleHeight / 2:
                self.vel.rotate(-2 * self.vel.heading())
                
    def EnemyCollision(self): 
        for enemyball in enemyBallList:
            for playerball in playerBallList:
                if not playerball.collidedThisFrame and not enemyball.collidedThisFrame:
                    if dist(playerball.pos.x, playerball.pos.y, enemyball.pos.x, enemyball.pos.y) < (playerball.rad/2 + enemyball.rad/2):
                        reflect(playerball, enemyball)
                        playerball.collidedThisFrame = True
                        enemyball.collidedThisFrame = True
                        enemyball.enemyHP -= playerBallPenPower
