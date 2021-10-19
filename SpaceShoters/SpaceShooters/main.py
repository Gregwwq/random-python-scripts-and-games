import pygame
import random

pygame.init()

screen = pygame.display.set_mode((1350, 600))
background = pygame.image.load("space.jpg")
running = True
gameOver = True

class Player(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.speed = 3
        self.img = pygame.image.load("spaceship_up.png")
        self.dir = "up"
        self.hitbox = (self.x, self.y, 32, 32)
        self.state = "alive"

    def draw(self):
        global screen
        screen.blit(self.img, (self.x, self.y))
        self.hitbox = (self.x, self.y, 32, 32)
        # pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

    def kill(self):
        global gameOverFont
        global screen
        self.state = "dead"
        self.img = pygame.transform.scale(pygame.image.load("skull.png"), (32, 32))


class Enemy(object):
    def __init__(self, _player):
        self.x = random.randint(0, 1350)
        self.y = random.randint(0, 600)
        if _player.x - 64 < self.x < _player.x + 64:
            self.x = random.randint(0, 1350)
        if _player.y - 64 < self.y < _player.y + 64:
            self.y = random.randint(0, 600)
        self.speed = 1
        self.disTrav = 0
        self.dir = random.randint(0, 3)
        self.img = pygame.image.load("enemy.png")
        self.hitbox = (self.x, self.y, 32, 32)

    def draw(self):
        global screen
        screen.blit(self.img, (self.x, self.y))
        self.hitbox = (self.x, self.y, 32, 32)
        #pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

    def move(self):
        if self.dir == 0:
            self.y -= self.speed
            self.disTrav += self.speed
        elif self.dir == 1:
            self.y += self.speed
            self.disTrav += self.speed
        elif self.dir == 2:
            self.x -= self.speed
            self.disTrav += self.speed
        elif self.dir == 3:
            self.x += self.speed
            self.disTrav += self.speed

        if self.disTrav >= 150:
            self.dir = random.randint(0, 3)
            self.disTrav = 0

        if self.x <= 0:
            self.x = 0
            self.dir = 3
            self.disTrav = 0
        elif self.x >= 1318:
            self.x = 1318
            self.dir = 2
            self.disTrav = 0
        if self.y <= 0:
            self.y = 0
            self.dir = 1
            self.disTrav = 0
        elif self.y >= 568:
            self.y = 568
            self.dir = 0
            self.disTrav = 0

    def hit(self):
        global score
        score += 100
        print("hit")


class Bullet(object):
    def __init__(self, _player):
        self.x = _player.x + 8
        self.y = _player.y + 10
        self.img = pygame.image.load("bullet_up.png")
        self.speed = 5
        self.dir = _player.dir
        self.hitbox = (self.x, self.y, 16, 16)

    def draw(self):
        global screen
        screen.blit(self.img, (self.x, self.y))
        self.hitbox = (self.x, self.y, 16, 16)
        #pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

    def shoot(self):
        if self.dir == "up":
            self.img = pygame.image.load("bullet_up.png")
            self.y -= self.speed
        elif self.dir == "down":
            self.img = pygame.image.load("bullet_down.png")
            self.y += self.speed
        elif self.dir == "left":
            self.img = pygame.image.load("bullet_left.png")
            self.x -= self.speed
        elif self.dir == "right":
            self.img = pygame.image.load("bullet_right.png")
            self.x += self.speed


class Explosion(object):
    def __init__(self, object):
        self.x = object.x - 9
        self.y = object.y - 9
        self.frame = 0
        self.frameRate = 50
        self.img = explAnimiation[self.frame]
        self.lastUpdate = pygame.time.get_ticks()

    def draw(self):
        global screen
        screen.blit(self.img, (self.x, self.y))

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.lastUpdate > self.frameRate and self.frame < 8:
            self.lastUpdate = now
            self.frame += 1
            self.img = explAnimiation[self.frame]


class Button(object):
    def __init__(self, x, y, color, width, height, text):
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height
        self.text = text

    def draw(self):
        global screen
        pygame.draw.rect(screen, (0, 0, 0,), (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)
        btnFont = pygame.font.SysFont('comicsans', 40)
        text = btnFont.render(self.text, 1, (0, 0, 0))
        screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
            return True
        else:
            return False


enemies = []
bullets = []
explosions = []
shootDel = 0
startingNumOfEnemies = 3
totalNumOfEnemies = 10
maxTotalNumOfEnemies = 100
enemySpawnRate = 2000
maxEnemySpawnRate = 300
enemyMaxSpeed = 2.5
score = 0
scoreFont = pygame.font.SysFont("comicsans", 50, True)

explAnimiation = []
for i in range(9):
    filename = "regularExplosion0{}.png".format(i)
    _img = pygame.image.load(filename)
    img = pygame.transform.scale(_img, (50, 50))
    explAnimiation.append(img)

def spawnEnemies():
    global enemySpawnRate
    global maxEnemySpawnRate
    global enemyMaxSpeed
    global totalNumOfEnemies
    global maxTotalNumOfEnemies
    global enemies
    if len(enemies) <= totalNumOfEnemies:
        enemies.append(Enemy(player))
        if totalNumOfEnemies < maxTotalNumOfEnemies:
            totalNumOfEnemies += 2
        if enemySpawnRate > maxEnemySpawnRate:
            enemySpawnRate -= 100
        for _enemy in enemies:
            if _enemy.speed < enemyMaxSpeed:
                _enemy.speed += 0.05
    pygame.time.set_timer(pygame.USEREVENT, enemySpawnRate)


def updateGame():
    global gameOver
    for _enemy in enemies:
        _enemy.draw()
        _enemy.move()
        if player.state == "alive":
            if player.hitbox[0] < _enemy.hitbox[0] + _enemy.hitbox[2] and player.hitbox[0] + player.hitbox[2] > \
                    _enemy.hitbox[0]:
                if player.hitbox[1] < _enemy.hitbox[1] + _enemy.hitbox[3] and player.hitbox[1] + player.hitbox[3] > \
                        _enemy.hitbox[1]:
                    explosions.append(Explosion(player))
                    player.kill()

    for _bullet in bullets:
        _bullet.draw()

    currentScore = scoreFont.render("Score: " + str(score), 1, (255, 255, 255))
    screen.blit(currentScore, (20, 10))

    for explosion in explosions:
        if explosion.frame < 9:
            explosion.draw()
            explosion.update()
        else:
            explosions.pop(explosions.index(explosion))

    if player.state == "dead":
        gameOverFont = pygame.font.SysFont("comicsans", 100, True, True)
        txtGameOver = gameOverFont.render("GAME OVER", 0, (255, 255, 255))
        screen.blit(txtGameOver, (430, 200))
        btnRetry = Button(615, 300, (255, 255, 255), 120, 60, "Retry")
        btnRetry.draw()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btnRetry.isOver(pos):
                    gameOver = True
                    print("Retry")

    player.draw()
    pygame.display.update()


def showTitleScreen():
    global screen, running, gameOver
    screen.blit(background, (0, 0))
    titleFont = pygame.font.SysFont("comicsans", 100, True, True)
    title = titleFont.render("Space Shooters", 1, (255, 255, 255))
    screen.blit(title, (380, 200))
    startFont = pygame.font.SysFont("comicsans", 35, True, True)
    start = startFont.render("Press any key to start", 1, (255, 255, 255))
    screen.blit(start, (530, 300))
    instrFont = pygame.font.SysFont("comicsans", 25, True, True)
    instr = instrFont.render("Space is to shoot and the arrow keys are to move", 1, (255, 255, 255))
    screen.blit(instr, (460, 400))
    pygame.display.flip()
    waiting = True
    while waiting:
        for _event in pygame.event.get():
            if _event.type == pygame.QUIT:
                pygame.quit()
            if _event.type == pygame.KEYUP:
                waiting = False
                gameOver = False

pygame.time.set_timer(pygame.USEREVENT, enemySpawnRate)

while running:
    if gameOver:
        showTitleScreen()
        player = Player(675, 300)
        enemies = []
        bullets = []
        explosions = []
        shootDel = 0
        startingNumOfEnemies = 3
        totalNumOfEnemies = 10
        maxTotalNumOfEnemies = 100
        enemySpawnRate = 2000
        maxEnemySpawnRate = 300
        enemyMaxSpeed = 2.5
        score = 0
        for e in range(startingNumOfEnemies):
            enemies.append(Enemy(player))

    screen.blit(background, (0, 0))
    updateGame()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not gameOver and player.state == "alive":
            if event.type == pygame.USEREVENT:
                spawnEnemies()

    for bullet in bullets:
        for enemy in enemies:
            if bullet.hitbox[0] < enemy.hitbox[0] + enemy.hitbox[2] and bullet.hitbox[0] + bullet.hitbox[2] > \
                    enemy.hitbox[0]:
                if bullet.hitbox[1] < enemy.hitbox[1] + enemy.hitbox[3] and bullet.hitbox[1] + bullet.hitbox[3] > \
                        enemy.hitbox[1]:
                    enemy.hit()
                    explosions.append(Explosion(enemy))
                    enemies.pop(enemies.index(enemy))
                    bullets.pop(bullets.index(bullet))

        if 0 <= bullet.x <= 1334 and 0 <= bullet.y <= 584:
            bullet.shoot()
        else:
            bullets.pop(bullets.index(bullet))

    pressedKey = pygame.key.get_pressed()
    if pressedKey[pygame.K_UP] and player.state == "alive":
        player.img = pygame.image.load("spaceship_up.png")
        player.dir = "up"
        if player.y >= 0:
            player.y -= player.speed
        player.draw()
    elif pressedKey[pygame.K_DOWN] and player.state == "alive":
        player.img = pygame.image.load("spaceship_down.png")
        player.dir = "down"
        if player.y <= 568:
            player.y += player.speed
        player.draw()
    elif pressedKey[pygame.K_RIGHT] and player.state == "alive":
        player.img = pygame.image.load("spaceship_right.png")
        player.dir = "right"
        if player.x <= 1318:
            player.x += player.speed
        player.draw()
    elif pressedKey[pygame.K_LEFT] and player.state == "alive":
        player.img = pygame.image.load("spaceship_left.png")
        player.dir = "left"
        if player.x >= 0:
            player.x -= player.speed
        player.draw()

    if pressedKey[pygame.K_SPACE] and shootDel == 0 and player.state == "alive":
        if len(bullets) <= 10:
            bullets.append(Bullet(player))
        shootDel = 1

    if shootDel > 0:
        shootDel += 1
    if shootDel > 15:
        shootDel = 0
