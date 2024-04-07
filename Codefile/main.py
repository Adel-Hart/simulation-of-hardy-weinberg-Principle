import random
import simpy
import numpy


entityList = [0]

listNonMarried = []

isProceeding = True


def chooseGene(mgeneList : list, fgeneList : list): # ex) mgeneList = AA, aa

    mgeneFir = list(mgeneList[0]) # >> ex) ["A", "A"]
    mgeneSec = list(mgeneList[1])
    fgeneFir = list(fgeneList[0])
    fgeneSec = list(fgeneList[1])


    return list((mgeneFir[0], fgeneFir[0])), list((mgeneFir[0], fgeneSec[0])), list((mgeneSec[0], fgeneFir[0])), list((mgeneSec[0], fgeneSec[0]))


#Aa, aA


#Aa AA aA aa


def improveMakeBABY(env, store):
    print("start finding")
    while True:
        temp = random.sample(listNonMarried, 2)
        if temp[0].Sex + temp[1].Sex == 1 and temp[0].geneRation == temp[1].geneRation: #다른 성이면 && 같은 세대일 때
            print("lets'go sex")
            break
        else:
            continue

    listNonMarried.remove(temp[0])
    listNonMarried.remove(temp[1]) #사용중이므로, 메이팅 가능 리스트에서 빼기

    temp[0].isMating = True
    temp[1].isMating = True

    if(temp[0].Sex):
        mEntity = temp[1]
        fEntity = temp[0]
    else:
        mEntity = temp[0]
        fEntity = temp[1]

    sexList = [0, 0, 0, 1, 1, 1]
    random.shuffle(sexList) #성별 무작위 (하지만 6명의 자식이 남자 3명 여자 3명임)

    mGeneA = mEntity.geneA.copy() # ex)  => ["a", "A"]
    mGeneB = mEntity.geneB.copy()
    fGeneA = fEntity.geneA.copy()
    fGeneB = fEntity.geneB.copy()



    mGeneA = list(map(lambda x : str(x * 2), mGeneA)) # A, a >> AA, aa
    mGeneB = list(map(lambda x : str(x * 2), mGeneB))
    fGeneA = list(map(lambda x : str(x * 2), fGeneA))
    fGeneB = list(map(lambda x : str(x * 2), fGeneB))

    random.shuffle(mGeneA)
    random.shuffle(mGeneB)
    random.shuffle(fGeneA)
    random.shuffle(fGeneB)
    #mix Gene

    indexNum = len(entityList)
    resA = chooseGene(mGeneA, fGeneA) #4개 나옴
    resB = chooseGene(mGeneB, fGeneB)

    globals()['entity_%d' % indexNum] = entity(indexNum, sexList[0] , mEntity, fEntity, resA[0], resB[0], geneRation=mEntity.geneRation+1)
    entityList.append(globals()['entity_%d' % indexNum])

    indexNum += 1
    globals()['entity_%d' % indexNum] = entity(indexNum, sexList[1], mEntity, fEntity, resA[1], resB[0], geneRation=mEntity.geneRation+1)
    entityList.append(globals()['entity_%d' % indexNum])

    indexNum += 1
    globals()['entity_%d' % indexNum] = entity(indexNum, sexList[2], mEntity, fEntity, resA[0], resB[1], geneRation=mEntity.geneRation+1)
    entityList.append(globals()['entity_%d' % indexNum])

    indexNum += 1
    globals()['entity_%d' % indexNum] = entity(indexNum, sexList[3], mEntity, fEntity, resA[1], resB[1], geneRation=mEntity.geneRation+1)
    entityList.append(globals()['entity_%d' % indexNum])

    yield env.timeout(10)







'''
class matingHelper():
    def __init__(self, env):

        self.env = env
        self.nonMarried = simpy.Resource(self.env, capacity=120)
        self.listNonMarried = [] #짝짓기 안한 엔티티 목록(대기열 같은 느낌)

    def makeBaby(self, env):
        while True:
            temp = random.sample(self.listNonMarried, 2)
            if temp[0].Sex + temp[1].Sex == 1 and temp[0].geneRation == temp[1].geneRation: #다른 성이면 && 같은 세대일 때
                break
            else:
                continue

        self.listNonMarried.remove(temp[0])
        self.listNonMarried.remove(temp[1]) #사용중이므로, 메이팅 가능 리스트에서 빼기

        temp[0].isMating = True
        temp[1].isMating = True

        if(temp[0].Sex):
            mEntity = temp[1]
            fEntity = temp[0]
        else:
            mEntity = temp[0]
            fEntity = temp[1]

        sexList = [0, 0, 0, 1, 1, 1]
        random.shuffle(sexList) #성별 무작위 (하지만 6명의 자식이 남자 3명 여자 3명임)

        mGeneA = mEntity.geneA.copy() # ex)  => ["a", "A"]
        mGeneB = mEntity.geneB.copy()
        fGeneA = fEntity.geneA.copy()
        fGeneB = fEntity.geneB.copy()



        mGeneA = list(map(lambda x : str(x * 2), mGeneA)) # A, a >> AA, aa
        mGeneB = list(map(lambda x : str(x * 2), mGeneB))
        fGeneA = list(map(lambda x : str(x * 2), fGeneA))
        fGeneB = list(map(lambda x : str(x * 2), fGeneB))

        random.shuffle(mGeneA)
        random.shuffle(mGeneB)
        random.shuffle(fGeneA)
        random.shuffle(fGeneB)
        #mix Gene
        
        indexNum = len(entityList)
        resA = chooseGene(mGeneA, fGeneA) #4개 나옴
        resB = chooseGene(mGeneB, fGeneB)

        globals()['entity_%d' % indexNum] = entity(indexNum, sexList[0] , mEntity, fEntity, resA[0], resB[0], geneRation=mEntity.geneRation+1)
        entityList.append(globals()['entity_%d' % indexNum])

        indexNum += 1
        globals()['entity_%d' % indexNum] = entity(indexNum, sexList[1], mEntity, fEntity, resA[1], resB[0], geneRation=mEntity.geneRation+1)
        entityList.append(globals()['entity_%d' % indexNum])
        
        indexNum += 1
        globals()['entity_%d' % indexNum] = entity(indexNum, sexList[2], mEntity, fEntity, resA[0], resB[1], geneRation=mEntity.geneRation+1)
        entityList.append(globals()['entity_%d' % indexNum])
        
        indexNum += 1
        globals()['entity_%d' % indexNum] = entity(indexNum, sexList[3], mEntity, fEntity, resA[1], resB[1], geneRation=mEntity.geneRation+1)
        entityList.append(globals()['entity_%d' % indexNum])
        


'''




class entity():

    def __init__(self, UID, Sex, rootM, rootF, geneA : list, geneB : list, geneRation : int):
        self.UID = UID #index on entityList

        self.Sex = Sex #0:M, 1:F
        self.rootM = rootM #index num
        self.rootF = rootF #index num

        #dominant : Large Letter

        self.geneA = list(geneA) #ex AA, aa 
        self.geneB = list(geneB) #ex BB, Bb


        self.isDead = False
        self.isMating = False
        

        self.geneRation = geneRation

        self.startMate()


    def __str__(self) -> str:
        print(" UID : {}\n SEX : {}\n MOTHER : {}\n FATHER : {}\n GENE.A : {}\n GENE.B : {}\n".format(self.UID, self.Sex, self.rootM, self.rootF, self.geneA, self.geneB))


    def goDead(self):
        self.isDead = True;
    
    def startMate(self):
        if(not self.isMating):
            # with nonMarried.request() as req:
            #     yield req #가능하면 넘어감, 순서 있으면 대기
            listNonMarried.append(self) #짝짓기 가능 대기열에 자신 추가
                #yield env.process(helper.makeBaby())


'''


def initAdamNEve():
    adamGeneA, adamGeneB = str(input("set ADAM(Male)  >> geneA geneB >>")).split()
    eveGeneA, eveGeneB = str(input("set ADAM(Male)  >> geneA geneB >>")).split()

    list(adamGeneA)
    list(adamGeneB)
    list(eveGeneA)
    list(eveGeneB)


    globals()['entity_1'] = entity(1, 0, 0, 0, adamGeneA, adamGeneB, 0)
    entityList.append(globals()['entitiy_1'])

    globals()['entity_2'] = entity(2, 1, 0, 0, eveGeneA, eveGeneB, 0)
    entityList.append(globals()['entitiy_2'])


def matingCouple(male : entity, female : entity, sex : int):
    if(male.Sex == 0 and female.Sex == 1 and male.geneRation == female.geneRation):

        indexNum = len(entityList)
        maleA = male.extractGeneSingle[0]
        maleB = male.extractGeneSingle[1]

        femaleA = female.extractGeneSingle[0]
        femaleB = female.extractGeneSingle[1]

        resA = maleA + femaleA
        resB = maleB + femaleB

        male.isMating = True
        female.isMating = True
        
        globals()['entitiy_1'.format(indexNum)] = entity(indexNum, sex, male.UID, female.UID, resA, resB, male.geneRation + 1)

        entityList.append(globals()['entitiy_{}'.format(indexNum)])
        

    else:
        return


initAdamNEve() #set first entity



'''

def setting(env):
    print("hello")


            




def setup(env):

    global helper
    global store
    store = simpy.Store(env, capacity=1000)


    adamGeneA, adamGeneB = str(input("set ADAM(Male)  >> geneA geneB >>")).split()
    eveGeneA, eveGeneB = str(input("set ADAM(Male)  >> geneA geneB >>")).split()

    list(adamGeneA)
    list(adamGeneB)
    list(eveGeneA)
    list(eveGeneB)

    globals()['entity_1'] = entity(1, 0, 0, 0, adamGeneA, adamGeneB, 0)
    entityList.append(globals()['entity_1'])

    globals()['entity_2'] = entity(2, 1, 0, 0, eveGeneA, eveGeneB, 0)
    entityList.append(globals()['entity_2'])

    while len(entityList) < 50: #초기 2명에서 4씩 증가 >> 51까지 됨
        yield env.process(improveMakeBABY(env,store))
-        print(len(entityList))


env = simpy.Environment()

env.process(setup(env))
env.run()
print("end")