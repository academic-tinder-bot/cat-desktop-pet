import sys

from PyQt6 import QtGui
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from sprite.sprite_cat import Cat as sprite

# Image Path
SYSTEM_TRAY_ICON_PATH = "assets\\systemtray_icon\\icon.png"


class PetWindow(QWidget):

    def __init__(self, parent=None):
        super(PetWindow, self).__init__(parent)

        self.xcoord = QtGui.QGuiApplication.primaryScreen().availableGeometry().width() - \
            sprite.SPRITE_SIZE.x - 150
        self.ycoord = QtGui.QGuiApplication.primaryScreen(
        ).availableGeometry().height() - sprite.SPRITE_SIZE.y
        self.move(self.xcoord, self.ycoord)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint |
                            Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.SubWindow)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.repaint()
        self.label = QLabel(self)

        self.installEventFilter(self)

        self.resize(sprite.SPRITE_SIZE.x, sprite.SPRITE_SIZE.y)

        self.timer = QTimer()
        # self.next_state()
        sprite.init(self.xcoord, self.ycoord)
        # self.timer.timeout.connect(self.update)
        # self.timer.start(1)

        # Animation Timer
        self.animationTimer = QTimer()
        self.animationTimer.timeout.connect(self.update_sprite_render)
        self.animationTimer.start(1)
        # I don't know why, but not having this line breaks the animation, and I'm not going to question why
        self.label.setPixmap(QPixmap(sprite.getCurrentFramePath()))

    animationTimer: QTimer

    # def update(self):
    #     self.update_sprite_render()

    def update_sprite_render(self):
        sprite.update()
        self.label.setPixmap(QPixmap(sprite.getCurrentFramePath()))
        self.animationTimer.start(sprite.getCurrentFrameDelay())
        self.move(sprite.getCurrentPos().x, sprite.getCurrentPos().y)

    coordsFromMouse = QPoint()

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if(event.button() == Qt.MouseButton.LeftButton):
            sprite.onLeftClick(event)
            self.resetAnimationTimer()

        self.xcoord = sprite.pos.x
        self.ycoord = sprite.pos.y

        self.coordsFromMouse = QPoint(self.xcoord, self.ycoord) - QPoint(
            int(event.globalPosition().x()), int(event.globalPosition().y()))

        self.animationTimer.stop()
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        self.animationTimer.stop()
        eventPos = QPoint(int(event.globalPosition().x()), int(event.globalPosition().y()))
        delta = eventPos - QPoint(self.xcoord, self.ycoord)

        newPos = QPoint(self.xcoord, self.ycoord) + delta + self.coordsFromMouse
        self.move(newPos.x(), newPos.y())
        self.xcoord = newPos.x()
        self.ycoord = newPos.y()
        return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        # print("Release!")
        self.resetAnimationTimer()
        sprite.setCurrentPos(self.xcoord, self.ycoord)
        return super().mouseReleaseEvent(event)

    def resetAnimationTimer(self) -> None:
        self.animationTimer.stop()
        self.animationTimer = QTimer()
        self.animationTimer.timeout.connect(self.update_sprite_render)
        self.animationTimer.start(1)

    def resetTimer(self) -> None:
        self.timer.stop()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1)


class SystemTrayIcon(QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtGui.QMenu(parent)
        exitAction = menu.addAction("Exit")
        self.setContextMenu(menu)


def main():
    app = QApplication(sys.argv)

    # Application Window
    ex = PetWindow()
    ex.show()

    # System Tray
    tray = QSystemTrayIcon()
    tray.setIcon(QIcon(SYSTEM_TRAY_ICON_PATH))
    tray.setVisible(True)

    menu = QMenu()
    # option1 = QAction("Option 1")
    # menu.addAction(option1)

    # To quit the app
    quit = QAction("Kill Pet")
    quit.triggered.connect(app.quit)
    menu.addAction(quit)

    tray.setContextMenu(menu)

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
