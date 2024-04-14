import pygame
from sys import exit
import random
import math
import time



class Player(pygame.sprite.Sprite):
    def __init__(self,pos,group):
        super().__init__(group)
        self.image = pygame.Surface((50,50))
        self.image.fill('White')
        self.rect = self.image.get_rect(center = pos)
        self.direction = pygame.math.Vector2()
        self.speed = 4
        self.gravity = 0
    
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.gravity = -3
            self.direction.y = -2
        elif keys[pygame.K_s]:
            self.gravity = 5
            self.direction.y = 2
        else:
            self.direction.y = 0

        if keys[pygame.K_a]:
            self.direction.x = -2
        elif keys[pygame.K_d]:
            self.direction.x = 2
        else:
            self.direction.x = 0

    def apply_gravity(self):
        if self.rect.colliderect(camera_group.ground_rect):
            self.rect.bottom = camera_group.ground_rect.top
        if self.rect.colliderect(camera_group.top_rect):
            self.rect.top = camera_group.top_rect.bottom
    
    def update(self):
        self.input()
        self.apply_gravity()
        self.rect.center += self.direction * self.speed

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        image = pygame.Surface((20, 20))  # You can replace this with your enemy image
        image.fill('red')  # Red color, you can replace this with your enemy image
        self.image = image
        self.rect = self.image.get_rect(topleft=(pos[0]+player.rect.centerx,pos[1]))
        self.speed = 10
    
    def movement(self,target):
        dx = target[0] - self.rect.centerx
        dy = target[1] - self.rect.centery
        distance = math.sqrt(dx**2 + dy**2)

        if distance>self.speed:
            self.rect.centerx +=dx / distance*self.speed
            self.rect.centery +=dy / distance*self.speed

    def destroy(self,enemy):
        for i in enemy:
            if i!=self and self.rect.colliderect(i.rect):
                i.kill()
                enemy.remove(i)



class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        self.offset = pygame.math.Vector2()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2
        self.ground_surf = pygame.Surface((50000000,10))
        self.hori_surf = pygame.Surface((100,10))
        self.hori_surf.fill('violet')
        self.ground_surf.fill('Purple')
        self.ground_rect = self.ground_surf.get_rect(topleft = (-100000,600))
        self.top_surf = self.ground_surf
        self.top_rect = self.top_surf.get_rect(topleft = (-100000,150))

    def center_target_camera(self,target):
        if target.rect.centerx >200 or target.rect.centerx < 750:
            self.offset.x = target.rect.centerx - self.half_w
        else:
            self.offset.x = 0

    def custom_draw(self,player):
        
        self.center_target_camera(player)
        ground_offset = self.ground_rect.topleft - self.offset
        top_offset = self.top_rect.topleft - self.offset
        self.display_surface.blit(self.ground_surf,ground_offset)
        self.display_surface.blit(self.top_surf,top_offset)
        for i in range(-100000,400000,200):
            self.hori_rect = self.hori_surf.get_rect(topleft = (i,650))
            hori_offset = self.hori_rect.topleft - self.offset
            self.display_surface.blit(self.hori_surf,hori_offset)

        tutorial_surf = mainfont.render('WASD to move...',False,'Orange')
        gl = sidefont.render('Good luck',False,'white')
        tutorial_rect = tutorial_surf.get_rect(topleft = (200 -camera_group.offset.x, 200-camera_group.offset.y))
        gl_rect = gl.get_rect(topleft=(200 -camera_group.offset.x, 300-camera_group.offset.y))
        if(count<300):
            self.display_surface.blit(tutorial_surf,tutorial_rect)
            self.display_surface.blit(gl,gl_rect)
        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)

def gamecheck(player,enemy):
    if enemy:
        for i in enemy:
            if player.rect.colliderect(i): 
                return False
    return True

def display_score():
    global score
    score = int(pygame.time.get_ticks()/1000) - start_time
    score_surf = sidefont.render(f'Score: {score}',False,(255,255,255))
    score_rect = score_surf.get_rect(center = (1150,100))
    screen.blit(score_surf,score_rect)

pygame.init()
screen= pygame.display.set_mode((1280,720))
pygame.display.set_caption("Purple & Red")
clock= pygame.time.Clock()
interval = 5
qf = 1.5
last_trigger_time = time.time()
camera_group = CameraGroup()
player = Player((640,400),camera_group)
enemy=[]
mainfont = pygame.font.Font('graphics/minecraft.ttf',60)
sidefont = pygame.font.Font('graphics/minecraft.ttf',30)
main_bg=pygame.image.load('graphics/space_bg.png')
gamename = mainfont.render('Purple & ',False,'Purple')
gamename2 = mainfont.render('Red',False,'Red')
gamename_rect=gamename.get_rect(center=(230,500))
gamename2_rect = gamename2.get_rect(center=(460,490))
count = 0
score = 0
highscore = 0
game_active = False
while True: 
    for event in pygame.event.get():    
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if not game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks()/1000)

    if game_active:
        screen.fill('Black')
        
        camera_group.update()
        pos_x = random.choice([-600,600])
        pos_y = random.randint(150,600)
        elapsed_time = time.time() - last_trigger_time
        if(count%25==0):
            targx = player.rect.centerx
            targy = player.rect.centery
        if elapsed_time>=interval:
            enemy.append(Enemy((pos_x,pos_y),camera_group))
            interval/=qf
            last_trigger_time = time.time()
        for i in enemy:
            i.movement([targx,targy])
            i.destroy(enemy)
        if interval<0.7:
            qf = 1.2
        if interval<0.4:
            qf = 1.05
        if interval<0.27:
            qf = 1
        camera_group.custom_draw(player)
        count+=1
        display_score()
        if (not gamecheck(player,enemy)): game_active = False

    else:
        screen.fill('Black')
        screen.blit(gamename,gamename_rect)
        screen.blit(gamename2,gamename2_rect)
        space_Surf = sidefont.render(f'Press space to play',False,'violet')
        space_Rect = space_Surf.get_rect(center = (260,650))
        screen.blit(space_Surf,space_Rect)
        for i in enemy:
            i.kill()
        enemy.clear()
        interval = 5
        qf = 1.5
        if score:
            if score>highscore: highscore = score
            score_Surf = sidefont.render(f'Score: {score}        High Score: {highscore}',False,'white')
            score_Rect = score_Surf.get_rect(center = (330,580))
            screen.blit(score_Surf,score_Rect)
        
    pygame.display.update()
    clock.tick(60)

    