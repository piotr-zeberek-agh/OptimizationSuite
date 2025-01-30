from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QTabWidget, QWidget, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
import json

class HelpWindowDefault(QDialog):
    """Window displaying information about the program with tabs."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Help")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(800, 600)
        self.setStyleSheet("background-color: #2f2f2f; color: white;")

        layout = QVBoxLayout()
        container = QWidget()
        container.setLayout(layout)
        self.tab_widget = QTabWidget()

        self.algorithm = self.load_help_data("config/algorithm.json")
        self.add_algorithm_tab()

        layout.addWidget(self.tab_widget)
        self.setLayout(layout)

    def load_help_data(self, file_path):
        """Load JSON file with help data."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print("File 'help.json' not found in 'config' directory.")
            return None
        except json.JSONDecodeError:
            print("Error loading JSON file. It may be corrupted or in incorrect format.")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    def add_algorithm_tab(self):
        """Adds the algorithm tab."""
        main_tab = QWidget()
        main_layout = QVBoxLayout()
        
        for key, value in self.algorithm.items():
            label = QLabel(f"<b>{key}</b>: {value}")
            label.setWordWrap(True)
            main_layout.addWidget(label)
        
        main_tab.setLayout(main_layout)
        self.tab_widget.addTab(main_tab, "Algorithm")