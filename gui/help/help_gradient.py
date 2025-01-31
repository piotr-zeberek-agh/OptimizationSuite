from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QTabWidget, QWidget, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
import json

class HelpWindowGradient(QDialog):
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
        layout.addWidget(self.tab_widget)

        path = "config/help_gradient/"
        self.gradient_help = self.load_help_data(path+"help_gradient.json")

        self.add_main_tab()

        self.tab_widget.setCurrentIndex(1)
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

    def add_main_tab(self):
        """Adds the main tab."""
        main_tab = QWidget()
        main_layout = QVBoxLayout()

        label_1 = QLabel("Gradient Descent: An algorithm that minimizes a function by following its steepest descent.")
        label_1.setStyleSheet("""
            font-family: Arial, Helvetica, sans-serif;
            font-size: 16px;
            font-weight: bold;
            text-align: center;
            color: #CCC;
        """)
        label_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(label_1)

        for key, value in self.gradient_help.items():
            label = QLabel(f"<b>{key}</b>: {value}")
            label.setWordWrap(True)
            main_layout.addWidget(label)

        note = QLabel()
        note.setText('<a href="https://www.ibm.com/think/topics/gradient-descent">Click here to view the article</a>')
        note.setOpenExternalLinks(True) 
        main_layout.addWidget(note)
        
        main_tab.setLayout(main_layout)
        self.tab_widget.addTab(main_tab, "Main")