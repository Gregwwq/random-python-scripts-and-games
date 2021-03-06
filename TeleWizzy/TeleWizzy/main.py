import pygame
import sys
import random

pygame.init()
screenH = 600
screenW = 1200
screen = pygame.display.set_mode((screenW, screenH))
clock = pygame.time.Clock()
background = pygame.image.load("background/background.png")


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.standRight = []
        for i in range(10):
            standRight = "player/standRight/standRight{}.png".format(i)
            self.standRight.append(pygame.image.load(standRight))
        self.standLeft = []
        for i in range(10):
            standLeft = "player/standLeft/standLeft{}.png".format(i)
            self.standLeft.append(pygame.image.load(standLeft))
        self.walkRight = []
        for i in range(10):
            walkRight = "player/moveRight/moveRight{}.png".format(i)
            self.walkRight.append(pygame.image.load(walkRight))
        self.walkLeft = []
        for i in range(10):
            walkLeft = "player/moveLeft/moveLeft{}.png".format(i)
            self.walkLeft.append(pygame.image.load(walkLeft))
        self.jumpRight = []
        for i in range(10):
            jumpRight = "player/jumpRight/jumpRight{}.png".format(i)
            self.jumpRight.append(pygame.image.load(jumpRight))
        self.jumpLeft = []
        for i in range(10):
            jumpLeft = "player/jumpLeft/jumpLeft{}.png".format(i)
            self.jumpLeft.append(pygame.image.load(jumpLeft))
        self.attackRight = []
        for i in range(10):
            attackRight = "player/attackRight/attackRight{}.png".format(i)
            self.attackRight.append(pygame.image.load(attackRight))
        self.attackLeft = []
        for i in range(10):
            attackLeft = "player/attackLeft/attackLeft{}.png".format(i)
            self.attackLeft.append(pygame.image.load(attackLeft))
        self.x = x
        self.y = y
        self.jumpY = 380
        self.speed = 4
        self.jumpSpeed = 10
        self.frame = 0
        self.jumpFrame = 0
        self.attackFrame = 0
        self.right = True
        self.left = False
        self.up = False
        self.down = False
        self.moving = False
        self.jumping = False
        self.attacking = False
        self.attacked = False
        self.attackHB = 0
        self.hitbox = (self.x + 45, self.y + 40, 70, 90)
        self.image = self.standRight[self.frame]
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]

    def update(self):
        self.hitbox = (self.x + 45, self.y + 40, 70, 90)
        #pygame.draw.rect(screen, (255, 0, 0), (1020, 360, 50, 1), 2)
        self.frame += 0.25
        if self.frame >= len(self.standRight):
            self.frame = 0
        if self.right and not self.moving:
            self.image = self.standRight[int(self.frame)]
        if self.left and not self.moving:
            self.image = self.standLeft[int(self.frame)]
        if self.right and self.moving:
            self.image = self.walkRight[int(self.frame)]
            if self.x <= 900:
                self.x += self.speed
            if self.x >= 900 and self.y <= 250:
                self.x += self.speed
        if self.left and self.moving:
            self.image = self.walkLeft[int(self.frame)]
            if self.x >= -40:
                self.x -= self.speed
        if self.right and self.jumping:
            neg = 1
            if self.jumpSpeed < 0:
                neg = -1
            self.y -= (self.jumpSpeed ** 2) * 0.25 * neg
            self.jumpSpeed -= 0.5
            self.image = self.jumpRight[int(self.jumpFrame)]
            self.jumpFrame += 0.125
        if self.left and self.jumping:
            neg = 1
            if self.jumpSpeed < 0:
                neg = -1
            self.y -= (self.jumpSpeed ** 2) * 0.25 * neg
            self.jumpSpeed -= 0.5
            self.image = self.jumpLeft[int(self.jumpFrame)]
            self.jumpFrame += 0.125
        if self.hitbox[1] + self.hitbox[3] >= 520 and self.hitbox[0] + self.hitbox[2] <= 1020:
            self.y = 380
            self.jumping = False
            self.jumpSpeed = 10
            self.jumpFrame = 0
        if self.hitbox[1] + self.hitbox[3] >= 370 and self.hitbox[0] + self.hitbox[2] >= 1020:
            self.y = 230
            self.jumping = False
            self.jumpSpeed = 10
            self.jumpFrame = 0
        if self.right and self.attacking:
            if self.attackFrame < 10:
                self.attackHB = (self.x + 80, self.y + 40, 50, 90)
                self.image = self.attackRight[int(self.attackFrame)]
                self.attackFrame += 0.5
            else:
                self.attackFrame = 0
                self.attackHB = 0
                self.attacking = False
        if self.left and self.attacking:
            if self.attackFrame < 10:
                self.attackHB = (self.x + 30, self.y + 40, 50, 90)
                self.image = self.attackLeft[int(self.attackFrame)]
                self.attackFrame += 0.5
            else:
                self.attackFrame = 0
                self.attackHB = 0
                self.attacking = False
        self.rect.topleft = [self.x, self.y]


class Wizard(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.standRight = pygame.image.load("wizard/standRight.png")
        self.standLeft = pygame.image.load("wizard/standLeft.png")
        self.moveRight = []
        for i in range(4):
            moveRight = "wizard/moveRight/moveRight{}.png".format(i)
            self.moveRight.append(pygame.image.load(moveRight))
        self.moveLeft = []
        for i in range(4):
            moveLeft = "wizard/moveLeft/moveLeft{}.png".format(i)
            self.moveLeft.append(pygame.image.load(moveLeft))
        self.teleport = []
        for i in range(24):
            teleport = "wizard/teleport/bluspark{}.png".format(i)
            self.teleport.append(pygame.image.load(teleport))
        self.x = x
        self.y = y
        self.speed = 2
        self.frame = 0
        self.teleportFrame = 23
        self.distTrav = 0
        self.waiting = True
        self.teleporting = False
        self.tpIn = False
        self.tpOut = False
        self.wait = 50
        self.dir = 0
        self.prevDir = 0
        self.maxDir = 0
        self.hitbox = (self.x + 7.5, self.y + 2.5, 80, 95)
        self.image = self.standRight
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]

    def update(self):
        self.hitbox = (self.x + 7.5, self.y + 2.5, 80, 95)
        self.frame += 0.125
        if self.frame >= len(self.moveRight):
            self.frame = 0
        if self.dir == 0 and self.waiting:
            self.image = self.standRight
        if self.dir == 1 and self.waiting:
            self.image = self.standLeft
        if self.waiting:
            self.wait += 1
            if self.wait == 100:
                self.waiting = False
        if self.x >= 930:
            self.x = 930
            self.dir = 1
            self.distTrav = random.randint(0, 80)
        if self.x <= 0:
            self.x = 0
            self.dir = 0
            self.distTrav = random.randint(0, 80)
        if self.dir == 0 and not self.waiting:
            self.image = self.moveRight[int(self.frame)]
            self.distTrav += self.speed
            self.x += self.speed
        if self.dir == 1 and not self.waiting:
            self.image = self.moveLeft[int(self.frame)]
            self.distTrav += self.speed
            self.x -= self.speed
        if self.distTrav >= 200:
            self.distTrav = random.randint(0, 80)
            self.wait = random.randint(0, 50)
            self.dir = random.randint(0, 1)
            self.waiting = True
            if self.prevDir == self.dir:
                self.maxDir += 1
            else:
                self.maxDir = 0
                self.prevDir = self.dir
            if self.dir == 0 and self.maxDir >= 2:
                self.dir = 1
                self.maxDir = 0
            elif self.dir == 1 and self.maxDir >= 2:
                self.dir = 0
                self.maxDir = 0
        if player.attacking and not player.attacked:
            if player.attackHB[0] < self.hitbox[0] + self.hitbox[2] and player.attackHB[0] + player.attackHB[2] > self.hitbox[0]:
                if player.attackHB[1] < self.hitbox[1] + self.hitbox[3] and player.attackHB[1] + player.attackHB[3] > self.hitbox[1]:
                    self.teleporting = True
                    self.tpOut = True
                    player.attacked = True
        if self.teleporting:
            self.waiting = True
            self.rect.topleft = [self.x - 80, self.y - 70]
            if self.teleportFrame <= 0:
                self.tpOut = False
                self.tpIn = True
                self.x = random.randint(0, 930)
            if self.tpOut:
                self.image = self.teleport[self.teleportFrame]
                self.teleportFrame -= 1
            if self.tpIn:
                self.image = self.teleport[self.teleportFrame]
                self.teleportFrame += 1
            if self.teleportFrame >= 23:
                self.teleportFrame = 23
                self.teleporting = False
                self.tpIn = False
                self.tpOut = False
                self.waiting = False
                player.attacked = False
        else:
            self.rect.topleft = [self.x, self.y]


playerGrp = pygame.sprite.Group()
wizardGrp = pygame.sprite.Group()
player = Player(500, 380)
playerGrp.add(player)
wizard = Wizard(800, 415)
wizardGrp.add(wizard)
rock0 = pygame.image.load("background/rock0.png")
rock1 = pygame.image.load("background/rock1.png")
platform0 = pygame.image.load("background/platform0.png")
platform0X = 1000
platform0Y =  250


def updateScreen():
    screen.blit(background, (0, 0))
    screen.blit(rock0, (50, 250))
    screen.blit(rock1, (300, 250))
    screen.blit(platform0, (platform0X, platform0Y))
    playerGrp.draw(screen)
    playerGrp.update()
    wizardGrp.draw(screen)
    wizardGrp.update()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            player.attacking = True

    player.moving = False
    pressedKey = pygame.key.get_pressed()
    if pressedKey[pygame.K_d]:
        player.right = True
        player.left = False
        player.moving = True
    if pressedKey[pygame.K_a]:
        player.right = False
        player.left = True
        player.moving = True
    if pressedKey[pygame.K_SPACE]:
        player.jumping = True
        player.up = True

    updateScreen()
    pygame.display.flip()
    clock.tick(60)
