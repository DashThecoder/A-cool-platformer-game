import pygame,sys
from pygame.locals import *
from pygame import mixer
import pickle
from os import path
blob_group=pygame.sprite.Group()
coin_group=pygame.sprite.Group()
exit_group=pygame.sprite.Group()
#Starting the game
pygame.init()
mixer.init()
clock=pygame.time.Clock()
fps=60
#Setting up the screen
Screen_width=600
Screen_height=600
screen=pygame.display.set_mode((Screen_width,Screen_height))
pygame.display.set_caption("Mario")
pygame.display.set_icon(pygame.image.load("guy1.png"))
#The variables
tile_size=30
game_over=0
level=1
main_menu=True
bg_img=pygame.transform.scale(pygame.image.load("sky.png"),(600,600))
sun_img=pygame.image.load("sun.png")
mixer.music.load("img_coin.wav")
restart_img=pygame.image.load("restart_btn.png")
start_img=pygame.image.load("start_btn.png")
start_img=pygame.transform.scale(start_img,(150,75))
exit_img=pygame.image.load("exit_btn.png")
exit_img=pygame.transform.scale(exit_img,(150,75))
Victory_img=pygame.image.load("Ending_cup.jpg")
Victory_img=pygame.transform.scale(Victory_img,(600,600))
coin_amount=0
max_levels=4
#classes and defs
def reset_level(Level):
    atom.reset(50,Screen_height-65)
    blob_group.empty()
    coin_group.empty()
    exit_group.empty()
    if path.exists(f"level{level}_data"):
        pickle_in=open(f"level{level}_data","rb")
        world_data=pickle.load(pickle_in)
    world=World(world_data)
    return world
class Button():
    def __init__(self,x,y,image):
        self.image=image
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.clicked=False
    def draw(self):
        action=False
        pos=pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==1 and self.clicked==False:
                action=True
                self.clicked==True
        if pygame.mouse.get_pressed()[0]==0:
            self.clicked==False
        screen.blit(self.image,self.rect)
        return action
class Atom:
    def __init__(self,x,y):
        self.reset(x,y)
    def update(self,game_over):
        dx=0
        dy=0
        walk_cooldown=5
        if game_over==0:
            key=pygame.key.get_pressed()
            #Left and right movement
            if key[pygame.K_LEFT]:
                dx-=2.5
                self.counter+=1
                self.direction=-1
            if key[pygame.K_RIGHT]:
                dx+=2.5
                self.counter+=1
                self.direction=1
            #jumping movement
            if key[K_SPACE] and self.jumped==False:
                self.vel_y=-7.5
                self.jumped=True
            if key[pygame.K_SPACE]==False:
                self.jumped=False
            self.vel_y+=0.5
            if self.vel_y>10:
                self.vel_y=10
            dy+=self.vel_y
            #character animation
            if self.counter>walk_cooldown:
                self.counter=0
                self.index+=1
                if self.index>=len(self.images_right):
                    self.index=0
                if self.direction==1:
                    self.image=self.images_right[self.index]
                if self.direction==-1:
                    self.image=self.images_left[self.index]
            #Collision detection
            for tile in world.tile_list:
                #x collision detection
                if tile[1].colliderect(self.rect.x+dx,self.rect.y,self.width,self.height):
                    dx=0
                #y collision detection
                if tile[1].colliderect(self.rect.x,self.rect.y+dy,self.width,self.height):
                    if self.vel_y<0:
                        dy=tile[1].bottom-self.rect.top
                        self.vel_y=0
                    if self.vel_y>0:
                        dy=tile[1].top-self.rect.bottom
                        self.vel_y=0
        #Checking for enemy collision
            if pygame.sprite.spritecollide(self,blob_group,False):
                game_over=-1
            if pygame.sprite.spritecollide(self, coin_group, True):
                mixer.music.play()
            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over=1
        #updating
            self.rect.x+=dx
            self.rect.y+=dy
        elif game_over==-1:
            self.image=self.dead_image
            if self.rect.y>80:
                self.rect.y-=5
        screen.blit(self.image,self.rect)
        return game_over
    def reset(self,x,y):
        self.images_right=[]
        self.images_left=[]
        self.index=0
        self.counter=0
        for num in range(1,5):
            img_right=pygame.image.load(f"guy{num}.png")
            img_right=pygame.transform.scale(img_right,(20,40))
            img_left=pygame.transform.flip(img_right,True,False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_image=pygame.image.load("ghost.png")
        self.image=self.images_right[self.index]
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.width=self.image.get_width()
        self.height=self.image.get_height()
        self.vel_y=0
        self.jumped=False
        self.direction=0
class World:
    def __init__(self,data):
        self.tile_list=[]
        dirt_img=pygame.image.load("dirt.png")
        grass_img=pygame.image.load("grass.png")
        lava_img=pygame.image.load("lava.png")
        pipe_top_img=pygame.image.load("pipe_top.png")
        pipe_low_img=pygame.image.load("pipe_down.png")
        coin_img=pygame.image.load("coin.png")
        row_count=0
        for row in data:
            col_count=0
            for tile in row:
                if tile==1:
                    img=pygame.transform.scale(dirt_img,(tile_size,tile_size))
                    img_rect=img.get_rect()
                    img_rect.x=col_count*tile_size
                    img_rect.y=row_count*tile_size
                    tile=(img,img_rect)
                    self.tile_list.append(tile)
                if tile==2:
                    img=pygame.transform.scale(grass_img,(tile_size,tile_size))
                    img_rect=img.get_rect()
                    img_rect.x=col_count*tile_size
                    img_rect.y=row_count*tile_size
                    tile=(img,img_rect)
                    self.tile_list.append(tile)
                if tile==3:
                    blob=Ender(col_count*tile_size,row_count*tile_size)
                    blob_group.add(blob)
                if tile==4:
                    img=pygame.transform.scale(lava_img,(tile_size*2,tile_size))
                    img_rect=img.get_rect()
                    img_rect.x=col_count*tile_size
                    img_rect.y=row_count*tile_size
                    tile=(img,img_rect)
                    self.tile_list.append(tile)
                if tile==5:
                    img=pygame.transform.scale(pipe_top_img,(tile_size,tile_size))
                    img_rect=img.get_rect()
                    img_rect.x=col_count*tile_size
                    img_rect.y=row_count*tile_size
                    tile=(img,img_rect)
                    self.tile_list.append(tile)
                if tile==6:
                    img=pygame.transform.scale(pipe_low_img,(tile_size,tile_size))
                    img_rect=img.get_rect()
                    img_rect.x=col_count*tile_size
                    img_rect.y=row_count*tile_size
                    tile=(img,img_rect)
                    self.tile_list.append(tile)
                if tile==7:
                    coin=Coin(col_count*tile_size+8,row_count*tile_size+8)
                    coin_group.add(coin)
                if tile==8:
                    exit=Exit(col_count*tile_size,row_count*tile_size-10)
                    exit_group.add(exit)
                col_count+=1
            row_count+=1
    def draw(self):
            for tile in self.tile_list:
                screen.blit(tile[0],tile[1])
class Ender(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(pygame.image.load("blob.png"),(40,30))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.move_direction=1
        self.move_counter=0
    def update(self):
        self.rect.x+=self.move_direction
        self.move_counter+=1
        if self.move_counter>83:
            self.move_direction*=-1
            self.move_counter=0
class Coin(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("coin.png")
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
class Exit(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img=pygame.image.load("exit.png")
        self.image=pygame.transform.scale(img,(tile_size,tile_size+13))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

def pyquit():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
def draw_grid():
    for line in range(0,20):
        pygame.draw.line(screen,(255,255,255),(0,line*tile_size),(Screen_width,line*tile_size))
        pygame.draw.line(screen,(255,255,255),(line*tile_size,0),(line*tile_size,Screen_height))
if path.exists(f"level{level}_data"):
    pickle_in=open(f"level{level}_data","rb")
    world_data=pickle.load(pickle_in)
world=World(world_data)
atom=Atom(50,Screen_height-65)
restart_button=Button(Screen_width//2,Screen_height//2,restart_img)
start_button=Button(Screen_width//2-200,Screen_height//2,start_img)
exit_button=Button(Screen_width//2+50,Screen_height//2,exit_img)
run=True
#the game loop
while run:
    clock.tick(fps)
    screen.blit(bg_img,(0,0))
    screen.blit(sun_img,((25,25)))
    if main_menu:
        if start_button.draw():
            main_menu=False
        if exit_button.draw():
            run=False
    else:
        world.draw()
 #       draw_grid()
        if game_over==0:
            blob_group.update()
        blob_group.draw(screen)
        coin_group.draw(screen)
        exit_group.draw(screen)
        if game_over==-1:
            if restart_button.draw():
                atom.reset(50,Screen_height-65)
                game_over=0
        game_over=atom.update(game_over)
        if game_over==1:
            if level<4:
                level+=1
            if level==4:
                screen.blit(Victory_img,(0,0))
            else:
                world_data=[]
                world=reset_level(level)
                game_over=0
        if level==4:
            screen.blit(Victory_img,(0,0))
    for event in pygame.event.get():
        pyquit()
    pygame.display.update()


