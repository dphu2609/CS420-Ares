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

    def __init__(self, type, size, weight=None):
        super().__init__()

        # Load the main image
        decoded_type = self.decoder.get(type, "flat")
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
        if type == "stone" and weight is not None:
            self.add_stacked_item(size)

    def add_stacked_item(self, size):
        # Load a smaller object image (for example, "half_stone")
        stacked_image_path = ResourceHolder().get_image("half_stone")  # Ensure a "half_stone" image exists
        stacked_label = QLabel(self)

        if isinstance(stacked_image_path, str):
            stacked_pixmap = QPixmap(stacked_image_path)
        elif isinstance(stacked_image_path, QPixmap):
            stacked_pixmap = stacked_image_path
        else:
            raise ValueError("Invalid image source in ResourceHolder")

        # Scale to half the size
        half_size = size // 2
        stacked_scaled_pixmap = stacked_pixmap.scaled(half_size, half_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        stacked_label.setPixmap(stacked_scaled_pixmap)

        # Position the stacked item on top of the stone
        stacked_label.move((size - half_size) // 2, (size - half_size) // 2)
        stacked_label.setFixedSize(half_size, half_size)
        stacked_label.show()
