import pygame
import random
import time

pygame.init()

WIDTH, HEIGHT = 600, 600
GROUND_HEIGHT = HEIGHT - 50
GAME_SPEED = 10

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MY DINO")

dino_img = pygame.image.load('dino.png')
dino_img = pygame.transform.scale(dino_img, (44, 56))
cactus_img = pygame.image.load('cactus.png')
cactus_img = pygame.transform.scale(cactus_img, (20, 40))

class Dino:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 44
        self.height = 56
        self.is_jumping = False
        self.jump_count = 10
        self.is_dead = False

    def draw(self, win):
        win.blit(dino_img, (self.x, self.y))

class Cactus:
    def __init__(self, x):
        self.x = x
        self.y = GROUND_HEIGHT - 40
        self.width = 20
        self.height = 40
        self.speed = GAME_SPEED

    def draw(self, win):
        win.blit(cactus_img, (self.x, self.y))

dino = Dino(50, GROUND_HEIGHT - 56)

cacti = []
score = 0
font = pygame.font.SysFont('comicsans', 30)
next_cactus_time = 0

clock = pygame.time.Clock()
run = True
while run:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    current_time = pygame.time.get_ticks()
    if current_time > next_cactus_time:
        cacti.append(Cactus(WIDTH))
        next_cactus_time = current_time + random.randint(1000, 3000)

    for cactus in cacti:
        if dino.x < cactus.x + cactus.width and dino.x + dino.width > cactus.x and dino.y < cactus.y + cactus.height and dino.y + dino.height > cactus.y:
            dino.is_dead = True
            break

    for cactus in cacti:
        cactus.x -= cactus.speed

    if cacti and cacti[0].x < -cacti[0].width:
        cacti.pop(0)
        score += 1

    keys = pygame.key.get_pressed()
    if not dino.is_jumping and keys[pygame.K_SPACE]:
        dino.is_jumping = True
    if dino.is_jumping:
        if dino.jump_count >= -10:
            neg = 1
            if dino.jump_count < 0:
                neg = -1
            dino.y -= (dino.jump_count ** 2) * 0.5 * neg
            dino.jump_count -= 1
        else:
            dino.is_jumping = False
            dino.jump_count = 10

    if dino.is_dead:
        time.sleep(3)
        dino.is_dead = False
        cacti = []
        score = 0

    win.fill(WHITE)
    dino.draw(win)
    for cactus in cacti:
        cactus.draw(win)
    else:
        text = font.render("Score: " + str(score), True, BLACK)
        win.blit(text, (10, 10))
    pygame.display.update()

pygame.quit()