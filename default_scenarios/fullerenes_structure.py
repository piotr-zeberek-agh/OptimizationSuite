from scenario import Scenario
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


def calc_r(first, second):
    return np.linalg.norm(first - second)


def calc_r(i, j, atoms):
    return calc_r(atoms[j], atoms[i])


def to_cartesian(spherical):
    r, phi, theta = spherical
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    return np.array([x, y, z])


def to_spherical(cartesian):
    x, y, z = cartesian
    r = np.sqrt(x**2 + y**2 + z**2)
    phi = np.arctan2(y, x)
    theta = np.arccos(z / r)
    return np.array([r, phi, theta])


class BrennerPotential:
    def __init__(
        self,
        size,
        limit_bonds=False,
        xi=10.0,
        R0=1.315,
        R1=1.70,
        R2=2.00,
        De=6.325,
        S=1.29,
        lambda_=1.5,
        delta=0.80469,
        a0=0.011304,
        c0=19,
        d0=2.5,
    ):
        self.n = size
        self.limit_bonds = limit_bonds
        self.xi = xi
        self.R0 = R0
        self.R1 = R1
        self.R2 = R2
        self.De = De
        self.S = S
        self.lambda_ = lambda_
        self.delta = delta
        self.a0 = a0
        self.c0 = c0
        self.d0 = d0

        self.V_coeff = 0
        self.g_prep = 0

        self.r = np.zeros((size, size))
        self.f = np.zeros((size, size))
        self.V_R = np.zeros((size, size))
        self.V_A = np.zeros((size, size))
        self.B_avg = np.zeros((size, size))
        self.V = np.zeros(size)

    def __call__(self, atoms):
        self.fill_r(atoms)
        self.fill_f_VR_VA()
        self.fill_B_avg(atoms)
        self.fill_V()
        return 0.5 * np.sum(self.V)

    def fill_r(self, atoms):
        for i in range(self.n):
            for j in range(i + 1, self.n):
                self.r[i, j] = self.r[j, i] = calc_r(i, j, atoms)

    def fill_f_VR_VA(self):
        for i in range(self.n):
            for j in range(self.n):
                r_ij = self.r[i, j]

                if r_ij > self.R2 or i == j:
                    self.f[i, j] = self.f[j, i] = 0.0
                    self.V_R[i, j] = self.V_R[j, i] = 0.0
                    self.V_A[i, j] = self.V_A[j, i] = 0.0
                    continue

                if r_ij <= self.R1:
                    self.f[i, j] = self.f[j, i] = 1.0
                else:
                    self.f[i, j] = self.f[j, i] = 0.5 * (
                        1.0 + np.cos(np.pi * (r_ij - self.R1) / (self.R2 - self.R1))
                    )

                arg = self.lambda_ * (r_ij - self.R0)

                self.V_R[i, j] = self.V_R[j, i] = self.V_coeff * np.exp(
                    -np.sqrt(2.0 * self.S) * arg
                )
                self.V_A[i, j] = self.V_A[j, i] = (
                    self.V_coeff * self.S * np.exp(-np.sqrt(2.0 / self.S) * arg)
                )

    def fill_B_avg(self, atoms):
        for i in range(self.n):
            for j in range(i + 1, self.n):
                r_ij = self.r[i, j]

                if r_ij > self.R2 or i == j:
                    self.B_avg[i, j] = self.B_avg[j, i] = 0.0
                    continue

                vr_ij = atoms[j] - atoms[i]
                vr_ji = -vr_ij

                xi_ij = 0.0

                for k in range(self.n):
                    r_ik = self.r[i, k]

                    if r_ik > self.R2 or k == i or k == j:
                        continue

                    cos_theta_ijk = np.dot(vr_ij, atoms[k] - atoms[i]) / (r_ij * r_ik)

                    if self.limit_bonds and cos_theta_ijk > 0.0:
                        xi_ij = self.xi
                        break

                    xi_ij += (
                        self.f[i, k]
                        * self.a0
                        * (
                            self.g_prep
                            - self.c0**2 / (self.d0**2 + (1.0 + cos_theta_ijk) ** 2)
                        )
                    )

                xi_ji = 0.0

                for k in range(self.n):
                    r_jk = self.r[j, k]

                    if r_jk > self.R2 or k == i or k == j:
                        continue

                    cos_theta_jik = np.dot(vr_ji, atoms[k] - atoms[j]) / (r_ij * r_jk)

                    if self.limit_bonds and cos_theta_jik > 0.0:
                        xi_ji += self.xi
                    else:
                        xi_ji += (
                            self.f[j, k]
                            * self.a0
                            * (
                                self.g_prep
                                - self.c0**2 / (self.d0**2 + (1.0 + cos_theta_jik) ** 2)
                            )
                        )

                self.B_avg[i, j] = self.B_avg[j, i] = 0.5 * (
                    (1.0 + xi_ij) ** (-self.delta) + (1.0 + xi_ji) ** (-self.delta)
                )

    def fill_V(self):
        self.V.fill(0)

        for i in range(self.n):
            for j in range(self.n):
                if self.r[i, j] > self.R2 or i == j:
                    continue

                self.V[i] += self.f[i, j] * (
                    self.V_R[i, j] - self.B_avg[i, j] * self.V_A[i, j]
                )

    def calc_f(self, r_ij):
        if r_ij <= self.R1:
            return 1.0
        if r_ij <= self.R2:
            return 0.5 * (1.0 + np.cos(np.pi * (r_ij - self.R1) / (self.R2 - self.R1)))
        return 0.0

    def calc_V_R(self, r_ij):
        return (
            self.De
            / (self.S - 1.0)
            * np.exp(-np.sqrt(2.0 * self.S) * self.lambda_ * (r_ij - self.R0))
        )

    def calc_V_A(self, r_ij):
        return (
            self.De
            / (self.S - 1.0)
            * self.S
            * np.exp(-np.sqrt(2.0 / self.S) * self.lambda_ * (r_ij - self.R0))
        )

    def calc_V(self, i, atoms):
        V = 0.0
        for j in range(self.n):
            r_ij = calc_r(atoms[i], atoms[j])
            if r_ij > self.R2 or i == j:
                continue
            V += self.calc_f[i, j] * (
                self.calc_V_R[i, j] - self.calc_B_avg[i, j] * self.calc_V_A[i, j]
            )
        return V

    def calc_B_avg(self, i, j, atoms):
        r_ij = calc_r(atoms[i], atoms[j])
        if r_ij > self.R2 or i == j:
            return 0.0

        vr_ij = atoms[j] - atoms[i]
        vr_ji = -vr_ij

        xi_ij = 0.0
        xi_ji = 0.0

        for k in range(self.n):
            r_ik = calc_r(atoms[i], atoms[k])

            if r_ik > self.R2 or k == i or k == j:
                continue

            cos_theta_ijk = np.dot(vr_ij, atoms[k] - atoms[i]) / (r_ij * r_ik)
            if self.limit_bonds and cos_theta_ijk > 0.0:
                xi_ij = self.xi
                break

            xi_ij += (
                self.calc_f[i, k]
                * self.a0
                * (self.g_prep - self.c0**2 / (self.d0**2 + (1.0 + cos_theta_ijk) ** 2))
            )

        for k in range(self.n):
            r_jk = calc_r(atoms[j], atoms[k])
            if r_jk > self.R2 or k == i or k == j:
                continue

            cos_theta_jik = np.dot(vr_ji, atoms[k] - atoms[j]) / (r_ij * r_jk)

            if self.limit_bonds and cos_theta_jik > 0.0:
                xi_ji += self.xi
            else:
                xi_ji += (
                    self.calc_f[j, k]
                    * self.a0
                    * (
                        self.g_prep
                        - self.c0**2 / (self.d0**2 + (1.0 + cos_theta_jik) ** 2)
                    )
                )

        return 0.5 * ((1.0 + xi_ij) ** -self.delta + (1.0 + xi_ji) ** -self.delta)


class Fullerene:
    def __init__(self, size, r, limit_bonds=False):
        self.n = size
        self.atoms = np.zeros((size, 3))
        self.atoms_spherical = np.zeros((size, 3))
        self.v_tot = 0.0
        self.r_avg = r
        self.init_atoms(r)
        self.brenner_potential = BrennerPotential(size, limit_bonds)

    def init_atoms(self, r):
        for i in range(self.n):
            self.atoms_spherical[i] = np.array(
                [r, 2 * np.pi * np.random.uniform(), np.pi / 2 * np.random.uniform()]
            )
            self.atoms[i] = to_cartesian(self.atoms_spherical[i])

    def calc_r_avg(self):
        return np.average(self.atoms_spherical[:, 0])

    def restrict_quadruple_bonds(self, xi=10.0):
        self.brenner_potential.xi = xi
        self.brenner_potential.limit_bonds = True

    def allow_quadruple_bonds(self):
        self.brenner_potential.limit_bonds = False

    def try_shifting(self, beta, w_r, w_phi, w_theta, W_all, use_full_potential=False):
        for i in range(self.n):
            atom_old = self.atoms[i].copy()
            atom_old_spherical = self.atoms_spherical[i].copy()

            r_new = atom_old_spherical[0] * (
                1.0 + (2.0 * np.random.uniform() - 1) * w_r
            )
            phi_new = atom_old_spherical[1] * (
                1.0 + (2.0 * np.random.uniform() - 1) * w_phi
            )
            theta_new = atom_old_spherical[2] * (
                1.0 + (2.0 * np.random.uniform() - 1) * w_theta
            )

            if phi_new < 0.0:
                phi_new += 2 * np.pi

            if phi_new > 2.0 * np.pi:
                phi_new -= 2.0 * np.pi

            if theta_new < 0.0 or theta_new > np.pi:
                theta_new = atom_old_spherical[2]

            atom_new_spherical = np.array([r_new, phi_new, theta_new])

            self.atoms[i] = to_cartesian(atom_new_spherical)

            if use_full_potential:
                dV = self.brenner_potential(self.atoms) - self.v_tot
            else:
                dV = (
                    self.brenner_potential.calc_V(i, self.atoms)
                    - self.brenner_potential.V[i]
                )

            if dV <= 0.0:
                self.atoms_spherical[i] = atom_new_spherical
                continue

            p = np.exp(-beta * dV)

            if np.random.uniform() <= p:
                self.atoms_spherical[i] = atom_new_spherical
            else:
                self.atoms[i] = atom_old

        self.r_avg = self.calc_r_avg()
        self.v_tot = self.brenner_potential(self.atoms)

        r_coeff = 1.0 + (2.0 * np.random.uniform() - 1.0) * W_all

        atoms_old = self.atoms.copy()

        for atom in self.atoms:
            atom *= r_coeff

        dV = self.brenner_potential(self.atoms) - self.v_tot

        if dV <= 0.0:
            for atom in self.atoms_spherical:
                atom[0] *= r_coeff

            self.r_avg *= r_coeff
            self.v_tot += dV

            return

        p = min(1.0, np.exp(-beta * dV))

        if np.random.uniform() <= p:
            for i in range(self.n):
                self.atoms_spherical[i][0] *= r_coeff

            self.r_avg *= r_coeff
            self.v_tot += dV

            return

        self.atoms = atoms_old


class FullerenesStructureScenario(Scenario):
    def __init__(self, layout):
        super().__init__(layout)
        self.default_number_of_atoms = 60
        self.default_min_val = -1
        self.default_max_val = 1

        self.var_names = []
        self.var_values = np.array([])
        self.var_min_values = np.array([])
        self.var_max_values = np.array([])

        self.adjust_layout()

    def adjust_layout(self):

        # left layout
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
        self.formula_field.setPlaceholderText("Enter formula (e.g. x1+4)")

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
        self.var_table.setSizeAdjustPolicy(
            QTableWidget.SizeAdjustPolicy.AdjustToContents
        )

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
        self.chart = FullerenesStructureChartWidget()
        self.right_layout.addWidget(self.chart)

        # main layout
        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)

        self.layout.addLayout(self.main_layout)

    def set_row_data(self, idx, data=None):
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
        for row, val in enumerate(self.var_values):
            self.var_table.setItem(
                row, self.var_table.columnCount() - 1, QTableWidgetItem(str(val))
            )

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
                    self.output_field.setText(
                        f"Convergence criterium reached after {i+1} iterations."
                    )
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
            self.output_field.setText("Some variables are below min values")
            return 0, ()
        if np.any(new_vars > self.var_max_values):
            self.output_field.setText("Some variables are above max values")
            return 0, ()

        diff = new_vars - self.var_values
        self.var_values = new_vars
        return 1, diff


class FullerenesStructureChartWidget(QWidget):
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
        self.var_values_plot.clear()
        for i, var_name in enumerate(var_names):
            self.var_values_plot.plot(
                [v[i] for v in var_values], pen=pg.mkPen(i), name=var_name
            )

        self.formula_values_plot.clear()
        self.formula_values_plot.plot(formula_values, pen=pg.mkPen("r"))

        # update the plot
        pg.QtCore.QCoreApplication.processEvents()
