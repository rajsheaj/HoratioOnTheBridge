
import pygame
import os
import time
import random
import math

WIDTH, HEIGHT = 1200, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SIC SEMPER TYRANNIS")
pygame.font.init()

TIBER = pygame.transform.scale(pygame.image.load(os.path.join("assets", "tiber.png")), (WIDTH, HEIGHT))
SCROLL = pygame.transform.scale(pygame.image.load(os.path.join("assets", "scroll.png")), (WIDTH, HEIGHT))
HORATIO = pygame.transform.scale(pygame.image.load(os.path.join("assets", "horatio.jpg")), (50, 50))
ENEMY = pygame.transform.scale(pygame.image.load(os.path.join("assets", "enemy.png")), (50, 50))
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (48, 28, 2)
HOR_VEL = 3
ENEMY_VEL = 1
JAVELIN_A = 0.7 #10
JAVELIN_B = 0.8 #15
JAVELIN_C = 0.9  #20
level = 0
lives = 5
main_font = pygame.font.SysFont("comicsans", 50)
lost_font = pygame.font.SysFont("comicsans", 30)
enemies = []
bridges = []
wave_length = 0
Bridge_X = 680
Bridge_Y = 273
bridge_count = 0


# setup game loop
FPS = 60
clock = pygame.time.Clock()
run = True
lost = False
first = True

class Bridge:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, window):
        #pygame.draw.rect(win, BROWN, (680, 273, 70, 20))
        pygame.draw.rect(win, BROWN, (self.x, self.y, 70, 20))

class Projectile:
    def __init__(self, x, y, velocity):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.trajectory = "Up"

    def draw(self, window):
        pygame.draw.rect(window, BLACK, (self.x, self.y + 30, 10, 3))

    #def move(self):
        #self.x = self.x + self.velocity

    def move(self):

        velx = math.cos(self.velocity) * 15
        vely = math.sin(self.velocity) * 15

        distX = velx * 1
        distY = (vely * 1) + ((-4.9 * (1 ** 2)) / 2)

        self.x = round(distX + self.x)
        if self.y < 20:
            self.trajectory = "Down"

        if self.trajectory == "Up":
            self.y = round(self.y - distY)
        else:
            self.y = round(self.y + distY)

    def off_screen(self, width):
        #print(self.x, " ", self.y)
        return not((self.x <= width) and (self.y < 250))

    def collision(self, obj):

        offset_x = obj.x - self.x
        offset_y = obj.y - self.y
        #print(offset_x)
        if 0 < offset_x < 30 and 0 < offset_y < 30:
            print(offset_x, " ", offset_y)
            return True

class Vir():

    COOLDOWN = 10

    def __init__(self, x, y, health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.img = None
        self.mask = None
        self.javelin = []
        self.cool_down_counter = 0

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter >= 0:
            self.cool_down_counter += 1

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
        for j in self.javelin:
            j.draw(window)

    def get_width(self):
        return self.img.get_width()

    def get_height(self):
        return self.img.get_height()

    def shoot(self, speed):
        if self.cool_down_counter == 0:
            jav = Projectile(self.x, self.y, speed)
            self.javelin.append(jav)

    def move_proj(self):
        self.cooldown()
        for jav in self.javelin:
            jav.move()
            if jav.off_screen(WIDTH):
                self.javelin.remove(jav)
            else:
                for enemy in enemies:
                    if jav.collision(enemy):
                        enemies.remove(enemy)
                        self.javelin.remove(jav)


class Roman(Vir):
    def __init__(self, x, y, health = 100):
        super().__init__(x, y, health)
        self.img = HORATIO
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        super().draw(window)

class Etruscan(Vir):
    def __init__(self, x, y, health = 100):
        super().__init__(x, y, health)
        self.img = ENEMY
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        super().draw(window)

    def move(self, vel):
        self.x -= vel

def display_message():
    win.blit(SCROLL, (0, 0))
    str = "The year is 509 BC. The Etruscans led by Lars Porsena march on"
    lost_label = lost_font.render(str, True, BLACK)
    win.blit(lost_label, (270, 200))

    str = " Rome to destroy the newly formed Roman Republic."
    lost_label = lost_font.render(str, True, BLACK)
    win.blit(lost_label, (270, 230))

    str = "The Etruscans vastly outnumber the Romans but they still have"
    lost_label = lost_font.render(str, True, BLACK)
    win.blit(lost_label, (270, 260))

    str = "to cross the Pons Sublicus, the only bridge across the river Tiber."
    lost_label = lost_font.render(str, True, BLACK)
    win.blit(lost_label, (270, 290))

    str = "In their defence, the Romans have destroyed the bridge but"
    lost_label = lost_font.render(str, True, BLACK)
    win.blit(lost_label, (270, 320))

    str = "will they be able to stave off the repeated Etruscan onslaught?"
    lost_label = lost_font.render(str, True, BLACK)
    win.blit(lost_label, (270, 350))

    str = "You play Publius Horatius Cocles, the hero of the Romans."
    lost_label = lost_font.render(str, True, BLACK)
    win.blit(lost_label, (270, 380))

    str = "May the God Mars infuse your soul with courage!"
    lost_label = lost_font.render(str, True, BLACK)
    win.blit(lost_label, (270, 410))


    pygame.display.update()
    pygame.time.delay(6000)

def draw():

    win.blit(TIBER, (0,0))
    lives_label = main_font.render(f"Lives: {lives}", True, BLACK)
    level_label = main_font.render(f"Level: {level}", True, BLACK)

    win.blit(lives_label, (10, 10))
    win.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))



    horatio.draw(win)
    for enemy in enemies:
        enemy.draw(win)
    for b in bridges:
        b.draw(win)


    pygame.display.update()

    if lost:
        lost_label = lost_font.render("YOU LOST! LARS PORSENA HAS SNUFFED OUT A NASCENT ROMAN REPUBLIC!!", True, BLACK)
        win.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 200))
        pygame.display.update()
        pygame.time.delay(2000)

horatio = Roman(300, 220)

while run:
    clock.tick(FPS)

    if first:
        display_message()
        first = False

    if lost:
        run = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and horatio.x - HOR_VEL > 0:  # left
        horatio.x -= HOR_VEL
    if keys[pygame.K_RIGHT] and horatio.x + HOR_VEL + horatio.get_width() < WIDTH - 800:  # right
        horatio.x += HOR_VEL
    if keys[pygame.K_a]:
        horatio.shoot(JAVELIN_A)
    if keys[pygame.K_s]:
        horatio.shoot(JAVELIN_B)
    if keys[pygame.K_d]:
        horatio.shoot(JAVELIN_C)

    horatio.move_proj()

    if len(enemies) == 0:
        level += 1
        wave_length += 1

        for i in range(wave_length):
            enemy = Etruscan(random.randrange(1250, 1800), 220)
            enemies.append(enemy)

    for enemy in enemies[:]:
        enemy.move(ENEMY_VEL)

        if enemy.x < 730:
            enemies.remove(enemy)
            lives -= 1
            brid = Bridge(Bridge_X, Bridge_Y)
            bridges.append(brid)
            Bridge_X -= 75
            bridge_count += 1

        if bridge_count == 5:
            lost = True

    draw()

pygame.quit()
