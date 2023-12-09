gameState=0
TITLE_STATE=0
PLAY_STATE=1
GAME_OVER_STATE=2
#游戏暂停
paused=False
#敌人的球球
#血量
wallHitCount=10
startPos = None
enemyBallList=[]
INITIAL_BALL_SIZE = 60
BALL_IMPACT_DECAY = 0.95
BALL_SIZE_DECAY = -0.02
startPos=None
#玩家的球球
playerBallList=[]
#板子
paddlePosX=0
paddlePosY=0
paddleWidth=120
paddleHeight=20
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
def drawTitleScreen():
    textSize(64)
    textAlign(CENTER)
    text("Title Screen",width/2,height/2)
    #text(str(millis()),width/2,height/2)
    textSize(32)
    textAlign(LEFT)
    text("Today's Date:"+str(month())+"-"+str(day())+"-"+str(year()),20,40)
    textAlign(RIGHT)
    text(str(hour())+":"+nf(minute(),2)+":"+nf(second(),2),width-20,40)
    textAlign(CENTER)
    text("Press P to Start",width/2,height*2/3)
def drawPlayScreen():
    global gameState,startPos,paddlePosY,paddlePosX,pause
    if not paused:        
        paddlePosX=mouseX
        paddlePosY=height
        offsetTime=millis()-startTime
        seondsString=str(offsetTime/1000)
        middleString=str((offsetTime%1000-(offsetTime%100))/100)
        millisecondsString=nf(offsetTime%100,2)
        offsetString=seondsString+":"+middleString+":"+millisecondsString
        #板子
        textAlign(CENTER)
        fill(255)
        text(offsetString+"\n"+str(offsetTime),width/2,height/2)
        rectMode(CENTER)
        fill(255)
        rect(paddlePosX,paddlePosY,paddleWidth,paddleHeight)
        #球球
        if frameCount % 30 == 0:            
            startPos=PVector(random(0,width),0)
            tempVel=PVector(random(0,1), random(0,2))
            tempColor=color(random(120, 255), random(120, 255), random(120, 255))
            newEnemyBall=EnemyBall(startPos,tempVel,INITIAL_BALL_SIZE,tempColor,wallHitCount)
            enemyBallList.append(newEnemyBall)
        UpdateEnemyBalls()
        UpdatePlayerBalls()
    if paused:
        
        
        
def drawGameOverScreen():
    global objects
    textAlign(CENTER)
    text("GAME OVER",width/2,height/2)
    objects=[]
def keyPressed():
    global gameState,startTime,startPos,paused
    if key =="p" or key=="P":
        if gameState==TITLE_STATE:
            gameState=PLAY_STATE
            startTime=millis()
            print(startTime)
        elif gameState==PLAY_STATE:
            gameState=GAME_OVER_STATE                
        elif gameState==GAME_OVER_STATE:
            gameState=TITLE_STATE
    #测试
    if key=="A" or key=="a":
        startPos=PVector(random(0,width),0)
        tempVel=PVector(random(0,10), random(0,4))
        tempColor=color(random(120, 255), random(120, 255), random(120, 255))
       # newEnemyBall=EnemyBall(startPos,tempVel,INITIAL_BALL_SIZE,tempColor)
        tempVel2=PVector(random(10,10), random(4,4))        
        newPlayerBall=PlayerBall(startPos,tempVel2,INITIAL_BALL_SIZE,tempColor,10)       
        playerBallList.append(newPlayerBall)
    #暂停测试
    if key=="S" or key=="s":
        print("zanting")
        paused = not paused
def UpdateEnemyBalls():
    global gameState,enemyBallList,playerBallList
    for ball in enemyBallList:
        ball.update()    
        ball.render()
        #print(ball.pos.x)
        if ball.rad<0:            
            enemyBallList.remove(ball)
        if ball.collision(paddlePosX,paddlePosY,paddleWidth,paddleHeight):
            enemyBallList=[]
            playerBallList=[]
            gameState=GAME_OVER_STATE
def UpdatePlayerBalls():
    for playerBall in playerBallList:
        playerBall.update()    
        playerBall.render()
        playerBall.collision(paddlePosX,paddlePosY,paddleWidth,paddleHeight)
        playerBall.EnemyCollision()
            
def offScreen(vector):
    if vector.x < 0:
        return 1 # N
    elif vector.y > height:
        return 2 # E
    elif vector.x > width:
        return 3 # S
    elif vector.y < 0:
        return 4 # W
    return 0    
class EnemyBall:
    #Class Constructor
    def __init__(self,tempPos,tempVel,tempSize,tempColor,wallHitCount):
        self.pos=tempPos
        self.vel=tempVel
        self.rad=tempSize
        self.col=tempColor
        #这个就是血量属性
        self.wallHitCount=wallHitCount
        self.colliedThisFrame=False
    def update(self):
         # Move EnemyBall
        self.pos+= self.vel #/10.0        
        # Hit a Wall
        whichWall = offScreen(self.pos)
        if whichWall > 0:    
            self.rad *= BALL_IMPACT_DECAY   
            #self.wallHitCount+=1                
            # Reflecting Off of Walls
            if whichWall == 1 or whichWall == 3:
                self.vel.rotate(PI - 2*self.vel.heading())
            else:
                self.vel.rotate(-2*self.vel.heading())        
        # Size Decay
        if self.rad > 0:
            if self.rad > INITIAL_BALL_SIZE/4:
                self.rad += BALL_SIZE_DECAY
            else:
                self.rad += BALL_SIZE_DECAY * 10
        #pass
        if self.colliedThisFrame==True:
            #这里现在会多次检测
                self.wallHitCount-=1
                self.colliedThisFrame=False                    
        if self.wallHitCount==0:
            enemyBallList.remove(self)
            
    def render(self):
        pushStyle()
        fill(0,0,0,0)
        stroke(self.col, 255 * self.rad/float(INITIAL_BALL_SIZE))
        #circle(self.pos.x, self.pos.y, self.rad)
        ellipse(self.pos.x, self.pos.y, self.rad, self.rad)
        #square(slef.pos.x,slef.pos.y,self.rad)        
        fill(self.col)
        text(self.wallHitCount,self.pos.x,self.pos.y)
        popStyle()
        #pass
    #板子碰撞检测
    def collision(self,paddlePosX,paddlePosY,paddleWidth,paddleHeight):
        if self.pos.x>paddlePosX-paddleWidth/2 and self.pos.x<paddlePosX+paddleWidth/2:
            if self.pos.y>paddlePosY-paddleHeight/2 and self.pos.y<paddlePosY+paddleHeight/2:
                return True
            return False

class PlayerBall(EnemyBall):
    def update(self):
         # Move EnemyBall
        self.pos+= self.vel #/10.0        
        # Hit a Wall
        whichWall = offScreen(self.pos)
        if whichWall > 0:     
            #self.wallHitCount+=1                
            # Reflecting Off of Walls
            if whichWall == 1 or whichWall == 3:
                self.vel.rotate(PI - 2*self.vel.heading())
            else:
                self.vel.rotate(-2*self.vel.heading())       
    def render(self):
        #print("zaolegeqiu")
        pushStyle()
        fill(255)
        circle(self.pos.x, self.pos.y, self.rad)    
        fill(self.col)
        text(self.wallHitCount,self.pos.x,self.pos.y)
        popStyle()
    def collision(self,paddlePosX,paddlePosY,paddleWidth,paddleHeight):
        if self.pos.x>paddlePosX-paddleWidth/2 and self.pos.x<paddlePosX+paddleWidth/2:
            if self.pos.y>paddlePosY-paddleHeight/2 and self.pos.y<paddlePosY+paddleHeight/2:
                #self.vel.rotate(PI - 2*self.vel.heading())
                self.vel.rotate(-2*self.vel.heading())
    def EnemyCollision(self): 
        for enemyball in enemyBallList:            
            for playerball in playerBallList:    
                #if self!=playerball and playerball.colliedThisFrame==False: 
                if playerball.colliedThisFrame==False:     
                    if dist(self.pos.x,self.pos.y,enemyball.pos.x,enemyball.pos.y)<(self.rad/2+enemyball.rad/2):        
                            #Collision
                        #self.colliedThisFram=True
                        #print("pengdaole")
                        enemyball.colliedThisFrame=True
