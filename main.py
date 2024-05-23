import sys
import os
import random
import threading
import time
import pygame
import pyautogui



#variable initalize

set_fps = 60 #variable

currentPath = os.path.dirname(__file__)

imgPath = os.path.join("C:\\Users\\bepue\\Desktop\\Task\\Simulation-Hardy-Weinberg", 'src', 'img')

#graph Setting

#https://pypi.org/project/pygame-matplotlib/, pip install pygame-matplotlib
import matplotlib
import matplotlib.pyplot as plt
import numpy
matplotlib.use('module://pygame_matplotlib.backend_pygame')

label = ["AA", "Aa(aA)", "aa"]
index = numpy.arange(len(label))

    #run by "showChart" Func



#set display
#세로 크기에 맞춤.

displayHeight = pyautogui.size()[1] - 200

widthRatio = 0.9 #var

circumSectionHeight = 200 #var

print(displayHeight)

maxSectionSize = (0, 0, displayHeight * widthRatio, displayHeight)
circumSectionSize = (0, 0, displayHeight * widthRatio, displayHeight - circumSectionHeight)  #   ->x, y, w, h

threadAlive = True




globalUid = 0

onBoardEntity = []



##사용자 변경

# --초기 세팅 --
globalMoveSpeed = 100
globalAge = 15 #second
globalChildNum = 2

# --실험 중 가변 세팅 --
allowIncest = False #근친가능 설정.




initEntityQuantity = [50, 100, 25]


class Button():
    def __init__(self, color, hlColor, inText, textSize, textColor, x, y, sizeX, sizeY, action = None, parm = None):
        
        self.mousePos = pygame.mouse.get_pos()
        self.isClick = pygame.mouse.get_pressed()

        self.btnFont = pygame.font.SysFont("arial", int(textSize))
        self.text = self.btnFont.render(inText, True, textColor)



        if (x + sizeX) >= self.mousePos[0] >= x and (y + sizeY) >= self.mousePos[1] >= y:

            btn = pygame.draw.rect(gameDisplay, hlColor, [x, y, sizeX, sizeY])
            gameDisplay.blit(self.text, (btn.centerx, btn.centery))
            #gameDisplay.blit(btn, (x, y))


            if self.isClick[0] and action != None:
                action(parm)
    

        else:
            btn = pygame.draw.rect(gameDisplay, color, [x, y, sizeX, sizeY])
            gameDisplay.blit(self.text, (btn.centerx, btn.centery))
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




class manager():
    
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
            globals()[f'ent-{globalUid}'] = entity(['A', 'A'], globalUid, random.randrange(int(circumSectionSize[2] - miyuSizeX * 2)), random.randrange(int(circumSectionSize[3] - miyuSizeY * 2)))
            globalUid += 1

        for _ in range(initEntityQuantity[1]):
            globals()[f'ent-{globalUid}'] = entity(['A', 'a'], globalUid, random.randrange(int(circumSectionSize[2] - miyuSizeX * 2)), random.randrange(int(circumSectionSize[3] - miyuSizeY * 2)))
            globalUid += 1

        for _ in range(initEntityQuantity[2]):
            globals()[f'ent-{globalUid}'] = entity(['a', 'a'], globalUid, random.randrange(int(circumSectionSize[2] - miyuSizeX * 2)), random.randrange(int(circumSectionSize[3] - miyuSizeY * 2)))
            globalUid += 1

        #  위 : 객체 생성
        #  아래: 화면 표시.



        for i in onBoardEntity: 
            i.draw() 


    def moveEntity(self, deltaTime):
        for i in onBoardEntity:
            i.moving(deltaTime)



    
    def killEntity(self):
        global globalAge
        now = time.time()
        for i in onBoardEntity:
            now = time.time()
            if i.isMated and now - i.birth > globalAge: #자식있고, 나이 일정 지나면
                i.dead()
                
            else:
                pass


    def coupleEntity(self):
        tempCouple = []
        
        for i in onBoardEntity:
             
            if allowIncest: #근친 허용 모드
                tempCouple.append(i)
            else:

                if not i.isMated and not i.isMating: #교배경험o or 교배 중인경우 아닐 때만 선별.
                    tempCouple.append(i)
                else:
                    pass
        if len(tempCouple) != 0:
            for i in range(len(tempCouple) // 2):

                ent1 = random.choice(tempCouple)
                tempCouple.remove(ent1)
                ent2 = random.choice(tempCouple)
                tempCouple.remove(ent2)

                ent1.oper = ent2
                ent2.oper = ent1

                ent1.isMating = True
                ent2.isMating = True #서로를 향해 움직이게.







            
    def matingEntity(self, ent1, ent2):
        global globalUid
        global globalChildNum

        newGene = [random.choice(ent1.gene), random.choice(ent2.gene)]

        for i in range(globalChildNum):

            globals()[f'ent-{globalUid}'] = entity(newGene, globalUid, random.randrange(int(circumSectionSize[2] - miyuSizeX * 2)), random.randrange(int(circumSectionSize[3] - miyuSizeY * 2)))
            globalUid += 1


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
    
    def __init__(self, gene, uid, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.pos = pygame.Vector2()
        self.pos.xy = x, y
        self.dirVec = pygame.Vector2(random.randint(1,10) * randomSign(), random.randint(1,10) * randomSign()) #처음 소환될 때 바라보는 방향은 무작위
        self.dirVec = self.dirVec.normalize()
        self.moveSpeed = globalMoveSpeed

        self.changeStack = 0


        self.birth = time.time()
        self.gene = gene
        self.uid = uid
        self.isMated = False
        self.isMating = False
        self.stop = False


        self.oper = None

        self.img = miyu
        self.img = pygame.transform.scale(self.img, (miyuSizeX, miyuSizeY))
        self.rect = self.img.get_rect()
        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y
    
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
                self.pos += self.dirVec * self.moveSpeed * deltaTime * 3
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
        if self.rect.centerx + miyuSizeX / 2 > circumSectionSize[2]:

            return True
            

            self.rect.x, self.rect.y = self.pos #rect 와 pos 는 왼쪽 상단이 기준점.     
            

        elif self.rect.centerx - miyuSizeX / 2 < 0:

            return True
            
            self.__tp((self.pos.x + (circumSectionSize[2] - miyuSizeX), self.pos.y), self.dirVec)

            self.rect.x, self.rect.y = self.pos #rect 와 pos 는 왼쪽 상단이 기준점.     
            
        

        if self.rect.centery - miyuSizeY / 2 < 0:
            
            return True

            self.__tp((self.pos.x - (circumSectionSize[3] + miyuSizeY), self.pos.y), self.dirVec)

            self.rect.x, self.rect.y = self.pos #rect 와 pos 는 왼쪽 상단이 기준점.     
            
            
 
        elif self.rect.centery + miyuSizeY / 2 > circumSectionSize[3]:

        
            return True

            self.__tp((self.pos.x - (circumSectionSize[3] - miyuSizeY), self.pos.y), self.dirVec)            

            self.rect.x, self.rect.y = self.pos #rect 와 pos 는 왼쪽 상단이 기준점.     
            


    def _go2Lover(self, oper): #mating 진행중일 땐, move 대신해서 실행됨.
        self.dirVec = self.oper.pos - self.pos #상대를 향함
        self.dirVec = self.dirVec.normalize()
        self.pos += self.dirVec * self.moveSpeed * deltaTime * 1

        self.rect.x, self.rect.y = self.pos #rect 와 pos 는 왼쪽 상단이 기준점. 



    def __tp(self, pos, dir):

        self.pos = pygame.Vector2(pos)
        self.dirVec = dir
        self.rect.x, self.rect.y = self.pos    



    def dead(self):
        onBoardEntity.remove(self)
        del self



def printBackground():
    gameDisplay.fill((255, 255, 255))
    pygame.draw.rect(gameDisplay, (0, 0, 0), circumSectionSize)

def randomSign():
    return 1 if random.random() < 0.5 else -1


def showChart():
    AA = 0
    Aa = 0
    aa = 0


    for i in onBoardEntity:
        gene = i.gene
        resGene = ''.join(gene)

        if resGene == "AA":
            AA += 1
        elif resGene == "aa":
            aa += 1
        else:
            Aa += 1


    plt.bar(index, [AA, Aa, aa], align='edge', edgecolor = 'lightgray', linewidth=3, color = ['r', 'g', 'b'])
    plt.xlabel('Dna')
    plt.ylabel('amount')
    plt.xticks(index, label)
    
    plt.show()


#sys initialize


pygame.init()
gameFrame = pygame.time.Clock()
gameDisplay = pygame.display.set_mode((maxSectionSize[2], maxSectionSize[3]))
gameDisplay.fill((255, 255, 255))

# showGrpThread = threading.Thread(target=showGrp)
# showGrpThread.start()


miyu = pygame.image.load(os.path.join(imgPath, 'miyu.png'))
miyuImgScale = miyu.get_rect()

miyuSizeRatio = .01

miyuSizeX = int(miyuImgScale[2] * miyuSizeRatio)
miyuSizeY = int(miyuImgScale[3] * miyuSizeRatio)



#배경 설정
pygame.draw.rect(gameDisplay, (0, 0, 0), circumSectionSize)

gameManager = manager()

gameManager.initSummon()


#game loop
prevTime = time.time()

while True:
    
    nowTime = time.time()
    deltaTime = nowTime - prevTime
    prevTime = nowTime

    gameManager.killEntity()
    
    printBackground()
    gameManager.moveEntity(deltaTime)
    gameManager.coupleEntity()
    gameManager.detectCollide()

    showChart()

    #gui section

    #testBtn = Button((102, 52, 153), (148, 0, 211), "allow incest", 15, (0, 0, 0), 600, 700, 100, 50, grp.showGraph, lambda: allowIncest = not allowIncest)
    amountTxt = text(f"entity amount:{len(onBoardEntity)}", (400, 700), (0, 0, 0), 20)


    pygame.display.update()
    for event in pygame.event.get():    
        if event.type == pygame.QUIT:
            threadAlive = False #스레드 종료
            pygame.quit()
            sys.exit()

    gameFrame.tick(set_fps)


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
    한 세대의 죽는 시간은 똑같음
    근친 불가.

'''


