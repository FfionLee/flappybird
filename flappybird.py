import pygame
import random

from pygame.locals import *
pygame.init()

screen=pygame.display.set_mode((860,820))

bg=pygame.image.load('flappybg.png')
ground=pygame.image.load('flappyground.png')

clock=pygame.time.Clock()
fps=60

ground_scroll=0
scroll_speed=4

score=0
pass_pipe=False

flying=False
gameover=False
pipe_gap=150
pipeinterval=1500
last_pipe=pygame.time.get_ticks()-pipeinterval

font=pygame.font.SysFont('Bauhaus 93',60)

class FlappyBird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images=[]
        self.index=0
        self.counter=0
        for i in range(1,4):
            img=pygame.image.load(f'flappy{i}.png')
            self.images.append(img)
        self.image=self.images[self.index]
        self.rect=self.image.get_rect()
        self.rect.center=[x,y]
        self.vel=0
        self.clicked=False
    
    def update(self):
        global gameover
        if flying==True:
            self.vel+=0.5
            if self.rect.bottom<780:
                self.rect.y+=int(self.vel)
                #add gravity later on
            if pygame.mouse.get_pressed()[0]==1 and self.clicked==False:
                self.vel=-10
                self.clicked=True
            if pygame.mouse.get_pressed()[0]==0:
                self.clicked=False
        if gameover==False:
            self.counter=self.counter+1
            flap_cooldown=5
            if self.counter>flap_cooldown:
                self.counter=0
                self.index+=1
                if self.index>=3:
                    self.index=0
            self.image=self.images[self.index]
            self.image=pygame.transform.rotate(self.images[self.index],self.vel*-2)
            if self.rect.bottom>780:
                self.image=pygame.transform.rotate(self.images[self.index],-90)
                gameover=True
        
class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,pos):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('flappypipe.png')
        self.rect=self.image.get_rect()
        if pos==1:
            self.image=pygame.transform.flip(self.image,False,True)
            self.rect.bottomleft=[x,y-75]
        if pos==-1:
            self.rect.topleft=[x,y+75]
        
    def update(self):
        self.rect.x-=scroll_speed
        if self.rect.right<0:
            self.kill()

birdgroup=pygame.sprite.Group()
flappy=FlappyBird(100,400)
birdgroup.add(flappy)

pipegroup=pygame.sprite.Group()


playing=True

while playing:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            playing=False
        if event.type==pygame.MOUSEBUTTONDOWN and flying==False:
            flying=True
    screen.blit(bg,(0,0))
    screen.blit(ground,(ground_scroll,760))
    if gameover==False:
        ground_scroll=ground_scroll-scroll_speed
        if abs(ground_scroll)>35:
            ground_scroll=0
        time_now=pygame.time.get_ticks()
        if time_now-last_pipe>pipeinterval:
            pipe_height=random.randint(-100,100)
            bottom_pipe=Pipe(850,400+pipe_height,-1)
            top_pipe=Pipe(850,400+pipe_height,1)
            pipegroup.add(top_pipe)
            pipegroup.add(bottom_pipe)
            last_pipe=time_now
    if len(pipegroup)>0:
        if birdgroup.sprites()[0].rect.left>pipegroup.sprites()[0].rect.left \
            and birdgroup.sprites()[0].rect.right<pipegroup.sprites()[0].rect.right and pass_pipe==False:
            pass_pipe=True
        if pass_pipe==True:
            if birdgroup.sprites()[0].rect.left>pipegroup.sprites()[0].rect.right:
                score=score+1
                pass_pipe=False

    score_text=font.render('Score'+str(score),True,'white')
    screen.blit(score_text,(10,10))

    birdgroup.draw(screen)
    birdgroup.update()

    pipegroup.draw(screen)
    pipegroup.update()

    pygame.display.update()
    
