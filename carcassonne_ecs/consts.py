VERSION = "1.1.0"

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 128, 0)

DEFAULT_GAME_PARAMS = dict(
    is_menu=True,
    play=False,
    pause=False,
    players=2
)


class SysEvents:
    FULLSCREEN = 'fullscreen'
    SET_SCREEN_SIZE = 'set_screen_size'


FPS_MAX = 100
FPS_CORR = 24 / FPS_MAX

BALL_SIZE = 0.03  # relative to screen height
BALL_SPEED_MIN = 0.02 * FPS_CORR  # relative to screen height

RACKET_WIDTH = BALL_SIZE
RACKET_HEIGHT = 0.22  # relative to screen height
RACKET_SPEED = 0.03 * FPS_CORR  # relative to screen height
