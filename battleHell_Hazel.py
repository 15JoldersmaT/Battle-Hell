import pygame
import sys
import random
import math

pygame.init()


display = pygame.display.set_mode((1300,800))
pygame.display.set_caption('Battle Hell:Mythe!')

clock = pygame.time.Clock()

mapSize = 888

mapList = []
time = 0

unitsPop = 0
maxUnits = 100
units = []


unitsInTile = []

MytheMoney = 1
HazelMoney = 1

mountains = 0
mountainsMax = 100

mudTimer = 2000


gX = 100
gY = 100

mx = 0
my = 0

takeTurn = False

northCas = 0
southCas = 0

hazelSupport = random.randint(1,5000)
mytheSupport = random.randint(1,5000)
#Two Sides
#Mythe Rebels
#GOD

#load images
#mush_img = pygame.image.load('imgs/EmsquestMush.png')

class Unit:
    def __init__(self,x, y,startX, startY,name,uType,faction, cost, population, tech, speed, attack, defense, attackRange,digIn, tactic, engaged,hasTarget,targetX, targetY, currentMissionTime, maxMissionTime, Marsh):
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
        self.Marsh = False

            

    def takeTurn(self):
        global mx
        global my
        global southCas
        global northCas
        global mudTimer
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
                    if ((self.faction == 'Hazel' and tile.control < 100) or (self.faction == 'Mythe' and tile.control >-107) and self.uType != 'Builder' and self.uType != 'Aircraft' and self.uType != 'Border'):

                        chance = random.randint(1,10)
                        if tile.population >= 20:
                            chance = 1

                        if chance == 1:
                            self.targetX = tx
                            self.targetY = ty
                            self.hasTarget = True
                    elif self.uType == 'Builder' and ((self.faction == 'Hazel' and tile.control >= 7 and tile.control < 100) or (self.faction == 'Mythe' and tile.control <= 3 and tile.control > -107)):
                        chance = random.randint(1,100)
                        if tile.population >= 20:
                            chance = 1

                        if chance == 1:
                            self.targetX = tx
                            self.targetY = ty
                            self.hasTarget = True
                    elif (self.uType == 'Border'  or self.uType =='AirCraft')and ((self.faction == 'Hazel' and tile.control >= 7 and tile.control < 100) or (self.faction == 'Mythe' and tile.control <= 3 and tile.control > -107)):
                        chance = random.randint(1,10)
                        if tile.population >= 20:
                            chance = 1

                        if chance == 1:
                            self.targetX = tx
                            self.targetY = ty
                            self.hasTarget = True

                    elif (self.uType == 'Mountain')and ((self.faction == 'Hazel' and  tile.control < 100) or (self.faction == 'Mythe' and tile.control > -107)):
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
                if self.faction == 'Hazel':
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
                Marsh = 0
                if self.uType != 'Mountain' and tile.mountain == True:
                    mountain = 200
                if self.Marsh == False and tile.Marsh == True and mudTimer < 1000:
                    Marsh = 400
                    
                    
                if tile.hasFort == True:
                    fort = 150
                    if tile.control >= 7:
                        fort = 300
                    #print('Using')

                if self.faction == 'Mythe':
                    if tile.control > 3:
                        takeChance = random.randint(1,  50+ fort + mountain+Marsh)
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
                if self.faction == 'Hazel':
                    if tile.control < 7:
                        takeChance = random.randint(1,  50+fort + mountain+Marsh)
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
                if moveChance == 1 and rv == 1 and ((tile.control > 3  and self.faction =='Hazel') or (tile.control < 7 and self.faction =='Mythe')) :
                    

                    if self.hasTarget == False :
                        self.y = ty
                        
                        if self.tactic == 'Surge' and self.faction == 'Hazel':
                            if tx <= self.x:
                                self.x = tx
                                if self.x == 100:
                                    self.targetX = self.startX
                                    self.tartgetY = self.startY
                                    self.hasTarget = True
                                    self.tactic = 'Roam'
                        elif self.tactic == 'Surge' and self.faction == 'Mythe':
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
                        if unit.faction =='Hazel':
                            northCas = northCas + 1
                        else:
                            southCas = southCas + 1
                            
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
        if self.name == 'Mythe Irregulars':
            color = (225, 225, 182)  # Standard Orange
        elif self.name == 'Mythe Regulars':
            color = (255, 255, 0)  # Coral Orange
        elif self.name == 'Red Flower Centuria':
            color = (255, 0, 0)  
        elif self.name == 'Mythe Raiding Party':
            color = (255, 255, 0)  # Tomato Orange
        elif self.name == 'Xetta Trained Regular':
            color = (15, 0, 55)  # Dark Orange
        elif self.name == 'Royal Combat Engineer':
                color = (200, 0, 0)  # Cobalt Blue
            
            
        xSpot = self.x
        ySpot = self.y
        #print('Show')
        if self.faction == 'Hazel':
            if self.name == 'Hazel Regulars':
                color = (140, 110, 70)  # Vivid Royal Blue
            elif self.name == 'Hazel Milita':
                color = (210, 180, 140)  # Cobalt Blue
            elif self.name == 'Royal Sentinels':
                color = (0, 140, 0)  # Cobalt Blue
            elif self.name == 'Royal Air Patrol':
                color = (0, 180, 0)  # Cobalt Blue
            elif self.name == 'Royal Combat Engineer':
                color = (0, 180, 0)  # Cobalt Blue
            
            else:
                color = (0, 50, 200)  # Sapphire Blue
            ySpot = ySpot+10

        if self.faction == 'Mythe' and self.uType == 'Aircraft':
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
    def __init__(self, x, y, width, height, control, population, unit, hasFort,mountain,river,Marsh):
        global mountains
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.control = control
        self.population = population
        self.unit = unit
        self.hasFort = hasFort
        self.Marsh = Marsh
        self.mountain = mountain
        self.river = river
        self.unit = ''

        mountainChance = random.randint(1,200)
        if self.x < 300:
            mountainChance = 1
        if mountainChance == 1:
            #self.mountain = True
            mountains = mountains + 1

        

        cityChance = random.randint(1,150)
        if x > 550:
            cityChance = random.randint(1,15)
            
        if cityChance == 1:
            self.population = 20

     

        MarshChance = random.randint(1,35)
        if MarshChance == 1:
            self.Marsh = True
            
        rebelChance = random.randint(1,40)

        if x > 550:
            rebelChance = random.randint(1,3)
            unitChance = random.randint(1,20)
            if unitChance == 1:
                HazelV = Unit(self.x, self.y, self.x, self.y,'Hazel Regulars', 'Milita' ,'Hazel', 1, 100, 1, 50, 50, 100, 100, 1, 'Roam', False,False, 0, 0, 0, 100,True)

                units.append(HazelV)
                for i in range(2):
                    HazelV2 = Unit(self.x, self.y, self.x, self.y,'Hazel Milita', 'Milita' ,'Hazel', 1, 20, 1, 5, 5, 10, 10, 1, 'Roam', False,False, 0, 0, 0, 100,False)

                    units.append(HazelV2)

            
                
                
                
        elif x <=550:
            rebelChance = random.randint(1,10)
            unitChance = random.randint(1,5)
            if unitChance == 1:
                #self,x, y,startX, startY,name,uType,faction, cost, population, tech, speed, attack, defense, attackRange,digIn
                #self,x, y,startX, startY,name,uType,faction, cost, population, tech, speed, attack, defense, attackRange,digIn, tactic, engaged,hasTarget,targetX, targetY, currentMissionTime, maxMissionTime
                if rebelChance <= 3:
                    rebelMilita = Unit(self.x, self.y, self.x, self.y,'Mythe Irregulars', 'Milita' ,'Mythe', 1, 100, 1, 1, 1, 60, 10, 1, 'Roam', False,False, 0,0,0,100,False)
                    units.append(rebelMilita)

                else:    
                    rebelMilita = Unit(self.x, self.y, self.x, self.y,'Mythe Regulars', 'Border' ,'Mythe', 1, 100, 1, 40, 30, 160, 600, 1, 'Roam', False,False, 0,0,0,100,False)
                    units.append(rebelMilita)
                    rebelMilita2 = Unit(self.x, self.y, self.x, self.y,'Red Flower Centuria', 'Border' ,'Mythe', 1, 100, 1, 100, 50, 200, 600, 1, 'Roam', False,False, 0,0,0,1000,True)
                    units.append(rebelMilita2)
                
                #units.append(HazelRRF)
                #units.append(HazelOffensiveGuard)
                
            
                
                
        if rebelChance == 1:
            self.control = self.control - random.randint(1,10)
        if self.x >=550:
            self.control = 100
        else:
            self.control = 0
        
            
            

    def main(self, display):
        color = (0, 0, 255)  # A pure blue color

        # Initially setting the color to a shade of grey or orange based on the control value
        if self.control < 3:
            color = (0, 128, 128)  # Dark Teal
        elif self.control < 7:
            color = (0, 153, 153)  # Medium Teal
        elif self.control < 10:
            color = (0, 178, 178)
        elif self.control < 50:
            color = (160, 82, 45)  # Light Brown
        elif self.control < 100:
            color = (139, 69, 19)  # Medium Brown
        else:
            color = (101, 67, 33)

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
                color = (55, 50, 55)  # A royal blue color
            elif self.control <= 3:
                color = (55, 50, 55)  # Pure blue
            else:
                color = (55, 50, 55)  # A light blue (baby blue)
            pygame.draw.rect(display, color, (self.x, self.y, 6, 6))

        if self.Marsh == True:
            color = (0, 225, 10)  # A dark blue color for mountains
            pygame.draw.rect(display, color, (self.x, self.y, 5, 5))
            
            

        

            

    def takeTurn(self):
        global HazelMoney
        global MytheMoney

        if self.control > 3 and self.control < 7:
            self.hasFort = False
        addMoneyChance = random.randint(1,90000)
        if addMoneyChance == 1:
            if self.control <= 3:
                MytheMoney = MytheMoney + self.population
            elif self.control >= 7:
                HazelMoney = HazelMoney + self.population
        buyUnitChance = random.randint(1,100)
        if buyUnitChance == 1 and self.population >= 20:
            unitChance = random.randint(1,30)
            
            if self.control >= 7:
                if unitChance < 6 and HazelMoney >= 1:
                    HazelMoney = HazelMoney - 1
                    #self,x, y,startX, startY,name,uType,faction, cost, population, tech, speed, attack, defense, attackRange,digIn, tactic, engaged,hasTarget,targetX, targetY, currentMissionTime, maxMissionTime
                    for i in range(3):
                        HazelV = Unit(self.x, self.y, self.x, self.y,'Hazel Regulars', 'Milita' ,'Hazel', 1, 100, 1, 50, 50, 100, 100, 1, 'Roam', False,False, 0, 0, 0, 100,True)
                        units.append(HazelV)
                        HazelV2 = Unit(self.x, self.y, self.x, self.y,'Hazel Milita', 'Milita' ,'Hazel', 1, 20, 1, 5, 5, 10, 10, 1, 'Roam', False,False, 0, 0, 0, 100,False)
                        units.append(HazelV2)
                    dandyRRF = Unit(self.x, self.y, self.x, self.y,'Royal Combat Engineer', 'Builder' ,'Hazel', 1, 100, 10, 1, 1, 1, 1, 1, 'Roam', False,False, 0, 0, 0, 500, False)
                    units.append(dandyRRF)


                    for i in range(1):
                        HazelV = Unit(self.x, self.y, self.x, self.y,'Royal Sentinels', 'Border' ,'Hazel', 1, 100, 1, 20, 50, 200, 500, 1, 'Roam', False,False, 0, 0, 0, 100,True)
                        units.append(HazelV)
                elif unitChance > 26 and HazelMoney >= 1:
                    HazelMoney = HazelMoney - 1

                    if time > hazelSupport:
                        for i in range(6):
                            HazelV = Unit(self.x, self.y, self.x, self.y,'Moonglaven Regular', 'Border' ,'Hazel', 1, 100, 1, 50, 80, 120, 700, 1, 'Roam', False,False, 0, 0, 0, 100,False)
                            units.append(HazelV)
                        for i in range(2):
                            MoonglaveV = Unit(self.x, self.y, self.x, self.y,'Janjil Jet', 'Aircraft' ,'Hazel', 1, 30, 1, 150, 80, 300, 1000, 1, 'Roam', False,False, 0, 0, 0, 400,False)
                            units.append(MoonglaveV)
                    if unitChance == 29:
                        HazelV = Unit(self.x, self.y, self.x, self.y,'Royal Air Patrol', 'Aircraft' ,'Hazel', 1, 30, 1, 140, 50, 100, 500, 1, 'Roam', False,False, 0, 0, 0, 300,False)
                        units.append(HazelV)
                        

                    
                
                
                    


                    
            elif self.control <= 3:
                if unitChance < 6 and MytheMoney >= 1:
                    MytheMoney = MytheMoney - 1
                    for i in range(8):
                        rebelMilita = Unit(self.x, self.y, self.x, self.y,'Mythe Irregulars', 'Milita' ,'Mythe', 1, 30, 1, 1, 1, 60, 10, 1, 'Roam', False,False, 0,0,0,100,False)
                        units.append(rebelMilita)
                    for i in range(3):
                        rebelMilita = Unit(self.x, self.y, self.x, self.y,'Red Flower Centuria', 'Border' ,'Mythe', 1, 100, 1, 100, 50, 200, 600, 1, 'Roam', False,False, 0,0,0,1000,True)
                        units.append(rebelMilita)
                    dandyRRF = Unit(self.x, self.y, self.x, self.y,'Royal Combat Engineer', 'Builder' ,'Mythe', 1, 100, 10, 1, 1, 1, 1, 1, 'Roam', False,False, 0, 0, 0, 500, False)
                    units.append(dandyRRF)
              

                if unitChance > 15 and unitChance < 20 and MytheMoney >= 1:
                    MytheMoney = MytheMoney - 1
                    for i in range(2):
                        rebelMilita = Unit(self.x, self.y, self.x, self.y,'Mythe Regulars', 'Border' ,'Mythe', 1, 60, 1, 40, 30, 160, 600, 1, 'Roam', False,False, 0,0,0,100,False)
                        units.append(rebelMilita)

                    if time > mytheSupport:
                        HazelV = Unit(self.x, self.y, self.x, self.y,'Xetta Trained Regulars', 'Border' ,'Mythe', 1, 100, 1, 80, 120, 120, 700, 1, 'Roam', False,False, 0, 0, 0, 500,False)
                        units.append(HazelV)
                        
                        XettaV = Unit(self.x, self.y, self.x, self.y,'Haax Jet', 'Aircraft' ,'Mythe', 1, 30, 1, 150, 80, 100, 500, 1, 'Roam', False,False, 0, 0, 0, 700,False)
                        units.append(XettaV)


                
                if unitChance > 25 and MytheMoney >= 1:
                    MytheMoney = MytheMoney - 1
                    
                    for i in range(3):
                        rebelMilita = Unit(self.x, self.y, self.x, self.y,'Mythe Raiding Party', 'Aircraft' ,'Mythe', 1, 30, 1, 20, 1, 60, 400, 1, 'Roam', False,False, 0,0,0,100,False)
                        units.append(rebelMilita)
                  
                    
                   
         
                    
                
        #print('Test')
                
                
        

            

#player = Player(400, 300, 32, 32,0,0,0,0)

myFont = pygame.font.SysFont("Times New Roman", 18)

for t in range(mapSize):
    
    newTile = Tile(gX, gY, 20, 20, 10,1,[], False, False,False,False)
    gX += 25
    if gX > 1000:
        #print('Last X' + str(gX))
        gX = 100
        gY += 25
    mapList.append(newTile)


for t in mapList:

    
    
    for t2 in mapList:

        if t.Marsh == True and t.x > t2.x - 120 and t.x < t2.x + 120 and t.y > t2.y - 120 and t.y < t2.y + 120:
            sChance =  random.randint(1,27)
            if sChance == 1:
                t2.Marsh = True

        if t.mountain == True and t.x > t2.x - 50 and t.x < t2.x + 50 and t.y > t2.y - 50 and t.y < t2.y + 50:
            sChance =  random.randint(1,5)
            if sChance == 1:
                t2.mountain = True

        if t.river == True and t.x > t2.x - 20 and t.x < t2.x + 20 and t.y > t2.y - 80 and t.y < t2.y + 80 and t.y != t2.y:
            sChance =  random.randint(1,2)
            if sChance == 1 and t2.population <20:
                t2.river = True
                
        if t.population == 20 and t.x > t2.x - 50 and t.x < t2.x + 50 and t.y > t2.y - 50 and t.y < t2.y + 50:
            sChance =  random.randint(1,6)
            if sChance == 1:
                t2.population = 20
        
        
    

paused = False

tileHist= {}

while True:
    HazelMLabel = myFont.render("Hazel Money:" + str(HazelMoney), 1, (255,255,255))
    MytheMLabel = myFont.render("Mythe Money:" + str(MytheMoney), 1, (255,255,255))

    HazelCLabel = myFont.render("Hazel Losses:" + str(northCas), 1, (255,255,255))
    MytheCLabel = myFont.render("Mythe Losses:" + str(southCas), 1, (255,255,255))

    print ('Mythe Unclock Time ' + str(mytheSupport))
    print ('Hazel Unclock Time ' + str(hazelSupport))

    print ('Time ' + str(time))
    
    mx, my = pygame.mouse.get_pos()
    #print(str(mx))
    
    unitsInTile = []
    if takeTurn == True and  paused == False:
   
        for unit in units:
            unit.takeTurn()
            

        ci = 0
        xT = 0
        bT = 0
        for tile in mapList:
            ci = ci+1
            if tile.control < 7:
                
                bT = bT + 1
            else:
                xT = xT + 1
            tileHist[ci] = [bT,xT]
            tile.takeTurn()

        #print (tileHist)
        time = time+1
        mudTimer = mudTimer - random.randint(1,2)
        print (mudTimer)
        if mudTimer < 0:
            mudTimer = 2000
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
        if unit.faction == 'Hazel':
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
        MytheMoney = MytheMoney + 1

    if keys[pygame.K_d]:
        HazelMoney = HazelMoney + 1

    if keys[pygame.K_p]:
        if paused == False:
            paused = True
            print (paused)
        else:
            paused = False

        #print(time)
  
    #player.main(display)
    display.blit(HazelMLabel, (20, 20))
    display.blit(MytheMLabel, (20, 40))
    display.blit(HazelCLabel, (20, 710))
    display.blit(MytheCLabel, (20, 730))
    
    if mudTimer < 1000:
        print ('MUD')
        mudL = myFont.render("MUD SEASON" , 1, (255,255,255))
        display.blit(mudL, (20, 750))
    clock.tick(60)

    pygame.display.update()
   
