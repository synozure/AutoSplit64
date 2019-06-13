from . import constants

from . import config


#
# Constants
#

VERSION = constants.VERSION
DEFAULT_FRAME_RATE = constants.DEFAULT_FRAME_RATE
DEFAULT_LS_HOST = constants.DEFAULT_LS_HOST
DEFAULT_LS_PORT = constants.DEFAULT_LS_PORT
GAME_JP = constants.GAME_JP
GAME_US = constants.GAME_US
SPLIT_NORMAL = constants.SPLIT_NORMAL
SPLIT_FINAL = constants.SPLIT_FINAL
SPLIT_MIPS = constants.SPLIT_MIPS
NO_FADE = constants.NO_FADE
FADEOUT_PARTIAL = constants.FADEOUT_PARTIAL
FADEOUT_COMPLETE = constants.FADEOUT_COMPLETE
FADEIN_PARTIAL = constants.FADEIN_PARTIAL
FADEIN_COMPLETE = constants.FADEIN_COMPLETE
GAME_REGION = constants.GAME_REGION
STAR_REGION = constants.STAR_REGION
LIFE_REGION = constants.LIFE_REGION
NO_HUD_REGION = constants.NO_HUD_REGION
RESET_REGION = constants.RESET_REGION
FADEOUT_REGION = constants.FADEOUT_REGION
FADEIN_REGION = constants.FADEIN_REGION


#
# Route Class
#

class Route(object):
    def insert_split(self, index) -> None:
        pass

    def remove_split(self, index) -> None:
        pass


#
# Split Class
#

class Split(object):
    pass


#
# Base
#
ls_host: str = DEFAULT_LS_HOST
ls_port: int = DEFAULT_LS_PORT

fps: float = DEFAULT_FRAME_RATE
game_version: str = GAME_JP
route = Route()
route_length: int = 0
star_count: int = 0
collection_time: int = 0
fadeout_count: int = 0
fadein_count: int = 0
fade_status: str = NO_FADE
prediction_info = None


def init() -> None:
    import sys
    from .base import Base

    module = sys.modules[__name__]

    Base(module)


def start() -> None:
    pass


def stop() -> None:
    pass


def set_star_count(p_int: int) -> None:
    pass


def enable_predictions(enable: bool) -> None:
    pass


def enable_fade_count(enable: bool) -> None:
    pass


def get_region(region):
    pass


def get_region_rect(region) -> list:
    pass


def register_split_processor(split_type, processor) -> None:
    pass


#
# Split Functions
#

def split() -> None:
    pass


def reset() -> None:
    pass


def skip() -> None:
    pass


def undo() -> None:
    pass


#
# Tracking Functions
#

def fadeout() -> None:
    pass


def fadein() -> None:
    pass


def increment_star() -> None:
    pass


def incoming_split() -> bool:
    pass


def current_split():
    pass


def split_index() -> int:
    pass


#
# Route
#

def load() -> Route:
    pass


def save() -> None:
    pass


#
# Listeners
#

def set_update_listener(listener) -> None:
    pass


def set_error_listener(listener) -> None:
    pass