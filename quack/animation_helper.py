__all__ = (
    "Animation",
    "AnimationType",
)

from typing import TypeVar

from aenum import Enum

import quack.animations as animations
from quack.element import Element


class AnimationType(Enum):
    HOVER_DIM = 0


TElement = TypeVar("TElement", bound=Element)


class Animation:
    @staticmethod
    def apply_hover_anim(animation_type: AnimationType, element: TElement) -> TElement:
        if animation_type == AnimationType.HOVER_DIM:
            element.on_hover(animations.hover_dim)
            element.on_hover_exit(animations.unhover_dim)

        return element
