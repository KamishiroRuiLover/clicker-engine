import pygame as pg
import sys
import json
from os import path


# arguments #
if len(sys.argv) != 2:
    print("Usage: python play.py GAME_NAME")
    sys.exit(1)
GAME = "game/" + sys.argv[1]


# Pygame initialization #
pg.init()
screen = pg.display.set_mode(pg.display.get_desktop_sizes()[0]) # 1280 x 720 default size
clock = pg.time.Clock()
running = True
dt = 0


# Misc globals #
bg_color = pg.Color(0, 0, 0)
game_bg_color = pg.Color(0, 0, 0)
active_world = "none"
active_feats = {}
loaded_feats = []
pre_print_screen = pg.Surface((1280, 720))
funcs = {}
gbls = json.loads(open(GAME + "/variables/globals.json").read())
lcls = {}
stages = ["NONE"]


# Classes #
class World_Obj():
    def __init__(self, x, y, img, type, func, param):
        self.t = type
        self.f = func
        self.p = param
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
    
    def draw(self):

        if self.t == "button":
            pos = pg.mouse.get_pos()
            pos = ((pos[0] / screen.get_rect().size[0]) * 1280, (pos[1] / screen.get_rect().size[1]) * 720)

            if self.rect.collidepoint(pos):
                if pg.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    funcs[self.f](self.p)
                    self.clicked = True
            
            if pg.mouse.get_pressed()[0] == 0:
                self.clicked = False

        pre_print_screen.blit(i.image, (i.rect.x, i.rect.y))


# Loading files #
def read_core(game):
    global funcs

    file = open(game + "/core.json").read()
    j_dict = json.loads(file)

    pg.display.set_caption(j_dict["name"] + " - " + j_dict["author"] + " - " + j_dict["version"])

    icon = pg.image.load(game + "/" + j_dict["icon"])
    pg.display.set_icon(icon)

    code = open(game + "/" + j_dict["func_file"] + ".py").read()
    tags = json.loads(open(game + "/" + j_dict["func_file"] + ".json").read())["funcs"]
    exec(code, globals())
    for i in tags:
        funcs[i] = globals().get(i)

    game_bg_color.r = j_dict["global_bg_color"][0]
    game_bg_color.g = j_dict["global_bg_color"][1]
    game_bg_color.b = j_dict["global_bg_color"][2]

read_core(GAME)


def feat_param(param):
    if type(param) == type([]):
        for i in range(len(param)):
            if param[i] == "GAME":
                param[i] = GAME
    else:
        if param == "GAME":
            param = GAME
    return param


def feat_req(req):
    return req


def load_active_feats():
    global loaded_feats
    loaded_feats = []

    for i in active_feats:
        feat = active_feats[i]

        if feat["req"] in stages:
            n_feat = World_Obj(feat["location"][0], feat["location"][1], feat["sprite"], feat["type"], feat["func"], feat["param"])

            loaded_feats.append(n_feat)


def read_world(game, world):
    global active_feats
    active_feats = {}
    global active_world
    active_world = world
    global bg_color

    path = game + "/worlds/" + world + "/"
    file = open(path + world + ".json").read()
    j_dict = json.loads(file)

    if j_dict["name"] != "default":
        pg.display.set_caption(j_dict["name"])

    if j_dict["bg_color"] == "default":
        bg_color = game_bg_color
    else:
        bg_color.r = j_dict["bg_color"][0]
        bg_color.g = j_dict["bg_color"][1]
        bg_color.b = j_dict["bg_color"][2]
    
    for i in j_dict["feats"]:
        n_feat = {}

        file = open(path + "feat/" + i).read()
        feat_dict = json.loads(file)

        n_feat["sprite"] = pg.image.load(game + "/sprites/" + feat_dict["sprite"])
        n_feat["location"] = feat_dict["location"]
        n_feat["type"] = feat_dict["type"]
        n_feat["func"] = feat_dict["func"]
        n_feat["param"] = feat_param(feat_dict["param"])
        n_feat["req"] = feat_req(feat_dict["req"])

        active_feats[feat_dict["name"]] = n_feat
    
    load_active_feats()
read_world_func = read_world


read_world(GAME, "main")


# pg.display.toggle_fullscreen()


# Post-launch Data Funcs #
def save():
    scontent = {
        "gbls": gbls,
        "lcls": lcls,
        "stages": stages,
        "open_world": active_world
    }
    sfile = open("saves/" + sys.argv[1] + ".save", "x")
    sfile.write(json.dumps(scontent))
save_func = save


def load():
    if path.exists("saves/" + sys.argv[1] + ".save"):
        sfile = open("saves/" + sys.argv[1] + ".save")
        scontent = json.loads(sfile.read())

        global gbls
        global lcls
        global stages

        gbls = scontent["gbls"],
        lcls = scontent["lcls"],
        stages = scontent["stages"],
        read_world(GAME, scontent["open_world"])
load_func = load


while(running):

    pre_print_screen.fill(bg_color)

    for i in loaded_feats:
        i.draw()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    screen.blit(pg.transform.scale(pre_print_screen, screen.get_rect().size), (0, 0))
    pg.display.update()

    clock.tick(30)


pg.quit()