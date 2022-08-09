from django.shortcuts import render
from django.http import HttpResponse
import pygame, sys, time, random
from pygame.constants import KEYDOWN
from pygame.math import Vector2
import math
import os

from pathlib import Path 
import pymunk
from pygame.constants import  K_LEFT, K_UP

    # Create your views here.
def home(request):
    
    return render(request, 'home.html')
def g1(request):
    pygame.init()

    S = pygame.display.set_mode((1100,600))
    pygame.display.set_caption("CATCH ME IF U CAN")
    # for music mixer is imported
    from pygame import mixer
    mixer.music.load(os.path.join('static','music.wav'))
    mixer.music.play(-1)

    back_ground = pygame.image.load(os.path.join("static","Track.png"))
    CLOUD = pygame.image.load(os.path.join("static","cloud.jpg"))
    RUN = [pygame.image.load(os.path.join("static","nobitha 2.jpg")),
               pygame.image.load(os.path.join("static","1.png"))]
    JUMP = pygame.image.load(os.path.join("static","2.png"))
    DUCK = [pygame.image.load(os.path.join("static","Nobyrollerskates-removebg-preview.png")),
               pygame.image.load(os.path.join("static","Nobyrollerskates-removebg-preview.png"))]

    SMALL = [pygame.image.load(os.path.join("static","Teacher_nobitha (2).jpg")),

                    pygame.image.load(os.path.join("static","topper_prev_ui.png")),
                    pygame.image.load(os.path.join("static","nobithamom.jpg"))]
    LARGE= [pygame.image.load(os.path.join("static","geyan.jpg")),
                    pygame.image.load(os.path.join("static","playground uncle.jpg")),
                    pygame.image.load(os.path.join("static","sunio.jpg"))]

    DORA= [pygame.image.load(os.path.join("static","doramon 1.png")),
            pygame.image.load(os.path.join("static","doramon 1.png"))]

    def main():
        # back ground position of x,y co ordinates
        global game_speed, x_pos_bg, y_pos_bg
        global dora_characters
        global points
        run = True

        clock = pygame.time.Clock()
        player = Nobita()
        cloud = Cloud()
        game_speed = 20
        x_pos_bg = 0
        y_pos_bg = 400


        points = 0

        font = pygame.font.Font('freesansbold.ttf', 20)

        dora_characters = []

        collision = 0

        def score():
            global points, game_speed
            points += 1
            if points %80 == 0:
                game_speed += 1
    # import os
            text = font.render("Points: " + str(points), True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (1000, 40)
            S.blit(text, textRect)

        def background():
            global x_pos_bg, y_pos_bg


            image_width = back_ground.get_width()
            S.blit(back_ground, (x_pos_bg, y_pos_bg))
            S.blit(back_ground, (image_width + x_pos_bg, y_pos_bg))


            if x_pos_bg <= -image_width:
                S.blit(back_ground, (image_width + x_pos_bg, y_pos_bg))
                x_pos_bg = 0
            x_pos_bg -= game_speed

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            S.fill((255, 255, 255))
            user_input = pygame.key.get_pressed()

            player.draw(S)
            player.update(user_input)

            if len(dora_characters) == 0:
                if random.randint(0, 2) == 0:
                    dora_characters.append(Small(SMALL))
                elif random.randint(0, 2) == 1:
                    dora_characters.append(Large(LARGE))
                elif random.randint(0, 2) == 2:
                    dora_characters.append(Dora(DORA))

            for obstacle in dora_characters:
                obstacle.draw(S)

                obstacle.update()
                if player.nobita_rect.colliderect(obstacle.rect):
                    pygame.time.delay(150)
                    collision += 1
                    menu(collision)

            background()

            cloud.draw(S)
            cloud.update()

            score()

            clock.tick(30)
            pygame.display.update()

    class Nobita:
        xcod_nobita = 100
        ycod_nobita = 310
        ycod_duck_nobita = 390
        jumpspeed = 12

        def __init__(self):
            self.duckingimage = DUCK
            self.runningimage = RUN
            self.jumpingimage = JUMP

            self.nobita_duck = False
            self.nobita_run = True
            self.nobita_jump = False

            self.initial_index = 0
            self.jump_vel = self.jumpspeed
            self.image = self.runningimage[0]
            self.nobita_rect = self.image.get_rect()
            self.nobita_rect.x = self.xcod_nobita
            self.nobita_rect.y = self.ycod_nobita

        def update(self, user_input):

            if self.nobita_run:
                self.run()
            if self.nobita_jump:
                self.jump()
            if self.nobita_duck:
                self.duck()

            if self.initial_index >= 10:
                self.initial_index = 0

            if user_input[pygame.K_UP] and not self.nobita_jump:

            
                self.nobita_run = False
                self.nobita_jump = True
                self.nobita_duck = False


            elif user_input[pygame.K_DOWN] and not self.nobita_jump:

                self.nobita_run = False
                self.nobita_jump = False
                self.nobita_duck = True

            elif not (self.nobita_jump or user_input[pygame.K_DOWN]):

                self.nobita_run = True
                self.nobita_jump = False
                self.nobita_duck = False


        def run(self):
            self.image = self.runningimage[self.initial_index // 5]
            self.nobita_rect = self.image.get_rect()
            self.nobita_rect.x = self.xcod_nobita
            self.nobita_rect.y = self.ycod_nobita
            self.initial_index += 1

        def jump(self):
            self.image = self.jumpingimage
            if self.nobita_jump:
                self.nobita_rect.y -= self.jump_vel * 4
                self.jump_vel -= 1
            if self.jump_vel < - self.jumpspeed:
                self.nobita_jump = False
                self.jump_vel = self.jumpspeed

        def duck(self):
            self.image = self.duckingimage[self.initial_index // 5]

            self.nobita_rect = self.image.get_rect()

            self.nobita_rect.x = self.xcod_nobita

            self.nobita_rect.y = self.ycod_duck_nobita

            self.initial_index += 1


        def draw(self, S):
            S.blit(self.image, (self.nobita_rect.x, self.nobita_rect.y))


    class Cloud:
        def __init__(self):
            self.x = 1100 + random.randint(1000,2000)
            self.y = random.randint(50, 100)
            self.image = CLOUD
            self.width = self.image.get_width()

        def update(self):
            self.x -= game_speed
            if self.x < -self.width:
                self.x = 1100+ random.randint(2500, 3000)
                self.y = random.randint(50, 100)

        def draw(self, S):
            S.blit(self.image, (self.x, self.y))


    class Obstacle:
        def __init__(self, image, type):
            self.image = image
            self.type = type
            self.rect = self.image[self.type].get_rect()
            self.rect.x = 1100

        def update(self):
            self.rect.x -= game_speed
            if self.rect.x < -self.rect.width:
                dora_characters.pop()

        def draw(self, S):
            S.blit(self.image[self.type], self.rect)


    class Small(Obstacle):
        def __init__(self, image):
            self.type = random.randint(0, 2)
            super().__init__(image, self.type)
            self.rect.y = 280


    class Large(Obstacle):
        def __init__(self, image):
            self.type = random.randint(0, 2)
            super().__init__(image, self.type)
            self.rect.y = 300


    class Dora(Obstacle):
        def __init__(self, image):
            self.type = 0
            super().__init__(image, self.type)
            self.rect.y = 250
            self.index = 0

        def draw(self, S):
            if self.index >9:
                self.index = 0
            S.blit(self.image[self.index//5], self.rect)
            self.index += 1



    def menu(collision):
        global points
        run = True

        while run:

            S.fill((255, 255, 255))
            font = pygame.font.Font('freesansbold.ttf', 20)

            if collision == 0:
                text = font.render("Press any Key to Start", True, (0, 0, 0))
            elif collision > 0:
                text = font.render("Press any Key to Restart", True, (0, 0, 0))
                score = font.render("Your Score: " + str(points), True, (0, 0, 0))
                scoreRect = score.get_rect()
                scoreRect.center = (550,350)
                S.blit(score, scoreRect)


            textRect = text.get_rect()
            textRect.center = (550,300)

            S.blit(text, textRect)
            S.blit(RUN[0], (510, 160))
            pygame.display.update()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    main()


    menu(collision=0)
    pygame.quit()
    name=request.GET["name"]
    return render(request, 'Scorecard.html',{"name":name,"score":points})
def g3(request):
    pygame.font.init()
    pygame.mixer.init()
    s_width=1200
    s_height=500
    vel=40
    speed=5
    i=1
    j=0
    WIN=pygame.display.set_mode((1200,500))
    character=pygame.image.load(os.path.join("static","x.png"))
    background=pygame.image.load(os.path.join("static","b.png"))
    jumpsound=pygame.mixer.Sound(os.path.join("static","jump.wav"))
    music=pygame.mixer.music.load(os.path.join("static","bg.wav"))
    pygame.mixer.music.play(-1)
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
            c=pygame.transform.scale(character,(self.width,self.height))
            red = pygame.Rect(self.x,self.y, self.width,self.height)
            WIN.blit(c, (red.x, red.y))
        @staticmethod
        def player_path(startx,starty,time,s):
                velx=math.sqrt(0.5)*s
                vely=math.sqrt(0.5)*s
                distx=velx*time
                disty=(vely*time)-((4.9*(time)**2)/2)
                newx=round(distx+startx)
                newy=round(starty-disty)
                if(newx<1150):
                    return (newx,newy)
                else:
                    return (1150,newy)
    def redraw():
        WIN.blit(background,(0,0))
        player1.draw(WIN)
        pygame.draw.rect(WIN,(255,0,0),(800,495,20,10))
        pygame.display.update()


    def draw_msg(text):
        draw_text = FOUL_FONT.render(text,1,(255,255,255))
        WIN.blit(draw_text, (600 - draw_text.get_width() /
                             2, 250 - draw_text.get_height()/2))
        pygame.display.update()
        pygame.time.delay(500)
    def draw_msg1(text):
        draw_text = FOUL_FONT.render(text,1,(255,255,255))
        WIN.blit(draw_text, (1000,100))
        pygame.display.update()
        pygame.time.delay(500)


    def foul_check(player,foul_line):
        if image.colliderect(foul_line):
            draw_msg('FOUL')

    player1=player(40,250,100,300,(255,255,255))
    image=pygame.Rect(40,250,100,300)
    foul_line=pygame.Rect(800,495,20,10)
    x=0
    y=0
    time=0
    jump=False

    clock = pygame.time.Clock()
    FPS=60
    JFPS=2000
    run=True
    while run:
        if jump:
            if player1.y+player1.width<360:
                clock.tick(JFPS)
                time+=0.05
                po=player.player_path(x,y,time,speed)
                player1.x=po[0]
                player1.y=po[1]
            else:
                jump=False
                player1.y=250
                break
                
        redraw()
        for event in  pygame.event.get():
            if(event.type == pygame.QUIT):
                run =False
        foul_text=""
        if ((player1.x>=800) and (player1.y ==250) and(player1.x <=820) or (i!=1 and player1.x+player1.width<800 and player1.y==449)): 
            foul_text="FOUL"
            redraw()
        if foul_text !="":
            draw_msg(foul_text) 
            j=1     
            pygame.time.delay(500)
            break      
        
            
        keys=pygame.key.get_pressed()
        if(keys[pygame.K_SPACE] and i==1):
            jumpsound.play()
            if jump==False:
                clock.tick(JFPS)
                jump=True
                x=player1.x
                y=player1.y
                time=0
            i=2
        if(player1.y>248 and i==1):
            if((keys[pygame.K_RIGHT] and (player1.x +player1.width +speed< 800 or player1.x<1150))):
                clock.tick(FPS)
                player1.x+=speed
                speed+=1
            if(keys[pygame.K_LEFT] and player1.x - speed>0):
                speed=5
                clock.tick(FPS)
                player1.x-=speed
                speed-=1
    if (player1.x>820 and j!=1):
        draw_msg1(str(round(player1.x/100-8,2)*3.8)+'m')
        score=round((player1.x/100-8)*3.8,2)
    else:
        draw_msg1(str(0))
        score=0
    pygame.time.delay(5000)
    pygame.quit()
    name=request.GET["name"]
    return render(request, 'Scorecard.html',{"name":name,"score":score})

def g4(request):
    pygame.init()
    score=0
    snake_block = 20
    cells = 20
    dis_height = snake_block * cells
    dis_width = snake_block * cells

    display = pygame.display.set_mode((dis_height, dis_width))
    pygame.display.set_caption('Snake Game')
    jumpsound=pygame.mixer.Sound(os.path.join("static","jump.wav"))
    music=pygame.mixer.music.load(os.path.join("static","bg.wav"))
    pygame.mixer.music.play(-1)

    apple = pygame.image.load(os.path.join('static','apple.png'))

    class FOOD:
        def __init__(self):
            self.x = random.randint(0, cells - 1)
            self.y = random.randint(0, cells - 1)
            self.pos = Vector2(self.x, self.y)

        def food_draw(self):
            food_rect = pygame.Rect(self.pos.x * snake_block, self.pos.y * snake_block, snake_block, snake_block)
            display.blit(apple, food_rect)
            #pygame.draw.rect(display,(pygame.Color('red')), food_rect)

        def randomiser(self):
            self.x = random.randint(0, cells - 1)
            self.y = random.randint(0, cells - 1)
            self.pos = Vector2(self.x, self.y)

    class SNAKE:
        def __init__(self):
            self.body = [Vector2(6, 10)]
            self.dir = Vector2(0, 0)
            self.grow = False

        def draw_snake(self):
            head_rect = pygame.Rect(self.body[0].x * snake_block, self.body[0].y * snake_block, snake_block, snake_block)
            pygame.draw.rect(display, (pygame.Color('gold')), head_rect)
            for block in self.body[1:]:
                snake_rect = pygame.Rect(block.x * snake_block, block.y * snake_block, snake_block, snake_block)
                pygame.draw.rect(display, (pygame.Color('black')), snake_rect)

        def move(self):
            if self.grow == False:
                step = self.body[1:]
                step.insert(0, self.body[0] + self.dir)
                self.body = step[:]
            else:
                step = self.body[:]
                step.insert(0, self.body[0] + self.dir)
                self.body = step[:]
                self.grow = False

        def add(self):
            self.grow = True

    class MAIN:
        def __init__(self):
            self.snake = SNAKE()
            self.food = FOOD()

        def update(self):
            self.snake.move()

        def draw(self):
            self.food.food_draw()
            self.snake.draw_snake()

        def eat(self):
            qw=False
            if self.food.pos == self.snake.body[0]:
                self.food.randomiser()
                self.snake.add()
                jumpsound.play()
                qw=True
            for block in self.snake.body[1:]:
                if block == self.food.pos:
                    self.food.randomiser()
                    qw=True
            return qw
                

        def gameover(self):
            return 1
            

        def collide(self):
            if not 0 <= self.snake.body[0].x < cells or not 0 <= self.snake.body[0].y < cells:
                return self.gameover()
            for block in self.snake.body[1:]:
                if block == self.snake.body[0]:
                    return self.gameover()

    game = MAIN()

    SCREENUPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREENUPDATE, 150)

    clock = pygame.time.Clock();
    
    snake = 10
    speed = 60

    surface = pygame.Surface((100, 200))

    lightblue = (135, 206, 235)

    close = False
    while not close:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.snake.dir = Vector2(0, -1)
                if event.key == pygame.K_DOWN:
                    game.snake.dir = Vector2(0, 1)
                if event.key == pygame.K_LEFT:
                    game.snake.dir = Vector2(-1, 0)
                if event.key == pygame.K_RIGHT:
                    game.snake.dir = Vector2(1, 0)
            if event.type == SCREENUPDATE:
                game.snake.move()
        display.fill(lightblue)
        game.draw()
        er=game.eat()
        if er:
            score+=1000
        score+=1
        wq=game.collide()
        if(wq==1):
            break
        pygame.display.update()
        clock.tick(speed)
    pygame.quit()

    name=request.GET["name"]
    return render(request, 'Scorecard.html',{"name":name,"score":score/60})
def g5(request):
    class SNAKE:
        def __init__(self):
            self.body = [Vector2(7,10),Vector2(6,10),Vector2(5,10)]
            self.direction = Vector2(0
            ,0)
            self.new_block = False

            self.head_up = pygame.image.load(os.path.join('static','head_up.png')).convert_alpha()
            self.head_up=pygame.transform.scale(self.head_up, (40, 40))

            self.head_down = pygame.image.load(os.path.join('static','head_down.png')).convert_alpha()
            self.head_down=pygame.transform.scale(self.head_down, (40, 40))

            self.head_right = pygame.image.load(os.path.join('static','head_right.png')).convert_alpha()
            self.head_right=pygame.transform.scale(self.head_right, (40, 40))

            self.head_left = pygame.image.load(os.path.join('static','head_left.png')).convert_alpha()
            self.head_left=pygame.transform.scale(self.head_left, (40, 40))

            self.tail_up = pygame.image.load(os.path.join('static','tail_up.png')).convert_alpha()
            self.tail_up=pygame.transform.scale(self.tail_up, (40, 40))

            self.tail_down = pygame.image.load(os.path.join('static','tail_down.png')).convert_alpha()
            self.tail_down=pygame.transform.scale(self.tail_down, (40, 40))

            self.tail_right = pygame.image.load(os.path.join('static','tail_right.png')).convert_alpha()
            self.tail_right=pygame.transform.scale(self.tail_right, (40, 40))

            self.tail_left = pygame.image.load(os.path.join('static','tail_left.png')).convert_alpha()
            self.tail_left=pygame.transform.scale(self.tail_left, (40, 40))

            self.body_vertical = pygame.image.load(os.path.join('static','body_vertical.png')).convert_alpha()
            self.body_vertical=pygame.transform.scale(self.body_vertical, (40, 40))

            self.body_horizontal = pygame.image.load(os.path.join('static','body_horizontal.png')).convert_alpha()
            self.body_horizontal=pygame.transform.scale(self.body_horizontal, (40, 40))


            self.body_tr = pygame.image.load(os.path.join('static','body_tr.png')).convert_alpha()
            self.body_tr=pygame.transform.scale(self.body_tr, (40, 40))

            self.body_tl = pygame.image.load(os.path.join('static','body_tl.png')).convert_alpha()
            self.body_tl=pygame.transform.scale(self.body_tl, (40, 40))

            self.body_br = pygame.image.load(os.path.join('static','body_br.png')).convert_alpha()
            self.body_br=pygame.transform.scale(self.body_br, (40, 40))

            self.body_bl = pygame.image.load(os.path.join('static','body_bl.png')).convert_alpha()
            self.body_bl=pygame.transform.scale(self.body_bl, (40, 40))
            self.crunch_sound = pygame.mixer.Sound(os.path.join('static','aud_chomp(1).wav'))

        def draw_snake(self):

            self.update_head_graphics()
            self.update_tail_graphics()

            for index,block in enumerate(self.body):
                x_pos = int(block.x * cell_size)
                y_pos = int(block.y * cell_size)                  
                block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)

                if index == 0:
                    screen.blit(self.head,block_rect)
                elif index == (len(self.body)-1):
                    screen.blit(self.tail,block_rect)

                else:
                    previous_block = self.body[index + 1] - block
                    next_block = self.body[index - 1] - block
                    if previous_block.x == next_block.x:
                        screen.blit(self.body_vertical,block_rect)
                    elif previous_block.y == next_block.y:
                        screen.blit(self.body_horizontal,block_rect)
                    else:
                        if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                            screen.blit(self.body_tl,block_rect)
                        elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                            screen.blit(self.body_bl,block_rect)
                        elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                            screen.blit(self.body_tr,block_rect)
                        elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                            screen.blit(self.body_br,block_rect)

        def update_head_graphics(self):
            head_relation = self.body[1] - self.body[0]
            if head_relation == Vector2(1,0): self.head = self.head_left
            elif head_relation == Vector2(-1,0): self.head = self.head_right
            elif head_relation == Vector2(0,1): self.head = self.head_up
            elif head_relation == Vector2(0,-1): self.head = self.head_down

        def update_tail_graphics(self):
            tail_relation = self.body[-2] - self.body[-1]
            if tail_relation == Vector2(1,0): self.tail = self.tail_left
            elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
            elif tail_relation == Vector2(0,1): self.tail = self.tail_up
            elif tail_relation == Vector2(0,-1): self.tail = self.tail_down

        def move_snake(self):
            if self.new_block == True :
                body_copy = self.body[:]
                body_copy.insert(0,body_copy[0] + self.direction)
                self.body = body_copy[:]
                self.new_block =False

            else:
                body_copy = self.body[:-1]
                body_copy.insert(0,body_copy[0] + self.direction)
                self.body = body_copy[:]

        def add_block(self):
            self.new_block = True
            # self.body.append()

        # def play_crunch_sound(self):
        #     self.crunch_sound.play()

        def play_crunch_sound(self):
            self.crunch_sound.play()

        def reset(self):
            self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
            self.direction = Vector2(0,0)


    class FRUIT:
        def __init__(self):
            self.x = random.randint(0,cell_number-1)
            self.y = random.randint(0,cell_number-1)        
            self.pos = Vector2(self.x,self.y)
        def draw_fruit(self):
            x_pos = int(self.pos.x * cell_size)
            y_pos = int(self.pos.y * cell_size)
            fruit_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)
            screen.blit(mouse,fruit_rect)
            # pygame.draw.rect(screen,(0,255,0),fruit_rect)

        def randomize(self):
            self.x = random.randint(0,cell_number-1)
            self.y = random.randint(0,cell_number-1)        
            self.pos = Vector2(self.x,self.y)

    class MAIN:
        def __init__(self):
            self.snake=SNAKE()
            self.fruit=FRUIT()

        def update(self):
            self.snake.move_snake()
            self.check_collision()
            self.check_fail()

        def draw_elements(self):
            self.snake.draw_snake()
            self.fruit.draw_fruit()
            self.draw_score()

        def check_collision(self):
            if self.fruit.pos == self.snake.body[0]:
                self.fruit.randomize()
                # clock.tick(30)
                self.snake.play_crunch_sound()
                self.snake.add_block()

        def check_fail(self):
            if (not (0 <= (self.snake.body[0].x )< (cell_number)) or (not (0 <= (self.snake.body[0].y )< (cell_number)))):
                self.game_over()

            for block in self.snake.body[1:]:
                if block == self.snake.body[0]:
                    self.game_over()

        def game_over(self):
            self.snake.reset()

        def draw_score(self):
            score_text = str(len(self.snake.body) - 3)
            score_surface = game_font.render(score_text,True,(128,0,128))
            score_x = int((cell_size * cell_number)- 60)
            score_y = int((cell_size * cell_number)- 40)

            score_rect = score_surface.get_rect(center = (score_x,score_y))
            mouse_rect = mouse.get_rect(midright = (score_rect.left,score_rect.centery))

            bg_rect = pygame.Rect(mouse_rect.left,mouse_rect.top,mouse_rect.width + score_rect.width + 6,mouse_rect.height)

            pygame.draw.rect(screen,(167,209,61),bg_rect)


            screen.blit(score_surface,score_rect)
            screen.blit(mouse,mouse_rect)

            pygame.draw.rect(screen,(56,74,12),bg_rect,2)

    # class Background(pygame.sprite.Sprite):
    #     def __init__(self, image_file, location):
    #         pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
    #         self.image = pygame.image.load('background_image1.jpg').convert_alpha()
    #         self.rect = self.image.get_rect()
    #         self.rect.left, self.rect.top = location


    pygame.mixer.pre_init(44100,-16,2,512)
    pygame.init()


    icon = pygame.image.load(os.path.join('static','Logo.png'))
    pygame.display.set_icon(icon)

    cell_number = 20
    cell_size = 40
    screen = pygame.display.set_mode((cell_number*cell_size,cell_number*cell_size))
    mouse = pygame.image.load(os.path.join('static','mouse(1).png')).convert_alpha()

    clock = pygame.time.Clock()

    game_font = pygame.font.Font('static/Kenthir.ttf', 25)


    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE,150)
    pygame.display.set_caption("SLYTHERIN")
    # icon = pygame.image.load("Logo.png")
    # icon=pygame.transform.scale(icon, (32,32))
    icon = pygame.image.load(os.path.join('static','Logo.png'))
    pygame.display.set_icon(icon)

    background = pygame.image.load(os.path.join('static','background_image1.png')).convert(24)
    background.set_alpha(128)
    # def blit_alpha(target, source, location, opacity):
    #         x = location[0]
    #         y = location[1]
    #         temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    #         temp.blit(target, (-x, -y))
    #         temp.blit(source, (0, 0))
    #         temp.set_alpha(opacity)        
    #         target.blit(temp, location)


    main_game = MAIN()

    running = True

    while running:
        screen.fill((255,255,255))
        # icon = pygame.image.load('Logo.png') #.convert_alpha()
        # icon=pygame.transform.scale(icon, (32,32))
        # pygame.display.set_icon(icon)

        # BackGround = Background('background_image.jpg', [0,0])
        # icon=pygame.transform.scale(icon, (800,800))
        # screen.blit(BackGround.image, BackGround.rect)

        # screen.blit(screen,background,[200,200],128)
        screen.blit(background,[0,0])
        # screen.blit(icon)
        # pygame.display.set_icon(icon)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == SCREEN_UPDATE:
                main_game.update()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if main_game.snake.direction.y != 1:                    
                        main_game.snake.direction = Vector2(0,-1)
                if event.key == pygame.K_DOWN:
                    if main_game.snake.direction.y != -1:  
                        main_game.snake.direction = Vector2(0,1)
                if event.key == pygame.K_LEFT:
                    if main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1,0)
                if event.key == pygame.K_RIGHT:
                    if main_game.snake.direction.x != -1: 
                        main_game.snake.direction = Vector2(1,0)

        icon = pygame.image.load(os.path.join('static','Logo.png'))
        pygame.display.set_icon(icon)

        main_game.draw_elements()

        pygame.display.update()
        clock.tick(60)
    pygame.quit()
    name=request.GET["name"]
    points="As Shown In The Game"
    return render(request, 'Scorecard.html',{"name":name,"score":points})