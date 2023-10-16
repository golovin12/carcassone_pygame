from pygame.sprite import Sprite
from ecs_pattern import component


@component
class Event:
    name: str


@component
class ComVisible:
    sprite: Sprite
    x: int
    y: int


@component
class ComScore:
    score: int
