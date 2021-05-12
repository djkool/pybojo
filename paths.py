"""
paths.py : Maintain path constants to our data.

"""
from os.path import join

# DEFAULT PATH CONSTANTS
DATA_PATH = "assets"
IMG_PATH = join(DATA_PATH, "images")
LEVEL_PATH = join(DATA_PATH, "levels")
STATES_PATH = "states"

CONFIG_BLOCK = "paths"

def loadFromConfig(config):
    cfg_bind = {
        "data": "DATA_PATH",
        "image": "IMG_PATH",
        "level": "LEVEL_PATH",
        "states": "STATES_PATH"
    }

    try:
        block = config[CONFIG_BLOCK]
        for item in block:
            if item in cfg_bind:
                globals()[cfg_bind[item]] = block.get(item)
    except KeyError:
        pass


# Helper Functions
def getDataPath(data):
    return join(DATA_PATH, data)

def getImagePath(img_file):
    return join(IMG_PATH, img_file)

def getLevelPath(lvl_file):
    return join(LEVEL_PATH, lvl_file)
