# from .object_bases import AnimatedObjectBase


class MapKey():
    """A key object for the map."""

    def __init__(self, key):
        # super().__init__(frames, frame_durations)
        self.key = key

    def __repr__(self) -> str:
        return super().__repr__() + f" - {self.key}"
