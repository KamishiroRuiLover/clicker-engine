from os import path
import json


# engine funcs #
def read_saves_dir(param):
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
        if path.exists("saves/" + param + "/" + i):
            saves[i]["loaded"] = True
    
    return saves


def none(param):
    pass


def exit(param):
    global running
    running = False


def add_stage(param):
    global stages
    stages.append(param)


# template/clicker project specific funcs #
def inc_global_by_global(param):
    # param = [var_name, inc_var_name] #
    global gbls
    gbls[param[0]] += gbls[param[1]]


def purchase_stage(param):
    # param = [stage, currency, cost]
    global gbls
    global stages

    if gbls[param[1]] >= gbls[param[2]]:
        stages.append(param[0])

        gbls[param[1]] -= param[2]


# end of file #