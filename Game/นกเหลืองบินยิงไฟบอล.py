import pygame
import time
import random
import os

Icon = pygame.image.load('Bird3.png')
pygame.display.set_icon(Icon)
FPS = 30
#ขนาดหน้าจอ
width = 800
height = 600
#สี
black=(0,0,0)
white=(225,225,225)
blue=(0,0,225)
red=(225,0,0)
#จัดโปรแกรม
pygame.init()
pygame.mixer.init()
#จัดหน้าจอ
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('Bird')
clock = pygame.time.Clock()

#สร้างตัวละคร
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder,'img')

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #ใส่ภาพนก
        Bird_img = os.path.join(img_folder,'Bird3.png')
        self.image = pygame.image.load(Bird_img).convert()
        #self.image.fill(blue)
        self.rect = self.image.get_rect()
        #ตำแหน่งของนก
        self.rect.centerx = int(20)
        self.rect.centery = int(600/2)

        self.speedy = 0
    #การขยับ
    def update(self):
        self.speedy = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_UP]:
            self.speedy = -10
        if key[pygame.K_DOWN]:
            self.speedy = 10
        self.rect.y += self.speedy
        #จำกัดเขต
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > height:
            self.rect.bottom = height
    #การยิ่ง
    def shoot(self):
        fireball = Fireball(self.rect.centery,self.rect.top)
        all_sprites.add(fireball)
        fireballs.add(fireball)

#สิ่งกีดขวาง
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        Bird_img = os.path.join(img_folder,'Enemy.jpg')
        self.image = pygame.image.load(Bird_img).convert()
        #self.image = pygame.Surface((30,40))
        #self.image.fill(blue)
        self.rect = self.image.get_rect()
        self.rect.y = random.randrange(height - self.rect.height)
        self.rect.x = random.randrange(800,850)
        self.speedx = random.randrange(5,10)
    #ตำแหน่งสิ่งกีดขวางที่จะเกิด
    def update(self):
        self.rect.x -= self.speedx
        if self.rect.right < 0:
            self.rect.y = random.randrange(height - self.rect.height)
            self.rect.x = random.randrange(800,850)
            self.speedx = random.randrange(1,5)

#ไฟเยอร์บอลลลล
class Fireball(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        Bird_img = os.path.join(img_folder,'Fire.png')
        self.image = pygame.image.load(Bird_img).convert()
        #self.image = pygame.Surface((20,10))
        #self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.bottom = x
        self.rect.centery = y
        self.speedx = 50
    #ตำแหน่งที่ไฟบอลออกมา
    def update(self):
        self.rect.x += self.speedx
        if self.rect.left < 0:
            self.kill()

all_sprites = pygame.sprite.Group()
Bird = Bird()
all_sprites.add(Bird)

enemy = pygame.sprite.Group()

fireballs = pygame.sprite.Group()

for i in range(10):
    em = Enemy()
    all_sprites.add(em)
    enemy.add(em)

#RunProgram        
run = True

while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        #ยิ่งไฟเมื่อกดspace
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                Bird.shoot()

    all_sprites.update()
    #สิ่งกีดขวางโดนไฟแล้วหายไป สร้างขึ้นมาใหม่
    hit = pygame.sprite.groupcollide(enemy,fireballs,True,True)
    if hit:
        em = Enemy()
        all_sprites.add(em)
        enemy.add(em)
    #ถ้าสิ่งกีดขวางโดนตัว ออกเกม
    hit = pygame.sprite.spritecollide(Bird,enemy,False)
    if hit:
        run = False

    screen.fill(black)
    all_sprites.draw(screen)
    pygame.display.flip()


pygame.quit()
