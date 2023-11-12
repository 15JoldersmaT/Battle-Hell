import pygame
import sys
import random
import math

pygame.init()


display = pygame.display.set_mode((1300,800))
pygame.display.set_caption('Battle Hell:Civil War!')

clock = pygame.time.Clock()

mapSize = 888

mapList = []
time = 0

unitsPop = 0
maxUnits = 100
units = []


unitsInTile = []

tralishMoney = 1
dandyMoney = 1

mountains = 0
mountainsMax = 100

gX = 100
gY = 100

mx = 0
my = 0

takeTurn = False


#Two Sides
#Tralish Rebels
#GOD

#load images
#mush_img = pygame.image.load('imgs/EmsquestMush.png')

class Unit:
    def __init__(self,x, y,startX, startY,name,uType,faction, cost, population, tech, speed, attack, defense, attackRange,digIn, tactic, engaged,hasTarget,targetX, targetY, currentMissionTime, maxMissionTime):
        self.x = x
        self.y = y
        self.startX = startX
        self.startY = startY
        self.name = name
        self.uType = uType
        self.faction = faction
        self.cost = cost
        self.population = population
        self.tech = tech
        self.speed = speed
        self.attack = attack
        self.defense = defense
        self.attackRange = attackRange
        self.digIn = digIn
        self.tactic = tactic
        self.engaged = engaged
        self.hasTarget = hasTarget
        self.targetX = targetX
        self.targetY = targetY
        self.currentMissionTime = currentMissionTime
        self.maxMissionTime = maxMissionTime
        self.hasTarget = False

            

    def takeTurn(self):
        global mx
        global my
        
        if mx >= self.x and mx <= self.x + 25 and my >= self.y and my <= self.y + 25:
            unitsInTile.append(self)

        if self.uType == 'Offensive':
            surgeChance = random.randint(1,100)
            if surgeChance <= 10:
                self.tactic = 'Surge'
                self.hasTarget = False
            elif surgeChance == 100:
                self.tactic = 'Roam'
            
        self.currentMissionTime = self.currentMissionTime + 1
        if self.currentMissionTime >= self.maxMissionTime or self.hasTarget == False:
            self.curretMissionTime = 0
            self.targetX = 0
            self.targetY = 0
            self.hasTarget = False
            for tile in mapList:
                #is close enough
                tx = tile.x
                ty = tile.y
                
                selectChance2 = random.randint(1,50)
                if selectChance2 == 1 and tx  > self.x - (26 * self.attackRange) and tx < self.x + (26 *self.attackRange)  and ty > self.y - (26 * self.attackRange) and ty < self.y +(26 * self.attackRange) and self.engaged == False:
                    if ((self.faction == 'Dandy' and tile.control < 100) or (self.faction == 'Tralish' and tile.control >-107) and self.uType != 'Builder' and self.uType != 'Aircraft' and self.uType != 'Border'):

                        chance = random.randint(1,10)
                        if tile.population >= 20:
                            chance = 1

                        if chance == 1:
                            self.targetX = tx
                            self.targetY = ty
                            self.hasTarget = True
                    elif self.uType == 'Builder' and ((self.faction == 'Dandy' and tile.control >= 7 and tile.control < 100) or (self.faction == 'Tralish' and tile.control <= 3 and tile.control > -107)):
                        chance = random.randint(1,100)
                        if tile.population >= 20:
                            chance = 1

                        if chance == 1:
                            self.targetX = tx
                            self.targetY = ty
                            self.hasTarget = True
                    elif (self.uType == 'Border'  or self.uType =='AirCraft')and ((self.faction == 'Dandy' and tile.control >= 7 and tile.control < 100) or (self.faction == 'Tralish' and tile.control <= 3 and tile.control > -107)):
                        chance = random.randint(1,10)
                        if tile.population >= 20:
                            chance = 1

                        if chance == 1:
                            self.targetX = tx
                            self.targetY = ty
                            self.hasTarget = True

                    elif (self.uType == 'Mountain')and ((self.faction == 'Dandy' and  tile.control < 100) or (self.faction == 'Tralish' and tile.control > -107)):
                        chance = random.randint(1,100)
                        if tile.mountain == True:
                            chance = random.randint(1,10)
                        
                        

                        if chance == 1:
                            self.targetX = tx
                            self.targetY = ty
                            self.hasTarget = True
                        
                        
                
                
            
        for tile in mapList:
            tx = tile.x
            ty = tile.y

            if tx == self.x and ty == self.y and tx == self.targetX and ty == self.targetY:
                buildChance = random.randint(1,200)
                if self.faction == 'Dandy':
                    buildChance = random.randint(1,30)
                    
                    
                if buildChance == 1:
                    self.hasTarget = False
                    if self.uType =='Builder':
                        #print('Dead')
                        tile.hasFort = True
                        #print('BUILT')
                        units.remove(self)
                    
            #is close enough
            if tx  > self.x - 30 and tx < self.x + 30 and ty > self.y - 30 and ty < self.y +30 and (self.engaged == False or self.uType == 'Aircraft'):
                moveChance = random.randint(1,(200-self.speed))
                fort = 0
                mountain = 0
                if self.uType != 'Mountain' and tile.mountain == True:
                    mountain = 200
                    
                    
                if tile.hasFort == True:
                    fort = 150
                    if tile.control >= 7:
                        fort = 300
                    #print('Using')

                if self.faction == 'Tralish':
                    if tile.control > 3:
                        takeChance = random.randint(1,  50+ fort + mountain)
                    else:
                        takeChance = random.randint(1,  50)
                        
                    if takeChance == 1:
                        tile.control = tile.control - math.floor(self.population/10)
                    
                    if tile.control < -147:
                        tile.control = -147
                    
                    if tile.control <= 3:
                        numChance = random.randint(1,150)
                        if numChance == 1:
                            self.population = self.population + tile.population
                        if self.population > 100:
                            self.population = 100
                        if self.uType == 'Aircraft' and self.population >= 30:
                            self.population = 30
                    #print(tile.control)
                if self.faction == 'Dandy':
                    if tile.control < 7:
                        takeChance = random.randint(1,  50+fort + mountain)
                    else:
                        takeChance = random.randint(1,  50)
                            
                    if takeChance == 1:
                        tile.control = tile.control + math.floor(self.population/10)
                    if tile.control > 150:
                        tile.control = 150
                    if tile.control >= 7:
                        numChance = random.randint(1,150)
                        if numChance == 1:
                            self.population = self.population + tile.population
                        if self.population > 100:
                            self.population = 100
                        if self.uType == 'Aircraft' and self.population >= 30:
                            self.population = 30
                        
                    #print(tile.control)

                
                if moveChance == 1  and ((tile.control > 3  and self.faction =='Dandy') or (tile.control < 7 and self.faction =='Tralish')) :
                    

                    if self.hasTarget == False :
                        self.y = ty
                        
                        if self.tactic == 'Surge' and self.faction == 'Dandy':
                            if tx <= self.x:
                                self.x = tx
                                if self.x == 100:
                                    self.targetX = self.startX
                                    self.tartgetY = self.startY
                                    self.hasTarget = True
                                    self.tactic = 'Roam'
                        elif self.tactic == 'Surge' and self.faction == 'Tralish':
                            if tx >= self.x:
                                self.x = tx
                                if self.x == 1025:
                                    self.targetX = self.startX
                                    self.tartgetY = self.startY
                                    self.hasTarget = True
                                    self.tactic = 'Roam'
                        else:
                            self.x = tx
                            self.y = ty
                    elif self.hasTarget == True :
                        #print('New Move')
                        if self.x < self.targetX:
                            self.x = self.x + 25
                        if self.x > self.targetX:
                            self.x = self.x - 25
                        if self.y < self.targetY:
                            self.y = self.y + 25
                        if self.y > self.targetY:
                            self.y = self.y - 25
                   
                        

        self.engaged = False

        for unit in units:
            tx = unit.x
            ty = unit.y
            #contact
            if tx == self.x and ty == self.y and self.faction != unit.faction and unit.population > 0:
                self.engaged = True
                for i in range(self.population):
                    attackChance = random.randint(self.attack, 100+unit.defense)
                    if attackChance == 100:
                        unit.population = unit.population - 1
                        #if unit.population <= 0:
                         #   self.engaged = False
                           # print('kill')
                
                    
                
       
                        
                        #print('Test')
    def main(self, display):
        if self.population <=0:
            #print('Dead')
            units.remove(self)
        
        color = (255,252,0)
        if self.name == 'Arkish Guard':
            color = (139, 0, 0)
        elif self.name == 'Fire Heart':
            color = (255, 55,55)
            
            
        xSpot = self.x
        ySpot = self.y
        #print('Show')
        if self.faction == 'Dandy':
            color = (10, 125, 20)
            if self.name == 'Narkish Guard':
                color = (87, 8, 97)
            elif self.name == 'Watcher':
                color = (67, 188, 224)
            ySpot = ySpot+10

        if self.faction == 'Tralish' and self.uType == 'Aircraft':
            ySpot = ySpot+ 5
            xSpot = xSpot - 5
            

      

        wSize = 10

        if self.uType == 'Builder':
            wSize = 5
        if self.uType != 'Aircraft':
            if self.population > 70:
                pygame.draw.rect(display, color, (xSpot + 10,  ySpot, 10, wSize))
            elif self.population > 50:
                pygame.draw.rect(display, color, (xSpot + 10,  ySpot, 7, wSize))
            elif self.population >30:
                pygame.draw.rect(display, color, (xSpot + 10,  ySpot, 5, wSize))
            else:
                pygame.draw.rect(display, color, (xSpot + 10,  ySpot, 3, wSize))


        else :
            if self.population > 70:
                pygame.draw.circle(display, color, (xSpot+10, ySpot),10)
            elif self.population > 50:
                pygame.draw.circle(display, color, (xSpot+10, ySpot),7)
            elif self.population >30:
                pygame.draw.circle(display, color, (xSpot+10, ySpot),5)
            else:
                pygame.draw.circle(display, color, (xSpot+10, ySpot),3)

            

            
        
            
                
            

    
class Tile:
    def __init__(self, x, y, width, height, control, population, unit, hasFort,mountain):
        global mountains
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.control = control
        self.population = population
        self.unit = unit
        self.hasFort = hasFort
        self.mountain = mountain
        self.unit = ''
        mountainChance = random.randint(1,100)
        if mountainChance == 1:
            self.mountain = True
            mountains = mountains + 1
        cityChance = random.randint(1,50)
        if cityChance == 1:
            self.population = 20
        rebelChance = random.randint(1,40)
        if x < 600:
            rebelChance = random.randint(1,3)
            unitChance = random.randint(1,3)
            if unitChance == 1:
                rebelMilita = Unit(self.x, self.y, self.x, self.y,'Tralish Mob', 'Milita' ,'Tralish', 10, 100, 1, 1, 1, 60, 1, 1, 'Roam', False,False, 0,0,0,100)
                units.append(rebelMilita)

                rebArkC = random.randint(1,10)
                if rebArkC == 1:
                    rebelArk = Unit(self.x, self.y, self.x, self.y,'Arkish Guard', 'Offensive' ,'Tralish', 10, 100, 1, 1, 40, 2, 100, 1, 'Roam', False,False, 0,0,0,1000)
                    #units.append(rebelArk)
                if rebArkC == 2:
                    rebelArk = Unit(self.x, self.y, self.x, self.y,'Yazel Moonlight', 'Aircraft' ,'Tralish', 10, 30, 1, 100, 99, 500, 100, 1, 'Roam', False,False, 0,0,0,1000)
                    #units.append(rebelArk)
                
                
                
        elif x >700:
            rebelChance = random.randint(1,13)
            unitChance = random.randint(1,9)
            if unitChance == 1:
                #self,x, y,startX, startY,name,uType,faction, cost, population, tech, speed, attack, defense, attackRange,digIn
                #self,x, y,startX, startY,name,uType,faction, cost, population, tech, speed, attack, defense, attackRange,digIn, tactic, engaged,hasTarget,targetX, targetY, currentMissionTime, maxMissionTime
                if rebelChance == 1:
                    rebelMilita = Unit(self.x, self.y, self.x, self.y,'Tralish Mob', 'Milita' ,'Tralish', 10, 100, 1, 1, 1, 60, 1, 1, 'Roam', False,False, 0,0,0,100)
                    units.append(rebelMilita)

                else:    
                    dandyV = Unit(self.x, self.y, self.x, self.y,'Dandy Volunteer', 'Milita' ,'Dandy', 1, 100, 1, 100, 10, 30, 10, 50, 'Roam', False,False, 0, 0, 0, 50)
                    units.append(dandyV)
                
                #units.append(dandyRRF)
                #units.append(dandyOffensiveGuard)
                
            
                
                
        if rebelChance == 1:
            self.control = self.control - random.randint(1,10)
        
            
            

    def main(self, display):
        color = (124,252,0)
        
        if self.control >= 100:
            color = (128,128,0)
        elif self.control < 7 and self.control > 3:
            color = (220,220,220)
            
        elif self.control <= 3:
            color = (240,160,89)
            if self.control <= -107:
                color = (204,85,0)
            
        pygame.draw.rect(display, color, (self.x, self.y, self.width, self.height))
        if self.population >= 20:
            pygame.draw.rect(display, (0,0,0), (self.x, self.y, 10, 10))
        if self.unit != '':
            
                
            pygame.draw.rect(display, (0,0,0), (self.x+15, self.y, 10, 10))

        if self.mountain == True:
            color = (150, 75, 0)
            pygame.draw.rect(display, color, (self.x, self.y, 7, 7))


        if self.hasFort == True:
            if self.control >= 7:
                color = (137,207,240)
            elif self.control <= 3:
                color = (255, 105, 180)
            else:
                color = (220,220,220)
            pygame.draw.rect(display, color, (self.x, self.y, 5, 5))

            
            

        

            

    def takeTurn(self):
        global dandyMoney
        global tralishMoney

        if self.control > 3 and self.control < 7:
            self.hasFort = False
        addMoneyChance = random.randint(1,90000)
        if addMoneyChance == 1:
            if self.control <= 3:
                tralishMoney = tralishMoney + self.population
            elif self.control >= 7:
                dandyMoney = dandyMoney + self.population
        buyUnitChance = random.randint(1,100)
        if buyUnitChance == 1 and self.population >= 20:
            unitChance = random.randint(1,30)
            
            if self.control >= 7:
                if unitChance < 6 and dandyMoney >= 1:
                    dandyMoney = dandyMoney - 1
                    #self,x, y,startX, startY,name,uType,faction, cost, population, tech, speed, attack, defense, attackRange,digIn, tactic, engaged,hasTarget,targetX, targetY, currentMissionTime, maxMissionTime
                    for i in range(9):
                        dandyV = Unit(self.x, self.y, self.x, self.y,'Dandy Volunteer', 'Milita' ,'Dandy', 1, 100, 1, 100, 3, 30, 10, 1, 'Roam', False,False, 0, 0, 0, 10)
                        units.append(dandyV)

                elif unitChance >= 6 and  unitChance <= 12 and dandyMoney >= 1:
                    dandyMoney = dandyMoney - 1
                    for i in range(10):
                        dandyOffensiveGuard = Unit(self.x, self.y, self.x, self.y,'Narkish Guard', 'Milita' ,'Dandy', 1, 300, 50, 150, 80, 100, 100, 1, 'Roam', False,False,0,0,0,1000)
                        units.append(dandyOffensiveGuard)
                    for i in range(3):
                        dandyOffensiveGuard = Unit(self.x, self.y, self.x, self.y,'Odludian Artillery', 'Border' ,'Dandy', 1, 100, 20, 99, 1, 100, 100, 1, 'Roam', False,False,0,0,0,2000)
                        units.append(dandyOffensiveGuard)
                

                    
                elif unitChance > 12 and unitChance  < 20 and dandyMoney >= 1:
                    dandyMoney = dandyMoney - 1
                    for i in range(6):
                        dandyRRF = Unit(self.x, self.y, self.x, self.y,'Rapid Reaction Force', 'Aircraft' ,'Dandy', 1, 10, 150, 170, 30, 300, 100, 1, 'Roam', False,False, 0, 0, 0, 100)
                        units.append(dandyRRF)
                    for i in range(9):
                        dandyRRF = Unit(self.x, self.y, self.x, self.y,'Dandy Mountaineer', 'Mountain' ,'Dandy', 1, 100, 150, 1, 50, 50, 100, 1, 'Roam', False,False, 0, 0, 0, 100)
                        units.append(dandyRRF)
                elif unitChance >= 20 and dandyMoney >= 1:
                    dandyMoney = dandyMoney - 1
                    for i in range(10):
                        dandyRRF = Unit(self.x, self.y, self.x, self.y,'Odludian Engineer', 'Builder' ,'Dandy', 1, 10, 150, 195, 1, 50, 100, 1, 'Roam', False,False, 0, 0, 0, 100)
                        units.append(dandyRRF)
                    for i in range(9):
                        dandyRRF = Unit(self.x, self.y, self.x, self.y,'Watcher', 'Border' ,'Dandy', 1, 200, 10, 1, 10, 300, 100, 1, 'Roam', False,False,0,0,0,100)
                        units.append(dandyRRF)
                    


                    
            elif self.control <= 3:
                if unitChance < 6 and tralishMoney >= 1:
                    tralishMoney = tralishMoney - 1
                    for i in range(7):
                        rebelMilita = Unit(self.x, self.y, self.x, self.y,'Tralish Mob', 'Milita' ,'Tralish', 10, 100, 1, 1, 1, 60, 10, 1, 'Roam', False,False, 0,0,0,100)
                        units.append(rebelMilita)
                    for i in range(9):
                        rebelMilita = Unit(self.x, self.y, self.x, self.y,'Candle Hill Brawlers', 'Mountain' ,'Tralish', 1, 100, 150, 100, 80, 150, 7, 1, 'Roam', False,False, 0, 0, 0, 100)
                        units.append(rebelMilita)
                     
                   

                elif unitChance>= 6 and  unitChance < 14 and tralishMoney >= 1:
                    tralishMoney = tralishMoney - 1
                    attackX = 0
                    attackY = 0
                    for tile in mapList:
                        selectC = random.randint(1,888)
                        if tile.control >3 and selectC == 1:
                            attackX = tile.x
                            attackY = tile.y



                            
                    for i in range(8):
                        rebelArk = Unit(self.x, self.y, self.x, self.y,'Arkish Guard', 'Milita' ,'Tralish', 10, 300, 1, 100, 40, 2, 100, 1, 'Roam', False,False, 0,0,0,1000)
                        units.append(rebelArk)
                    for i in range(3):
                        rebelArk = Unit(self.x, self.y, self.x, self.y,'Tralish Canon', 'Border' ,'Tralish', 10, 300, 1, 1, 90, 10, 100, 1, 'Roam', False,False, 0,0,0,2000)
                        units.append(rebelArk)
                 

                elif unitChance>= 14 and unitChance <= 18 and tralishMoney >= 1:
                    tralishMoney = tralishMoney - 1
                    for i in range(3):
                        rebelArk = Unit(self.x, self.y, self.x, self.y,'Yazel Reaper', 'Aircraft' ,'Tralish', 10, 30, 1, 100, 99, 500, 100, 1, 'Roam', False,False, 0,0,0,100)
                        units.append(rebelArk)

                elif unitChance > 18 and tralishMoney >= 1:
                    for i in range(13):
                        #self,x, y,startX, startY,name,uType,faction, cost, population, tech, speed, attack, defense, attackRange,digIn, tactic, engaged,hasTarget,targetX, targetY, currentMissionTime, maxMissionTime

                        rebelArk = Unit(self.x, self.y, self.x, self.y,'Tralish Builder', 'Builder' ,'Tralish', 10, 10, 1, 190, 1, 2, 100, 1, 'Roam', False,False, 0,0,0,1000)
                        units.append(rebelArk)

                    for i in range(10):
                        dandyRRF = Unit(self.x, self.y, self.x, self.y,'Fire Heart', 'Border' ,'Tralish', 1, 300, 1, 20, 10, 300, 100, 1, 'Roam', False,False,0,0,0,100)
                        units.append(dandyRRF)
                    
                
        #print('Test')
                
                
        

            

#player = Player(400, 300, 32, 32,0,0,0,0)

myFont = pygame.font.SysFont("Times New Roman", 18)

for t in range(mapSize):
    
    newTile = Tile(gX, gY, 20, 20, 10,1,[], False, False)
    gX += 25
    if gX > 1000:
        #print('Last X' + str(gX))
        gX = 100
        gY += 25
    mapList.append(newTile)


for t in mapList:

    
    
    for t2 in mapList:

        if t.mountain == True and t.x > t2.x - 50 and t.x < t2.x + 50 and t.y > t2.y - 50 and t.y < t2.y + 50:
            sChance =  random.randint(1,5)
            if sChance == 1:
                t2.mountain = True
        
    

    
while True:
    dandyMLabel = myFont.render("Dandy Money:" + str(dandyMoney), 1, (255,255,255))
    tralishMLabel = myFont.render("Tralish Money:" + str(tralishMoney), 1, (255,255,255))

   
    
    mx, my = pygame.mouse.get_pos()
    #print(str(mx))
    
    unitsInTile = []
    if takeTurn == True:
        
        for unit in units:
            unit.takeTurn()
            time = time+1

            
        for tile in mapList:
            tile.takeTurn()

  
        time = time+1
        takeTurn = False
 
        
    display.fill((24,164,86))
    pygame.draw.rect(display, (0,0,25), (0,0,1300,1200))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed();

    #background

    for tile in mapList:
        tile.main(display)

    for unit in units:
        unit.main(display)

    counter = 0
        
    for unit in unitsInTile:
        #print(unit.name)
        counter = counter+1
        if unit.faction == 'Dandy':
            color= (0,255,0)
        else:
            color = (255,0,0)
            
        nameLabel = myFont.render(str(unit.name) + '-' +str(unit.population), 1, color)
        display.blit(nameLabel, (1050, 40*counter))
            

    #Move around
    #pygame.draw.rect(display, (255,255,255), (100-display_scroll[0],100 -display_scroll[1],16,16))

    if keys[pygame.K_a]:
        takeTurn = True

    takeTurn = True
    if keys[pygame.K_t]:
        tralishMoney = tralishMoney + 1

    if keys[pygame.K_d]:
        dandyMoney = dandyMoney + 1

        #print(time)
  
    #player.main(display)
    display.blit(dandyMLabel, (20, 20))
    display.blit(tralishMLabel, (20, 40))

    
    clock.tick(60)

    pygame.display.update()
   
