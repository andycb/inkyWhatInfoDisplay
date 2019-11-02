class DebugInky:
    WIDTH = 400
    HEIGHT = 300
    WHITE = "#ffffff"
    RED = "#ff0000"
    BLACK = "#000000"
    _img = 0

    def set_image(self,  img):
        self._img = img

    def show(self):
        self._img.save("debug.png")

    def set_border(self, b):
        self._ = b