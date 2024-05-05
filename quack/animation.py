__all__ = (
    "Animation",
    "AnimationType",
)

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Callable, Coroutine, Optional, TypeVar

import pygame
from aenum import Enum

import quack.animations as animations

if TYPE_CHECKING:
    from quack.dispatcher import EventContext
    from quack.element import Element


class AnimationType(Enum):
    NONE = -1
    HOVER_DIM = pygame.MOUSEMOTION


TElement = TypeVar("TElement", bound="Element")
ElementCB = Callable[["EventContext"], Coroutine[None, None, None]]


class Animation(ABC):
    def __init__(self, animation_type: AnimationType, anim_duration: Optional[float] = None) -> None:
        self.animation_type: AnimationType = animation_type
        self.animation_duration: Optional[float] = anim_duration

    @abstractmethod
    def on_click(self, cb: ElementCB) -> None: ...

    @abstractmethod
    def on_click_up(self, cb: ElementCB) -> None: ...

    @abstractmethod
    def on_hover(self, cb: ElementCB) -> None: ...

    @abstractmethod
    def on_hover_exit(self, cb: ElementCB) -> None: ...

    @abstractmethod
    def set_animation(self, cb: ElementCB) -> None: ...

    def apply_animation(self, animation_type: AnimationType, anim_duration: Optional[float] = None) -> None:
        if animation_type == AnimationType.HOVER_DIM:
            self.on_hover(animations.hover_dim)
            self.on_hover_exit(animations.unhover_dim)

        self.animation_duration = anim_duration
        self.animation_type = animation_type
