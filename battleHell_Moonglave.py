import pygame
import sys
import random
import math

pygame.init()


display = pygame.display.set_mode((1300,800))
pygame.display.set_caption('Battle Hell:South Moonglave!')

clock = pygame.time.Clock()

mapSize = 888

mapList = []
time = 0

unitsPop = 0
maxUnits = 100
units = []


unitsInTile = []

RoyalistMoney = 1
MoonglaveMoney = 1

mountains = 0
mountainsMax = 100

gX = 100
gY = 100

mx = 0
my = 0

takeTurn = False

northCas = 0
southCas = 0
#Two Sides
#Royalist Rebels
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
        global southCas
        global northCas
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
                    if ((self.faction == 'Moonglave' and tile.control < 100) or (self.faction == 'Royalist' and tile.control >-107) and self.uType != 'Builder' and self.uType != 'Aircraft' and self.uType != 'Border'):

                        chance = random.randint(1,10)
                        if tile.population >= 20:
                            chance = 1

                        if chance == 1:
                            self.targetX = tx
                            self.targetY = ty
                            self.hasTarget = True
                    elif self.uType == 'Builder' and ((self.faction == 'Moonglave' and tile.control >= 7 and tile.control < 100) or (self.faction == 'Royalist' and tile.control <= 3 and tile.control > -107)):
                        chance = random.randint(1,100)
                        if tile.population >= 20:
                            chance = 1

                        if chance == 1:
                            self.targetX = tx
                            self.targetY = ty
                            self.hasTarget = True
                    elif (self.uType == 'Border'  or self.uType =='AirCraft')and ((self.faction == 'Moonglave' and tile.control >= 7 and tile.control < 100) or (self.faction == 'Royalist' and tile.control <= 3 and tile.control > -107)):
                        chance = random.randint(1,10)
                        if tile.population >= 20:
                            chance = 1

                        if chance == 1:
                            self.targetX = tx
                            self.targetY = ty
                            self.hasTarget = True

                    elif (self.uType == 'Mountain')and ((self.faction == 'Moonglave' and  tile.control < 100) or (self.faction == 'Royalist' and tile.control > -107)):
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
                if self.faction == 'Moonglave':
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

                if self.faction == 'Royalist':
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
                if self.faction == 'Moonglave':
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

                rv = 1
                if tile.river == True:
                    rv = random.randint(1,  50)
                if moveChance == 1 and rv == 1 and ((tile.control > 3  and self.faction =='Moonglave') or (tile.control < 7 and self.faction =='Royalist')) :
                    

                    if self.hasTarget == False :
                        self.y = ty
                        
                        if self.tactic == 'Surge' and self.faction == 'Moonglave':
                            if tx <= self.x:
                                self.x = tx
                                if self.x == 100:
                                    self.targetX = self.startX
                                    self.tartgetY = self.startY
                                    self.hasTarget = True
                                    self.tactic = 'Roam'
                        elif self.tactic == 'Surge' and self.faction == 'Royalist':
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
                        rv = 1

                        if tile.river == True:
                            rv = random.randint(1, 5)
                            

                        if rv == 1:
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
                        if unit.faction =='Moonglave':
                            northCas = northCas + 1
                            print ("North Losses " + str(northCas))
                        else:
                            southCas = southCas + 1
                            print ("South Losses " + str(southCas))
                            
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
        if self.name == 'Royalist Irregular':
            color = (153, 0, 153)
        elif self.name == 'Royalist Regular':
            color = (122, 51, 153)
        elif self.name == 'Night Guard':
            color = (102, 51, 153)
        elif self.name == 'Azgarathi Raiding Party':
            color = (153, 0, 153)
        elif self.name == 'Attic Sacred Guard':
            color = (129, 0, 127)
            
        xSpot = self.x
        ySpot = self.y
        #print('Show')
        if self.faction == 'Moonglave':
            color = (10, 125, 20)
            if self.name == 'Lunis Company':
                color = (0, 120, 255)  # A bright, noticeable blue
            elif self.name == 'Janjil Jet':
                color = (0, 120, 255)
            else:
                color = (3, 168, 158)
            ySpot = ySpot+10

        if self.faction == 'Royalist' and self.uType == 'Aircraft':
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
    def __init__(self, x, y, width, height, control, population, unit, hasFort,mountain,river):
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
        self.river = river
        self.unit = ''

        mountainChance = random.randint(1,200)
        if mountainChance == 1:
            self.mountain = True
            mountains = mountains + 1

        

        cityChance = random.randint(1,50)
        if cityChance == 1:
            self.population = 20

        riverChance = random.randint(1,200)
        if riverChance == 1 and cityChance !=1:
            self.river = True
            
        rebelChance = random.randint(1,40)

        if y > 250:
            rebelChance = random.randint(1,3)
            unitChance = random.randint(1,3)
            if unitChance == 1:
                rebelMilita = Unit(self.x, self.y, self.x, self.y,'Royalist Irregular', 'Milita' ,'Royalist', 10, 30, 1, 1, 1, 30, 1, 1, 'Roam', False,False, 0,0,0,100)
                units.append(rebelMilita)

            
                
                
                
        elif y <=250:
            rebelChance = random.randint(1,40)
            unitChance = random.randint(1,3)
            if unitChance == 1:
                #self,x, y,startX, startY,name,uType,faction, cost, population, tech, speed, attack, defense, attackRange,digIn
                #self,x, y,startX, startY,name,uType,faction, cost, population, tech, speed, attack, defense, attackRange,digIn, tactic, engaged,hasTarget,targetX, targetY, currentMissionTime, maxMissionTime
                if rebelChance == 1:
                    rebelMilita = Unit(self.x, self.y, self.x, self.y,'Royalist Irregular', 'Milita' ,'Royalist', 10, 50, 1, 1, 1, 30, 1, 1, 'Roam', False,False, 0,0,0,100)
                    units.append(rebelMilita)

                else:    
                    MoonglaveV = Unit(self.x, self.y, self.x, self.y,'Lunis Company', 'Milita' ,'Moonglave', 1, 100, 1, 100, 3, 30, 10, 1, 'Roam', False,False, 0, 0, 0, 10)
                    units.append(MoonglaveV)
                
                #units.append(MoonglaveRRF)
                #units.append(MoonglaveOffensiveGuard)
                
            
                
                
        if rebelChance == 1:
            self.control = self.control - random.randint(1,10)
        
            
            

    def main(self, display):
        color = (0, 0, 255)  # A pure blue color

        if self.control < 3:
            color = (75, 0, 130)  # Dark Purple
        elif self.control < 7:
            color = (138, 43, 226)  # Medium Purple
        elif self.control < 10:
            color = (147, 112, 219)  # Light Purple
        elif self.control < 50:
            color = (173, 216, 230)  # Light Blue
        elif self.control < 100:
            color = (0, 0, 255)  # Pure Blue

        else:
            color = (0, 0, 139)  # Dark Blue

        pygame.draw.rect(display, color, (self.x, self.y, self.width, self.height))

        if self.population >= 20:
            pygame.draw.rect(display, (0, 0, 0), (self.x, self.y, 10, 10))

        if self.unit != '':
            pygame.draw.rect(display, (0, 0, 0), (self.x+15, self.y, 10, 10))

        if self.mountain == True:
            color = (139, 69, 19)  # A dark blue color for mountains
            pygame.draw.rect(display, color, (self.x, self.y, 7, 7))

        if self.river == True:
            color = (64, 130, 54)  
            pygame.draw.rect(display, color, (self.x, self.y, 7, 7))

        if self.hasFort == True:
            if self.control >= 7:
                color = (65, 105, 225)  # A royal blue color
            elif self.control <= 3:
                color = (75, 0, 130)  # Pure blue
            else:
                color = (173, 216, 230)  # A light blue (baby blue)
            pygame.draw.rect(display, color, (self.x, self.y, 5, 5))

            
            

        

            

    def takeTurn(self):
        global MoonglaveMoney
        global RoyalistMoney

        if self.control > 3 and self.control < 7:
            self.hasFort = False
        addMoneyChance = random.randint(1,90000)
        if addMoneyChance == 1:
            if self.control <= 3:
                RoyalistMoney = RoyalistMoney + self.population
            elif self.control >= 7:
                MoonglaveMoney = MoonglaveMoney + self.population
        buyUnitChance = random.randint(1,100)
        if buyUnitChance == 1 and self.population >= 20:
            unitChance = random.randint(1,30)
            
            if self.control >= 7:
                if unitChance < 6 and MoonglaveMoney >= 1:
                    MoonglaveMoney = MoonglaveMoney - 1
                    #self,x, y,startX, startY,name,uType,faction, cost, population, tech, speed, attack, defense, attackRange,digIn, tactic, engaged,hasTarget,targetX, targetY, currentMissionTime, maxMissionTime
                    for i in range(9):
                        MoonglaveV = Unit(self.x, self.y, self.x, self.y,'Lunis Company', 'Milita' ,'Moonglave', 1, 50, 1, 100, 3, 30, 10, 1, 'Roam', False,False, 0, 0, 0, 10)
                        units.append(MoonglaveV)
                    for i in range(3):
                        MoonglaveV = Unit(self.x, self.y, self.x, self.y,'Fanatic', 'Border' ,'Moonglave', 1, 100, 1, 100, 3, 30, 10, 1, 'Roam', False,False, 0, 0, 0, 10)
                        units.append(MoonglaveV)
                    for i in range(1):
                        dandyRRF = Unit(self.x, self.y, self.x, self.y,'Moonglave Engineer', 'Builder' ,'Moonglave', 1, 10, 150, 195, 1, 50, 100, 1, 'Roam', False,False, 0, 0, 0, 100)
                        units.append(dandyRRF)
                elif unitChance > 26 and MoonglaveMoney >= 1:
                    MoonglaveMoney = MoonglaveMoney - 1
                    for i in range(4):
                        MoonglaveV = Unit(self.x, self.y, self.x, self.y,'Janjil Jet', 'Aircraft' ,'Moonglave', 1, 30, 1, 150, 80, 300, 1000, 1, 'Roam', False,False, 0, 0, 0, 400)
                        units.append(MoonglaveV)

                    
                
                
                    


                    
            elif self.control <= 3:
                if unitChance < 6 and RoyalistMoney >= 1:
                    RoyalistMoney = RoyalistMoney - 1
                    for i in range(7):
                        rebelMilita = Unit(self.x, self.y, self.x, self.y,'Royalist Irregular', 'Milita' ,'Royalist', 1, 30, 1, 1, 1, 60, 10, 1, 'Roam', False,False, 0,0,0,100)
                        units.append(rebelMilita)
                    for i in range(1):
                        rebelMilita = Unit(self.x, self.y, self.x, self.y,'Night Guard', 'Border' ,'Royalist', 1, 100, 1, 10, 5, 60, 100, 1, 'Roam', False,False, 0,0,0,10)
                        units.append(rebelMilita)
                    for i in range(5):
                        dandyRRF = Unit(self.x, self.y, self.x, self.y,'Torobundi Trencher', 'Builder' ,'Royalist', 1, 10, 150, 195, 1, 50, 100, 1, 'Roam', False,False, 0, 0, 0, 100)
                        units.append(dandyRRF)

                if unitChance > 15 and unitChance < 20 and RoyalistMoney >= 1:
                    RoyalistMoney = RoyalistMoney - 1
                    for i in range(4):
                        rebelMilita = Unit(self.x, self.y, self.x, self.y,'Royalist Regular', 'Border' ,'Royalist', 1, 60, 1, 40, 70, 160, 600, 1, 'Roam', False,False, 0,0,0,100)
                        units.append(rebelMilita)

                if unitChance > 20 and unitChance < 24 and RoyalistMoney >= 1:
                    RoyalistMoney = RoyalistMoney - 1
                    for i in range(2):
                        dandyRRF = Unit(self.x, self.y, self.x, self.y,'Torobundi Regular', 'Milita' ,'Royalist', 1, 100, 10, 1, 1, 500, 25, 1, 'Roam', False,False, 0, 0, 0, 1000)
                        units.append(dandyRRF)
                    
                if unitChance > 25 and RoyalistMoney >= 1:
                    RoyalistMoney = RoyalistMoney - 1
                    for i in range(7):
                        rebelMilita = Unit(self.x, self.y, self.x, self.y,'Azgarathi Raiding Party', 'Aircraft' ,'Royalist', 1, 30, 1, 20, 1, 360, 400, 1, 'Roam', False,False, 0,0,0,100)
                        units.append(rebelMilita)
                    if unitChance > 25:
    
                        for i in range(2):
                            rebelMilita = Unit(self.x, self.y, self.x, self.y,'Attic Sacred Guard', 'Mountain' ,'Royalist', 1, 100, 1, 50, 80, 150, 550, 1, 'Roam', False,False, 0,0,0,100)
                            units.append(rebelMilita)
                    
                   
         
                    
                
        #print('Test')
                
                
        

            

#player = Player(400, 300, 32, 32,0,0,0,0)

myFont = pygame.font.SysFont("Times New Roman", 18)

for t in range(mapSize):
    
    newTile = Tile(gX, gY, 20, 20, 10,1,[], False, False,False)
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

        if t.river == True and t.x > t2.x - 20 and t.x < t2.x + 20 and t.y > t2.y - 80 and t.y < t2.y + 80 and t.y != t2.y:
            sChance =  random.randint(1,2)
            if sChance == 1 and t2.population <20:
                t2.river = True
                
        if t.population == 20 and t.x > t2.x - 50 and t.x < t2.x + 50 and t.y > t2.y - 50 and t.y < t2.y + 50:
            sChance =  random.randint(1,5)
            if sChance == 1:
                t2.population = 20
        
        
    

paused = False

while True:
    MoonglaveMLabel = myFont.render("New Moonglave Money:" + str(MoonglaveMoney), 1, (255,255,255))
    RoyalistMLabel = myFont.render("South Moonglave Money:" + str(RoyalistMoney), 1, (255,255,255))

    MoonglaveCLabel = myFont.render("New Moonglave Losses:" + str(northCas), 1, (255,255,255))
    RoyalistCLabel = myFont.render("South Moonglave Losses:" + str(southCas), 1, (255,255,255))
    
    mx, my = pygame.mouse.get_pos()
    #print(str(mx))
    
    unitsInTile = []
    if takeTurn == True and  paused == False:
   
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
        if unit.faction == 'Moonglave':
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
        RoyalistMoney = RoyalistMoney + 1

    if keys[pygame.K_d]:
        MoonglaveMoney = MoonglaveMoney + 1

    if keys[pygame.K_p]:
        if paused == False:
            paused = True
            print (paused)
        else:
            paused = False

        #print(time)
  
    #player.main(display)
    display.blit(MoonglaveMLabel, (20, 20))
    display.blit(RoyalistMLabel, (20, 40))
    display.blit(MoonglaveCLabel, (20, 710))
    display.blit(RoyalistCLabel, (20, 730))
    
    clock.tick(60)

    pygame.display.update()
   
