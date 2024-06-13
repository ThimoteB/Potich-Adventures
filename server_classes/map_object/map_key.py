# from .object_bases import AnimatedObjectBase


class MapKey:
    """A key object for the map."""

    def __init__(self, key):
        self.key = key

    def __repr__(self) -> str:
        return super().__repr__() + f" - {self.key}"
