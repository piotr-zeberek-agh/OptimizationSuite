from PyQt6.QtWidgets import (
    QApplication, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QWidget, QSizePolicy
)

class ExampleWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Główny układ poziomy
        main_layout = QHBoxLayout()

        # Lewa kolumna
        left_layout = QVBoxLayout()

        # Ustawienie szerokości lewego layoutu
        left_layout.setSpacing(10)

        # Etykieta z opisem
        self.interval_label = QLabel("Enter the interval for the data")
        self.interval_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.interval_label.setMinimumWidth(200)  # Minimalna szerokość
        left_layout.addWidget(self.interval_label)

        # Pole do wprowadzania danych
        self.interval_input = QLineEdit()
        self.interval_input.setPlaceholderText("e.g., 1-100")
        left_layout.addWidget(self.interval_input)

        # Przycisk do akcji
        self.submit_button = QPushButton("Submit")
        left_layout.addWidget(self.submit_button)

        # Dodanie lewej kolumny do głównego układu
        main_layout.addLayout(left_layout, stretch=1)  # Przyznanie większego miejsca

        # Prawa kolumna
        right_layout = QVBoxLayout()

        # Przykładowy placeholder w prawej kolumnie
        self.placeholder_label = QLabel("Chart or results go here")
        self.placeholder_label.setStyleSheet("background-color: lightgray;")
        self.placeholder_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        right_layout.addWidget(self.placeholder_label)

        # Dodanie prawej kolumny do głównego układu
        main_layout.addLayout(right_layout, stretch=2)  # Większy stretch dla prawej kolumny

        # Ustawienie głównego układu w widżecie
        self.setLayout(main_layout)

# Główna aplikacja
if __name__ == "__main__":
    app = QApplication([])
    widget = ExampleWidget()
    widget.setWindowTitle("Example Layout Adjustment")
    widget.resize(600, 400)
    widget.show()
    app.exec()