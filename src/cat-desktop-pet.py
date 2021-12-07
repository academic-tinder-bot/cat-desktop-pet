import os
import os.path
import sys

from PyQt6 import QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from enum import Enum
import random

# Image Path
ANIMATION_FRAMES_PATH = 'assets\\animation_frames\\'
tempgifpath = "assets\\animation_frames\\idle\\"
tempimgspath = [ANIMATION_FRAMES_PATH +
                name for name in os.listdir(ANIMATION_FRAMES_PATH)]


class State(Enum):
    idle = 0
    idle_to_sleep = 1
    sleep = 2
    sleep_to_idle = 3
    walk_left = 4
    walk_right = 5


# [State.idle, State.idle_to_sleep,  State.sleep, State.sleep_to_idle, State.walk_left, State.walk_right]
# Possible next states of cat based on current state
NEXT_STATE = {
    State.idle: [State.idle, State.idle_to_sleep, State.walk_left, State.walk_right],
    State.idle_to_sleep: [State.sleep],
    State.sleep: [State.sleep, State.sleep_to_idle],
    State.sleep_to_idle: [State.idle, State.walk_left, State.walk_right],
    State.walk_left: [State.idle, State.idle_to_sleep, State.walk_left, State.walk_right],
    State.walk_right: [State.idle, State.idle_to_sleep, State.walk_left, State.walk_right],
}

STATE_DELAYS = {
    State.idle: 400,
    State.idle_to_sleep: 100,
    State.sleep: 1000,
    State.sleep_to_idle: 100,
    State.walk_left: 100,
    State.walk_right: 100,
}

STATE_DISPLACEMENTS = {
    State.idle: 0,
    State.idle_to_sleep: 0,
    State.sleep: 0,
    State.sleep_to_idle: 0,
    State.walk_left: -3,
    State.walk_right: 3,
}


class window(QWidget):
    cycle = 0
    animationFramePaths = None
    state = State.idle

    xcoord = 0
    ycoord = 0

    def __init__(self, parent=None):
        super(window, self).__init__(parent)

        # Get window size
        self.xcoord = QtGui.QGuiApplication.primaryScreen().availableGeometry().width() - 250
        self.ycoord = QtGui.QGuiApplication.primaryScreen().availableGeometry().height() - 100

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint |
                            Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.SubWindow)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.repaint()
        self.label = QLabel(self)

        self.installEventFilter(self)

        self.resize(100, 100)
        # self.label.move(50, 20)

        self.timer = QTimer()
        self.next_state()
        self.timer.timeout.connect(self.update)
        self.timer.start(1)

        # I don't know why, but not having this line breaks the animation, and I'm not going to question why
        self.label.setPixmap(QPixmap(self.animationFramePaths[self.cycle]))

    def update(self):
        # print("Update!")
        self.render_next_frame()

    def render_next_frame(self):
        self.get_next_frame()
        self.label.setPixmap(QPixmap(self.animationFramePaths[self.cycle]))
        # self.label.setStyleSheet("""background-color: #000000""")
        self.timer.start(STATE_DELAYS[self.state])

        self.xcoord += STATE_DISPLACEMENTS[self.state]
        self.move(self.xcoord, self.ycoord)

    # Gets the next frame in the cycle, or updates to a new state otherwise.
    def get_next_frame(self):
        if(self.cycle < len(self.animationFramePaths) - 1):
            self.cycle += 1
        else:
            self.next_state()

    # Updates state and gif
    def next_state(self):
        # print("Before: ", self.state)
        self.state = random.choice(NEXT_STATE[self.state])
        # print("After: ", self.state)
        self.cycle = 0
        self.animationFramePaths = [ANIMATION_FRAMES_PATH +
                                    self.state.name + "\\" + name for name in os.listdir(ANIMATION_FRAMES_PATH +
                                                                                         self.state.name + "\\")]

    # Update state, but make sure that the next state is different from the previous.
    def change_state_to(self, state: State):
        self.state = state
        self.cycle = 0
        self.animationFramePaths = [ANIMATION_FRAMES_PATH +
                                    self.state.name + "\\" + name for name in os.listdir(ANIMATION_FRAMES_PATH +
                                                                                         self.state.name + "\\")]

    def mousePressEvent(self, event) -> None:
        if(event.button() == Qt.MouseButton.LeftButton):
            if(self.state == State.sleep or self.state == State.idle_to_sleep):
                self.change_state_to(State.idle)
            else:
                self.change_state_to(State.sleep_to_idle)
            self.resetTimer()
        return super().mousePressEvent(event)

    def resetTimer(self) -> None:
        self.timer.stop()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1)


def main():
    app = QApplication(sys.argv)
    ex = window()

    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
