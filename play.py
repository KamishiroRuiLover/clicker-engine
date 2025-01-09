import pygame as pg


# Pygame initialization #
pg.init()
screen = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()
running = True
dt = 0


while(running):
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False


pg.quit()