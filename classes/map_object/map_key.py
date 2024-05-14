from .object_bases import AnimatedObjectBase


class MapKey(AnimatedObjectBase):
    """A key object for the map."""

    def __init__(self, frames, frame_durations, key):
        super().__init__(frames, frame_durations)
        self.key = key

    def __repr__(self) -> str:
        return super().__repr__() + f" - {self.key}"
