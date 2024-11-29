from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget
from PyQt6.QtWidgets import QApplication, QComboBox, QTableWidget, QTableWidgetItem
import pandas as pd

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Optimization Suite")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)



        # Dropdown menu for scenario selection
        self.combo_box = QComboBox()
        self.combo_box.addItem("Structure Of Fullerenes")
        self.combo_box.addItem("Portfolio Optimization")
        self.combo_box.currentIndexChanged.connect(self.on_scenario_selected)

        # Table to display data
        self.table_widget = QTableWidget()
        self.layout.addWidget(self.combo_box)
        self.layout.addWidget(self.table_widget)

        # Button to load data from CSV
        self.load_button = QPushButton("Load Data")
        self.load_button.clicked.connect(self.load_data)
        self.layout.addWidget(self.load_button)


    def on_scenario_selected(self):
        # Update view based on the selected scenario
        selected_scenario = self.combo_box.currentText()
        if selected_scenario == "Structure Of Fullerenes":
            # self.set_aaaa_view()
            self.label = QLabel("Structure Of Fullerenes")
            self.layout.addWidget(self.label)

        elif selected_scenario == "Portfolio Optimization":

            self.set_portfolio_view()

    # def set_aaaa_view(self):
    #     # Example of view for "aaaa" scenario
    #     self.setWindowTitle("Scenario Aaaa")
    #     self.load_data()

    def set_portfolio_view(self):
        # Example of view for "bbbb" scenario
        self.setWindowTitle("Portfolio Optimization")
        self.load_data()

    def load_data(self):
        # Load data from CSV (replace with your actual file path)
        try:
            data = pd.read_csv("asset_data.csv")

            # Populate the table widget with data
            self.table_widget.setRowCount(len(data))
            self.table_widget.setColumnCount(len(data.columns))
            self.table_widget.setHorizontalHeaderLabels(data.columns)

            for row in range(len(data)):
                for col in range(len(data.columns)):
                    item = QTableWidgetItem(str(data.iloc[row, col]))
                    self.table_widget.setItem(row, col, item)
        except Exception as e:
            print(f"Error loading data: {e}")


        # test code
    #     self.label = QLabel("Initial Text")
    #     self.button = QPushButton("Click Me")
    #     self.button.clicked.connect(self.on_button_click)

    #     self.layout.addWidget(self.label)
    #     self.layout.addWidget(self.button)

    # def on_button_click(self):
    #     self.label.setText("Clicked")
