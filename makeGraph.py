import sys
import os
import random
import pygame
import threading


#variable initalize

display_sizeX = 800
display_sizeY = 1000
set_fps = 30 #variable

currentPath = os.path.dirname(__file__)

imgPath = os.path.join(currentPath, 'src', 'img')

moveSize = 20


onBoardEntity = []

class manager():
    def __init__(self):
        pass

    def move(self): #move entity, run by thread
        for i in onBoardEntity:
            i.moving()

class entity(pygame.sprite.Sprite):
    
    def __init__(self, gene, uid, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.vec = pygame.Vector2()
        self.vec.xy = x, y
        self.dir = pygame.Vector2()
        self.dir = self.dir.normalize()


        self.gene = gene
        self.uid = uid
        self.isMated = False


        self.img = miyu
        self.img = pygame.transform.scale(self.img, (int(miyuImgScale[2] * miyuSize), int(miyuImgScale[3] * miyuSize)))
        self.rect = self.img.get_rect()
        self.rect.centerx = self.vec.x
        self.rect.centery = self.vec.y
    
        onBoardEntity.append(self)


    def __str__(self):
        print(self.uid)

    def draw(self):
        print("blit start")
        gameDisplay.blit(self.img, (self.vec.x, self.vec.y))
        print("blit end")

    def moving(self):
        self.vec.le

        printBackground()
        gameDisplay.blit(self.img, (self.vec.x, self.vec.y))


    def changeRotate(self):
    


    def OnCollision():

        pass
    def checkWall():
        pass

    def dead(self):
        None


def printBackground():
    gameDisplay.fill((255, 255, 255))
    pygame.draw.rect(gameDisplay, (0, 0, 0), (0, 0, 600, 1000))


#sys initialize


pygame.init()
gameFrame = pygame.time.Clock()
gameDisplay = pygame.display.set_mode((display_sizeX, display_sizeY))
gameDisplay.fill((255, 255, 255))

miyu = pygame.image.load(os.path.join(imgPath, 'miyu.png'))
miyuImgScale = miyu.get_rect()
print(miyuImgScale)
miyuSize = 0.05

pygame.draw.rect(gameDisplay, (0, 0, 0), (0, 0, 600, 1000))

gameManager = manager() 
test1 = entity(0, 1, 300, 300)
test1.draw()

#game loop
while True:

    gameManager.move()


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


    def checkWall():
        pass



