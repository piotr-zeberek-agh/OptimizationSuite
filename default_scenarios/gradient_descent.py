from scenario import Scenario
from PyQt6.QtWidgets import (
    QTableWidget,
    QPushButton,
    QSpinBox,
    QHBoxLayout,
    QLabel,
    QTableWidgetItem,
    QLineEdit,
)


class GradientDescentScenario(Scenario):
    def __init__(self, layout):
        super().__init__(layout)

    def adjust_layout(self):
        self.var_count_label = QLabel("No. independent variables: ")

        self.var_count_spin_box = QSpinBox()
        self.var_count_spin_box.setRange(1, 100)
        self.var_count_spin_box.setValue(1)
        self.var_count_spin_box.valueChanged.connect(self.on_var_count_change)

        self.var_count_layout = QHBoxLayout()
        self.var_count_layout.addWidget(QLabel("No. independent variables: "))
        self.var_count_layout.addWidget(self.var_count_spin_box)

        self.layout.addLayout(self.var_count_layout)

        self.formula_label = QLabel("Formula: ")

        self.formula_field = QLineEdit()
        self.formula_field.setPlaceholderText("Enter formula (e.g. x1+4)")

        self.formula_layout = QHBoxLayout()
        self.formula_layout.addWidget(self.formula_label)
        self.formula_layout.addWidget(self.formula_field)

        self.layout.addLayout(self.formula_layout)

        self.var_table = QTableWidget()
        self.var_table.setColumnCount(3)
        self.var_table.setHorizontalHeaderLabels(
            ["Variable Name", "Min. Value", "Max. Value"]
        )
        self.var_table.setRowCount(1)
        self.var_table.setItem(0, 0, QTableWidgetItem("x1"))

        self.layout.addWidget(self.var_table)

        self.run_button = QPushButton()
        self.run_button.setText("Run")
        self.run_button.clicked.connect(self.run)

        self.layout.addWidget(self.run_button)

    def on_var_count_change(self):
        row_count = self.var_table.rowCount()
        spin_box_val = self.var_count_spin_box.value()

        if spin_box_val > row_count:
            for i in range(row_count, spin_box_val):
                self.var_table.insertRow(i)
                self.var_table.setItem(i, 0, QTableWidgetItem(f"x{i+1}"))
        elif spin_box_val < row_count:
            for _ in range(row_count - spin_box_val):
                self.var_table.removeRow(self.var_table.rowCount() - 1)

    def run(self):
        """as of now evaluates formula with min values"""
        formula = self.formula_field.text()
        variables = self.get_vars()
        try:
            for vname, (vmin, vmax) in variables.items():
                formula = formula.replace(vname, vmin)
            result = eval(formula)
            print(result)
        except Exception as e:
            print(f"Error evaluating formula: {e}")

    def get_vars(self):
        variables = {}
        try:
            for row in range(self.var_table.rowCount()):
                var_name_item = self.var_table.item(row, 0)
                var_min_value_item = self.var_table.item(row, 1)
                var_max_value_item = self.var_table.item(row, 2)

                if not var_name_item or not var_name_item.text():
                    break

                var_name = var_name_item.text()
                var_min_value = var_min_value_item.text() if var_min_value_item else "0"
                var_max_value = var_max_value_item.text() if var_max_value_item else "0"

                if var_name not in variables:
                    variables[var_name] = (var_min_value, var_max_value)

        except Exception as e:
            print(f"Error retriving variables: {e}")

        return variables
