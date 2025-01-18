import pygame

from pygame.locals import *
pygame.init()

screen=pygame.display.set_mode((850,800))

bg=pygame.image.load('flappybg.png')
ground=pygame.image.load('flappyground.png')

clock=pygame.time.Clock()
fps=40

ground_scroll=0
scroll_speed=4

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
        self.vel+=0.5
        if self.rect.bottom<700:
        #continue next class
            self.rect.y+=int(self.vel)
        self.counter=self.counter+1
        flap_cooldown=5
        if self.counter>flap_cooldown:
            self.counter=0
            self.index+=1
            if self.index>=3:
                self.index=0
        self.image=self.images[self.index]

birdgroup=pygame.sprite.Group()
flappy=FlappyBird(100,400)
birdgroup.add(flappy)


playing=True

while playing:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            playing=False
    screen.blit(bg,(0,0))
    screen.blit(ground,(ground_scroll,700))
    ground_scroll=ground_scroll-scroll_speed
    if abs(ground_scroll)>35:
        ground_scroll=0
    
    birdgroup.draw(screen)
    birdgroup.update()

    pygame.display.update()
    