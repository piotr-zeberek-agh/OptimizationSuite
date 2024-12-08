from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QWidget, QComboBox, QTableWidget, QTableWidgetItem, QLineEdit
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

        self.combo_box = QComboBox()
        self.combo_box.addItem("Select Scenario")  # Option for null/empty state
        self.combo_box.addItem("Structure Of Fullerenes")
        self.combo_box.addItem("Portfolio Optimization")
        self.combo_box.addItem("Gradient Descent")

        self.set_base_layout()

        # Initialize load_button to None
        self.load_button = None
        
        self.combo_box.currentTextChanged.connect(self.on_scenario_change)

    def set_base_layout(self):
        """Sets up the base layout with combo box and table widget."""
        self.layout.addWidget(self.combo_box)

        # Initialize and add table widget
        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)

        # Initialize and add text box
        self.text_box = QLineEdit()
        self.layout.addWidget(self.text_box)

    def on_scenario_change(self, selected_scenario: str):
        """Handle the scenario selection event."""
        print(f"Selected scenario: {selected_scenario}")

        # Usuń wszystkie widżety, w tym load_button, przed załadowaniem nowych
        if self.load_button:
            self.layout.removeWidget(self.load_button)
            self.load_button.deleteLater()
            self.load_button = None

        self.clear_layout()
        self.combo_box = QComboBox()

        self.scenario = {"Structure Of Fullerenes", "Portfolio Optimization", "Gradient Descent"}

        self.cb_list = [selected_scenario] + sorted(self.scenario - {selected_scenario})
        self.combo_box.addItems(self.cb_list)

        self.set_base_layout()

        if selected_scenario == "Select Scenario":
            return
        elif selected_scenario == "Structure Of Fullerenes":
            self.set_fullerenes_view()
        elif selected_scenario == "Portfolio Optimization":
            self.set_portfolio_view()
        elif selected_scenario == "Gradient Descent":
            self.set_gradient_descent_view()

    def clear_layout(self):
        """Clear all widgets in the current layout."""
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

    # fulereny

    def set_fullerenes_view(self):
        """Set the view for the Structure Of Fullerenes scenario."""
        self.setWindowTitle("Structure Of Fullerenes")    

        # tracks option changes in the combo box
        self.combo_box.currentTextChanged.connect(self.on_scenario_change)

    # portfolio

    def set_portfolio_view(self):
        """Set the view for the Portfolio Optimization scenario."""
        self.setWindowTitle("Portfolio Optimization")

        # tracks option changes in the combo box
        self.combo_box.currentTextChanged.connect(self.on_scenario_change)

        # Create and add 'Load Data' button only if it doesn't already exist
        if not self.load_button:
            self.load_button = QPushButton("Load Data")
            self.load_button.clicked.connect(lambda: self.load_csv("asset_data.csv"))
            self.layout.addWidget(self.load_button)

    def load_csv(self, file_name: str):
        try:
            data = pd.read_csv(file_name)
            self.table_widget.setRowCount(len(data))
            self.table_widget.setColumnCount(len(data.columns))
            self.table_widget.setHorizontalHeaderLabels(data.columns)

            for row in range(len(data)):
                for col in range(len(data.columns)):
                    item = QTableWidgetItem(str(data.iloc[row, col]))
                    self.table_widget.setItem(row, col, item)
        except Exception as e:
            print(f"Error loading data: {e}")

    # gradient

    def set_gradient_descent_view(self):
        """Set the view for the Gradient Descent scenario."""
        self.setWindowTitle("Gradient Descent")

        # tracks option changes in the combo box
        self.combo_box.currentTextChanged.connect(self.on_scenario_change)

        # create table for variables
        self.table_widget.clear()
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["Variable Name", "Value"])
        self.table_widget.setRowCount(3)

        self.save_button = QPushButton("Save variables")
        self.save_button.clicked.connect(self.save_variables)
        self.layout.addWidget(self.save_button)

        self.load_button = QPushButton("Load variables")
        # self.load_button.clicked.connect(self.) trzeba obsluzyc inne wczytanie, albo zapisac w .csv
        self.layout.addWidget(self.load_button)

    def save_variables(self):
        variables = {}
        try:
            for row in range(self.table_widget.rowCount()):
                var_name_item = self.table_widget.item(row, 0)
                var_value_item = self.table_widget.item(row, 1)

                if not var_name_item or not var_name_item.text():
                    break

                var_name = var_name_item.text()
                var_value = float(var_value_item.text()) if var_value_item else 0.0

                if var_name not in variables:
                    variables[var_name] = var_value
            
            self.text_box.setText(repr(variables))
        except Exception as e:
            print(f"Error saving variables: {e}")



        # test code

    #     self.label = QLabel("Initial Text")
    #     self.button = QPushButton("Click Me")
    #     self.button.clicked.connect(self.on_button_click)

    #     self.layout.addWidget(self.label)
    #     self.layout.addWidget(self.button)

    # def on_button_click(self):
    #     self.label.setText("Clicked")
