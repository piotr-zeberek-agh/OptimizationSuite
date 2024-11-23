import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Przykładowa Aplikacja PyQt6")
        self.setGeometry(100, 100, 400, 200)

        # Tworzenie widżetów
        label = QLabel("Witaj w PyQt6!")
        label.setStyleSheet("font-size: 16px;")

        button = QPushButton("Kliknij mnie")
        button.clicked.connect(self.on_button_click)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(button)

        # Ustawienie centralnego widżetu
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def on_button_click(self):
        self.statusBar().showMessage("Kliknięto przycisk!", 2000)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
