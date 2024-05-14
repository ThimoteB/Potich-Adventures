from .object_bases import AnimatedObjectBase


class MapCard(AnimatedObjectBase):
    """A card object for the map."""

    def __init__(self, frames, frame_durations, card):
        super().__init__(frames, frame_durations, reverse_at_end=False)
        self.card = card
