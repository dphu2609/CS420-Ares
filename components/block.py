from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from components.resource_holder import ResourceHolder

class Block(QWidget):
    decoder = {
        "#" : "wall",
        " " : "flat",
        "$" : "stone",
        "@" : "ares",
        "." : "switch",
        "*" : "stone",
        "+" : "ares"
    }

    def __init__(self, block_type: str, size: int, weight: int = None):
        super().__init__()

        # Load the main image
        decoded_type = self.decoder.get(block_type, "flat")
        image_path = ResourceHolder().get_image(decoded_type)
        self.image_label = QLabel(self)

        if isinstance(image_path, str):
            pixmap = QPixmap(image_path)
        elif isinstance(image_path, QPixmap):
            pixmap = image_path
        else:
            raise ValueError("Invalid image source in ResourceHolder")

        # Scale the main image to fit
        scaled_pixmap = pixmap.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.image_label.setPixmap(scaled_pixmap)

        # Set fixed size for the Block widget and QLabel
        self.setFixedSize(size, size)
        self.image_label.setFixedSize(size, size)

        # Stack a smaller object if type is stone and weight is provided
        if decoded_type == "stone" and weight is not None:
            weight_label = QLabel(str(weight), self)
            weight_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            weight_label.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 0);")
            weight_label.setFixedSize(size // 2, size // 2)
            weight_label.move(size // 4, size // 4)
