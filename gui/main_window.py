from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Optimization Suite")
        self.setGeometry(100, 100, 400, 200)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.label = QLabel("Initial Text")
        self.button = QPushButton("Click Me")
        self.button.clicked.connect(self.on_button_click)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.button)

    def on_button_click(self):
        self.label.setText("Clicked")
