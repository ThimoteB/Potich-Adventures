from __future__ import annotations
from server_classes.goal.goal import Goal


class cardGoal(Goal):
    def __init__(self):
        super().__init__(5, 0.05)
        self.name = "cardGoal"
