from scenario import Scenario
from PyQt6.QtWidgets import (
    QSpinBox,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QWidget,
)

from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot
import time

import numpy as np
import pyqtgraph as pg
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


def calc_r(first, second):
    return np.linalg.norm(first - second)


def calc_r_idx(i: int, j: int, atoms):
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
        limit_bonds=True,
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

        self.V_coeff = De / (S - 1.0)
        self.g_prep = 1 + c0 * c0 / d0 / d0

        self.r = np.zeros((size, size))
        self.f = np.zeros((size, size))
        self.V_R = np.zeros((size, size))
        self.V_A = np.zeros((size, size))
        self.B_avg = np.zeros((size, size))
        self.V = np.zeros(size)

    def get_V_tot(self, atoms):
        self.fill_r(atoms)
        self.fill_f_VR_VA()
        self.fill_B_avg(atoms)
        self.fill_V()
        return 0.5 * np.sum(self.V)

    def fill_r(self, atoms):
        for i in range(self.n):
            for j in range(i + 1, self.n):
                self.r[i, j] = self.r[j, i] = calc_r_idx(i, j, atoms)

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
                    np.pow(1.0 + xi_ij, -self.delta) + np.pow(1.0 + xi_ji, -self.delta)
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
            V += self.calc_f(r_ij) * (
                self.calc_V_R(r_ij) - self.calc_B_avg(i, j, atoms) * self.calc_V_A(r_ij)
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
                self.calc_f(r_ik)
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
                    self.calc_f(r_jk)
                    * self.a0
                    * (
                        self.g_prep
                        - self.c0**2 / (self.d0**2 + (1.0 + cos_theta_jik) ** 2)
                    )
                )

        return 0.5 * ((1.0 + xi_ij) ** (-self.delta) + (1.0 + xi_ji) ** -self.delta)


class Fullerene:
    def __init__(self, size, r, limit_bonds=True):
        self.n = size
        self.atoms = np.zeros((size, 3))
        self.atoms_spherical = np.zeros((size, 3))
        self.init_atoms(r)
        self.brenner_potential = BrennerPotential(size, limit_bonds)
        self.v_tot = self.brenner_potential.get_V_tot(self.atoms)
        self.r_avg = r

    def init_atoms(self, r):
        for i in range(self.n):
            self.atoms_spherical[i] = np.array(
                [r, 2 * np.pi * np.random.uniform(), np.pi * np.random.uniform()]
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

        # Shifting individual atoms
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
                dV = self.brenner_potential.get_V_tot(self.atoms) - self.v_tot
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

        # Shifting all atoms simultaneously
        self.r_avg = self.calc_r_avg()
        self.v_tot = self.brenner_potential.get_V_tot(self.atoms)

        r_coeff = 1.0 + (2.0 * np.random.uniform() - 1.0) * W_all

        atoms_old = self.atoms.copy()

        for atom in self.atoms:
            atom *= r_coeff

        dV = self.brenner_potential.get_V_tot(self.atoms) - self.v_tot

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


class FullereneWorkerThread(QThread):
    progress_signal = pyqtSignal(str, list, list, list, np.ndarray)
    final_message = "Finished."
    stop_message = "Stopped."

    def __init__(
        self,
        fullerene,
        min_beta,
        max_beta,
        beta_exponent,
        w_r,
        w_phi,
        w_theta,
        w_all,
        max_iter,
        retrive_interval,
    ):
        super().__init__()
        self.fullerene = fullerene
        self.min_beta = min_beta
        self.max_beta = max_beta
        self.beta_exponent = beta_exponent
        self.w_r = w_r
        self.w_phi = w_phi
        self.w_theta = w_theta
        self.w_all = w_all
        self.max_iter = max_iter
        self.retrive_interval = retrive_interval
        self.running = True

    def run(self):
        beta_history = []
        r_avg_history = []
        v_tot_history = []

        for i in range(self.max_iter):
            if not self.running:
                self.progress_signal.emit(
                    self.stop_message,
                    beta_history,
                    r_avg_history,
                    v_tot_history,
                    self.fullerene.atoms,
                )
                break

            beta = (
                self.min_beta
                + (self.max_beta - self.min_beta)
                * (i / self.max_iter) ** self.beta_exponent
            )
            self.fullerene.try_shifting(
                beta, self.w_r, self.w_phi, self.w_theta, self.w_all
            )

            beta_history.append(beta)
            r_avg_history.append(float(self.fullerene.r_avg))
            v_tot_history.append(float(self.fullerene.v_tot))

            if i % self.retrive_interval == 0:
                self.progress_signal.emit(
                    f"{i} iterations",
                    beta_history,
                    r_avg_history,
                    v_tot_history,
                    self.fullerene.atoms,
                )

        if self.running:
            self.progress_signal.emit(
                self.final_message,
                beta_history,
                r_avg_history,
                v_tot_history,
                self.fullerene.atoms,
            )

    def stop(self):
        self.running = False


class FullerenesStructureScenario(Scenario):
    def __init__(self, layout):
        super().__init__(layout)
        self.default_number_of_atoms = 60
        self.default_init_r = 3.3
        self.default_min_beta = 1
        self.default_max_beta = 100
        self.default_beta_exponent = 2
        self.default_w_r = 1e-4
        self.default_w_phi = 0.05
        self.default_w_theta = 0.05
        self.default_w_all = 5e-4
        self.default_nn_scaling = 0.5
        self.default_max_iter = 1000
        self.default_refresh_interval = 5

        self.worker_thread = None
        self.beta_history = []
        self.r_avg_history = []
        self.v_tot_history = []
        self.structure = None

        self.adjust_layout()

    def adjust_layout(self):

        # left layout
        self.left_layout = QVBoxLayout()

        self.atom_count_spin_box = QSpinBox()
        self.atom_count_spin_box.setRange(4, 80)
        self.atom_count_spin_box.setValue(60)
        self.atom_count_layout = QHBoxLayout()
        self.atom_count_layout.addWidget(QLabel("No. atoms: "))
        self.atom_count_layout.addWidget(self.atom_count_spin_box)

        self.left_layout.addLayout(self.atom_count_layout)

        self.init_r_field, self.init_r_layout = self.add_field_input(
            "Init r: ", self.default_init_r, self.left_layout
        )
        self.min_beta_field, self.min_beta_layout = self.add_field_input(
            "Min beta: ", self.default_min_beta, self.left_layout
        )
        self.max_beta_field, self.max_beta_layout = self.add_field_input(
            "Max beta: ", self.default_max_beta, self.left_layout
        )
        self.beta_exponent_field, self.beta_exponent_layout = self.add_field_input(
            "Beta exponent: ", self.default_beta_exponent, self.left_layout
        )
        self.w_r_field, self.w_r_layout = self.add_field_input(
            "w_r: ", self.default_w_r, self.left_layout
        )
        self.w_phi_field, self.w_phi_layout = self.add_field_input(
            "w_phi: ", self.default_w_phi, self.left_layout
        )
        self.w_theta_field, self.w_theta_layout = self.add_field_input(
            "w_theta: ", self.default_w_theta, self.left_layout
        )
        self.w_all_field, self.w_all_layout = self.add_field_input(
            "w_all: ", self.default_w_all, self.left_layout
        )
        self.nn_scaling_field, self.nn_scaling_layout = self.add_field_input(
            "NN scaling: ", self.default_nn_scaling, self.left_layout
        )
        self.max_iter_field, self.max_iter_layout = self.add_field_input(
            "Max iter: ", self.default_max_iter, self.left_layout
        )
        self.refresh_interval_field, self.refresh_interval_layout = (
            self.add_field_input(
                "Refresh interval: ", self.default_refresh_interval, self.left_layout
            )
        )

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

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop)
        self.stop_button.setEnabled(False)
        self.left_layout.addWidget(self.stop_button)

        # right layout
        self.right_layout = QVBoxLayout()
        self.chart = FullerenesStructureChartWidget()
        self.right_layout.addWidget(self.chart)

        # main layout
        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)

        self.layout.addLayout(self.main_layout)

    def add_field_input(self, label, default_value, layout):
        field = QLineEdit()
        field.setText(str(default_value))
        field_layout = QHBoxLayout()
        field_layout.addWidget(QLabel(label))
        field_layout.addWidget(field)
        layout.addLayout(field_layout)
        return field, field_layout

    def run(self):
        self.run_button.setEnabled(False)
        self.stop_button.setEnabled(True)

        self.beta_history = []
        self.r_avg_history = []
        self.v_tot_history = []
        self.structure = None

        atom_count = self.atom_count_spin_box.value()
        init_r = float(self.init_r_field.text())
        min_beta = float(self.min_beta_field.text())
        max_beta = float(self.max_beta_field.text())
        beta_exponent = float(self.beta_exponent_field.text())
        w_r = float(self.w_r_field.text())
        w_phi = float(self.w_phi_field.text())
        w_theta = float(self.w_theta_field.text())
        w_all = float(self.w_all_field.text())
        max_iter = int(self.max_iter_field.text())
        refresh_interval = int(self.refresh_interval_field.text())

        self.chart.nn_scaling = float(self.nn_scaling_field.text())
        fullerene = Fullerene(atom_count, init_r)

        self.worker_thread = FullereneWorkerThread(
            fullerene,
            min_beta,
            max_beta,
            beta_exponent,
            w_r,
            w_phi,
            w_theta,
            w_all,
            max_iter,
            refresh_interval,
        )

        self.worker_thread.progress_signal.connect(self.update_data)

        self.output_field.setText("Starting...")
        self.worker_thread.start()

    def update_data(self, message, beta_history, r_avg_history, v_tot_history, atoms):
        self.output_field.setText(message)
        self.beta_history = beta_history
        self.r_avg_history = r_avg_history
        self.v_tot_history = v_tot_history
        self.chart.update(
            self.beta_history, self.r_avg_history, self.v_tot_history, atoms
        )

        if message == FullereneWorkerThread.final_message:
            self.stop()

    def stop(self):
        if self.worker_thread:
            self.worker_thread.stop()
        self.run_button.setEnabled(True)
        self.stop_button.setEnabled(False)


class FullerenesStructureChartWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.beta_plot = pg.PlotWidget(title="Beta")
        self.beta_plot.setLabel("bottom", "Iterations")
        self.beta_plot.setLabel("left", "Value")

        self.r_avg_plot = pg.PlotWidget(title="R avg")
        self.r_avg_plot.setLabel("bottom", "Iterations")
        self.r_avg_plot.setLabel("left", "Value")

        self.v_tot_plot = pg.PlotWidget(title="V tot")
        self.v_tot_plot.setLabel("bottom", "Iterations")
        self.v_tot_plot.setLabel("left", "Value")

        self.nn_scaling = 0.5
        self.structure_figure = Figure()
        self.structure_canvas = FigureCanvas(self.structure_figure)

        layout = QGridLayout()
        layout.addWidget(self.beta_plot, 0, 0)
        layout.addWidget(self.r_avg_plot, 0, 1)
        layout.addWidget(self.v_tot_plot, 1, 0)
        layout.addWidget(self.structure_canvas, 1, 1)

        self.setLayout(layout)

    def update(self, betas, r_avgs, v_tots, atoms):
        for plot, vals in zip(
            [self.beta_plot, self.r_avg_plot, self.v_tot_plot],
            [betas, r_avgs, v_tots],
        ):
            plot.clear()
            plot.plot(vals)

        self.plot_fullerene_structure(atoms, r_avgs[-1])
        pg.QtCore.QCoreApplication.processEvents()

    def plot_fullerene_structure(self, atoms, r_avg):
        x, y, z = atoms[:, 0], atoms[:, 1], atoms[:, 2]
        nn_dist = self.nn_scaling * r_avg

        self.structure_figure.clear()
        ax = self.structure_figure.add_subplot(111, projection="3d")

        # Plot vertices
        ax.scatter(x, y, z, c="r", marker="o")

        # Plot edges
        for i in range(len(x)):
            for j in range(i + 1, len(x)):
                dist = np.sqrt(
                    (x[i] - x[j]) ** 2 + (y[i] - y[j]) ** 2 + (z[i] - z[j]) ** 2
                )
                if dist <= nn_dist:
                    ax.plot([x[i], x[j]], [y[i], y[j]], [z[i], z[j]], c="b")

        # adjust view
        max_range = np.ceil(np.max(atoms))
        ax.set_xlim([-max_range, max_range])
        ax.set_ylim([-max_range, max_range])
        ax.set_zlim([-max_range, max_range])

        ax.set_box_aspect([1, 1, 1])

        ax.set_title("Fullerene structure")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")

        self.structure_canvas.draw()
