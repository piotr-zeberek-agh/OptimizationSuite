from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QTabWidget, QWidget, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt

class HelpWindowFullerenes(QDialog):
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
        self.add_main_tab()

        layout.addWidget(self.tab_widget)
        self.setLayout(layout)

    def add_main_tab(self):
        """Adds the main tab."""
        main_tab = QWidget()
        main_layout = QVBoxLayout()

        label_1 = QLabel("Window displaying information about the program designed for fullerenes structure.")
        label_1.setStyleSheet("""
            font-family: Arial, Helvetica, sans-serif;
            font-size: 20px;
            font-weight: bold;
            text-align: center;
            color: #CCC;
        """)
        label_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(label_1)

        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        main_layout.addItem(spacer)
        
        main_tab.setLayout(main_layout)
        self.tab_widget.addTab(main_tab, "Main")
