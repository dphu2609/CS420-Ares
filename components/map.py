from PyQt6.QtWidgets import QWidget, QGridLayout
from components.block import Block

class VisualMap(QWidget):
    def __init__(self, matrix, total_width, total_height):
        super().__init__()

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        # Calculate block size based on matrix dimensions and total available size
        rows = len(matrix)
        cols = len(matrix[0]) if rows > 0 else 0
        block_size = min(total_width // cols, total_height // rows)

        # Initialize the matrix with the calculated block size
        self.init_matrix(matrix, block_size)

    def init_matrix(self, matrix, block_size):
        for i, row in enumerate(matrix):
            for j, block_type in enumerate(row):
                block = Block(block_type, block_size)
                self.layout.addWidget(block, i, j)
                block.show()
