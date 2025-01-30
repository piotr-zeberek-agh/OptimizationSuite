from utilities.scenario import Scenario
from PyQt6.QtWidgets import (
    QTableWidget,
    QSpinBox,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QTableWidgetItem,
    QLineEdit,
    QPushButton,
    QWidget,
)

import numpy as np
import pyqtgraph as pg


class GradientDescentScenario(Scenario):
    """ class representing the gradient descent scenario """ 
    def __init__(self, layout):
        super().__init__(layout)
        self.default_init_val = 0
        self.default_min_val = -1
        self.default_max_val = 1
        self.default_learning_rate = 0.01
        self.default_max_iter = 1000
        self.default_convergence = 1e-6
        self.default_refresh_interval = 10

        self.formula_text = "x1**2-x1+1"

        self.var_names = []
        self.var_values = np.array([])
        self.var_min_values = np.array([])
        self.var_max_values = np.array([])

        self.adjust_layout()
        
    def autosave(self, autosave_enabled):
        """ Enable or disable the autosave feature """
        pass

    def adjust_layout(self):
        """ adjust the layout of the scenario """

        self.left_layout = QVBoxLayout()
        self.var_count_label = QLabel("No. independent variables: ")

        self.var_count_spin_box = QSpinBox()
        self.var_count_spin_box.setRange(1, 100)
        self.var_count_spin_box.setValue(1)
        self.var_count_spin_box.valueChanged.connect(self.on_var_count_change)

        self.var_count_layout = QHBoxLayout()
        self.var_count_layout.addWidget(QLabel("No. independent variables: "))
        self.var_count_layout.addWidget(self.var_count_spin_box)

        self.left_layout.addLayout(self.var_count_layout)

        self.learning_rate_field = QLineEdit()
        self.learning_rate_field.setText(str(self.default_learning_rate))

        self.learning_rate_layout = QHBoxLayout()
        self.learning_rate_layout.addWidget(QLabel("Learning rate: "))
        self.learning_rate_layout.addWidget(self.learning_rate_field)

        self.left_layout.addLayout(self.learning_rate_layout)

        self.max_iter_field = QLineEdit()
        self.max_iter_field.setText(str(self.default_max_iter))

        self.max_iter_layout = QHBoxLayout()
        self.max_iter_layout.addWidget(QLabel("Max iter: "))
        self.max_iter_layout.addWidget(self.max_iter_field)

        self.left_layout.addLayout(self.max_iter_layout)

        self.convergence_field = QLineEdit()
        self.convergence_field.setText(str(self.default_convergence))

        self.convergence_layout = QHBoxLayout()
        self.convergence_layout.addWidget(QLabel("Convergence: "))
        self.convergence_layout.addWidget(self.convergence_field)

        self.left_layout.addLayout(self.convergence_layout)

        self.formula_label = QLabel("Formula: ")

        self.formula_field = QLineEdit()
        self.formula_field.setText(self.formula_text)

        self.formula_layout = QHBoxLayout()
        self.formula_layout.addWidget(self.formula_label)
        self.formula_layout.addWidget(self.formula_field)

        self.left_layout.addLayout(self.formula_layout)

        self.var_table = QTableWidget()
        self.var_table.setColumnCount(5)
        self.var_table.setHorizontalHeaderLabels(
            [
                "Variable Name",
                "Initial value",
                "Min. Value",
                "Max. Value",
                "Calc. Value",
            ]
        )
        self.var_table.setRowCount(1)
        self.set_row_data(0)
        self.var_table.setSizeAdjustPolicy(QTableWidget.SizeAdjustPolicy.AdjustToContents)

        self.left_layout.addWidget(self.var_table)
        
        self.output_label = QLabel("Output: ")
        self.output_field = QLineEdit()
        self.output_field.setReadOnly(True)
        
        self.output_layout = QHBoxLayout()
        self.output_layout.addWidget(self.output_label)
        self.output_layout.addWidget(self.output_field)
        
        self.left_layout.addLayout(self.output_layout)

        self.run_button = QPushButton("Run")
        self.run_button.clicked.connect(self.run)

        self.left_layout.addWidget(self.run_button)

        # right layout
        self.right_layout = QVBoxLayout()
        self.chart = GradientDescentChartWidget()
        self.right_layout.addWidget(self.chart)

        # main layout
        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)

        self.layout.addLayout(self.main_layout)

    def set_row_data(self, idx, data=None):
        """ Set the data for a row in the table """
        if data is None:
            data = [
                f"x{idx+1}",
                self.default_init_val,
                self.default_min_val,
                self.default_max_val,
                "",
            ]
        for col, val in enumerate(data):
            self.var_table.setItem(idx, col, QTableWidgetItem(str(val)))

    def update_calculated_values(self):
        """ Update the calculated values in the table """
        for row, val in enumerate(self.var_values):
            self.var_table.setItem(
                row, self.var_table.columnCount() - 1, QTableWidgetItem(str(val))
            )

    def on_var_count_change(self):
        """ Handle the change of the number of variables """
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
        """ Run the gradient descent algorithm """
        learning_rate = float(self.learning_rate_field.text())
        max_iter = int(self.max_iter_field.text())
        convergence = float(self.convergence_field.text())

        self.formula_text = self.formula_field.text()
        self.retrieve_vars()

        vars_values_history = []
        formula_values_history = []

        vars_values_history.append(self.var_values)
        formula_values_history.append(self.calc_formula_value(self.var_values))

        try:
            for i in range(max_iter):
                status, diff = self.make_step(learning_rate)

                if status == 0:
                    break

                vars_values_history.append(self.var_values)
                formula_values_history.append(self.calc_formula_value(self.var_values))

                if i % self.default_refresh_interval == 0:
                    self.update_calculated_values()
                    self.chart.update_chart(
                        self.var_names, vars_values_history, formula_values_history
                    )

                if np.all(np.abs(diff) < convergence):
                    self.output_field.setText(f"Convergence criterium reached after {i+1} iterations.")
                    break

                # print(f"Step {i}: {self.var_values}, diff: {diff}")

            if i == max_iter - 1:
                self.output_field.setText(f"Max iterations reached.")

            self.update_calculated_values()
            self.chart.update_chart(
                self.var_names, vars_values_history, formula_values_history
            )

        except Exception as e:
            print(f"Error making steps: {e}")
            
    def stop(self):
        """ Stop the scenario """
        pass

    def retrieve_vars(self):
        """ Retrieve the variables from the table """
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
        """ Calculate the value of the formula """
        try:
            return eval(self.formula_text, dict(zip(self.var_names, var_values)))
        except Exception as e:
            print(f"Error evaluating formula: {e}")
        return 0

    def calc_gradient(self, var_values, gradient_step=1e-4):
        """ Calculate the gradient of the formula """
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
        """ Make a step in the gradient descent algorithm """
        new_vars = self.var_values - learning_rate * self.calc_gradient(self.var_values)

        if np.any(new_vars < self.var_min_values):
            self.output_field.setText("Some variables are below min values")
            return 0, ()
        if np.any(new_vars > self.var_max_values):
            self.output_field.setText("Some variables are above max values")
            return 0, ()

        diff = new_vars - self.var_values
        self.var_values = new_vars
        return 1, diff


class GradientDescentChartWidget(QWidget):
    """ class representing the chart widget for the gradient descent scenario """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.var_values_plot = pg.PlotWidget(title="Variables")
        self.var_values_plot.setLabel("bottom", "Iterations")
        self.var_values_plot.setLabel("left", "Value")

        self.formula_values_plot = pg.PlotWidget(title="Formula Value")
        self.formula_values_plot.setLabel("bottom", "Iterations")
        self.formula_values_plot.setLabel("left", "Formula Value")

        layout = QVBoxLayout()
        layout.addWidget(self.var_values_plot)
        layout.addWidget(self.formula_values_plot)
        self.setLayout(layout)

    def update_chart(self, var_names, var_values, formula_values):
        """ Update the chart """
        self.var_values_plot.clear()
        for i, var_name in enumerate(var_names):
            self.var_values_plot.plot(
                [v[i] for v in var_values], pen=pg.mkPen(i), name=var_name
            )

        self.formula_values_plot.clear()
        self.formula_values_plot.plot(formula_values, pen=pg.mkPen("r"))

        # update the plot
        pg.QtCore.QCoreApplication.processEvents()

    def save(self):
        """ Save the chart """
        pass