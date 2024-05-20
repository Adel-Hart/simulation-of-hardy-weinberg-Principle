import sys
import os
import random
import time
import pygame
import threading


#variable initalize

set_fps = 60 #variable

currentPath = os.path.dirname(__file__)

imgPath = os.path.join("C:\\Users\\bepue\\Desktop\\Task\\Simulation-Hardy-Weinberg", 'src', 'img')

globalMoveSpeed = 100

maxSectionSize = (0, 0, 800, 800)
circumSectionSize = (0, 0, 800, 650)  #   ->x, y, w, h

initEntityQuantity = [100, 50, 20]

globalUid = 0

onBoardEntity = []

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
            globals()[f'ent-{globalUid}'] = entity(['A', 'A'], globalUid, random.randrange(circumSectionSize[2] - miyuSizeX * 2), random.randrange(circumSectionSize[3] - miyuSizeY * 2))
            globalUid += 1

        for _ in range(initEntityQuantity[1]):
            globals()[f'ent-{globalUid}'] = entity(['A', 'a'], globalUid, random.randrange(circumSectionSize[2] - miyuSizeX * 2), random.randrange(circumSectionSize[3] - miyuSizeY * 2))
            globalUid += 1

        for _ in range(initEntityQuantity[2]):
            globals()[f'ent-{globalUid}'] = entity(['a', 'a'], globalUid, random.randrange(circumSectionSize[2] - miyuSizeX * 2), random.randrange(circumSectionSize[3] - miyuSizeY * 2))
            globalUid += 1

        #  위 : 객체 생성
        #  아래: 화면 표시.



        for i in onBoardEntity: 
            i.draw() 


    def moveEntity(self, deltaTime):
        for i in onBoardEntity:
            i.moving(deltaTime)


    def changeDirEntity(self):
        for i in onBoardEntity:
            i.changeRotate()

    

class entity(pygame.sprite.Sprite):
    
    def __init__(self, gene, uid, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.pos = pygame.Vector2()
        self.pos.xy = x, y
        self.dirVec = pygame.Vector2(random.randint(1,10) * randomSign(), random.randint(1,10) * randomSign()) #처음 소환될 때 바라보는 방향은 무작위
        self.dirVec = self.dirVec.normalize()
        self.moveSpeed = globalMoveSpeed

        self.changeStack = 0



        self.gene = gene
        self.uid = uid
        self.isMated = False


        self.img = miyu
        self.img = pygame.transform.scale(self.img, (miyuSizeX, miyuSizeY))
        self.rect = self.img.get_rect()
        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y
    
        onBoardEntity.append(self)


    def __str__(self):
        print(self.uid)

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
        self._checkWall()
        self.pos += self.dirVec * self.moveSpeed * deltaTime
        self.rect.x, self.rect.y = self.pos #rect 와 pos 는 왼쪽 상단이 기준점.

        gameDisplay.blit(self.img, (self.pos.x, self.pos.y))
        #pygame.display.update()


    def changeRotate(self):
        
        if self.changeStack > 100: #가끔만 움직이게

            self.dirVec = self.dirVec.rotate(random.randint(1, 359)) 
            # * random.choice((0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 1)) 안돌거나 왼쪽으로 돌거나 오른쪽으로 돌거나 (확률 다름)
            self.changeStack = 0
        
        self.changeStack += 1



    def OnCollision():
        pass


    def _checkWall(self): #히트 박스 끝이 벽에 나가면, 방향 바꾸고 3배 이동. !moving에서 실행 됨.!
        if self.rect.centerx + miyuSizeX / 2 >= circumSectionSize[2]:

            

            self.dirVec = pygame.Vector2.reflect(self.dirVec, pygame.Vector2(-1, 0)) #<- 방향의 법선벡터 기준으로 전반사
            self.pos += self.dirVec * self.moveSpeed * deltaTime * 10
            self.rect.x, self.rect.y = self.pos #rect 와 pos 는 왼쪽 상단이 기준점.     
            

        elif self.rect.centerx - miyuSizeX / 2 <= 0:
            

            self.dirVec = pygame.Vector2.reflect(self.dirVec, pygame.Vector2(1, 0)) #-> 방향의 법선벡터 기준으로 전반사
            self.pos += self.dirVec * self.moveSpeed * deltaTime * 3
            self.rect.x, self.rect.y = self.pos #rect 와 pos 는 왼쪽 상단이 기준점.     
            
            

        elif self.rect.centery - miyuSizeY / 2 <= 0:
            

            self.dirVec = pygame.Vector2.reflect(self.dirVec, pygame.Vector2(0, -1)) # V 방향의 법선벡터 기준으로 전반사
            self.pos += self.dirVec * self.moveSpeed * deltaTime * 3
            self.rect.x, self.rect.y = self.pos #rect 와 pos 는 왼쪽 상단이 기준점.     
            
            
 
        elif self.rect.centery + miyuSizeY / 2 >= circumSectionSize[3]:
            

            self.dirVec = pygame.Vector2.reflect(self.dirVec, pygame.Vector2(0, 1)) # ^ 방향의 법선벡터 기준으로 전반사
            self.pos += self.dirVec * self.moveSpeed * deltaTime * 3
            self.rect.x, self.rect.y = self.pos #rect 와 pos 는 왼쪽 상단이 기준점.     
            




    def dead(self):
        None


def printBackground():
    gameDisplay.fill((255, 255, 255))
    pygame.draw.rect(gameDisplay, (0, 0, 0), circumSectionSize)

def randomSign():
    return 1 if random.random() < 0.5 else -1


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



#배경 설정
pygame.draw.rect(gameDisplay, (0, 0, 0), circumSectionSize)

gameManager = manager()

gameManager.initSummon()


#game loop
prevTime = time.time()

one = 0
while True:
    nowTime = time.time()
    deltaTime = nowTime - prevTime
    prevTime = nowTime



    gameManager.changeDirEntity()
    printBackground()
    gameManager.moveEntity(deltaTime)




    pygame.display.update()
    for event in pygame.event.get():    
        if event.type == pygame.QUIT:
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
class entityManager():
    def __init__(self) -> None:
        pass

    def creatInitEntity():
        pass


    def _checkWall():
        pass



