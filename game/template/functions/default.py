from os import path
import json


def read_saves_dir(game):
    saves = {
        "slot1": {
            "loaded": False
        },
        "slot2": {
            "loaded": False
        },
        "slot3": {
            "loaded": False
        }
    }

    for i in ["sav1", "sav2", "sav3"]:
        if path.exists("saves/" + game + "/" + i):
            saves[i]["loaded"] = True
    
    return saves


def none():
    pass


def test():
    print("test")


# end of file #