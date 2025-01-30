from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QTabWidget, QWidget, QSpacerItem, QSizePolicy
import json
from PyQt6.QtCore import Qt

class HelpWindowPortfolio(QDialog):
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

        self.algorithm = self.load_help_data("config/algorithm.json")
        path = "config/help_portfolio/"
        self.asset_descriptions = self.load_help_data(path+"asset_descriptions.json")
        self.stocks_help = self.load_help_data(path+"stocks.json")
        self.bonds_help = self.load_help_data(path+"bonds.json")
        self.commodities_help = self.load_help_data(path+"commodities.json")
        self.etfs_help = self.load_help_data(path+"etfs.json")
        self.currencies_help = self.load_help_data(path+"currencies.json")
        self.indexes_help = self.load_help_data(path+"indexes.json")

        self.add_algorithm_tab()
        self.add_main_tab()
        self.add_tab_stocks()
        self.add_tab_bonds()
        self.add_tab_commodities()
        self.add_tab_etfs()
        self.add_tab_currencies()
        self.add_tab_indexes()

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

        label_1 = QLabel("Welcome to the financial portfolio optimization application")
        label_1.setStyleSheet("""
            font-family: Arial, Helvetica, sans-serif;
            font-size: 20px;
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

        label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(label_2)
        
        for key, value in self.asset_descriptions.items():
            label = QLabel(f"<b>{key}</b>: {value}")
            label.setWordWrap(True)
            main_layout.addWidget(label)

        desc_label = QLabel("Note, you can add your own assets (check the yfinance library documentation for the name of the financial instrument)")
        main_layout.addWidget(desc_label)
        
        main_tab.setLayout(main_layout)
        self.tab_widget.addTab(main_tab, "Main")

    def add_tab_stocks(self):
        """Add tab with stocks help."""
        tab = QWidget()
        layout = QVBoxLayout()
        if self.stocks_help:
            for key, value in self.stocks_help.items():
                label = QLabel(f"<b>{key}</b>: {value}")
                label.setWordWrap(True)
                layout.addWidget(label)
        else:
            error_label = QLabel("Error loading help data.")
            layout.addWidget(error_label)
        tab.setLayout(layout)
        self.tab_widget.addTab(tab, "Stocks")

    def add_tab_bonds(self):
        """Add tab with bonds help."""
        tab = QWidget()
        layout = QVBoxLayout()
        if self.bonds_help:
            for key, value in self.bonds_help.items():
                label = QLabel(f"<b>{key}</b>: {value}")
                label.setWordWrap(True)
                layout.addWidget(label)
        else:
            error_label = QLabel("Error loading help data.")
            layout.addWidget(error_label)
        tab.setLayout(layout)
        self.tab_widget.addTab(tab, "Bonds")

    def add_tab_commodities(self):
        """Add tab with commodities help."""
        tab = QWidget()
        layout = QVBoxLayout()
        if self.commodities_help:
            for key, value in self.commodities_help.items():
                label = QLabel(f"<b>{key}</b>: {value}")
                label.setWordWrap(True)
                layout.addWidget(label)
        else:
            error_label = QLabel("Error loading help data.")
            layout.addWidget(error_label)
        tab.setLayout(layout)
        self.tab_widget.addTab(tab, "Commodities")

    def add_tab_etfs(self):
        """Add tab with etfs help."""
        tab = QWidget()
        layout = QVBoxLayout()
        if self.etfs_help:
            for key, value in self.etfs_help.items():
                label = QLabel(f"<b>{key}</b>: {value}")
                label.setWordWrap(True)
                layout.addWidget(label)
        else:
            error_label = QLabel("Error loading help data.")
            layout.addWidget(error_label)
        tab.setLayout(layout)
        self.tab_widget.addTab(tab, "ETFs")

    def add_tab_currencies(self):
        """Add tab with currencies help."""
        tab = QWidget()
        layout = QVBoxLayout()
        if self.currencies_help:
            for key, value in self.currencies_help.items():
                label = QLabel(f"<b>{key}</b>: {value}")
                label.setWordWrap(True)
                layout.addWidget(label)
        else:
            error_label = QLabel("Error loading help data.")
            layout.addWidget(error_label)
        tab.setLayout(layout)
        self.tab_widget.addTab(tab, "Currencies")

    def add_tab_indexes(self):
        """Add tab with indexes help."""
        tab = QWidget()
        layout = QVBoxLayout()
        if self.indexes_help:
            for key, value in self.indexes_help.items():
                label = QLabel(f"<b>{key}</b>: {value}")
                label.setWordWrap(True)
                layout.addWidget(label)
        else:
            error_label = QLabel("Error loading help data.")
            layout.addWidget(error_label)
        tab.setLayout(layout)
        self.tab_widget.addTab(tab, "Indexes")