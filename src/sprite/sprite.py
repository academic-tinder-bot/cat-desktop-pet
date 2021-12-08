


class Sprite:

    # Getter Functions
    def getCurrentFramePath(cls): pass
    def getCurrentFrameDelay(cls): pass
    def getCurrentPos(cls): pass

    # Interface for main to call
    def init(cls, xcoord: int, ycoord: int): pass
    def update(cls): pass

    # Interface to set sprite properties
    class SpriteProperties: pass
    
    # Interactivity
    def onLeftClick(cls, event): pass


class SpritePos:
    x: int
    y: int

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
