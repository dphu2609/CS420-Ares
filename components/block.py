from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt  # Import Qt for scaling options

# Assuming ResourceHolder is a class that loads images
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

    def __init__(self, type, size):
        super().__init__()

        # Load the image from ResourceHolder
        decoded_type = self.decoder.get(type, "flat")  # Default to flat if type is not found
        image_path = ResourceHolder().get_image(decoded_type)  # Ensure this returns a valid path or QPixmap
        self.image_label = QLabel(self)  # QLabel to hold the image

        # If image_path is a file path, load it as a QPixmap
        if isinstance(image_path, str):  # Check if it's a file path
            pixmap = QPixmap(image_path)
        elif isinstance(image_path, QPixmap):  # If already a QPixmap, use it directly
            pixmap = image_path
        else:
            raise ValueError("Invalid image source in ResourceHolder")

        # Scale the pixmap to fit the QLabel's size while maintaining aspect ratio
        scaled_pixmap = pixmap.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.image_label.setPixmap(scaled_pixmap)

        # Set fixed size for the Block widget and adjust QLabel size to fit
        self.setFixedSize(size, size)
        self.image_label.setFixedSize(size, size)
