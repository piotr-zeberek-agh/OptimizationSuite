from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QTabWidget, QWidget, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
import json

class HelpWindowFullerenes(QDialog):
    """Window displaying information about the program with tabs."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Help")
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(900, 600)
        self.setStyleSheet("background-color: #2f2f2f; color: white;")

        layout = QVBoxLayout()
        container = QWidget()
        container.setLayout(layout)
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        self.algorithm = self.load_help_data("config/algorithm.json")
        path = "config/help_fullerenes/"
        self.fullerenes_help = self.load_help_data(path+"help_fullerenes.json")

        self.add_algorithm_tab()
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

    def add_main_tab(self):
        """Adds the main tab."""
        main_tab = QWidget()
        main_layout = QVBoxLayout()

        label_1 = QLabel("Fullerenes: Carbon molecules with hexagonal and pentagonal rings forming spherical or cylindrical shapes.")
        label_1.setStyleSheet("""
            font-family: Arial, Helvetica, sans-serif;
            font-size: 16px;
            font-weight: bold;
            text-align: center;
            color: #CCC;
        """)
        label_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(label_1)

        label_2 = QLabel("Here you can check the importance of specific assets.")
        label_2.setStyleSheet("""
            font-family: Arial, Helvetica, sans-serif;
            font-size: 20px;
            font-weight: bold;
            text-align: center;
            color: #CCC;
        """)

        for key, value in self.fullerenes_help.items():
            label = QLabel(f"<b>{key}</b>: {value}")
            label.setWordWrap(True)
            main_layout.addWidget(label)

        note = QLabel()
        note.setText('<a href="https://journals.aps.org/prb/abstract/10.1103/PhysRevB.42.9458">Click here to view the article</a>')
        note.setOpenExternalLinks(True)  # This ensures the link opens in the browser
        main_layout.addWidget(note)
        
        main_tab.setLayout(main_layout)
        self.tab_widget.addTab(main_tab, "Main")