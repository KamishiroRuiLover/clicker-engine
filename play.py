import pygame as pg
import sys
import json


# arguments #
if len(sys.argv) != 2:
    print("Usage: python play.py GAME_NAME")
    sys.exit(1)
GAME = "game/" + sys.argv[1]


# Pygame initialization #
pg.init()
screen = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()
running = True
dt = 0


# Misc globals #
bg_color = pg.Color(0, 0, 0)


# Loading files #
execs = []
def read_core(game):
    file = open(game + "/core.json").read()
    j_dict = json.loads(file)

    pg.display.set_caption(j_dict["name"] + " - " + j_dict["author"] + " - " + j_dict["version"])

    icon = pg.image.load(game + "/" + j_dict["icon"])
    pg.display.set_icon(icon)

    for i in j_dict["func_files"]:
        file = open(game + "/" + i).read()
        exec(file, globals())
        # execs.append(file)

read_core(GAME)

globals


while(running):

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False


pg.quit()