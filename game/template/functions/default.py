from os import path
import json


# engine funcs #
def read_saves_dir(param):
    # as of now unused, may be used in the future
    #param "GAME" (Must literally be the string "GAME", not something else)

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
    #param "" (no parameters, just empty string)

    pass


def exit(param):
    #param "" (no parameters, just empty string)

    global running
    running = False


def add_stage(param):
    #param: "stage"

    global stages
    stages.append(param)


def switch_world(param):
    #param ["GAME", "world_name"] #GAME must be the first slot.

    global read_world_func

    read_world_func(param[0], param[1])


def make_save(param):
    #param "" (no parameters, just empty string)
    global save_func

    save_func()


def load_save(param):
    #param "" (no parameters, just empty string)
    global load_func

    load_func()


def set_global(param):
    #param ["var_name", new_value(any value)]
    global gbls

    gbls[param[0]] = param[1]


def set_local(param):
    #param ["local_var_name", new_value(any value)]
    global lcls

    lcls[param[0]] = param[1]


# template/clicker project specific funcs #
def inc_global_by_global(param):
    #param ["var_name", "var2_name"] #Slot 1 must be the variable you want to change, changed by the variable listed in slot 2. Both must be globals.

    global gbls
    gbls[param[0]] += gbls[param[1]]


def purchase_stage(param):
    # param ["stage", "currency"(global variable), cost(int)]
    global gbls

    if gbls[param[1]] >= param[2]:
        add_stage(param[0])

        gbls[param[1]] -= param[2]


def purchase_global_inc(param):
    #param ["var_to_change", "inc_amount", "currency"(global variable), cost(int)]
    global gbls

    if gbls[param[2]] >= param[3]:
        gbls[param[0]] += param[1]

        gbls[param[2]] -= param[3]


# end of file #