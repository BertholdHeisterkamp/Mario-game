#!/bin/python3

import pygame
import random
#import mysql.connector
import math
from pygame.locals import (
        RLEACCEL,
        K_UP,
        K_DOWN,
        K_LEFT,
        K_RIGHT,
        K_ESCAPE,
        KEYDOWN,
        QUIT,
        K_x
        )


lives = 3
time_livestext = 0
level = 1
score = 0

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("player.png")
        self.surf = pygame.transform.scale(self.surf, (50, 50))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
                center=(25, 575)
        )
        self.yspeed = 0
        self.xspeed = 0
        self.actualxspeed = 0
        self.invincible = 0
    def update(self, pressed_keys):
        global accelerate
        global negative_accelerate
        global jump_longer
        global i
        global testifbigmario
        jump_active = False
        global r
        global x
        global s
        global standingonsolid
        global k
        global lives
        global testiffiremario
        if CheckIfPlayerExceedsBoundsBool():
            standingonsolid = True
        if not standingonsolid:
            self.yspeed = -5
            jump_active = False
        if self.yspeed == 0:
            jump_active = True
        if self.xspeed < 7:
            if accelerate:
                if pressed_keys[K_RIGHT]:
                    self.xspeed = self.xspeed + 0.5
                else:
                    accelerate = False
                    self.xspeed = 0
        if self.xspeed > -7:
            if negative_accelerate:
                if pressed_keys[K_LEFT]:
                    self.xspeed = self.xspeed - 0.5 
                else:
                    negative_accelerate = False
                    self.xspeed = 0
        if not accelerate:
            if pressed_keys[K_RIGHT]:
                self.xspeed = 2
                accelerate = True
        if not negative_accelerate:
            if pressed_keys[K_LEFT]:
                self.xspeed = -2
                negative_accelerate = True
        if not pressed_keys[K_RIGHT] and not pressed_keys[K_LEFT]:
            self.xspeed = 0
        if not jump_active:
            if jump_longer and x <= 400:
                if pressed_keys[K_UP]:
                    r = r + 15
                    x = x + 15
                    s = -x
                elif r < s:
                    r = r - 10
                    x = self.rect.bottom 
                    s = -x
            elif r < s:
                r = r - 10
                x = self.rect.bottom
                s = -x
        if jump_active:
            if pressed_keys[K_UP]:
                if r < s:
                    x = 200
                    r = x
                    s = -r
                    jump_longer = True
        if not pressed_keys[K_UP]:
            jump_longer = False
        if r >= s:
            self.yspeed = r / 20
            if r >= 0:
                r = r - 13
            elif r < 0:
                r = r- 10
        self.rect.move_ip(self.xspeed, -self.yspeed)
        i = i - self.actualxspeed
        k = k + self.actualxspeed
        print(k)
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= screen_width / 2:
            self.rect.right = screen_width / 2
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.top >= screen_height:
            self.kill()
            lives = lives - 1
        self.invincible = self.invincible - 1
    def GetDamage(self):
        global testifbigmario
        global testiffiremario
        if testiffiremario == 1:
            player.surf = pygame.image.load("player.png")
            player.surf = pygame.transform.scale(player.surf, (50, 80))
            player.surf.set_colorkey((255, 255, 255), RLEACCEL)
            testifbigmario = 1
            testiffiremario = 0
            self.invincible = 120
        elif testifbigmario == 1:
            self.surf = pygame.image.load("player.png")
            self.surf = pygame.transform.scale(self.surf, (50, 50))
            self.surf.set_colorkey((255, 255, 255), RLEACCEL)
            testifbigmario = 0
            self.rect.bottom = self.rect.bottom + 25
            self.invincible = 120
class Goomba(pygame.sprite.Sprite):
    def __init__(self, associated=None):
        super(Goomba, self).__init__()
        self.surf = pygame.image.load("goomba.jpeg")
        self.surf = pygame.transform.scale(self.surf, (30, 30))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
                center = (screen_width + 20, 545)
        )
        self.speed = 2
        self.associated = associated
        self.direction = 1
        self.yspeed = 0
        self.floor_active = True
        self.dead = False
    def update(self):
        global testifbigmario
        global score
        if pressed_keys[K_LEFT] and player.rect.left == 0:
            self.speed = 2 * self.direction + player.actualxspeed
        elif pressed_keys[K_RIGHT] and player.rect.right == screen_width / 2:
            self.speed = 2 * self.direction + player.actualxspeed
        else:
            self.speed = 2 * self.direction
        if pygame.sprite.spritecollideany(self, löcher):
            self.floor_active = False
        if not self.floor_active:
            self.yspeed = self.yspeed + 0.5
        self.rect.move_ip(-self.speed, self.yspeed)
        if self.rect.colliderect(player):
            if player.rect.centery < self.rect.top and testifbigmario == 0:
                self.kill()
                score = score + 500
            elif player.rect.centery + 15 < self.rect.top and testifbigmario == 1:
                self.kill()
                score = score + 500
        if pygame.sprite.spritecollideany(self, blocks) or pygame.sprite.spritecollideany(self, pipes):
            self.direction = self.direction * -1
        if self.dead:
            self.kill()
class Itemblock(pygame.sprite.Sprite):
    def __init__(self):
        super(Itemblock, self).__init__()
        self.surf = pygame.image.load("itemblock.jpeg")
        self.surf = pygame.transform.scale(self.surf, (30, 30))
        self.rect = self.surf.get_rect(
                center = (screen_width + 20, 420)
        )
        self.xspeed = 0
        self.const = 0
    def update(self):
        global jump_longer
        global standingonsolid
        global standingonblock
        global r
        global s
        global x
        global runningintoblock
        global testifbigmario
        self.xspeed = player.actualxspeed
        self.rect.move_ip(-self.xspeed, 0)
        if player.yspeed != 0:
            if self.rect.colliderect(player) and self.const == 0 and player.yspeed > 0 and player.rect.centery > self.rect.bottom:
                if testifbigmario == 0:
                    global new_pilz
                    new_pilz = Pilz(self.rect.x, self.rect.y)
                    pilze.add(new_pilz)
                    all_sprites.add(new_pilz)
                elif testifbigmario == 1:
                    global new_fireflower
                    new_fireflower = Fireflower(self.rect.x + 20, self.rect.y + 15)
                    fireflowers.add(new_fireflower)
                    all_sprites.add(new_fireflower)
                player.rect.y = self.rect.y + 35
                player.yspeed = 0
                r = -10 
                s = 0 
                x = r
                self.const = 1
                self.surf = pygame.image.load("empty.jpeg")
                self.surf = pygame.transform.scale(self.surf, (30, 30))
                jump_longer = False
            elif self.rect.colliderect(player) and self.const == 1 and player.yspeed > 0 and player.rect.centery > self.rect.bottom:
                player.rect.y = self.rect.y + 35
                player.yspeed = 0
                r = -10
                s = 0
                x = r
                jump_longer = False
            elif self.rect.colliderect(player) and player.yspeed < 0 and player.rect.centery < self.rect.top:
                if testifbigmario == 0:
                    player.rect.bottom = self.rect.top + 5
                elif testifbigmario == 1:
                    player.rect.bottom = self.rect.top - 20
                player.yspeed = 0
                r = -10 
                s = 0 
                x = r
            elif self.rect.colliderect(player) and player.xspeed > 0 and player.rect.left < self.rect.left:
                player.rect.x = self.rect.x - 45
                player.yspeed = -5
            elif self.rect.colliderect(player) and player.xspeed < 0 and player.rect.right > self.rect.right:
                player.rect.left = self.rect.right 
                player.yspeed = -5
        if player.rect.x == self.rect.x - 45 and not self.CheckIfPlayerStandsOnBlock():
            runningintoblock = True
        elif player.rect.x == self.rect.x + 30 and not self.CheckIfPlayerStandsOnBlock() and player.xspeed < 0:
            runningintoblock = True
        if self.CheckIfPlayerStandsOnBlock():
            standingonsolid = True
            standingonblock = True
        if self.rect.right < 0:
            self.kill()

    def CheckIfPlayerStandsOnBlock(self):
        global testifbigmario
        if player.rect.bottom == self.rect.top + 5 and testifbigmario == 0 and (self.rect.left < player.rect.left < self.rect.right or self.rect.left < player.rect.right < self.rect.right or self.rect.left < player.rect.centerx < self.rect.right):
            return True
        elif player.rect.bottom == self.rect.top - 20 and testifbigmario == 1 and (self.rect.left < player.rect.left < self.rect.right or self.rect.left < player.rect.right < self.rect.right or self.rect.left < player.rect.centerx < self.rect.right):
            return True
        else:
            return False

class Pilz(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Pilz, self).__init__()
        self.surf = pygame.image.load("pilz.jpeg")
        self.surf = pygame.transform.scale(self.surf, (30, 30))
        self.surf.set_colorkey((1, 1, 1))
        self.rect = self.surf.get_rect(
                center = (x, y - 30)
        )
        self.xspeed = 3
        self.yspeed = 3 
        self.direction = 1
        self.floor_active = True
    def update(self):
        if pressed_keys[K_LEFT] and player.rect.left == 0:
            self.xspeed = 3 * self.direction + player.actualxspeed 
        elif pressed_keys[K_RIGHT] and player.rect.right == screen_width / 2:
            self.xspeed = 3 * self.direction + player.actualxspeed
        else:
            self.xspeed = 3 * self.direction
        self.rect.move_ip(-self.xspeed, self.yspeed)
        if self.rect.colliderect(new_itemblock):
            self.rect.bottom = new_itemblock.rect.top
        if pygame.sprite.spritecollideany(self, blocks):
            self.direction = self.direction * -1
        if pygame.sprite.spritecollideany(self, pipes):
            self.direction = self.direction * -1
        if pygame.sprite.spritecollideany(self, löcher):
            self.floor_active = False
        if self.floor_active:
            if self.rect.bottom > 555:
                self.rect.bottom = 555
                self.yspeed = 0
            else:
                self.yspeed = self.yspeed + 0.25
        if not self.floor_active:
            self.yspeed = self.yspeed + 0.25

class Fireflower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Fireflower, self).__init__()
        self.surf = pygame.image.load("fireflower.png")
        self.surf = pygame.transform.scale(self.surf, (30, 30))
        self.surf.set_colorkey((247, 247, 247))
        self.rect = self.surf.get_rect(
                center = (x, y - 30)
        )
        self.xspeed = 0
        self.yspeed = 0
        self.killed = False
    def update(self):
        self.xspeed = player.actualxspeed
        self.rect.move_ip(-self.xspeed, self.yspeed)
        if self.rect.colliderect(new_itemblock):
            self.rect.bottom = new_itemblock.rect.top
        if self.killed:
            self.kill()
        if self.rect.colliderect(player):
            self.killed = True
class FeuerballMario(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(FeuerballMario, self).__init__()
        self.surf = pygame.image.load("feuerball.png")
        self.surf = pygame.transform.scale(self.surf, (10, 10))
        for a in range(220, 255):
            self.surf.set_colorkey((a, a, a), RLEACCEL)
        self.rect = self.surf.get_rect(
                center=(x, y)
        )
        self.xspeed = 0
    def update(self):
        self.xspeed = player.actualxspeed - 8
        self.rect.move_ip(-self.xspeed, 1)
        if pygame.sprite.spritecollideany(self, goombas):
            self.kill()
            new_goomba.dead = True
        elif pygame.sprite.spritecollideany(self, bowsers):
            self.kill()
            new_bowser.damage = True
class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Block, self).__init__()
        self.surf = pygame.image.load("block.png")
        self.surf = pygame.transform.scale(self.surf, (30, 30))
        self.rect = self.surf.get_rect(
                center = (x, y)
        )
        self.xspeed = 0
        self.yspeed = 0
    def update(self):
        global jump_longer
        global t
        global standingonsolid
        global standingonblock
        global runningintoblock
        global x
        global s
        global r
        if player.yspeed != 0:
            if self.rect.colliderect(player) and player.yspeed > 0 and player.rect.centery > self.rect.bottom:
                player.rect.y = self.rect.y + 35
                player.yspeed = 0
                r = -10
                s = 0
                x = r
                jump_longer = False
            elif self.rect.colliderect(player) and player.yspeed < 0 and player.rect.centery < self.rect.top:
                if testifbigmario == 0:
                    player.rect.bottom = self.rect.top + 5
                elif testifbigmario == 1:
                    player.rect.bottom = self.rect.top - 20
                player.yspeed = 0
                r = -10 
                s = 0 
                x = r
            elif self.rect.colliderect(player) and player.xspeed > 0 and player.rect.left < self.rect.left:
                player.rect.x = self.rect.x - 45
                player.yspeed = -5 
            elif self.rect.colliderect(player) and player.xspeed < 0 and player.rect.right > self.rect.right:
                player.rect.x = self.rect.x + 30
                player.yspeed = -5
        if player.yspeed == 0:
            if not self.CheckIfPlayerStandsOnBlock():
                if self.rect.colliderect(player) and player.xspeed > 0 and player.rect.left < self.rect.left:
                    player.rect.x = self.rect.x - 45
                elif self.rect.colliderect(player) and player.xspeed < 0 and player.rect.right > self.rect.right:
                    player.rect.x = self.rect.x + 30
        if player.rect.x == self.rect.x - 45 and not self.CheckIfPlayerStandsOnBlock():
            runningintoblock = True
        elif player.rect.x == self.rect.x + 30 and not self.CheckIfPlayerStandsOnBlock():
            runningintoblock = True
        if self.CheckIfPlayerStandsOnBlock():
            standingonsolid = True
            standingonblock = True
        self.xspeed = player.actualxspeed
        self.rect.move_ip(-self.xspeed, self.yspeed)


    def CheckIfPlayerStandsOnBlock(self):
        global testifbigmario
        if player.rect.bottom == self.rect.top + 5 and testifbigmario == 0 and (self.rect.left < player.rect.left < self.rect.right or self.rect.left < player.rect.right < self.rect.right or self.rect.left < player.rect.centerx < self.rect.right):
            return True
        elif player.rect.bottom == self.rect.top - 20 and testifbigmario == 1 and (self.rect.left < player.rect.left < self.rect.right or self.rect.left < player.rect.right < self.rect.right or self.rect.left < player.rect.centerx < self.rect.right):
            return True
        else:
            return False

class Loch(pygame.sprite.Sprite):
    def __init__(self):
        super(Loch, self).__init__()
        self.surf = pygame.image.load("bg.png")
        self.rect = self.surf.get_rect(
                center=(screen_width + 80, 620)
        )
    def update(self):
        self.xspeed = player.actualxspeed
        self.rect.move_ip(-self.xspeed, 0)
class Pipe(pygame.sprite.Sprite):
    def __init__(self):
        super(Pipe, self).__init__()
        self.surf = pygame.image.load("pipe.jpeg")
        self.surf = pygame.transform.scale(self.surf, (60, 60))
        self.surf.set_colorkey((246, 246, 246), RLEACCEL)
        self.rect = self.surf.get_rect(
                center=(screen_width + 40, 525)
        )
        self.xspeed = 0
        self.yspeed = 0
    def update(self):
        global t
        global standingonsolid
        global standingonblock
        global runningintoblock
        global testifbigmario
        global jump_longer
        global r
        global s
        global x
        self.xspeed = player.actualxspeed
        if player.yspeed != 0:
            if self.rect.colliderect(player) and player.yspeed < 0 and player.rect.centery < self.rect.top:
                if testifbigmario == 0:
                    player.rect.bottom = self.rect.top + 5
                elif testifbigmario == 1:
                    player.rect.bottom = self.rect.top - 20
                player.yspeed = 0
                r = -10 
                s = 0 
                x = r
                jump_longer = False
            elif self.rect.colliderect(player) and player.xspeed > 0 and player.rect.left < self.rect.left:
                player.rect.x = self.rect.x - 35
                player.yspeed = -5 
            elif self.rect.colliderect(player) and player.xspeed < 0 and player.rect.right > self.rect.right:
                player.rect.x = self.rect.x + 50
                player.yspeed = -5
        if player.yspeed == 0:
            if not self.CheckIfPlayerStandsOnBlock():
                if self.rect.colliderect(player) and player.xspeed > 0 and player.rect.left < self.rect.left:
                    player.rect.x = self.rect.x - 35
                elif self.rect.colliderect(player) and player.xspeed < 0 and player.rect.right > self.rect.right:
                    player.rect.x = self.rect.x + 50
        if player.rect.x == self.rect.x - 35 and not self.CheckIfPlayerStandsOnBlock():
            runningintoblock = True
        elif player.rect.x == self.rect.x + 50 and not self.CheckIfPlayerStandsOnBlock():
            runningintoblock = True
        if self.CheckIfPlayerStandsOnBlock():
            standingonsolid = True
            standingonblock = True
        self.rect.move_ip(-self.xspeed, self.yspeed)


    def CheckIfPlayerStandsOnBlock(self):
        global testifbigmario
        if player.rect.bottom == self.rect.top + 5 and testifbigmario == 0 and (self.rect.left < player.rect.left < self.rect.right or self.rect.left < player.rect.right < self.rect.right or self.rect.left < player.rect.centerx < self.rect.right):
            return True
        elif player.rect.bottom == self.rect.top - 20 and testifbigmario == 1 and (self.rect.left < player.rect.left < self.rect.right or self.rect.left < player.rect.right < self.rect.right or self.rect.left < player.rect.centerx < self.rect.right):
            return True
        else:
            return False
class Bowser(pygame.sprite.Sprite):
    def __init__(self):
        super(Bowser, self).__init__()
        self.surf = pygame.image.load("bowser.png")
        self.surf = pygame.transform.scale(self.surf, (90, 90))
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
                center=(screen_width + 20, 510)
        )
        self.xspeed = 0
        self.leftright = 0
        self.cd = 0
        self.hp = 5
        self.damage = False
    def update(self):
        global new_feuerball
        self.xspeed = player.actualxspeed + (math.cos(self.leftright / 50) * math.sqrt(level))
        self.leftright = self.leftright + 1
        self.rect.move_ip(-self.xspeed, 0)
        print(math.cos(self.leftright / 50))
        self.cd = self.cd + 1
        if self.cd >= 300 / math.sqrt(level):
            self.cd = 0
            new_feuerball = Feuerball(self.rect.left, self.rect.centery)
            feuerbaelle.add(new_feuerball)
            all_sprites.add(new_feuerball)
        if self.damage:
            self.hp = self.hp - 1
            self.damage = False
        if self.hp <= 0:
            self.kill()
class Feuerball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Feuerball, self).__init__()
        self.surf = pygame.image.load("feuerball.png")
        self.surf = pygame.transform.scale(self.surf, (20, 20))
        for a in range(220, 255):
            self.surf.set_colorkey((a, a, a), RLEACCEL)
        self.rect = self.surf.get_rect(
                center=(x, y)
        )
        self.xspeed = 0
    def update(self):
        self.xspeed = player.actualxspeed + 2
        self.rect.move_ip(-self.xspeed, 0)
class Flag(pygame.sprite.Sprite):
    def __init__(self):
        super(Flag, self).__init__()
        self.surf = pygame.image.load("flag.jpg")
        self.surf = pygame.transform.scale(self.surf, (50, 220))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
                center=(screen_width + 20, 445)

        )
        self.xspeed = 0

    def update(self):
        global r
        global s
        global x
        global running
        global score
        global alive
        global level
        global onflag
        self.xspeed = player.actualxspeed
        self.rect.move_ip(-self.xspeed, 0)
        if player.rect.right >= self.rect.centerx and player.rect.y >= 470 and not onflag:
            player.rect.right = self.rect.centerx
        elif player.rect.right >= self.rect.centerx:
            player.rect.right = self.rect.left + 50
            player.yspeed = -1
            r = -10
            s = 0
            x = r
            if player.rect.bottom <= 335:
                player.rect.bottom = 335
            if player.rect.bottom >= 525:
                alive = False
                level = level + 1
            score = score + 10 
            onflag = True
            

def CheckIfPlayerExceedsBounds():
    global r
    global s
    global x
    if player.rect.bottom >= 565 and testifbigmario == 0:
       player.rect.bottom = 565
       player.yspeed = 0
       r = -10 
       s = 0 
       x = r
       return True
       return True
    elif player.rect.bottom >= 540 and testifbigmario == 1:
       player.rect.bottom = 540
       player.yspeed = 0
       r = -10 
       s = 0 
       x = r
       return True
    else:
       return False

def CheckIfPlayerExceedsBoundsBool():
    if player.rect.bottom >= 565 and testifbigmario == 0:
       return True
    elif player.rect.bottom >= 540 and testifbigmario == 1:
       return True
    else:
       return False

game_init = True
running = True

while running:
    if game_init:
        r = -10 
        s = 0 
        x = r
        i = 0
        k = 0
        onflag = False
        screen_width = 800
        screen_height = 600
        testifbigmario = 0
        testiffiremario = 0
        standingonsolid = False
        jump_longer = False
        accelerate = False
        negative_accelerate = False
        standingonblock = False
        runningintoblock = False
        blocksdontmove = False
        name = "Louis"
        player = Player()
        new_goomba = Goomba()
        new_itemblock = Itemblock()
        new_block = Block(0, 0)
        new_pilz = Pilz(0, 0)
        new_fireflower = Fireflower(0, 0)

        all_sprites = pygame.sprite.Group()
        all_sprites.add(player)
        goombas = pygame.sprite.Group()
        itemblocks = pygame.sprite.Group()
        pilze = pygame.sprite.Group()
        blocks = pygame.sprite.Group()
        löcher = pygame.sprite.Group()
        pipes = pygame.sprite.Group()
        bowsers = pygame.sprite.Group()
        feuerbaelle = pygame.sprite.Group()
        flags = pygame.sprite.Group()
        fireflowers = pygame.sprite.Group()
        feuerbällemario = pygame.sprite.Group()
                

        pygame.init()

        screen = pygame.display.set_mode((screen_width, screen_height))

        pygame.display.set_caption('Super Mario Bros')

        bg = pygame.image.load("bg.png")
        bg = pygame.transform.scale(bg, (800, 280))

        addenemy = pygame.USEREVENT + 1
        pygame.time.set_timer(addenemy, 3000)
        addblockline = pygame.USEREVENT + 2
        pygame.time.set_timer(addblockline, 3489)
        addloch = pygame.USEREVENT + 3
        pygame.time.set_timer(addloch, 4289)
        addpipe = pygame.USEREVENT + 4
        pygame.time.set_timer(addpipe, 4819)
        addbowser = pygame.USEREVENT + 7
        pygame.time.set_timer(addbowser, 5415)
        addstairs = pygame.USEREVENT + 5
        pygame.time.set_timer(addstairs, 5832)
        addobstacle = pygame.USEREVENT + 6
        pygame.time.set_timer(addobstacle, 8142)
        additemblock = pygame.USEREVENT - 1
        pygame.time.set_timer(additemblock, 849)
        addflag = pygame.USEREVENT - 2
        pygame.time.set_timer(addflag, 1)

        clock = pygame.time.Clock()
        myfont = pygame.font.SysFont("monospace", 16)

        floor_active = True

        running = True
        alive = True

        versatz = 0
        game_init = False

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
    if alive:
        if event.type == KEYDOWN:
            if event.key == K_x and testiffiremario == 1:
                new_feuerballmario = FeuerballMario(player.rect.right, player.rect.y + 20)
                feuerbällemario.add(new_feuerballmario)
                all_sprites.add(new_feuerballmario)
        if k >= 360000 + 500 * level:
            i = 4000
        if k >= 100000 + 500 * level:
            if event.type == addflag:
                k = 0
                new_flag = Flag()
                flags.add(new_flag)
                all_sprites.add(new_flag)
        if i <= 0:
            if event.type == addenemy:
                i = 100
                new_goomba = Goomba()
                goombas.add(new_goomba)
                all_sprites.add(new_goomba)
            elif event.type == addblockline:
                i = 130
                new_block1 = Block(screen_width + 10, 420)
                blocks.add(new_block1)
                all_sprites.add(new_block1)
                new_block2 = Block(screen_width + 40, 420)
                blocks.add(new_block2)
                all_sprites.add(new_block2)
                new_block3 = Block(screen_width + 70, 420)
                blocks.add(new_block3)
                all_sprites.add(new_block3)
            elif event.type == addstairs:
                i = 130
                new_block1 = Block(screen_width + 10, 545)
                blocks.add(new_block1)
                all_sprites.add(new_block1)
                new_block2 = Block(screen_width + 40, 545)
                blocks.add(new_block2)
                all_sprites.add(new_block2)
                new_block3 = Block(screen_width + 40, 515)
                blocks.add(new_block3)
                all_sprites.add(new_block3)
                new_block4 = Block(screen_width + 70, 545)
                blocks.add(new_block4)
                all_sprites.add(new_block4)
                new_block5 = Block(screen_width + 70, 515)
                blocks.add(new_block5)
                all_sprites.add(new_block5)
                new_block6 = Block(screen_width + 70, 485)
                blocks.add(new_block6)
                all_sprites.add(new_block6)
            elif event.type == addloch:
                i = 450
                new_loch = Loch()
                löcher.add(new_loch)
                all_sprites.add(new_loch)
            elif event.type == additemblock:
                i = 130
                new_itemblock = Itemblock()
                all_sprites.add(new_itemblock)
                itemblocks.add(new_itemblock)
                new_block1 = Block(screen_width + 50, 420)
                blocks.add(new_block1)
                all_sprites.add(new_block1)
                new_block2 = Block(screen_width + 80, 420)
                blocks.add(new_block2)
                all_sprites.add(new_block2)
            elif event.type == addobstacle:
                i = 100
                new_block1 = Block(screen_width + 10, 545)
                blocks.add(new_block1)
                all_sprites.add(new_block1)
                new_block2 = Block(screen_width + 10, 515)
                blocks.add(new_block2)
                all_sprites.add(new_block2)
                new_block3 = Block(screen_width + 10, 485)
                blocks.add(new_block3)
                all_sprites.add(new_block3)
                new_block4 = Block(screen_width + 10, 455)
                blocks.add(new_block4)
                all_sprites.add(new_block4)
            elif event.type == addpipe:
                i = 150
                new_pipe = Pipe()
                pipes.add(new_pipe)
                all_sprites.add(new_pipe)
            elif event.type == addbowser:
                i = 300
                new_bowser = Bowser()
                bowsers.add(new_bowser)
                all_sprites.add(new_bowser)

        if runningintoblock:
            blocksdontmove = True
        else:
            blocksdontmove = False
        if player.xspeed > 0 and player.rect.right >= screen_width / 2:
            if pygame.sprite.spritecollideany(player, blocks):
                if blocksdontmove:
                    player.actualxspeed = 0
                else:
                    player.actualxspeed = player.xspeed
            else:
                player.actualxspeed = player.xspeed
        elif player.xspeed < 0 and player.rect.left <= 0:
            if pygame.sprite.spritecollideany(player, blocks):
                if blocksdontmove:
                    player.actualxspeed = 0
                else: 
                    player.actualxspeed = player.xspeed
            else:
                player.actualxspeed = player.xspeed
        else:
            player.actualxspeed = 0
        blocksdontmove = False
        pressed_keys = pygame.key.get_pressed()
        standingonsolid = False
        standingonblock = False
        runningintoblock = False
        itemblocks.update()
        blocks.update()
        pipes.update()
        löcher.update()
        bowsers.update()
        feuerbaelle.update()
        feuerbällemario.update()
        fireflowers.update()
        player.update(pressed_keys)
        goombas.update()
        pilze.update()
        flags.update()
        versatz = versatz + int(player.actualxspeed) 
        if floor_active:
            CheckIfPlayerExceedsBounds()
        if not floor_active:
            player.yspeed = -5
        screen.blit(bg, (0, 0))
        screen.blit(bg, (0, 150))
        screen.blit(bg, (0 - versatz, 320))
        screen.blit(bg, (800 - versatz, 320))
        screen.blit(bg, (-800 - versatz, 320))
        if versatz >= 800:
            versatz = versatz - 800
        elif versatz <= -800:
            versatz = versatz + 800
        scoretext = myfont.render("Score = "+str(int(score)), 1, (0, 0, 0))
        screen.blit(scoretext, (5, 10))
       #scoreaddtext = myfont.render("+" +str(scoreadd), 1, (0, 0, 0))
       #screen.blit(scoreaddtext, (5, 30))

        
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
            if entity.rect.right <= -400:
                entity.kill()
        if player in all_sprites:
            screen.blit(player.surf, player.rect)
        if floor_active:
            if pygame.sprite.spritecollideany(player, löcher): 
                if new_loch.rect.right > player.rect.left > new_loch.rect.left and new_loch.rect.right > player.rect.right > new_loch.rect.left:
                    jump_active = False
                    floor_active = False
                    s = s - 100
        if pygame.sprite.spritecollideany(player, goombas):
            if player.invincible <= 0:
                if testifbigmario == 0:
                    player.kill()
                    lives = lives - 1
                elif testifbigmario == 1 or testiffiremario == 1:
                    player.GetDamage()
        if pygame.sprite.spritecollideany(player, bowsers):
            if player.invincible <= 0:
                if testifbigmario == 0:
                    player.kill()
                    lives = lives - 1
                elif testifbigmario == 1:
                    player.GetDamage()
        if pygame.sprite.spritecollideany(player, feuerbaelle):
            if player.invincible <= 0:
                if testifbigmario == 0:
                    player.kill()
                    lives = lives - 1
                elif testifbigmario == 1:
                    player.GetDamage()
        if pygame.sprite.spritecollideany(player, pilze):
            score = score + 1000
            player.surf = pygame.image.load("player.png")
            player.surf = pygame.transform.scale(player.surf, (50, 80))
            player.surf.set_colorkey((255, 255, 255), RLEACCEL)
            testifbigmario = 1
            new_pilz.kill()
        if pygame.sprite.spritecollideany(player, fireflowers):
            score = score + 2000
            player.surf = pygame.image.load("firemario.jpeg")
            player.surf = pygame.transform.scale(player.surf, (50, 70))
            player.surf.set_colorkey((255, 255, 255), RLEACCEL)
            testiffiremario = 1
            testifbigmario = 1

        if pygame.sprite.spritecollideany(new_itemblock, blocks):
            new_itemblock.kill()
        score = score + player.actualxspeed

        if player not in all_sprites:
            alive = False

    if not alive:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False
        if lives <= 0:
            running = False
        if lives >= 1:
            screen.fill((0, 0, 0))
            livestext = myfont.render("Lives = "+str(int(lives)), 1, (255, 255, 255))
            leveltext = myfont.render("Level = "+str(int(level)), 1, (255, 255, 255))
            screen.blit(leveltext, (300, 300))
            screen.blit(livestext, (300, 400))
            time_livestext = time_livestext + 1
            if time_livestext >= 120:
                time_livestext = 0
                game_init = True
                alive = True

    pygame.display.flip()

    clock.tick(60)


if not running:
    print("Score:" + str(int(score)))

#   mydb  = mysql.connector.connect(
#           host="localhost",
#           user="root",
#           password="bugs",
#           database="mariogame"
#   )
#   mycursor = mydb.cursor()

#   sql = "insert into scores (name, score) values (%s, %s)"
#   val = (name, score)
#   mycursor.execute(sql, val)

#   mydb.commit()

#   sql = "select * from scores order by score desc"

#   mycursor.execute(sql)
#   myresult = mycursor.fetchall()
#   for x in myresult:
#       print(x)
