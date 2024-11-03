from enum import Enum


class en_bird_part(Enum):
    head = 0
    leg = 1
    wing = 2
    tail = 3


class en_bird_head_pose(Enum):
    center = 0
    right = 1
    left = 2
    none = -1


class en_bird_leg_pose(Enum):
    down = 0
    up = 1
    none = -1


class en_bird_wing_pose(Enum):
    off = 0
    on = 1
    none = -1


class en_bird_tail_pose(Enum):
    center = 0
    right = 1
    left = 2
    none = -1