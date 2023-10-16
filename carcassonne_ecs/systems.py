from typing import Callable

import pygame
from pygame.event import Event
from pygame.locals import QUIT, KEYDOWN, K_F11, MOUSEBUTTONUP
from ecs_pattern import System, EntityManager

from carcassonne_ecs.sprites import MouseSprite, Button
from entities import GameStateInfo, SystemStateInfo, Mouse
from consts import DEFAULT_GAME_PARAMS, VERSION, RED, BLUE, WHITE


def set_screen_size(is_fullscreen: bool, default_size: tuple[int, int]) -> pygame.Surface:
    size = default_size
    if not is_fullscreen:
        size = (size[0] // 1.5, size[1] // 1.5)
    return pygame.display.set_mode(size)


class SysInit(System):
    def __init__(self, entities: EntityManager):
        self.entities = entities

    def start(self):
        is_fullscreen = True
        display_info = pygame.display.Info()
        default_size = (display_info.current_w, display_info.current_h - 60)
        screen = set_screen_size(is_fullscreen, default_size)
        pygame.display.set_caption(f'Каркассон v.{VERSION}')
        pygame.display.set_icon(pygame.image.load("img/Kark.png").convert())
        self.entities.add(
            SystemStateInfo(
                running=True,
                is_fullscreen=is_fullscreen,
                screen=screen,
                default_size=default_size,
            ),
        )


class SysControl(System):
    def __init__(self, entities: EntityManager, event_getter: Callable[..., list[Event]]):
        self.entities = entities
        self.event_getter = event_getter
        self.event_types = (KEYDOWN, QUIT)  # white list
        self.sys_state_info = None

    def start(self):
        self.sys_state_info = next(self.entities.get_by_class(SystemStateInfo))

    def update(self):
        for event in self.event_getter(self.event_types):
            event_type = event.type
            event_key = getattr(event, 'key', None)
            if event_type == QUIT:
                self.sys_state_info.running = False
            elif event_type == KEYDOWN and event_key == K_F11:
                print(self.sys_state_info.is_fullscreen)
                self.sys_state_info.is_fullscreen = not self.sys_state_info.is_fullscreen
                self.sys_state_info.screen = set_screen_size(self.sys_state_info.is_fullscreen,
                                                             self.sys_state_info.default_size)



class SysGameInit(System):
    def __init__(self, entities: EntityManager):
        self.entities = entities
        self.sys_state_info = None
        self.game_state_info = None

    def start(self):
        self.sys_state_info = next(self.entities.get_by_class(SystemStateInfo))
        self.game_state_info = GameStateInfo(**DEFAULT_GAME_PARAMS)
        self.entities.add(
            Mouse(sprite=MouseSprite()),
            self.game_state_info,
        )

    def update(self):
        if not self.game_state_info.is_menu:
            return
        screen = self.sys_state_info.screen
        size = self.sys_state_info.default_size
        myfont = pygame.font.SysFont('Comic Sans MS', 20)

        but1 = pygame.image.load("img/button1.png").convert()
        but2 = pygame.image.load("img/button2.png").convert()
        button1 = Button(but1, (size[1] / 2) - 140, size[0])
        button2 = Button(but1, (size[1] / 2) + 20, size[0])
        button1_sprites = pygame.sprite.Group()
        button2_sprites = pygame.sprite.Group()
        button1_sprites.add(button1)
        button2_sprites.add(button2)

        mouse_sprite = next(self.entities.get_by_class(Mouse)).sprite
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_sprite.update(mouse_x, mouse_y)
        screen.fill((255, 255, 255))
        menu_fon = pygame.image.load("img/menu_fon.jpg").convert()
        menu_fon = pygame.transform.scale(menu_fon, self.sys_state_info.default_size)
        screen.blit(menu_fon, (0, 0))

        if pygame.sprite.spritecollide(mouse_sprite, button1_sprites, False):
            textsurfaceb1 = myfont.render("НАЧАТЬ ИГРУ", False, RED)
            button1.update(but2)
        else:
            button1.update(but1)
            textsurfaceb1 = myfont.render("НАЧАТЬ ИГРУ", False, BLUE)

        if pygame.sprite.spritecollide(mouse_sprite, button2_sprites, False):
            textsurfaceb2 = myfont.render("Добавить игроков", False, RED)
            button2.update(but2)
        else:
            textsurfaceb2 = myfont.render("Добавить игроков", False, BLUE)
            button2.update(but1)

        for e in button1_sprites:
            screen.blit(e.image, e.rect)
        for e in button2_sprites:
            screen.blit(e.image, e.rect)

        screen.blit(textsurfaceb1, ((size[0] / 2) - 40, (size[1] / 2) - 115))
        screen.blit(textsurfaceb2, ((size[0] / 2) - 45, (size[1] / 2) + 45))
        pygame.draw.ellipse(screen, WHITE, ((size[0] / 2) - 85, (size[1] / 2) + 133, 250, 45))
        textsurfacem1 = myfont.render("Количество игроков = " + str(2), False, RED)
        screen.blit(textsurfacem1, ((size[0] / 2) - 75, (size[1] / 2) + 140))


class SysMenuController(System):
    def __init__(self, entities: EntityManager, event_getter: Callable[..., list[Event]]):
        self.entities = entities
        self.event_getter = event_getter
        self.event_types = (KEYDOWN, MOUSEBUTTONUP)  # white list
        self.sys_state_info = None

    def start(self):
        self.sys_state_info = next(self.entities.get_by_class(SystemStateInfo))

    def update(self):
        if not self.sys_state_info.is_menu:
            return
        for event in self.event_getter(self.event_types):
            event_type = event.type
            event_key = getattr(event, 'key', None)
            # if event_type == pygame.MOUSEBUTTONUP:
            #     if event.button == 1:
            #         if pygame.sprite.spritecollide(muse, button1_sprites, False):
            #             button2.sdvig(y=(height / 2) + 215)
            #             game = 1
            #             for i in range(kol_players):
            #                 mipls.append(Igrok(new_igrok(), player_sprites))
            #             move(0, 0)
            #
            #         if pygame.sprite.spritecollide(muse, button2_sprites, False):
            #             if kol_players < 5:
            #                 kol_players += 1
            #
            #     elif event.button == 3:
            #         if pygame.sprite.spritecollide(muse, button2_sprites, False):
            #             if kol_players > 2:
            #                 kol_players -= 1

            # elif event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_ESCAPE:
            #         self.sys_state_info.running = False


class SysMenuEventListener(System):
    def __init__(self, entities: EntityManager):
        self.entities = entities
        self.sys_state_info = None

    def start(self):
        self.sys_state_info = next(self.entities.get_by_class(SystemStateInfo))

    def update(self):
        if not self.sys_state_info.is_menu:
            return
