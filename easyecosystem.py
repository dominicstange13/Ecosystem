import pygame
import random
import time
import math

#Setup
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1600,800))
pygame.display.set_caption('Python Ecosystem')
pygame.font.init()
displayfont = pygame.font.SysFont('Consolas',20)
currenttime = pygame.time.get_ticks()
backgroundcolor = pygame.Color(52,99,38)

#Herbivore
herbivore = pygame.rect.Rect(350,150,50,50)
herbivore_pos = pygame.math.Vector2(herbivore.x,herbivore.y)
herbivorealive = True
herbivoreidle1 = pygame.image.load('assets/herbivore/hidle1.png').convert_alpha()
herbivoreidle2 = pygame.image.load('assets/herbivore/hidle2.png').convert_alpha()
fherbivoreidle1 = pygame.transform.flip(herbivoreidle1, True, False).convert_alpha()
fherbivoreidle2 = pygame.transform.flip(herbivoreidle2, True, False).convert_alpha()
herbivorerun1 = pygame.image.load('assets/herbivore/hrun1.png').convert_alpha()
herbivorerun2 = pygame.image.load('assets/herbivore/hrun2.png').convert_alpha()
fherbivorerun1 = pygame.transform.flip(herbivorerun1, True, False).convert_alpha()
fherbivorerun2 = pygame.transform.flip(herbivorerun2, True, False).convert_alpha()
herbivorewalk1 = pygame.image.load('assets/herbivore/hwalk1.png').convert_alpha()
herbivorewalk2 = pygame.image.load('assets/herbivore/hwalk2.png').convert_alpha()
fherbivorewalk1 = pygame.transform.flip(herbivorewalk1, True, False).convert_alpha()
fherbivorewalk2 = pygame.transform.flip(herbivorewalk2, True, False).convert_alpha()
hidleframes = [herbivoreidle1, herbivoreidle2]
fhidleframes = [fherbivoreidle1, fherbivoreidle2]
hwalkframes = [herbivorewalk1, herbivorewalk2]
fhwalkframes = [fherbivorewalk1, fherbivorewalk2]
hrunframes = [herbivorerun1, herbivorerun2]
fhrunframes = [fherbivorerun1, fherbivorerun2]
herbivorelastx = herbivore.x
hidleframeindex = 0
hwalkframeindex = 0
hrunframeindex = 0
herbivoreflipped = False

#Carnivore
carnivore = pygame.rect.Rect(0,730,70,70)
carnivore_pos = pygame.math.Vector2(carnivore.x,carnivore.y)
carnivorealive = True
carnivorestalk1 = pygame.image.load('assets/carnivore/cstalk1.png').convert_alpha()
carnivorestalk2 = pygame.image.load('assets/carnivore/cstalk2.png').convert_alpha()
fcarnivorestalk1 = pygame.transform.flip(carnivorestalk1, True, False).convert_alpha()
fcarnivorestalk2 = pygame.transform.flip(carnivorestalk2, True, False).convert_alpha()
carnivorechase1 = pygame.image.load('assets/carnivore/cchase1.png').convert_alpha()
carnivorechase2 = pygame.image.load('assets/carnivore/cchase2.png').convert_alpha()
fcarnivorechase1 = pygame.transform.flip(carnivorechase1, True, False).convert_alpha()
fcarnivorechase2 = pygame.transform.flip(carnivorechase2, True, False).convert_alpha()
cstalkframes = [carnivorestalk1, carnivorestalk2]
fcstalkframes = [fcarnivorestalk1, fcarnivorestalk2]
cchaseframes = [carnivorechase1, carnivorechase2]
fcchaseframes = [fcarnivorechase1, fcarnivorechase2]
carnivorelastx = carnivore.x
cstalkframeindex = 0
cchaseframeindex = 0
carnivoreflipped = False

#Herbivore variables for hunger and thirst
herbivorefood = 5
herbivorefoodtext = f"Herbivore Food: {str(herbivorefood)}"
herbivorefooddisplay = displayfont.render(herbivorefoodtext, False, 'green')
herbivoregivenhunger = False
herbivorewater = 5
herbivorewatertext = f"Herbivore Water: {str(herbivorewater)}"
herbivorewaterdisplay = displayfont.render(herbivorewatertext, False, 'green')

#Carnivore variables for hunger and thirst
carnivorefood = 7
carnivorefoodtext = f"Carnivore Food: {str(carnivorefood)}"
carnivorefooddisplay = displayfont.render(carnivorefoodtext, False, 'crimson')
carnivoregivenhunger = False
carnivorewater = 7
carnivorewatertext = f"Carnivore Water: {str(carnivorewater)}"
carnivorewaterdisplay = displayfont.render(carnivorewatertext, False, 'crimson')

#End of game texts
deathtext = ""
deathtextdisplay = displayfont.render(deathtext, False, 'red')
deathdisplaytime = 3000
whendisplayshown = 0

#Plant variables
plant = pygame.rect.Rect(1250,150,50,50)
plantimg = pygame.image.load('assets/plant.png')
newplant = pygame.rect.Rect(random.randint(0,1550), random.randint(0,750),50,50)
plant_pos = pygame.math.Vector2(plant.x,plant.y)
newplant_pos = pygame.math.Vector2(newplant.x,newplant.y)
plant_posses = []
plants = []
plantdist = 0
currentplant = 0
plantindex = 0
plantposindex = 1
loopcheckcd = 5000
nextloopcheck = 0
currenttime = 0
currentplantlen = 0
appendposses = False
deletedplant = False

#Herbivore movement variables
herbivoredirection = herbivore_pos - plant_pos
herbivorespeed = 6.5
herbivorecurrentdist = herbivore_pos.distance_to(plant_pos)
herbivoredists = []
herbivoredistanceindex = 0
herbivoreswitchedpos = False
herbivoretppoint = pygame.math.Vector2(0,0)

#Carnivore movement variables
carnivoredirection = carnivore_pos - herbivore_pos
carnivorespeed = 1.5
carnivorecurrentdist = carnivore_pos.distance_to(herbivore_pos)
carnivorechasing = False
chasetppoint = False
chasecountdown = 1750
chasetime = 0
setchasetime = False
chasecd = 4000
lastchase = 0

#Water variables
water = pygame.rect.Rect(random.randint(0,1500),random.randint(100,700), 100,100)
waterimg = pygame.image.load('assets/water.png')
water_pos = pygame.math.Vector2(water.x,water.y)
herbivoregrabbingwater = False

#Game events + timers
SPAWNPLANT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWNPLANT, 1500)
SUBTRACTHERBIVOREHUNGER = pygame.USEREVENT + 2
pygame.time.set_timer(SUBTRACTHERBIVOREHUNGER, 1750)
SUBTRACTHERBIVORETHIRST = pygame.USEREVENT + 3
pygame.time.set_timer(SUBTRACTHERBIVORETHIRST, 7000)
SUBTRACTCARNIVOREHUNGER = pygame.USEREVENT + 4
pygame.time.set_timer(SUBTRACTCARNIVOREHUNGER, 6000)
SUBTRACTCARNIVORETHIRST = pygame.USEREVENT + 5
pygame.time.set_timer(SUBTRACTCARNIVORETHIRST, 8000)

#Append first plant + track it (so lists aren't empty)
running = True
herbivoreeat = False
plants.append(plant)
plant_posses.append(pygame.math.Vector2((plants[0].x),(plants[0].y)))
herbivoredists.append(herbivore_pos.distance_to(plant_posses[0]))
currentplant = herbivoredists.index(min(herbivoredists))
herbivorecurrentdist = herbivoredists[0]

#Game loop
while running:
    screen.fill(backgroundcolor)
    plantcollision = herbivore.collideobjects(plants)
    currenttime = pygame.time.get_ticks()
    herbivorelastx = herbivore.x
    carnivorelastx = carnivore.x
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == SPAWNPLANT:
            newplant = pygame.rect.Rect(random.randint(0,1550), random.randint(0,750),50,50)
            newplant_pos = pygame.math.Vector2(newplant.x,newplant.y)
            for p in plant_posses:
                plantdist = newplant_pos.distance_to(p)
                if plantdist <= 500 or newplant.colliderect(water):
                    newplant = pygame.rect.Rect(random.randint(0,1550), random.randint(0,750),50,50)
                    newplant_pos = pygame.math.Vector2(newplant.x,newplant.y)
            plants.append(newplant)
            plant_posses.append(newplant_pos)
            appendposses = True
        if event.type == SUBTRACTHERBIVOREHUNGER:
            herbivorefood -= 1
            herbivorefoodtext = f"Herbivore Food: {str(herbivorefood)}"
            herbivorefooddisplay = displayfont.render(herbivorefoodtext, False, 'green')
        if event.type == SUBTRACTHERBIVORETHIRST:
            herbivorewater -= 2
            herbivorewatertext = f"Herbivore Water: {str(herbivorewater)}"
            herbivorewaterdisplay = displayfont.render(herbivorewatertext, False, 'green')
            screen.blit(herbivorefooddisplay, (0,0))
        if event.type == SUBTRACTCARNIVOREHUNGER:
            carnivorefood -= 1
            carnivorefoodtext = f"Carnivore Food: {str(carnivorefood)}"
            carnivorefooddisplay = displayfont.render(carnivorefoodtext, False, 'crimson')
        if event.type == SUBTRACTCARNIVORETHIRST:
            carnivorewater -= 1
            carnivorewatertext = f"Carnivore Water: {str(carnivorewater)}"
            carnivorewaterdisplay = displayfont.render(carnivorewatertext, False, 'crimson')
    herbivorefoodtext = f"Herbivore Food: {str(herbivorefood)}"
    herbivorewatertext = f"Herbivore Water: {str(herbivorewater)}"
    if herbivore.x >= 1700 or herbivore.y >= 900 or herbivore.x <= -150 or herbivore.y <= -150:
        if carnivorechasing:
            herbivoretppoint = pygame.math.Vector2(herbivore.x,herbivore.y)
            chasetppoint = True
        herbivore_pos = pygame.math.Vector2(800,400)
        herbivore.center = herbivore_pos
        herbivoredists.clear()
        for posses in plant_posses:
            herbivoredists.append(herbivore_pos.distance_to(posses))
    if carnivore.x >= 1700 or carnivore.y >= 900 or carnivore.x <= -150 or carnivore.y <= -150 or carnivore.collidepoint(herbivoretppoint):
        carnivore_pos = pygame.math.Vector2(800,400)
        carnivore.center = carnivore_pos
        chasetppoint = False
    if herbivoreeat == False:
        if herbivoredirection != pygame.math.Vector2(0,0):
            herbivoredirection = herbivoredirection.normalize()
        if plantcollision == None and not carnivorechasing:
            herbivoregivenhunger = False
            herbivoregiventhirst = False
            herbivoredists.clear()
            for posses in plant_posses:
                herbivoredists.append(herbivore_pos.distance_to(posses))
            if len(plants) > 1:
                herbivore_pos -= herbivoredirection * herbivorespeed
                herbivore.center = herbivore_pos
            else:
                if carnivorechasing:
                    herbivorecurrentdist = herbivore_pos.distance_to(carnivore_pos)
                    herbivoredirection = herbivore_pos - carnivore_pos
                    if herbivoredirection != pygame.math.Vector2(0,0):
                        herbivoredirection = herbivoredirection.normalize()
                    herbivore_pos += herbivoredirection * herbivorespeed
                else:
                    herbivoredists.clear()
                    for posses in plant_posses:
                        herbivoredists.append(herbivore_pos.distance_to(posses))
                    currentplant = herbivoredists.index(min(herbivoredists))
                    herbivorecurrentdist = min(herbivoredists)
                    herbivoredirection = herbivore_pos - plant_posses[currentplant]
                    herbivoredirection = herbivoredirection.normalize()
            herbivore.center = herbivore_pos
        elif plantcollision is not None and not carnivorechasing:
            if herbivorewater > 3:
                herbivoreeat = True
                plantposindex -= 1
                del plants[currentplant]
                del plant_posses[currentplant]
                herbivoredists.clear()
                for posses in plant_posses:
                    herbivoredists.append(herbivore_pos.distance_to(posses))
                currentplant = herbivoredists.index(min(herbivoredists))
                herbivoredirection = herbivore_pos - plant_posses[currentplant]
                herbivoredirection = herbivoredirection.normalize()
            else:
                herbivoredists.clear()
                herbivoredistanceindex = 0
                for posses in plant_posses:
                    herbivoredists.append(herbivore_pos.distance_to(posses))
                currentplant = herbivoredists.index(min(herbivoredists))
                herbivorecurrentdist = min(herbivoredists)
                herbivoredirection = herbivoredirection.normalize()
            if not herbivoregivenhunger:
                herbivorefood += 1
                herbivoregivenhunger = True
            herbivorefoodtext = f"Herbivore Food: {str(herbivorefood)}"
            herbivorefooddisplay = displayfont.render(herbivorefoodtext, False, 'green')
            herbivoredists.clear()
            herbivoredistanceindex = 0
            herbivoreeat = False
            if herbivorewater <= 3:
                del plants[currentplant]
                del plant_posses[currentplant]
                herbivoredirection = herbivore_pos - water_pos
                herbivoregrabbingwater = True
            else:
                herbivoredirection = herbivore_pos - plant_posses[currentplant]
            herbivoredirection = herbivoredirection.normalize()
        if carnivorechasing:
            herbivorespeed = 7.5
            herbivoregrabbingwater = False
            herbivorecurrentdist = herbivore_pos.distance_to(carnivore_pos)
            herbivoredirection = herbivore_pos - carnivore_pos
            if herbivoredirection != pygame.math.Vector2(0,0):
                herbivoredirection = herbivoredirection.normalize()
            herbivore_pos += herbivoredirection * herbivorespeed
            herbivore.center = herbivore_pos
            if not carnivorechasing:
                herbivoredists.clear()
                herbivoredistanceindex = 0
                for posses in plant_posses:
                    herbivoredists.append(herbivore_pos.distance_to(posses))
                currentplant = herbivoredists.index(min(herbivoredists))
                herbivoredirection = herbivore_pos - plant_posses[currentplant]
                herbivoredirection = herbivoredirection.normalize()
        if not carnivorechasing:
                herbivorespeed = 6.5
                if herbivorewater <= 3:
                    herbivoredirection = herbivore_pos - water_pos
                    herbivoregrabbingwater = True
                else:
                    herbivoredists.clear()
                    herbivoredistanceindex = 0
                    for posses in plant_posses:
                        herbivoredists.append(herbivore_pos.distance_to(posses))
                    currentplant = herbivoredists.index(min(herbivoredists))
                    herbivoredirection = herbivore_pos - plant_posses[currentplant]
                    if not herbivore_pos == plant_posses[currentplant]:
                        herbivoredirection = herbivoredirection.normalize()
    if herbivore.colliderect(water) and herbivoregrabbingwater:
        if not herbivoregiventhirst:
            herbivorewater += 2
            herbivoregiventhirst = True
            herbivoredists.clear()
            herbivoredistanceindex = 0
            for posses in plant_posses:
                herbivoredists.append(herbivore_pos.distance_to(posses))
            currentplant = herbivoredists.index(min(herbivoredists))
            herbivoredirection = herbivore_pos - plant_posses[currentplant]
            herbivoredirection = herbivoredirection.normalize()
            herbivore_pos -= herbivoredirection * herbivorespeed
            herbivore.center = herbivore_pos
            herbivorecurrentdist = min(herbivoredists)
            herbivoregrabbingwater = False
    if carnivorewater > 5 and not carnivorechasing:
        carnivoregiventhirst = False
        carnivorespeed = 1.5
        carnivoredirection = carnivore_pos - herbivore_pos
        carnivoredirection = carnivoredirection.normalize()
        carnivore_pos -= carnivoredirection * carnivorespeed
        carnivore.center = carnivore_pos
        carnivorecurrentdist = carnivore_pos.distance_to(herbivore_pos)
        chasedist = random.randint(300,400)
        if carnivorecurrentdist <= chasedist and currenttime - lastchase >= chasecd:
            chasetppoint = False
            carnivorechasing = True
        carnivorecurrentdist = carnivore_pos.distance_to(herbivore_pos)
    elif carnivorewater <= 5 and not carnivoregiventhirst and not carnivorechasing:
        carnivorespeed = 3
        carnivoredirection = carnivore_pos - water_pos
        carnivoredirection = carnivoredirection.normalize()
        carnivore_pos -= carnivoredirection * carnivorespeed
        carnivore.center = carnivore_pos
        carnivorecurrentdist = carnivore_pos.distance_to(water_pos)
        if carnivore.colliderect(water):
            carnivorewater += 2
            carnivoregiventhirst = True
    elif carnivorechasing:
        if setchasetime == False:
            chasetime = currenttime
            setchasetime = True
        carnivorespeed = 9
        if not chasetppoint:
            carnivoredirection = carnivore_pos - herbivore_pos
        else:
            carnivoredirection = carnivore_pos - herbivoretppoint
        if not carnivore.collidepoint(herbivoretppoint) or carnivore.colliderect(herbivore):
            if carnivoredirection != pygame.math.Vector2(0,0):
                carnivoredirection = carnivoredirection.normalize()
        carnivore_pos -= carnivoredirection * carnivorespeed
        carnivore.center = carnivore_pos
        carnivorecurrentdist = carnivore_pos.distance_to(herbivore_pos)
        if currenttime - chasetime >= chasecountdown:
            carnivorespeed = 1.5
            carnivorechasing = False
            setchasetime = False
            carnivoregivenhunger = False
            lastchase = currenttime
    if carnivore.colliderect(herbivore) and carnivorechasing:
        if not carnivoregivenhunger:
            carnivorefood += 3
            carnivoregivenhunger = True
        carnivorechasing = False
        lastchase = currenttime
        if carnivore.colliderect(herbivore):
            carnivore.x -= 500
            carnivore_pos = pygame.math.Vector2(carnivore.x,carnivore.y)
        whendisplayshown = currenttime
        deathtext = "Herbivore was eaten by carnivore"
        carnivorefoodtext = f"Carnivore Food: {str(carnivorefood)}"
        carnivorefooddisplay = displayfont.render(carnivorefoodtext, False, 'crimson')
        herbivorefooddisplay = displayfont.render(herbivorefoodtext, False, 'green')
        herbivorewaterdisplay = displayfont.render(herbivorewatertext, False, 'green')
        herbivorefood = 5
        herbivorewater = 5
        herbivore.center = (800,400)
        herbivore_pos = pygame.math.Vector2(herbivore.x,herbivore.y)
        chasetppoint = False
    elif herbivorefood <= 0:
        whendisplayshown = currenttime
        deathtext = "Herbivore starved to death"
        herbivorefood = 5
        herbivorewater = 5
        herbivorefooddisplay = displayfont.render(herbivorefoodtext, False, 'green')
        herbivore.center = (800,400)
        herbivore_pos = pygame.math.Vector2(herbivore.x,herbivore.y)
        carnivorechasing = False
        chasetppoint = False
    elif herbivorewater <= 0:
        whendisplayshown = currenttime
        deathtext = "Herbivore died of thirst"
        herbivorefood = 5
        herbivorewater = 5
        herbivorewaterdisplay = displayfont.render(herbivorewatertext, False, 'green')
        herbivore.center = (800,400)
        herbivore_pos = pygame.math.Vector2(herbivore.x,herbivore.y)
        carnivorechasing = False
        chasetppoint = False
    elif carnivorefood <= 0:
        whendisplayshown = currenttime
        deathtext = "Carnivore starved to death"
        carnivorefood = 7
        carnivorewater = 7
        carnivorefooddisplay = displayfont.render(carnivorefoodtext, False, 'crimson')
        carnivore.topleft = (0,730)
        carnivore_pos = pygame.math.Vector2(carnivore.x,carnivore.y)
        carnivorechasing = False
        chasetppoint = False
    elif carnivorewater <= 0:
        whendisplayshown = currenttime
        deathtext = "Carnivore died of thirst"
        carnivorefood = 7
        carnivorewater = 7
        carnivorewaterdisplay = displayfont.render(carnivorewatertext, False, 'crimson')
        carnivore.topleft = (0,730)
        carnivore_pos = pygame.math.Vector2(carnivore.x,carnivore.y)
        carnivorechasing = False
        chasetppoint = False
    if currenttime - whendisplayshown >= deathdisplaytime:
        showingdeathtext = False
    else:
        showingdeathtext = True
    herbivorewatertext = f"Herbivore Water: {str(herbivorewater)}"
    herbivorewaterdisplay = displayfont.render(herbivorewatertext, False, 'green')
    carnivorewatertext = f"Carnivore Water: {str(carnivorewater)}"
    carnivorewaterdisplay = displayfont.render(carnivorewatertext, False, 'crimson')
    screen.blit(waterimg, (water.x-50,water.y-60))
    for plant_rect in plants:
        screen.blit(plantimg, (plant_rect.x-20,plant_rect.y-20))
    if len(plants) <= 1 and not carnivorechasing:
        hidleframeindex += 0.1
        cstalkframeindex += 0.1
        if hidleframeindex >= len(hidleframes):
            hidleframeindex = 0
        if cstalkframeindex >= len(cstalkframes):
            cstalkframeindex = 0
        if herbivoreflipped == False:
            screen.blit(hidleframes[int(hidleframeindex)], (herbivore.x-20,herbivore.y-20))
        else:
            screen.blit(fhidleframes[int(hidleframeindex)], (herbivore.x-20,herbivore.y-20))
        if carnivoreflipped == False:
            screen.blit(cstalkframes[int(cstalkframeindex)], (carnivore.x-50,carnivore.y-50))
        else:
            screen.blit(fcstalkframes[int(cstalkframeindex)], (carnivore.x-50,carnivore.y-50))
    elif len(plants) > 1 and not carnivorechasing:
        cstalkframeindex += 0.1
        hwalkframeindex += 0.1
        if cstalkframeindex >= len(cstalkframes):
            cstalkframeindex = 0
        if hwalkframeindex >= len(hwalkframes):
            hwalkframeindex = 0
        if herbivoreflipped == False:
            screen.blit(hwalkframes[int(hwalkframeindex)], (herbivore.x-20,herbivore.y-20))
        else:
            screen.blit(fhwalkframes[int(hwalkframeindex)], (herbivore.x-20,herbivore.y-20))
        if carnivoreflipped == False:
            screen.blit(cstalkframes[int(cstalkframeindex)], (carnivore.x-50,carnivore.y-50))
        else:
            screen.blit(fcstalkframes[int(cstalkframeindex)], (carnivore.x-50,carnivore.y-50))
    elif carnivorechasing:
        hrunframeindex += 0.1
        cchaseframeindex += 0.1
        if hrunframeindex >= len(hrunframes):
            hrunframeindex = 0
        if herbivoreflipped == False:
            screen.blit(hrunframes[int(hrunframeindex)], (herbivore.x-20,herbivore.y-20))
        else:
            screen.blit(fhrunframes[int(hrunframeindex)], (herbivore.x-20,herbivore.y-20))
        if cchaseframeindex >= len(cchaseframes):
            cchaseframeindex = 0
        if carnivoreflipped == False:
            screen.blit(cchaseframes[int(cchaseframeindex)], (carnivore.x-50,carnivore.y-50))
        else:
            screen.blit(fcchaseframes[int(cchaseframeindex)], (carnivore.x-50,carnivore.y-50))
    if showingdeathtext:
        deathtextdisplay = displayfont.render(deathtext, False, 'red')
        screen.blit(deathtextdisplay, (700,760))
    screen.blit(herbivorefooddisplay, (0,0))
    screen.blit(herbivorewaterdisplay, (0,20))
    screen.blit(carnivorefooddisplay, (0,40))
    screen.blit(carnivorewaterdisplay, (0,60))
    if herbivore.x - herbivorelastx != 0:
        if herbivore.x - herbivorelastx < 0:
            herbivoreflipped = True
        else:
            herbivoreflipped = False
    if carnivore.x - carnivorelastx != 0:
        if carnivore.x - carnivorelastx < 0:
            carnivoreflipped = True
        else:
            carnivoreflipped = False
    if herbivoredirection != pygame.math.Vector2(0,0):
        herbivoredirection.normalize()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()