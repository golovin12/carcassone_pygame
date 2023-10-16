import pygame
from ecs_pattern import entity

from carcassonne_ecs.components import Event


@entity
class SystemStateInfo:
    running: bool
    is_fullscreen: bool
    screen: pygame.Surface
    default_size: tuple[int, int]


@entity
class SetScreenSizeEvent(Event):
    pass


@entity
class GameStateInfo:
    players: int
    play: bool
    pause: bool
    is_menu: bool


@entity
class Mouse:
    sprite: pygame.sprite.Sprite


@entity
class Player:
    pk: int
    score: int
    meeples: int


class Tail:
    ...


class Camera:
    ...
