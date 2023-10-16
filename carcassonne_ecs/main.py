import os

import pygame
from ecs_pattern import EntityManager, SystemManager

from consts import FPS_MAX
from entities import SystemStateInfo
from systems import SysControl, SysInit, SysGameInit

os.environ['SDL_VIDEO_CENTERED'] = '1'  # window at center


def main():
    """Каркассон"""
    pygame.init()  # init all imported pygame modules
    clock = pygame.time.Clock()
    entities = EntityManager()

    system_manager = SystemManager([
        SysInit(entities),
        SysControl(entities, pygame.event.get),
        SysGameInit(entities),
        # NewGameListener(entities),
    ])

    system_manager.start_systems()

    system_state_info: SystemStateInfo = next(entities.get_by_class(SystemStateInfo))
    while system_state_info.running:
        clock.tick_busy_loop(FPS_MAX)  # tick_busy_loop точный + ест проц, tick грубый + не ест проц
        system_manager.update_systems()
        pygame.display.flip()  # draw changes on screen

    system_manager.stop_systems()


if __name__ == '__main__':
    main()
