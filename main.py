import sys
import os
import random
import time
import pygame
import pyautogui

import showGraph

#variable initalize

set_fps = 60 #variable

currentPath = os.path.dirname(__file__)

imgPath = os.path.join(os.getcwd(), 'src', 'img')

#graph Setting
'''
#https://pypi.org/project/pygame-matplotlib/, pip install pygame-matplotlib
import matplotlib
import matplotlib.pyplot as plt
import numpy
matplotlib.use('module://pygame_matplotlib.backend_pygame')

label = ["AA", "Aa(aA)", "aa"]
index = numpy.arange(len(label))

    #run by "showChart" Func
'''


#set display
#세로 크기에 맞춤.

displayHeight = pyautogui.size()[1] - 200

widthRatio = 1.2 #var

circumSectionHeight = 200 #var

print(displayHeight)

maxSectionSize = (0, 0, displayHeight * widthRatio, displayHeight)
circumSectionSize = (0, 0, displayHeight * widthRatio - 400, displayHeight - circumSectionHeight)  #   ->x, y, w, h
guiSectionSize = (0, 0, 0, maxSectionSize[3] - circumSectionSize[3])


threadAlive = True




globalUid = 0

onBoardEntity = []
notMatedEntity = []


##사용자 변경

# --초기 세팅 --
globalMoveSpeed = 100
globalAge = 5 #second
globalChildNum = 2
globalHealth = 20 #기본 체력

# --실험 중 가변 세팅 --
allowIncest = False #근친가능 설정.


getInitGenesAA = input("AA 수( < 1000 ) : ")
getInitGenesAa = input("Aa(aA) 수 ( < 1000) : ")
getInitGenesaa = input("aa 수( < 1000) : ")

initEntityQuantity = [int(getInitGenesAA), int(getInitGenesAa), int(getInitGenesaa)]


class Button():
    def __init__(self, color, hlColor, inText, textSize, textColor, x, y, sizeX, sizeY, action = None, parm = None):
        
        self.mousePos = pygame.mouse.get_pos()
        self.isClicked = pygame.mouse.get_pressed()

        self.btnFont = pygame.font.SysFont("arial", int(textSize))
        self.text = self.btnFont.render(inText, True, textColor)



        if (x + sizeX) >= self.mousePos[0] >= x and (y + sizeY) >= self.mousePos[1] >= y:
            
            btn = pygame.draw.rect(gameDisplay, hlColor, [x, y, sizeX, sizeY])
            txtSize = self.text.get_rect()
            gameDisplay.blit(self.text, (btn.centerx - txtSize.width // 2, btn.centery - txtSize.height // 2))
            #gameDisplay.blit(btn, (x, y))

            if self.isClicked[0] and action != None:
                action(parm)

        else:
            btn = pygame.draw.rect(gameDisplay, color, [x, y, sizeX, sizeY])
            txtSize = self.text.get_rect()
            gameDisplay.blit(self.text, (btn.centerx - txtSize.width // 2, btn.centery - txtSize.height // 2))
            #gameDisplay.blit(btn, (x, y))



class text():
    def __init__(self, textContent, pos : tuple, color : tuple, fontSize):
        self.textContent = textContent
        self.fontSize = fontSize
        self.color = color
        self.pos = pos


        self.textFont = pygame.font.SysFont("arial", self.fontSize)
        self.text = self.textFont.render(self.textContent, True, self.color)
        gameDisplay.blit(self.text, pos)



class superEntityMarker(pygame.sprite.Sprite):
    def __init__(self):
        self.img = circleRange

        
        self.isClick = pygame.mouse.get_pressed()

        self.mousePos = pygame.mouse.get_pos()

        self.imgSize = self.img.get_rect().size
        self.img = pygame.transform.scale(self.img, (self.imgSize[0] * circleRangeRatio, self.imgSize[1] * circleRangeRatio))

        self.rect = self.img.get_rect()
        self.rect.centerx, self.rect.centery = self.mousePos

        self.img.set_alpha(128) #반투명

        gameDisplay.blit(self.img, (self.rect.x, self.rect.y)) #반투명 원 그리기.


        if self.isClick[0]:
            for i in onBoardEntity:
                collide = self.rect.colliderect(i.rect) #부딛히는 놈들은,
                if collide:
                    i.beSuper() #슈퍼맨으로 업그레이드.






 


class gameManager():
    
    def __init__(self):
        self.isAlive = True


    # def move(self, deltaTime): #move entity, run by thread
    #     prevTime = time.time()
    #     while self.isAlive:
    #         nowTime = time.time()
    #         deltaTime = nowTime - prevTime
    #         prevTime = nowTime

    #         for i in onBoardEntity:
    #             i.moving(deltaTime)


    def initSummon(self):
        global globalUid

        for _ in range(initEntityQuantity[0]):
            globals()[f'ent-{globalUid}'] = entity(['A', 'A'], globalUid, random.randrange(int(circumSectionSize[2] - miyuSizeX * 2)), random.randrange(int(circumSectionSize[3] - miyuSizeY * 2)), (0, 0), False)
            globalUid += 1

        for _ in range(initEntityQuantity[1]):
            globals()[f'ent-{globalUid}'] = entity(['A', 'a'], globalUid, random.randrange(int(circumSectionSize[2] - miyuSizeX * 2)), random.randrange(int(circumSectionSize[3] - miyuSizeY * 2)), (0, 0), False)
            globalUid += 1

        for _ in range(initEntityQuantity[2]):
            globals()[f'ent-{globalUid}'] = entity(['a', 'a'], globalUid, random.randrange(int(circumSectionSize[2] - miyuSizeX * 2)), random.randrange(int(circumSectionSize[3] - miyuSizeY * 2)), (0, 0), False)
            globalUid += 1
            #초기 생명체 부모 uid 는 0
            #초기 생명체 사망시간은, globalAge
            #초기 생명체는 super가 X

        #  위 : 객체 생성
        #  아래: 화면 표시.



        for i in onBoardEntity: 
            i.draw() 


    def moveEntity(self, deltaTime):
        for i in onBoardEntity:
            i.moving(deltaTime)



    
    def killEntity(self):
        global globalAge
        #now = time.time()
        for i in onBoardEntity:
            #now = time.time()
            if i.isMated: #교배 했다면
                i.dead()
                
            else:
                pass


    def coupleEntity(self):
        global notMatedEntity
        tempCouple = []
        notCase = False
        notMatedEntity = [] #초기화

        for i in onBoardEntity:

            if not i.isMated and not i.isMating: #교배 중인경우 아닐 때만 선별.
                tempCouple.append(i)
                notMatedEntity.append(i)
            else:
                pass
        if len(tempCouple) != 0:
            for i in range(len(tempCouple) // 2):

                    ent1 = random.choice(tempCouple)
                    tempCouple.remove(ent1)
                    ent2 = random.choice(tempCouple)
                    tempCouple.remove(ent2)



                    #근친 허용 -> or 이므로 바로 break 해서, 다시 선정X
                    #근친허용 X -> 그다음 구문(근친 판별)에서 참이여야 다시 선정X

                    # -> allowIncest(근친ok 가 꺼져있으면, 부모와 교배 X)
                    ent1.oper = ent2
                    ent2.oper = ent1

                    ent1.isMating = True
                    ent2.isMating = True #서로를 향해 움직이게.






            
    def matingEntity(self, ent1, ent2):
        global globalUid
        global globalChildNum

        

        for i in range(globalChildNum): #슈퍼는 자식 수 + 2 마리 낳음

            if not ent1.isSuper and not ent2.isSuper:
                    
                newGene = [random.choice(ent1.gene), random.choice(ent2.gene)]

                globals()[f'ent-{globalUid}'] = entity(
                                                        newGene,
                                                        globalUid,
                                                        random.randrange(int(circumSectionSize[2] - miyuSizeX * 2)),
                                                        random.randrange(int(circumSectionSize[3] - miyuSizeY * 2)),
                                                        (ent1.uid, ent2.uid),
                                                        False
                                                        ) #슈퍼 유전자는 슈퍼유전자를 따라감.
                globalUid += 1


            elif ent1.isSuper and not ent2.isSuper:
                
                newGene = ent1.gene #super 쪽 유전자가 우성 됨.
        

                globals()[f'ent-{globalUid}'] = entity(
                                                        newGene,
                                                        globalUid,
                                                        random.randrange(int(circumSectionSize[2] - miyuSizeX * 2)),
                                                        random.randrange(int(circumSectionSize[3] - miyuSizeY * 2)),
                                                        (ent1.uid, ent2.uid),
                                                        True
                                                        ) #슈퍼 유전자는 슈퍼유전자를 따라감.
                globalUid += 1
            elif not ent1.isSuper and ent2.isSuper:
                newGene = ent2.gene #super 쪽 유전자가 우성 됨.
        
                globals()[f'ent-{globalUid}'] = entity(
                                                        newGene,
                                                        globalUid,
                                                        random.randrange(int(circumSectionSize[2] - miyuSizeX * 2)),
                                                        random.randrange(int(circumSectionSize[3] - miyuSizeY * 2)),
                                                        (ent1.uid, ent2.uid),
                                                        True
                                                        ) #슈퍼 유전자는 슈퍼유전자를 따라감.
                globalUid += 1



            else:
                newGene = [random.choice(ent1.gene), random.choice(ent2.gene)] #둘다 super 면, 무작위.
        

                globals()[f'ent-{globalUid}'] = entity(
                                                        newGene,
                                                        globalUid,
                                                        random.randrange(int(circumSectionSize[2] - miyuSizeX * 2)),
                                                        random.randrange(int(circumSectionSize[3] - miyuSizeY * 2)),
                                                        (ent1.uid, ent2.uid),
                                                        True
                                                        ) #슈퍼 유전자는 슈퍼유전자를 따라감.
                globalUid += 1


        notMatedEntity.remove(ent1)
        notMatedEntity.remove(ent2)

        ent1.isMating = False
        ent2.isMating = False
        ent1.isMated = True
        ent2.isMated = True
        ent1.stop = False
        ent2.stop = False
        



    def detectCollide(self):

        for i in onBoardEntity:
            if i.isMating:    
                collide = i.rect.colliderect(i.oper.rect) #짝이랑 부딛히면
                if collide:

                    i.OnCollision()
                    i.oper.OnCollision() #멈추기.

                    self.matingEntity(i, i.oper) #짝짓기 시작
                 

    




class entity(pygame.sprite.Sprite):
    
    def __init__(self, gene, uid, x, y, rootUid : tuple, isInfantSuper : bool = False):
        pygame.sprite.Sprite.__init__(self)


        self.pos = pygame.Vector2()
        self.pos.xy = x, y
        self.dirVec = pygame.Vector2(random.randint(1,10) * randomSign(), random.randint(1,10) * randomSign()) #처음 소환될 때 바라보는 방향은 무작위
        self.dirVec = self.dirVec.normalize()
        self.moveSpeed = globalMoveSpeed

        self.changeStack = 0

        

        self.birth = time.time()
        self.destinyAge = globalAge #만약 슈퍼 유전자면, 생성 이후 바뀜
        self.gene = gene
        self.uid = uid
        self.isMated = False
        self.isMating = False
        self.stop = False
        self.root = rootUid #[부모1, 부모2]



        self.oper = None

        self.img = miyu
        self.img = pygame.transform.scale(self.img, (miyuSizeX, miyuSizeY))
        self.rect = self.img.get_rect()
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
    
        self.isSuper = False

        if isInfantSuper: #부모중 하나가 슈퍼 유전자면 따라감.
            self.beSuper()
        
        onBoardEntity.append(self)


    def __str__(self):
        print(self.uid)


    def __del__(self):
        pass

    def draw(self):
        gameDisplay.blit(self.img, (self.pos.x, self.pos.y))
    '''
움직임 lerp 함수?
두 좌표 거리 * 비율(deltaTime, 1프레임당 걸린 시간).


반복문N(반복 횟수 = N)이라 가정, (0,0)에서 (10, 0) 움직이면
lerp로 이동할 시

반복문0 = 위치:0 + 1 //거리 10 * 0.1
반복문1 = 위치:(0 + 1) + 0.9 //거리 9*0.1

이때 비율에 속도도 같이 곱해주면, 속도 정하는 효과 나옴!! 그렇기에, deltaTime을 인자로 받는다.

    '''


    def moving(self, deltaTime):

        if self.stop:
            pass
        else:
            

            if self._checkWall(): #벽을 넘으면, 다른 움직임 전부 멈추고 중앙을 향해서만 움직이기
                self.dirVec = (pygame.Vector2(circumSectionSize[2] // 2, circumSectionSize[3] // 2) - self.pos).normalize()
                self.pos += self.dirVec * self.moveSpeed * deltaTime * 1
                self.rect.x, self.rect.y = self.pos


            else:

                if self.isMating and self.oper != None: #짝짓기 시작하면, 상대를 향해 움직임.
                    self._go2Lover(self.oper) #벽 튕기기랑 겹침.

                else:
                    self._changeRotate()
                    self.pos += self.dirVec * self.moveSpeed * deltaTime
                    self.rect.x, self.rect.y = self.pos #rect 와 pos 는 왼쪽 상단이 기준점.

        gameDisplay.blit(self.img, (self.pos.x, self.pos.y))
        #pygame.display.update()


    def _changeRotate(self):
        
        if self.changeStack > random.randrange(50, 100): #가끔만 움직이게

            self.dirVec = self.dirVec.rotate(random.randint(1, 359)) 
            # * random.choice((0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 1)) 안돌거나 왼쪽으로 돌거나 오른쪽으로 돌거나 (확률 다름)
            self.changeStack = 0
        
        self.changeStack += 1



    def OnCollision(self):
        #멈추고(여기서), 짝짓기 시작(충돌 감지 함수에서).

        self.stop = True



    def _checkWall(self): #히트 박스 끝이 벽에 나가면, 방향 바꾸고 3배 이동. !moving에서 실행 됨.!
        if self.rect.centerx + self.rect.width / 2 > circumSectionSize[2]:

            return True
            

            self.rect.x, self.rect.y = self.pos #rect 와 pos 는 왼쪽 상단이 기준점.     
            

        elif self.rect.centerx - self.rect.width / 2 < 0:

            return True
            
            self.__tp((self.pos.x + (circumSectionSize[2] - miyuSizeX), self.pos.y), self.dirVec)

            self.rect.x, self.rect.y = self.pos #rect 와 pos 는 왼쪽 상단이 기준점.     
            
        

        if self.rect.centery - self.rect.height / 2 < 0:
            
            return True

            self.__tp((self.pos.x - (circumSectionSize[3] + miyuSizeY), self.pos.y), self.dirVec)

            self.rect.x, self.rect.y = self.pos #rect 와 pos 는 왼쪽 상단이 기준점.     
            
            
 
        elif self.rect.centery + self.rect.height / 2 > circumSectionSize[3]:

        
            return True

            self.__tp((self.pos.x - (circumSectionSize[3] - miyuSizeY), self.pos.y), self.dirVec)            

            self.rect.x, self.rect.y = self.pos #rect 와 pos 는 왼쪽 상단이 기준점.     
            


    def _go2Lover(self, oper): #mating 진행중일 땐, move 대신해서 실행됨.
        self.dirVec = self.oper.pos - self.pos #상대를 향함
        self.dirVec = self.dirVec.normalize()
        self.pos += self.dirVec * self.moveSpeed * deltaTime

        self.rect.x, self.rect.y = self.pos #rect 와 pos 는 왼쪽 상단이 기준점. 



    def __tp(self, pos, dir):

        self.pos = pygame.Vector2(pos)
        self.dirVec = dir
        self.rect.x, self.rect.y = self.pos


    def beSuper(self):
        if not self.isSuper:
            self.img = superMiyu
            self.img = pygame.transform.scale(self.img, (superMiyuSizeX, superMiyuSizeY))
            
            self.rect = self.img.get_rect()
            self.rect.x = self.pos.x
            self.rect.y = self.pos.y

            self.destinyAge += 1
            self.moveSpeed *= 2

            self.isSuper = True
        else:
            pass

    def dead(self):
        onBoardEntity.remove(self)
        del self



def printCircumSection():
    
    gameDisplay.fill((255, 255, 255))
    pygame.draw.rect(gameDisplay, (0, 0, 0), circumSectionSize)

def printGuiSection():
    pygame.draw.rect(gameDisplay, (255, 255, 255), guiSectionSize)

    

def randomSign():
    return 1 if random.random() < 0.5 else -1


def showGrp(wht = None):
    if wht == None:
        return
    showGraph.showGraph(wht)


def setSign(state : bool = False):
    global isNextStep
    isNextStep = state


#sys initialize


pygame.init()
gameFrame = pygame.time.Clock()
gameDisplay = pygame.display.set_mode((maxSectionSize[2], maxSectionSize[3]))
gameDisplay.fill((255, 255, 255))



miyu = pygame.image.load(os.path.join(imgPath, 'miyu.png'))
miyuImgScale = miyu.get_rect()

miyuSizeRatio = .01

miyuSizeX = int(miyuImgScale[2] * miyuSizeRatio)
miyuSizeY = int(miyuImgScale[3] * miyuSizeRatio)


superMiyu = pygame.image.load(os.path.join(imgPath, 'miyu_inverted.png'))
superMiyuImgScale = miyu.get_rect()
superMiyuSizeRatio = .03

superMiyuSizeX = int(superMiyuImgScale[2] * superMiyuSizeRatio)
superMiyuSizeY = int(superMiyuImgScale[3] * superMiyuSizeRatio)


circleRange = pygame.image.load(os.path.join(imgPath, 'range.png'))
circleRangeRatio = .05




#배경 설정
pygame.draw.rect(gameDisplay, (0, 0, 0), circumSectionSize)

gameManager = gameManager()

gameManager.initSummon()


#game loop
prevTime = time.time()
'''
1. 교배 시킴
2. 기다림.
3. 모든 애들이 교배가 끝나면,
4. 기존에 있던 애들 제거.
5. 그래프를 보여 줌.
6. 버튼을 누를 때 까지 대기. (이 과정 반복.)

'''

globalPhase = 0 #초기화

while True:
    globalPhase += 1

    nowTime = time.time()
    deltaTime = nowTime - prevTime
    prevTime = nowTime
    
    
    gameManager.coupleEntity()

    while(not len(notMatedEntity) == 0): #모두 교배 할 때 까지 교배.
        nowTime = time.time()
        deltaTime = nowTime - prevTime
        prevTime = nowTime

        printCircumSection()
        gameManager.moveEntity(deltaTime=deltaTime)
        gameManager.detectCollide()
        printGuiSection()

        marker = superEntityMarker()

        leftCoupleTxt = text(f"left couple :{len(notMatedEntity)}", (maxSectionSize[2] - 150, 10), (0, 0, 0), 20)
        stepTxt = text(f"phase : {globalPhase}", (maxSectionSize[2] - 150, 30), (0, 0, 0), 20)
        amountEntTxt = text(f"Entity Amount : {len(onBoardEntity)}", (maxSectionSize[2] - 200, 60), (0, 0, 0), 20)

        gameManager.killEntity()

        pygame.display.update()
        for event in pygame.event.get():    
            if event.type == pygame.QUIT:
                threadAlive = False #스레드 종료
                pygame.quit()
                sys.exit()

        gameFrame.tick(set_fps)


    gameManager.killEntity()

    isNextStep = False
    btnSize = (100, 60)

    while(not isNextStep):

        nextPhase_Btn = Button((153, 204, 102), (204, 255, 153), "Play", 20, (0, 0, 0), maxSectionSize[2] - btnSize[0] - 100, maxSectionSize[3] - btnSize[1] - 10, 
                            btnSize[0], btnSize[1], setSign, True)
        
        showGrp_Btn = Button((255, 153, 51), (255, 153, 120), "ShowGraph", 15, (0, 0, 0),maxSectionSize[2] - btnSize[0] - btnSize[0] - 105, maxSectionSize[3] - btnSize[1] - 10, 
                             btnSize[0], btnSize[1], showGrp, onBoardEntity) #그래프 보는 버튼


        pygame.display.update()
        for event in pygame.event.get():    
            if event.type == pygame.QUIT:
                threadAlive = False #스레드 종료
                pygame.quit()
                sys.exit()

        gameFrame.tick(set_fps)

        
    isNextStep = False

    


    '''
    nowTime = time.time()
    deltaTime = nowTime - prevTime
    prevTime = nowTime

    printCircumSection()
    #여기에 노란색 원 생성
    marker = superEntityMarker()

    
    gameManager.killEntity()

    gameManager.moveEntity(deltaTime)
    gameManager.coupleEntity()
    gameManager.detectCollide()
    printGuiSection()

    #showChart()

    #gui section

    #testBtn = Button((102, 52, 153), (148, 0, 211), "allow incest", 15, (0, 0, 0), 600, 700, 100, 50, grp.showGraph, lambda: allowIncest = not allowIncest)
    amountTxt = text(f"entity amount:{len(onBoardEntity)}", (400, 700), (0, 0, 0), 20)

    '''

    '''
    pygame.display.update()
    for event in pygame.event.get():    
        if event.type == pygame.QUIT:
            threadAlive = False #스레드 종료
            pygame.quit()
            sys.exit()

    gameFrame.tick(set_fps)
    '''

'''
W > w

WW : a
Ww : b
ww : c

W 빈도 : a + b = p
w 빈도 : b + c = q

p + q = 1


2세대 빈도
W 빈도 : p^2 + pq = p(p+q) = p * 1 = p
w 빈도 : q^2 + pq = "


프로그램은 수식기반이기 때문에, 제한하지 않을 것만 설정하면 나머지 조건은 자동으로 제한됨
또한 하디바인 베르크는 멘델 환경에서만 작용
>> 근친 교배 X


제한할 조건:
    무작위 교배시킴
    돌연변이 X
    한 세대의 죽는 시간은 똑같음 (변인)
    근친 불가.


'''


