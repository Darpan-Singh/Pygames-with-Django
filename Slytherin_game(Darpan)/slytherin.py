import pygame,sys,random
from pygame.math import Vector2

class SNAKE:
    def __init__(self):
        self.body = [Vector2(7,10),Vector2(6,10),Vector2(5,10)]
        self.direction = Vector2(0
        ,0)
        self.new_block = False

        self.head_up = pygame.image.load('head_up.png').convert_alpha()
        self.head_up=pygame.transform.scale(self.head_up, (40, 40))

        self.head_down = pygame.image.load('head_down.png').convert_alpha()
        self.head_down=pygame.transform.scale(self.head_down, (40, 40))

        self.head_right = pygame.image.load('head_right.png').convert_alpha()
        self.head_right=pygame.transform.scale(self.head_right, (40, 40))

        self.head_left = pygame.image.load('head_left.png').convert_alpha()
        self.head_left=pygame.transform.scale(self.head_left, (40, 40))
        
        self.tail_up = pygame.image.load('tail_up.png').convert_alpha()
        self.tail_up=pygame.transform.scale(self.tail_up, (40, 40))

        self.tail_down = pygame.image.load('tail_down.png').convert_alpha()
        self.tail_down=pygame.transform.scale(self.tail_down, (40, 40))
        
        self.tail_right = pygame.image.load('tail_right.png').convert_alpha()
        self.tail_right=pygame.transform.scale(self.tail_right, (40, 40))

        self.tail_left = pygame.image.load('tail_left.png').convert_alpha()
        self.tail_left=pygame.transform.scale(self.tail_left, (40, 40))

        self.body_vertical = pygame.image.load('body_vertical.png').convert_alpha()
        self.body_vertical=pygame.transform.scale(self.body_vertical, (40, 40))

        self.body_horizontal = pygame.image.load('body_horizontal.png').convert_alpha()
        self.body_horizontal=pygame.transform.scale(self.body_horizontal, (40, 40))

        
        self.body_tr = pygame.image.load('body_tr.png').convert_alpha()
        self.body_tr=pygame.transform.scale(self.body_tr, (40, 40))

        self.body_tl = pygame.image.load('body_tl.png').convert_alpha()
        self.body_tl=pygame.transform.scale(self.body_tl, (40, 40))

        self.body_br = pygame.image.load('body_br.png').convert_alpha()
        self.body_br=pygame.transform.scale(self.body_br, (40, 40))

        self.body_bl = pygame.image.load('body_bl.png').convert_alpha()
        self.body_bl=pygame.transform.scale(self.body_bl, (40, 40))
        self.crunch_sound = pygame.mixer.Sound('aud_chomp(1).wav')

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


icon = pygame.image.load('Logo.png')
pygame.display.set_icon(icon)

cell_number = 20
cell_size = 40
screen = pygame.display.set_mode((cell_number*cell_size,cell_number*cell_size))
mouse = pygame.image.load('mouse(1).png').convert_alpha()

clock = pygame.time.Clock()

game_font = pygame.font.Font('font/Kenthir.ttf', 25)


SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)
pygame.display.set_caption("SLYTHERIN")
# icon = pygame.image.load("Logo.png")
# icon=pygame.transform.scale(icon, (32,32))
icon = pygame.image.load('Logo.png')
pygame.display.set_icon(icon)

background = pygame.image.load('background_image1.png').convert(24)
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

    icon = pygame.image.load('Logo.png')
    pygame.display.set_icon(icon)

    main_game.draw_elements()

    pygame.display.update()
    clock.tick(60)