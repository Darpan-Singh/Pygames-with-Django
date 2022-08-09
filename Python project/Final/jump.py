import pygame
import math
import os
pygame.font.init()
pygame.mixer.init()
s_width=1200
s_height=500
vel=40
speed=5
WIN=pygame.display.set_mode((1200,500))
pygame.display.set_caption('Projectile motion')
FOUL_FONT = pygame.font.SysFont('comicsans', 100)
class player:
    def __init__(self,x,y,width,height,colour):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.colour=colour
    def draw(self,WIN):
        pygame.draw.rect(WIN,self.colour,(self.x,self.y,self.width,self.height))
    @staticmethod
    def player_path(startx,starty,time):
            velx=math.sqrt(0.5)*vel
            vely=math.sqrt(0.5)*vel
            distx=velx*time
            disty=(vely*time)-((4.9*(time)**2)/2)
            newx=round(distx+startx)
            newy=round(starty-disty)
            if(newx<1150):
                return (newx,newy)
            else:
                return (1150,newy)
def redraw():
    WIN.fill((0,0,0))
    player1.draw(WIN)
    pygame.draw.rect(WIN,(255,0,0),(800,495,20,10))
    pygame.display.update()


def draw_msg(text):
    draw_text = FOUL_FONT.render(text,1,(255,255,255))
    WIN.blit(draw_text, (600 - draw_text.get_width() /
                         2, 250 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(500)


def foul_check(player,foul_line):
    if image.colliderect(foul_line):
        draw_msg('FOUL')

player1=player(300,449,50,50,(255,255,255))
image=pygame.Rect(300,449,50,50)
foul_line=pygame.Rect(800,495,20,10)
x=0
y=0
time=0
jump=False

clock = pygame.time.Clock()
FPS=60
JFPS=90
run=True
while run:
    if jump:
        if player1.y+player1.width<500:
            time+=0.05
            po=player.player_path(x,y,time)
            player1.x=po[0]
            player1.y=po[1]
        else:
            jump=False
            player1.y=449
    redraw()
    for event in  pygame.event.get():
        if(event.type == pygame.QUIT):
            run =False
    foul_text=""
    if (player1.x+player1.width >=800) and (player1.y ==449) and(player1.x <=820): 
        foul_text="foul"
    if foul_text !="":
        draw_msg(foul_text)
        redraw()
    keys=pygame.key.get_pressed()
    if(keys[pygame.K_SPACE]):
        if jump==False:
            clock.tick(JFPS)
            jump=True
            x=player1.x
            y=player1.y
            time=0
    if(player1.y>448):
        if((keys[pygame.K_RIGHT] and (player1.x +player1.width +speed< 800 or player1.x<1150))):
            clock.tick(FPS)
            player1.x+=speed
        if(keys[pygame.K_LEFT] and player1.x - speed>0):
            clock.tick(FPS)
            player1.x-=speed
        
pygame.quit()