from PyQt6.QtWidgets import QWidget, QGridLayout
from components.block import Block
from src.map_data import MapData

class VisualMap(QWidget):
    def __init__(self, map_data, total_width, total_height):
        super().__init__()

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.matrix = map_data.get_display_map()
        self.stones = map_data.get_stones()

        # Calculate block size based on matrix dimensions and total available size
        rows = len(self.matrix)
        cols = len(self.matrix[0]) if rows > 0 else 0
        block_size = min(total_width // cols, total_height // rows)

        # Initialize the matrix with the calculated block size
        self.init_matrix(self.matrix, block_size, self.stones)

    def init_matrix(self, matrix, block_size, stones):
        index = 0
        for i, row in enumerate(matrix):
            for j, block_type in enumerate(row):
                if block_type == "$" or block_type == "*":
                    block = Block(block_type, block_size, stones[index])
                    index += 1
                else:
                    block = Block(block_type, block_size)
                self.layout.addWidget(block, i, j)
                block.show()
