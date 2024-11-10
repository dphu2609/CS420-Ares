from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QComboBox
import sys, collections

from components.resource_holder import ResourceHolder
from components.map import VisualMap
from src.map_data import MapData
from src.algorithms.base_algo import BaseAlgo
from src.algorithms.a_star import AStar

from PyQt6.QtCore import QTimer

class App(QMainWindow):
    DELAY_STEP = 500

    def __init__(self):
        super().__init__()

        self.resource_holder = ResourceHolder()
        self.resource_holder.load_images()
        self.map_data = MapData()

        self.moves = collections.deque()

        self.initUI()

        # self.test_move()

    def initUI(self):
        self.setWindowTitle("Algorithm Visualization")

        # Get screen size and set window size to 2/3 of the screen size
        screen = QApplication.primaryScreen().availableGeometry()
        width = int(screen.width() * 2 / 3)
        height = int(screen.height() * 2 / 3)
        self.setFixedSize(width, height)

        # Center the window
        self.setGeometry((screen.width() - width) // 2, (screen.height() - height) // 2, width, height)

        # Set the background color to white
        self.setStyleSheet("background-color: white;")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        # Create buttons with custom styles
        button_style = "background-color: #333333; color: white;"  # Dark grey background, white text

        self.file_button = QPushButton("Choose File", self)
        self.file_button.setStyleSheet(button_style)
        self.file_button.clicked.connect(self.choose_file)
        self.layout.addWidget(self.file_button)

        # Placeholder for the visualization map
        self.visualization_map = None  # Initialize without creating VisualMap yet

        # Create a dropdown with the same style as buttons
        self.algo_dropdown = QComboBox(self)
        self.algo_dropdown.setStyleSheet(button_style)  # Apply the same style to the dropdown
        self.algo_dropdown.addItems(["BFS", "DFS", "UCS", "A*"])
        self.layout.addWidget(self.algo_dropdown)

        self.start_button = QPushButton("Start Visualization", self)
        self.start_button.setStyleSheet(button_style)  # Apply the same style
        self.start_button.clicked.connect(self.start_visualization)
        self.layout.addWidget(self.start_button)

        self.central_widget.setLayout(self.layout)

    def display_map(self):
        # Remove the previous VisualMap widget if it exists
        if self.visualization_map is not None:
            self.central_widget.layout().removeWidget(self.visualization_map)
            self.visualization_map.deleteLater()
            self.visualization_map = None

        # Set the dimensions for the VisualMap based on the current window size
        total_width = self.width()
        total_height = self.height() - 140

        # Create a new VisualMap with the map data and calculated dimensions
        self.visualization_map = VisualMap(self.map_data, total_width, total_height)
        self.central_widget.layout().addWidget(self.visualization_map)

        # Set the background color of VisualMap to white
        self.visualization_map.setStyleSheet("background-color: white;")

        self.layout.insertWidget(1, self.visualization_map)  # Insert after file button

        self.visualization_map.update()
        self.update()

    def choose_file(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:  # Check if any files were selected
                file_path = selected_files[0]
                self.parse_map(file_path)
                self.display_map()
            else:
                print("No file selected.")  # Optionally inform the user

    def parse_map(self, file_path):
        content = []
        with open(file_path, "r") as file:
            content = file.readlines()

        stones = list(map(int, content[0].split()))
        map_data = [list(line.strip('\n')) for line in content[1:]]

        self.map_data.set_map_matrix(map_data, stones)

    def push_moves(self, moves_list: list):
        moves_list = [move.lower() for move in moves_list]
        self.moves.extend(moves_list)

    def reset_moves(self):
        self.moves.clear()

    def run_moves(self):
        if len(self.moves) == 0:
            return

        move = self.moves.popleft()
        self.map_data.move(move)
        self.display_map()

        QTimer.singleShot(self.DELAY_STEP, self.run_moves)
    
    def start_visualization(self):
        selected_algo = self.algo_dropdown.currentText()
        print(f"Starting visualization with {selected_algo}")

        # self.algo.set_map(self.map_matrix)
        # self.algo.run()

        # # Get the updated map data after running the algorithm
        # updated_map_data = self.algo.get_map()

        # # Display the updated map data
        # self.display_map(updated_map_data.get_display_map())

        if selected_algo == "A*":
            astar = AStar()
            astar.set_map(self.map_data.copy())
            astar.run()
            path, maps, total_w = astar.get_path()
            time_consumed, mem_consumed, num_explored = astar.get_stats()
            print(f"Path: {path}")
            print(f"Total weight: {total_w}")
            print(f"Time consumed: {time_consumed} seconds")
            print(f"Memory consumed: {mem_consumed} MB")
            print(f"Number of explored nodes: {num_explored}")

            self.push_moves(path)
            QTimer.singleShot(0, self.run_moves)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()  # This will display the window in full screen as we called showFullScreen() in initUI()
    sys.exit(app.exec())
