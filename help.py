from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel

class HelpWindow(QDialog):
    """Okno pomocy wyświetlające informacje o programie."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Help")
        self.setGeometry(100, 100, 400, 300)  # Określenie rozmiaru okna

        layout = QVBoxLayout()
        help_label = QLabel("Witaj w aplikacji optymalizacji portfela!\n\n"
                            "Poniżej znajduje się wprowadzenia do jego funkcji.\n"
        layout.addWidget(help_label)

        self.setLayout(layout)

    def show_help(self):
        """Wyświetla okno pomocy."""
        self.show()
