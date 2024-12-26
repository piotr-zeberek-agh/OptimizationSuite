from scenario import Scenario
from PyQt6.QtWidgets import (
    QTableWidget,
    QSpinBox,
    QHBoxLayout,
    QLabel,
    QTableWidgetItem,
    QLineEdit,
    QPushButton,
)
import numpy as np


class GradientDescentScenario(Scenario):
    def __init__(self, layout):
        super().__init__(layout)
        self.default_init_val = 0
        self.default_min_val = -1
        self.default_max_val = 1
        self.default_learning_rate = 0.01
        self.default_max_iter = 1000
        self.default_convergence = 1e-6

        self.formula_text = "0"

        self.var_names = []
        self.var_values = np.array([])
        self.var_min_values = np.array([])
        self.var_max_values = np.array([])

        self.adjust_layout()

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

        self.learning_rate_field = QLineEdit()
        self.learning_rate_field.setText(str(self.default_learning_rate))

        self.learning_rate_layout = QHBoxLayout()
        self.learning_rate_layout.addWidget(QLabel("Learning rate: "))
        self.learning_rate_layout.addWidget(self.learning_rate_field)

        self.layout.addLayout(self.learning_rate_layout)

        self.max_iter_field = QLineEdit()
        self.max_iter_field.setText(str(self.default_max_iter))

        self.max_iter_layout = QHBoxLayout()
        self.max_iter_layout.addWidget(QLabel("Max iter: "))
        self.max_iter_layout.addWidget(self.max_iter_field)

        self.layout.addLayout(self.max_iter_layout)

        self.convergence_field = QLineEdit()
        self.convergence_field.setText(str(self.default_convergence))

        self.convergence_layout = QHBoxLayout()
        self.convergence_layout.addWidget(QLabel("Convergence: "))
        self.convergence_layout.addWidget(self.convergence_field)

        self.layout.addLayout(self.convergence_layout)

        self.formula_label = QLabel("Formula: ")

        self.formula_field = QLineEdit()
        self.formula_field.setPlaceholderText("Enter formula (e.g. x1+4)")

        self.formula_layout = QHBoxLayout()
        self.formula_layout.addWidget(self.formula_label)
        self.formula_layout.addWidget(self.formula_field)

        self.layout.addLayout(self.formula_layout)

        self.var_table = QTableWidget()
        self.var_table.setColumnCount(4)
        self.var_table.setHorizontalHeaderLabels(
            ["Variable Name", "Initial value", "Min. Value", "Max. Value"]
        )
        self.var_table.setRowCount(1)
        self.set_row_data(0)

        self.layout.addWidget(self.var_table)

        self.run_button = QPushButton("Run")
        # self.run_button.setEnabled(False)
        self.run_button.clicked.connect(self.run)

        self.layout.addWidget(self.run_button)

    def set_row_data(self, idx, data=None):
        if data is None:
            data = [
                f"x{idx+1}",
                self.default_init_val,
                self.default_min_val,
                self.default_max_val,
            ]
        for col, val in enumerate(data):
            self.var_table.setItem(idx, col, QTableWidgetItem(str(val)))

    def on_var_count_change(self):
        row_count = self.var_table.rowCount()
        spin_box_val = self.var_count_spin_box.value()

        if spin_box_val > row_count:
            for i in range(row_count, spin_box_val):
                self.var_table.insertRow(i)
                self.set_row_data(i)
        elif spin_box_val < row_count:
            for _ in range(row_count - spin_box_val):
                self.var_table.removeRow(self.var_table.rowCount() - 1)

    def run(self):
        """as of now evaluates formula with min values"""
        learning_rate = float(self.learning_rate_field.text())
        max_iter = int(self.max_iter_field.text())
        convergence = float(self.convergence_field.text())

        self.formula_text = self.formula_field.text()
        self.retrieve_vars()

        try:
            for i in range(max_iter):
                status, diff = self.make_step(learning_rate)
                if status == 0:
                    break
                if np.all(np.abs(diff) < convergence):
                    print(f"Convergence criterium reached after {i+1} iterations.")
                    break
                print(f"Step {i}: {self.var_values}, diff: {diff}")
            print(f"Reached max iteration steps")
        except Exception as e:
            print(f"Error making steps: {e}")

    def retrieve_vars(self):
        names, vinit, vmin, vmax = [], [], [], []

        try:
            for row in range(self.var_table.rowCount()):
                var_name_item = self.var_table.item(row, 0)
                var_vinit_item = self.var_table.item(row, 1)
                var_vmin_item = self.var_table.item(row, 2)
                var_vmax_item = self.var_table.item(row, 3)

                if not var_name_item or not var_name_item.text():
                    break

                var_name = var_name_item.text()
                var_vinit = float(var_vinit_item.text()) if var_vinit_item else 0
                var_vmin = float(var_vmin_item.text()) if var_vmin_item else 0
                var_vmax = float(var_vmax_item.text()) if var_vmax_item else 0

                if var_name not in names:
                    names.append(var_name)
                    vinit.append(var_vinit)
                    vmin.append(var_vmin)
                    vmax.append(var_vmax)

        except Exception as e:
            print(f"Error retriving variables: {e}")

        self.var_names = names
        self.var_values = np.array(vinit)
        self.var_min_values = np.array(vmin)
        self.var_max_values = np.array(vmax)

    def calc_formula_value(self, var_values):
        try:
            return eval(self.formula_text, dict(zip(self.var_names, var_values)))
        except Exception as e:
            print(f"Error evaluating formula: {e}")
        return 0

    def calc_gradient(self, var_values, gradient_step=1e-4):
        dim = len(var_values)
        gradient = np.empty(dim, dtype=np.float64)
        
        for i in range(dim):
            shift = np.zeros(dim, dtype=np.float64)
            shift[i] = gradient_step
            forward = self.calc_formula_value(var_values + shift)
            backward = self.calc_formula_value(var_values - shift)
            gradient[i] = forward - backward

        return gradient / (2.0 * gradient_step)

    def make_step(self, learning_rate):
        new_vars = self.var_values - learning_rate * self.calc_gradient(self.var_values)

        if np.any(new_vars < self.var_min_values):
            print(
                "Warning: some variables are below min values"
            )  # throw exceptions instead, TODO later
            return 0, ()
        if np.any(new_vars > self.var_max_values):
            print("Warning: some variables are above max values")
            return 0, ()

        diff = new_vars - self.var_values
        self.var_values = new_vars
        return 1, diff
