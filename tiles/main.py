import pygame as pg
import sys
from os import path
from sprites import *
from settings import *

class Game:
    def __init__(self):
        pg.init()
        pg.display.set_caption(TITLE)
        self.screen = pg.display.set_mode((screenW, screenH))
        self.clock = pg.time.Clock()
        self.dt = self.clock.tick(FPS) / 1000
        self.running = True
        self.playing = False
        self.background = BLACK
        self.allSprites = pg.sprite.Group()
        self.wallSprites = pg.sprite.Group()
        self.load()

    def load(self):
        gameFolder = path.dirname(__file__)
        collLayout = []
        with open(path.join(gameFolder, "collLayout"), "r") as f:
            for line in f:
                collLayout.append(line)
            for row, tiles in enumerate(collLayout):
                for col, tile in enumerate(tiles):
                    if tile == "1":
                        Wall(self, col, row)
                    if tile == "p":
                        self.player = Player(self, col * TILESIZE, row * TILESIZE)

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.update()
            self.draw()
            self.events()

    def update(self):
        self.allSprites.update()

    def draw(self):
        self.screen.fill(self.background)
        self.allSprites.draw(self.screen)
        self.drawGrid()
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
                pg.quit()
                sys.exit()

    def drawGrid(self):
        for x in range(0, screenW, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, screenH))
        for y in range(0, screenH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (screenW, y))


g = Game()
while g.running:
    g.run()