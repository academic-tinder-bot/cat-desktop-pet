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

        self.xcoord = QtGui.QGuiApplication.primaryScreen().availableGeometry().width() - sprite.SPRITE_SIZE.x - 150
        self.ycoord = QtGui.QGuiApplication.primaryScreen().availableGeometry().height() - sprite.SPRITE_SIZE.y
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
        self.timer.timeout.connect(self.update)
        self.timer.start(1)

        # I don't know why, but not having this line breaks the animation, and I'm not going to question why
        self.label.setPixmap(QPixmap(sprite.getCurrentFramePath()))

    def update(self):
        self.update_sprite_render()

    def update_sprite_render(self):
        sprite.update()
        self.label.setPixmap(QPixmap(sprite.getCurrentFramePath()))
        self.timer.start(sprite.getCurrentFrameDelay())
        self.move(sprite.getCurrentPos().x, sprite.getCurrentPos().y)

    def mousePressEvent(self, event) -> None:
        if(event.button() == Qt.MouseButton.LeftButton):
            sprite.onLeftClick(event)
            self.resetTimer()
        return super().mousePressEvent(event)

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
