from __future__ import annotations
from server_classes.goal.goal import Goal

class playerGoal(Goal):
    def __init__(self):
        super().__init__(10,0.5)
        self.name = "playerGoal"
        