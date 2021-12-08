from enum import Enum

from PyQt6 import QtGui

from sprite.sprite import Sprite
from sprite.sprite import SpritePos as Pos
import os
import random


class Cat(Sprite):

    ANIMATION_FRAME_PATH = 'assets\\cat\\animation_frames\\'
    SPRITE_SIZE = Pos(100, 100)

    class States(Enum):
        idle = 0
        idle_to_sleep = 1
        sleep = 2
        sleep_to_idle = 3
        walk_left = 4
        walk_right = 5

    NEXT_POSSIBLE_STATES = {
        States.idle: [States.idle, States.idle_to_sleep, States.walk_left, States.walk_right],
        States.idle_to_sleep: [States.sleep],
        States.sleep: [States.sleep, States.sleep_to_idle],
        States.sleep_to_idle: [States.idle, States.walk_left, States.walk_right],
        States.walk_left: [States.idle, States.idle_to_sleep, States.walk_left, States.walk_right],
        States.walk_right: [States.idle, States.idle_to_sleep, States.walk_left, States.walk_right],
    }

    STATE_FRAME_DELAYS = {
        States.idle: 400,
        States.idle_to_sleep: 100,
        States.sleep: 1000,
        States.sleep_to_idle: 100,
        States.walk_left: 100,
        States.walk_right: 100,
    }

    STATE_DISPLACEMENTS = {
        States.idle: Pos(0, 0),
        States.idle_to_sleep: Pos(0, 0),
        States.sleep: Pos(0, 0),
        States.sleep_to_idle: Pos(0, 0),
        States.walk_left: Pos(-3, 0),
        States.walk_right: Pos(3, 0),
    }

    # Animation frame cycle
    cycle = 0
    animationFramePaths: list
    currentState: States
    pos = Pos(0, 0)

    @classmethod
    def getCurrentFramePath(cls):
        return cls.animationFramePaths[cls.cycle]

    @classmethod
    def getCurrentFrameDelay(cls):
        return cls.STATE_FRAME_DELAYS[cls.currentState]

    @classmethod
    def getCurrentPos(cls):
        return cls.pos
    
    @classmethod
    def setCurrentPos(cls, x, y):
        cls.pos.x, cls.pos.y = x, y

    @classmethod
    def init(cls, xcoord: int, ycoord: int, KeepInFrame=True):
        cls.pos.x = xcoord
        cls.pos.y = ycoord
        cls.SpriteProperties.init(cls, KeepInFrame)
        cls.currentState = cls.States.idle

        cls._update_frame_paths()

    @classmethod
    def update(cls):
        cls._update_frame()
        cls._update_pos()

        cls.checkSpriteProperties()


    @classmethod
    def onLeftClick(cls, event: QtGui.QMouseEvent):
        if(cls.currentState == cls.States.sleep or cls.currentState == cls.States.idle_to_sleep):
            cls._change_state_to(cls.States.idle)
        else:
            cls._change_state_to(cls.States.sleep_to_idle)
    


    @classmethod
    def _update_pos(cls):
        cls.pos = Pos(cls.pos.x + cls.STATE_DISPLACEMENTS[cls.currentState].x,
                      cls.pos.y + cls.STATE_DISPLACEMENTS[cls.currentState].y)

    @classmethod
    def _update_frame(cls):
        if(cls.cycle < len(cls.animationFramePaths) - 1):
            cls.cycle += 1
        else:
            cls.cycle = 0
            cls._next_state()

    @classmethod
    def _next_state(cls):
        cls._change_state_to(random.choice(
            cls.NEXT_POSSIBLE_STATES[cls.currentState]))

    @classmethod
    def _change_state_to(cls, state: States):
        cls.currentState = state
        cls.cycle = 0
        cls._update_frame_paths()

    @classmethod
    def _update_frame_paths(cls):
        # print(os.system("dir"))
        # print(cls.ANIMATION_FRAME_PATH +
        #       cls.currentState.name + "\\")
        cls.animationFramePaths = [cls.ANIMATION_FRAME_PATH +
                                   cls.currentState.name + "\\" + name for name in os.listdir(cls.ANIMATION_FRAME_PATH +
                                                                                              cls.currentState.name + "\\")]


    ## Class Properties
    class SpriteProperties:
        KeepInFrame: bool = True
        sprite = None

        max_x: int
        max_y: int

        @classmethod
        def init(cls, sprite, KeepInFrame = True):
            cls.KeepInFrame = KeepInFrame
            cls.sprite = sprite
            cls.max_x = QtGui.QGuiApplication.primaryScreen().availableGeometry().width() - sprite.SPRITE_SIZE.x
            cls.max_y = QtGui.QGuiApplication.primaryScreen().availableGeometry().height() - sprite.SPRITE_SIZE.y

    @classmethod
    def checkSpriteProperties(cls) -> None:
        if(cls.SpriteProperties.KeepInFrame):
            cls.keepSpriteInFrame()

    @classmethod
    def keepSpriteInFrame(cls) -> None:
        if(cls.pos.x <= 0):
            cls._change_state_to(cls.States.walk_right)
        elif (cls.pos.x >= cls.SpriteProperties.max_x):
            cls._change_state_to(cls.States.walk_left)