import pygame as pg
from settings import *


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self, game.allSprites)
        self.game = game
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def getKeys(self):
        self.vx = 0
        self.vy = 0
        pressedKey = pg.key.get_pressed()
        if pressedKey[pg.K_w]:
            self.vy = -PLAYERSPEED
        if pressedKey[pg.K_s]:
            self.vy = PLAYERSPEED
        if pressedKey[pg.K_a]:
            self.vx = -PLAYERSPEED
        if pressedKey[pg.K_d]:
            self.vx = PLAYERSPEED
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

    def update(self):
        self.getKeys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collideWall("x")
        self.rect.y = self.y
        self.collideWall("y")

    def collideWall(self, dir):
        if dir == "x":
            hit = pg.sprite.spritecollide(self, self.game.wallSprites, False)
            if hit:
                if self.vx > 0:
                    self.x = hit[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hit[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == "y":
            hit = pg.sprite.spritecollide(self, self.game.wallSprites, False)
            if hit:
                if self.vy > 0:
                    self.y = hit[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hit[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.allSprites, game.wallSprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.x = x
        self.y = y
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
