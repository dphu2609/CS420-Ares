from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QMutex, QMutexLocker

class ResourceHolder:
    _instance = None
    _mutex = QMutex()

    def __new__(cls):
        with QMutexLocker(cls._mutex):
            if cls._instance is None:
                cls._instance = super(ResourceHolder, cls).__new__(cls)
                cls._instance._images = {}
            return cls._instance
        
    paths = {
        "stone" : "assets/stone.png",
        "flat" : "assets/flat.png",
        "switch" : "assets/switch.jpeg",
        "wall" : "assets/wall.jpg",
        "ares" : "assets/ares.png",
    }

    def load_images(self):
        for name, path in self.paths.items():
            self.load_image(name, path)

    def load_image(self, name, path):
        if name not in self._images:
            self._images[name] = QPixmap(path)

    def get_image(self, name):
        return self._images.get(name, None)