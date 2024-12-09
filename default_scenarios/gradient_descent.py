from scenario import Scenario
from PyQt6.QtWidgets import QTableWidget

class GradientDescentScenario(Scenario):
    def __init__(self, window):
        super().__init__(window)
        pass

    def adjust_layout(self):
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["Variable Name", "Value"])
        self.table_widget.setRowCount(6)

        self.layout.addWidget(self.table_widget)

        # save_button = QPushButton("Save variables")
        # save_button.clicked.connect(lambda: save_variables(window))
        # window.layout.addWidget(save_button)

        # load_button = QPushButton("Load variables")
        # load_button.clicked.connect(lambda: load_variables(window))
        # window.layout.addWidget(load_button)

    # def save_variables(window):
    #     variables = {}
    #     try:
    #         for row in range(window.table_widget.rowCount()):
    #             var_name_item = window.table_widget.item(row, 0)
    #             var_value_item = window.table_widget.item(row, 1)

    #             if not var_name_item or not var_name_item.text():
    #                 break

    #             var_name = var_name_item.text()
    #             var_value = float(var_value_item.text()) if var_value_item else 0.0

    #             if var_name not in variables:
    #                 variables[var_name] = var_value
            
    #         window.text_box.setText(repr(variables))
    #     except Exception as e:
    #         print(f"Error saving variables: {e}")

    # def load_variables(window):
    #     print("Load variables")