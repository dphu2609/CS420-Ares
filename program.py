import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QComboBox, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt

class GraphAlgoVisualizer(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("Graph Algorithm Visualizer")
        self.setGeometry(400
                         , 400, 600, 400)

        # Initialize layout
        self.layout = QVBoxLayout()

        # Initialize file selection label
        self.file_label = QLabel("No file selected", self)
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # File selection button
        self.file_button = QPushButton("Select Graph Input File", self)
        self.file_button.clicked.connect(self.select_file)

        # Algorithm dropdown menu
        self.algo_label = QLabel("Select Algorithm:", self)
        self.algo_menu = QComboBox(self)
        self.algo_menu.addItems(["BFS", "DFS", "UCS", "A*"])

        # Visualization button
        self.visualize_button = QPushButton("Visualize", self)
        self.visualize_button.clicked.connect(self.visualize_algorithm)

        # Add widgets to the layout
        self.layout.addWidget(self.file_button)
        self.layout.addWidget(self.file_label)
        self.layout.addWidget(self.algo_label)
        self.layout.addWidget(self.algo_menu)
        self.layout.addWidget(self.visualize_button)

        # Set the layout for the main widget
        self.setLayout(self.layout)

        # Placeholder for the selected file path
        self.selected_file = None

    def select_file(self):
        # Open file dialog to select a graph input file
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select Graph Input File", "", "Text Files (*.txt);;All Files (*)")
        
        if file_path:
            self.selected_file = file_path
            self.file_label.setText(f"Selected File: {file_path}")

    def visualize_algorithm(self):
        # Check if a file is selected
        if not self.selected_file:
            QMessageBox.warning(self, "No File Selected", "Please select a graph input file.")
            return

        # Get the selected algorithm
        selected_algo = self.algo_menu.currentText()

        # Placeholder logic for visualization
        QMessageBox.information(self, "Visualization", f"Running {selected_algo} on {self.selected_file}")

        # Here you would implement visualization code, potentially using networkx and matplotlib

if __name__ == "__main__":
    # Initialize the application
    app = QApplication(sys.argv)
    window = GraphAlgoVisualizer()
    window.show()
    sys.exit(app.exec())
