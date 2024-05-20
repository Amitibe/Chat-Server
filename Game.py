"""שלום חנן, למרות שכן כתבתי את הקוד הזה הוא לא באמת היה בתיכנון של הפקוייקט אז לא כתבתי מה כל פונקציה עושה. בכל מקרה זה לא החלק העיקרי של הקוד"""


import os
os.system("pip install pygame")
import random
import pygame
from sys import exit
from random import randint

class Player(pygame.sprite.Sprite):
    def __init__(self, date):
        super().__init__()
        print(date)
        player_walk1 = pygame.image.load('Graphics/player_walk_1.png').convert_alpha()
        player_walk2 = pygame.image.load('Graphics/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk1, player_walk2]
        self.player_index = 0
        self.player_Jump = pygame.image.load('Graphics/jump.png').convert_alpha()
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (200,300))
        self.grav = 0

    def animation_state(self):
        if self.rect.bottom<300:
            self.image = self.player_Jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(player_walk): self.player_index= 0
            self.image = self.player_walk[int(self.player_index)]

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >=300:
            self.grav -= 20

    def apply_grav(self):
        self.grav +=1
        self.rect.y += self.grav
        if self.rect.bottom >=300:
            self.rect.bottom =300
            self.grav = 0


    def update(self):
        self.player_input()
        self.apply_grav()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        if type == "fly":
            fly_1 = pygame.image.load('Graphics/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load('Graphics/Fly2.png').convert_alpha()
            self.frames = [fly_1,fly_2]
            y_pos =210
        else:
            snail_1 = pygame.image.load('Graphics/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('Graphics/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(random.randint(900,1100),y_pos))

def display_score(Text):
    current_time = (pygame.time.get_ticks() - start_time)/1000
    score_surf = font.render(("Time: "+ str(int(current_time))),False,(64,64,64))
    score_rect = score_surf.get_rect(center = (400,100))
    screen.blit(score_surf,score_rect)
    score = font.render("Score   "+Text, False, "Black")
    score_rect = score.get_rect(center = (400,50))
    screen.blit(score, score_rect)
    return current_time

def display_start_text():
    name = font.render("Alian Runner", False, (111,196,169))
    name_rect = name.get_rect(center = (400,25))
    instruction_text = font.render("press space to start", False, (111,196,169))
    instruction_text_rect = name.get_rect(center=(350, 350))
    screen.blit(instruction_text,instruction_text_rect)
    screen.blit(name,name_rect)

def obstacle_movement(list):
    newlist = []
    counter = 0
    if list:
        for obstacle in list:
            obstacle.x -=5
            if obstacle.bottom == 300:
                screen.blit(snail,obstacle)
            else:
                screen.blit(fly,obstacle)
            if obstacle.x >-100:
                newlist.append(obstacle)
            else:
                counter +=1

        return newlist, counter
    return [], 0

def collsions(player, obstacles):
    if obstacles:
        for obstacle in obstacles:
            if player.colliderect(obstacle):
                return False
    return True

def player_animation():
    #play walking animation if on floor
    global player_index, player_surf
    if player_rect.bottom<300:
        player_surf = player_Jump
    else:
        player_index +=0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]



pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
font = pygame.font.Font('Graphics/Pixeltype.ttf',50)
snailStartPos = 600
gameActive = False
start_time = 0
score = 0

player = pygame.sprite.GroupSingle()
player.add(Player(2222))

obstacle_group = pygame.sprite.Group()


Sky = pygame.image.load('Graphics/Sky.png').convert()
Ground = pygame.image.load('Graphics/Ground.png.').convert()

#Obstacles
snail_frame1 = pygame.image.load('Graphics/snail1.png').convert_alpha()
snail_frame2 = pygame.image.load('Graphics/snail2.png').convert_alpha()
snail_frames = [snail_frame1,snail_frame2]
snail_index = 0
fly_frame1 = pygame.image.load('Graphics/Fly1.png').convert_alpha()
fly_frame2 = pygame.image.load('Graphics/Fly2.png').convert_alpha()
fly_frames = [fly_frame1,fly_frame2]
fly_index = 0
snail = snail_frames[snail_index]
fly = fly_frames[fly_index]

obstacle_rect_list = []

player_walk1 = pygame.image.load('Graphics/player_walk_1.png').convert_alpha()
player_walk2 = pygame.image.load('Graphics/player_walk_2.png').convert_alpha()
player_walk = [player_walk1,player_walk2]
player_index = 0
player_Jump = pygame.image.load('Graphics/jump.png').convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80, 300))
player_stand = pygame.image.load('Graphics/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))


#Veriables
player_grav = 0
TimesSnailPass = 0
doubleJump = True
countJ = 0
SnailV =0

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

snail_animation_timer = pygame.USEREVENT +2
pygame.time.set_timer(snail_animation_timer,500)

fly_animation_timer = pygame.USEREVENT +3
pygame.time.set_timer(fly_animation_timer,300)





while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if gameActive:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) :
                    player_grav = -20

            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_SPACE and player_rect.bottom == 300) or (event.key == pygame.K_SPACE and doubleJump):
                    player_grav = -20
                    countJ +=1
                    if countJ >=2:
                        doubleJump = False
        else:
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE):
                gameActive = True
                #SnailV =0
                TimesSnailPass =0
                start_time = pygame.time.get_ticks()
                obstacle_rect_list.clear()
                player_rect.midbottom = (80,300)
                player_grav =0
        if gameActive:
            if event.type == obstacle_timer and gameActive:
                if randint(0,2):
                    obstacle_rect_list.append(snail.get_rect(bottomright = (randint(900,1100),300)))
                else:
                    obstacle_rect_list.append(fly.get_rect(bottomright = (randint(900,1100),randint(100,300))))
            if event.type == snail_animation_timer:
                if snail_index == 0:
                    snail_index = 1
                else:
                    snail_index = 0
                snail = snail_frames[snail_index]
            if event.type == fly_animation_timer:
                if fly_index ==1:
                    fly_index =0
                else:
                    fly_index =1
                fly = fly_frames[fly_index]

    if gameActive:

        screen.blit(Sky,(0,0))
        screen.blit(Ground,(0,300))
        score = display_score(str(TimesSnailPass))

        player_grav += 1
        player_rect.y += player_grav
        if player_rect.bottom >=300:
            player_grav = 0
            player_rect.bottom = 300
            doubleJump = True
            countJ = 0
        player_animation()
        screen.blit(player_surf, player_rect)

        player.update()
        obstacle_group.draw(screen)

        #obsticles
        obstacle_rect_list, t  = obstacle_movement(obstacle_rect_list)
        TimesSnailPass +=t

        #Collisions
        gameActive = collsions(player_rect, obstacle_rect_list)


    else:
        screen.fill("Blue")
        screen.blit(player_stand,player_stand_rect)
        if score !=0:
            score_message = font.render(f'Your Time: {int(score)} seconds',False,(111,196,169))
            score_message_rect = score_message.get_rect(center = (400,350))
            screen.blit(score_message,score_message_rect)
        else:
            display_start_text()
    pygame.display.update()
    clock.tick(60)