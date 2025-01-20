from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QTabWidget, QWidget
import json

class HelpWindow(QDialog):
    """Okno pomocy wyświetlające informacje o programie z zakładkami."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Help")
        self.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout()
        self.tab_widget = QTabWidget()

        self.stocks_help = self.load_help_data("config/help/stocks.json")
        self.bonds_help = self.load_help_data("config/help/bonds.json")
        self.commodities_help = self.load_help_data("config/help/commodities.json")
        self.etfs_help = self.load_help_data("config/help/etfs.json")
        self.currencies_help = self.load_help_data("config/help/currencies.json")
        self.indexes_help = self.load_help_data("config/help/indexes.json")

        if self.stocks_help:
            self.add_main_tab()
            self.add_tab_stocks()
            # self.add_tab_bonds()
            # self.add_tab_commodities()
            # self.add_tab_etfs()
            # self.add_tab_currencies()
            # self.add_tab_indexes()

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

    # Zakładki dla różnych kategorii

    def add_main_tab(self):
        """Dodaje główną zakładkę."""
        main_tab = QWidget()
        main_layout = QVBoxLayout()
        main_label = QLabel("Witaj w aplikacji optymalizacji portfela!\n\n"
                            "Poniżej znajduje się wprowadzenie do jego funkcji.")
        main_layout.addWidget(main_label)
        main_tab.setLayout(main_layout)
        self.tab_widget.addTab(main_tab, "Główna")

    def add_tab_stocks(self):
        """Add tab with stocks help."""
        tab = QWidget()
        layout = QVBoxLayout()
        if self.stocks_help:
            for key, value in self.stocks_help.items():
                label = QLabel(f"<b>{key}</b>: {value}")
                layout.addWidget(label)
        else:
            error_label = QLabel("Error loading help data.")
            layout.addWidget(error_label)
        tab.setLayout(layout)
        self.tab_widget.addTab(tab, "Stocks")

    def add_tab_bonds(self):
        pass

    def add_tab_commodities(self):
        pass

    def add_tab_etfs(self):
        pass

    def add_tab_currencies(self):
        pass

    def add_tab_indexes(self):
        pass