from django.shortcuts import render
from django.http import HttpResponse
import pygame, sys, time, random
from pygame.constants import KEYDOWN
from pygame.math import Vector2
# Create your views here.
def home(request):
    return render(request, 'home.html')
def g1(request):
    pygame.init()

    win = pygame.display.set_mode((700, 500))
    pygame.display.set_caption("a vs b")

    x = 50
    y = 400

    width = 50
    height = 60
    speed = 7
    isjump = False
    jumpheight=10
    run = True

    while run:
        pygame.time.delay(50)

        for event in pygame.event.get():

            if event.type==pygame.QUIT:
                run=False
        keys=pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and x>speed:
            X-=speed
        if keys[pygame.K_RIGHT] and x<500-width-speed:
            x+=speed

        if isjump ==False:
            if keys[pygame.K_UP]:
                isjump==True

        else:
            if jumpheight>=-10:
                initial=1

                if jumpheight<0:
                    intial=-1
                y=y-((jumpheight**2)*0.5*initial)
                jumpheight-=1
            else:
                isjump=False
                jumpheight=10


        win.fill((0,0,0))
        pygame.draw.rect(win,(255,255,255),(x,y,width,height))
        pygame.display.update()
    pygame.quit()
    return render(request, 'home.html')
def g2(request):
    snake_block = 20
    cells = 30

    class FOOD:
        def __init__(self):
            self.x = random.randint(0, cells - 1)
            self.y = random.randint(0, cells - 1)
            self.pos = Vector2(self.x, self.y)

        def food_draw(self):
            food_rect = pygame.Rect(self.pos.x * snake_block, self.pos.y * snake_block, snake_block, snake_block)
            pygame.draw.rect(display,(pygame.Color('red')), food_rect)

        def randomiser(self):
            self.x = random.randint(0, cells - 1)
            self.y = random.randint(0, cells - 1)
            self.pos = Vector2(self.x, self.y)

    class SNAKE:
        def __init__(self):
            self.body = [Vector2(6, 10), Vector2(7, 10), Vector2(8, 10)]
            self.dir = Vector2(1, 0)
            self.grow = False

        def draw_snake(self):
                for block in self.body:
                    snake_rect = pygame.Rect(block.x * snake_block, block.y * snake_block, snake_block, snake_block)
                    pygame.draw.rect(display, (pygame.Color('gold')), snake_rect)

        def move(self):
            if self.grow == False:
                step = self.body[:-1]
                step.insert(0, step[0] + self.dir)
                self.body = step[:]
            else:
                step = self.body[:]
                step.insert(0, step[0] + self.dir)
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
            if self.food.pos == self.snake.body[0]:
                self.food.randomiser()
                self.snake.add()

        #def cut(self):
        #    if not 0 <= self.snake.body[0] <= 

    pygame.init()

    game = MAIN()

    SCREENUPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREENUPDATE, 150)

    dis_height = snake_block * cells
    dis_width = snake_block * cells

    display = pygame.display.set_mode((dis_height, dis_width))
    pygame.display.set_caption('Snake Game By Amadeus')

    clock = pygame.time.Clock();

    snake = 10
    speed = 60

    surface = pygame.Surface((100, 200))

    lightblue = (135, 206, 235)

    gameover = False
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
        game.eat()
        pygame.display.update()
        clock.tick(speed)
    pygame.quit()
    return render(request, 'home.html')