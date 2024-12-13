from scenario import Scenario
from PyQt6.QtWidgets import (
    QTableWidget,
    QSpinBox,
    QHBoxLayout,
    QLabel,
    QTableWidgetItem,
    QLineEdit,
)
import numpy as np


class GradientDescentScenario(Scenario):
    def __init__(self, layout):
        super().__init__(layout)
        self.default_init_val = 0
        self.default_min_val = -1
        self.default_max_val = 1
        self.default_step_size = 0.01

        self.formula_text = "0"

        self.adjust_layout()

    def adjust_layout(self):
        self.clear_layout()
        self.var_count_label = QLabel("No. independent variables: ")

        self.var_count_spin_box = QSpinBox()
        self.var_count_spin_box.setRange(1, 100)
        self.var_count_spin_box.setValue(1)
        self.var_count_spin_box.valueChanged.connect(self.on_var_count_change)

        self.var_count_layout = QHBoxLayout()
        self.var_count_layout.addWidget(QLabel("No. independent variables: "))
        self.var_count_layout.addWidget(self.var_count_spin_box)

        self.layout.addLayout(self.var_count_layout)

        self.step_size_field = QLineEdit()
        self.step_size_field.setText(str(self.default_step_size))

        self.step_size_layout = QHBoxLayout()
        self.step_size_layout.addWidget(QLabel("Step size: "))
        self.step_size_layout.addWidget(self.step_size_field)

        self.layout.addLayout(self.step_size_layout)

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
        step_size = float(self.step_size_field.text())
        self.formula_text = self.formula_field.text()
        names, v, vmin, vmax = self.get_vars()

        try:
            print(self.calc_formula_value(names, v))
        except Exception as e:
            print(f"Error evaluating formula: {e}")

    def get_vars(self):
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

        return (names, np.array(vinit), np.array(vmin), np.array(vmax))

    def calc_formula_value(self, var_names, var_values):
        formula = self.formula_text
        try:
            for vname, val in zip(var_names, var_values):
                formula = formula.replace(vname, str(val))
            return eval(formula)
        except Exception as e:
            print(f"Error evaluating formula: {e}")
        return 0

    def calc_gradient(self, var_names, var_values, gradient_step=1e-4):
        #use numpy
        
        # for i in range(len(var_names)):
        #     vo = var_values[i]
        #     var_values[i] = vo + gradient_step
        #     forward = self.calc_formula_value(var_names, var_values)
        #     var_values[i] = vo - gradient_step
        #     backward = self.calc_formula_value(var_names, var_values)
        #     gradient.append((forward - backward) / (2.0 * gradient_step))
            
        # return gradient
        pass
