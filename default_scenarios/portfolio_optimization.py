from scenario import Scenario
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QVBoxLayout, QDialog, QMessageBox, QListWidget, QLabel, QStackedWidget, QFileDialog, QDialogButtonBox, QListWidgetItem, QTableWidgetItem, QAbstractItemView, QFrame, QLineEdit, QTableWidget, QPushButton, QHBoxLayout, QWidget

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import json
from portfolio_data import fetch_data
from annealing import accept_move
import numpy as np
import pandas as pd
import random
import re
import os
from PyQt6.QtGui import QPixmap, QIcon

class PortfolioOptimizationScenario(Scenario):
    def __init__(self, layout):
        super().__init__(layout)
        self.selected_options = None
        self.data = None

        self.adjust_layout()

    def adjust_layout(self):
        """Adjusts the layout to include elements for portfolio optimization."""

        # title_font = QFont("Arial", 16, QFont.Weight.Bold)
        interval_font = QFont("Lora", 12)

        # its because self.layout is a QVBoxLayout
        self.main_window = QHBoxLayout()

        self.left_layout = QVBoxLayout()
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.left_layout.setSpacing(10)

        self.interval_label = QLabel("Fill out the section if you need data.")
        self.interval_label.setFont(interval_font)
        self.left_layout.addWidget(self.interval_label)

        self.date_row = QHBoxLayout()
        self.start_date_line = QLineEdit()
        self.start_date_line.setPlaceholderText("Start (YYYY-MM-DD)")
        self.date_row.addWidget(self.start_date_line)
        self.start_date_line.textChanged.connect(self.check_date_input)
        self.end_date_line = QLineEdit()
        self.end_date_line.setPlaceholderText("End (YYYY-MM-DD)")
        self.date_row.addWidget(self.end_date_line)
        self.end_date_line.textChanged.connect(self.check_date_input)

        self.open_dialog_button = QPushButton("Choose Assets")
        self.open_dialog_button.clicked.connect(self.open_selection_window)
        self.date_row.addWidget(self.open_dialog_button)

        self.left_layout.addLayout(self.date_row)

        self.download_data_button = QPushButton()
        self.download_data_button.setText("Download Data")
        self.download_data_button.setEnabled(False)
        self.download_data_button.clicked.connect(self.download_data)
        self.left_layout.addWidget(self.download_data_button)

        self.download_layout = QHBoxLayout()
        self.filename_line = QLineEdit()
        self.filename_line.setPlaceholderText("Enter filename")
        self.download_layout.addWidget(self.filename_line)
        self.filename_line.textChanged.connect(self.check_filename_input)
        self.save_data_button = QPushButton()
        self.save_data_button.setText("Save Data")
        self.save_data_button.setEnabled(False)
        self.save_data_button.clicked.connect(self.save_data)
        self.download_layout.addWidget(self.save_data_button)
        self.left_layout.addLayout(self.download_layout)

        self.line_download = QFrame()
        self.line_download.setFrameShape(QFrame.Shape.HLine)
        self.line_download.setFrameShadow(QFrame.Shadow.Sunken)
        self.left_layout.addWidget(self.line_download)


        # LINE ------------------------------



        # self.row_5 = QHBoxLayout()
        # self.row_5.addWidget(QLabel("Enter your budget"))
        # self.budget_line = QLineEdit()
        # self.budget_line.setPlaceholderText("")
        # self.row_5.addWidget(self.budget_line)
        # self.left_layout.addLayout(self.row_5)
        
        self.selected_table = QTableWidget()
        self.left_layout.addWidget(self.selected_table)

        self.assets_buttons_layout = QHBoxLayout()


        self.open_dialog_button = QPushButton("Load Data")
        self.open_dialog_button.clicked.connect(self.load_data)
        self.left_layout.addWidget(self.open_dialog_button)

        self.clear_data_button = QPushButton("Clear Assets")
        self.clear_data_button.clicked.connect(self.clear_data)
        self.assets_buttons_layout.addWidget(self.clear_data_button)
        self.left_layout.addLayout(self.assets_buttons_layout)
        # self.clear_data

        self.run_button = QPushButton("Run")
        self.run_button.setEnabled(False)
        self.run_button.clicked.connect(self.run)
        self.left_layout.addWidget(self.run_button)

        # Middle line

        self.mid_layout = QVBoxLayout()
        self.middle_line = QFrame()
        self.middle_line.setFrameShape(QFrame.Shape.VLine)
        self.middle_line.setFrameShadow(QFrame.Shadow.Sunken)
        self.mid_layout.addWidget(self.middle_line)

        # Right layout
        # dodatkowe :
        # Scenariusze ryzyka:Zwrot portfela w warunkach rynkowych (np. 10% spadek indeksu, kryzys, wysoka inflacja).
        # Średnia roczna stopa zwrotu (%): Uśredniona wartość zwrotów portfela w długim okresie.
        # Layout dla zakładek w lewej części

        tab_button_1 = QPushButton()
        tab_button_1.setIcon(QIcon(QPixmap("resources/images/tab_1.png")))
        tab_button_1.clicked.connect(lambda: self.switch_tab(0))

        tab_button_2 = QPushButton()
        tab_button_2.setIcon(QIcon(QPixmap("resources/images/tab_2.png")))
        tab_button_2.clicked.connect(lambda: self.switch_tab(1))

        # Dodanie zakładek do lewego layoutu
        self.tabs_layout = QHBoxLayout()
        self.tabs_layout.addWidget(tab_button_1)
        self.tabs_layout.addWidget(tab_button_2)
        self.left_layout.addLayout(self.tabs_layout)

        self.right_layout = QVBoxLayout()

        self.stacked_widget = QStackedWidget()
        self.chart_widget = PortfolioChartWidget()
        self.stacked_widget.addWidget(self.chart_widget)

        # self.right_layout.addWidget(self.chart_widget)
        self.right_layout.addWidget(self.stacked_widget)

        self.portfolio_table = QTableWidget()
        self.portfolio_table.setRowCount(5)
        self.portfolio_table.setColumnCount(3)
        self.portfolio_table.setHorizontalHeaderLabels(["Asset Name", "Allocation", "Expected Return", "Risk", "Beta", "Sharpe Ratio", "Treynor Ratio"])
        # SHARE RATIO oddzielny dla kazdego aktywaw okresie 
        self.right_layout.addWidget(self.portfolio_table)

        self.main_window.addLayout(self.left_layout)
        self.main_window.addLayout(self.mid_layout)
        self.main_window.addLayout(self.right_layout, stretch=1)
        self.layout.addLayout(self.main_window)

    def check_date_input(self):
        date_format_start = r"^\d{4}-\d{2}-\d{2}$"  # Format: YYYY-MM-DD
        date_text_start = self.start_date_line.text()
        date_format_end = r"^\d{4}-\d{2}-\d{2}$"
        date_text_end = self.end_date_line.text()

        if re.match(date_format_start, date_text_start) and re.match(date_format_end, date_text_end) \
                                                        and date_text_start <= date_text_end:
            if self.selected_options is not None:
                self.download_data_button.setEnabled(True)
            else:
                self.download_data_button.setEnabled(False)
        else:
            self.download_data_button.setEnabled(False)

    def download_data(self):
        start_date = self.start_date_line.text()
        end_date = self.end_date_line.text()
        self.data = fetch_data(self.selected_options, start_date, end_date)
        self.run_button.setEnabled(True)

    def switch_tab(self, index):
        """Funkcja zmieniająca widoczny widget w stacked widget"""
        self.stacked_widget.setCurrentIndex(index)

    def show_widget_visibility(self):
        """Funkcja pokazująca widoczność widgetu w stacked widget"""
        current_widget = self.stacked_widget.currentWidget()
        visibility = "visible" if current_widget.isVisible() else "hidden"
        print(f"Current widget visibility: {visibility}")        

    def check_filename_input(self):
        filename = self.filename_line.text().strip()

        if filename == '':
            self.save_data_button.setEnabled(False)
        elif not filename[0] in ['.', ' '] or not re.search(r'[<>:"/\\|?*]', filename):
            if self.data is not None:
                self.save_data_button.setEnabled(True)
            else:
                self.save_data_button.setEnabled(False)
        else:
            self.save_data_button.setEnabled(False)

    def check_run_button(self):
        if self.data is not None:
            self.run_button.setEnabled(True)
        else:
            self.run_button.setEnabled(False)

    def save_data(self):
        filename="data/" + self.filename_line.text()
        if not filename.endswith('.csv'):
            filename += '.csv'
        self.data.to_csv(filename)

    def clear_data(self):
        self.selected_table.setColumnCount(0)
        self.selected_table.setRowCount(0)
        self.selected_table.clear()
        self.download_data_button.setEnabled(False)
        self.save_data_button.setEnabled(False) 
        self.selected_options = None
        self.data = None
        self.chart_widget.clear_chart()

    def load_data(self):
        try:
            file_name, _ = QFileDialog.getOpenFileName(
                None, "Select CSV File", "data/", "CSV Files (*.csv);;All Files (*)"
            )
            if not file_name:
                print("No file selected!")
                return

            file_data = pd.read_csv(file_name)

            if file_data.columns[0] == 'Date':
                self.data = file_data.iloc[:, 1:]
                self.date = file_data.iloc[:, 0]
            # self.data = pd.read_csv(file_name)

            # Konwertowanie wszystkich kolumn na numeryczne (w przypadku, gdy są tekstowe)
            # Jeśli nie można przekonwertować, wartość zostanie ustawiona na NaN
            self.data = self.data.apply(pd.to_numeric, errors='coerce')

            # DEBUG: Sprawdzenie, jakie typy danych znajdują się w DataFrame
            # print(self.data.dtypes)

            # Ustawienie tabeli w UI
            self.selected_table.setRowCount(len(self.data))
            self.selected_table.setColumnCount(len(self.data.columns))
            self.selected_table.setHorizontalHeaderLabels(self.data.columns)

            # Wypełnianie tabeli danymi z DataFrame
            for row in range(len(self.data)):
                for col in range(len(self.data.columns)):
                    item = QTableWidgetItem(str(self.data.iloc[row, col]))
                    self.selected_table.setItem(row, col, item)

            print(f"Data successfully loaded from {file_name}!")

        except Exception as e:
            print(f"Error loading data: {e}")

        if self.data is not None:
            self.run_button.setEnabled(True)

    def open_selection_window(self):
        """Function to open a dialog for selecting assets"""
        try:
            dialog = SelectionDialog()
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.selected_options = dialog.get_selected_options()
                self.selected_table.setColumnCount(len(self.selected_options.keys()))
                self.selected_table.setHorizontalHeaderLabels(self.selected_options.keys())
                self.selected_table.setRowCount(max([len(v) for v in self.selected_options.values()]))
                for i, category in enumerate(self.selected_options.keys()):
                    for j, item in enumerate(self.selected_options[category]):
                        q_item = QTableWidgetItem(item)
                        q_item.setFlags(q_item.flags() & ~Qt.ItemFlag.ItemIsEditable)   # blokowanie komorek
                        self.selected_table.setItem(j, i, q_item) 
                if self.selected_options:
                    self.check_date_input()
                    
        except Exception as e:
            print(f"Error opening selection window: {e}")

# # ---------------------- Annealing ------------------
    def run(self):
        """Simulates portfolio optimization and updates the chart."""
        self.num_days = len(self.data)

        self.returns = self.data.pct_change(fill_method=None).dropna()
        self.expected_returns = self.returns.mean() * self.num_days
        self.covariance_matrix = self.returns.cov() * self.num_days

        # print("\nExpected annual returns:\n", expected_returns)
        # print("\nAnnual covariance matrix:\n", covariance_matrix)

        tickers = self.data.columns

        # Perform optimization
        optimal_portfolio, optimal_sharpe = self.simulated_annealing_portfolio(
            assets=tickers,
            expected_returns=self.expected_returns.values,
            covariance_matrix=self.covariance_matrix.values,
            risk_free_rate=0.02,
            max_iter=20000,
            initial_temperature=100,
            cooling_rate=0.95,
            max_allocation=0.25,
            min_allocation=0.0
        )
        
        self.chart_widget.update_chart(optimal_portfolio, tickers, optimal_sharpe) # zaktualizowanie wykresu
        self.portfolio_table.setRowCount(len(self.expected_returns))                                # Zaktualizowanie tabeli danymi
        for i, asset in enumerate(self.expected_returns.index): # Dla każdego aktywa
            if abs(self.expected_returns[asset]) > 1e-7:
                self.portfolio_table.setItem(i, 0, QTableWidgetItem(asset))  # Nazwa aktywa
                expected_return = f"{self.expected_returns[asset]:.6f}"
                self.portfolio_table.setItem(i, 1, QTableWidgetItem(expected_return))  # Oczekiwany zwrot
                risk_level = self.calculate_risk_level(asset)  # Obliczamy poziom ryzyka
                # Formatuj poziom ryzyka do dokładności 1e-6, jeśli ma sens
                risk_level_formatted = f"{risk_level:.6f}" if isinstance(risk_level, (float, np.float64)) else str(risk_level)
                self.portfolio_table.setItem(i, 2, QTableWidgetItem(risk_level_formatted))  # Poziom ryzyka


    def simulated_annealing_portfolio(self, assets, expected_returns, covariance_matrix, 
        risk_free_rate=0, max_iter=10000, initial_temperature=100, 
        cooling_rate=0.99, max_allocation=0.5, min_allocation=0.0):
        """Function to optimize a portfolio using simulated annealing."""
        num_assets = len(assets)
        current_portfolio = np.random.dirichlet(np.ones(num_assets))
        # current_portfolio = np.ones(num_assets) / num_assets
        current_portfolio = self.enforce_constraints(current_portfolio, min_allocation, max_allocation)
        current_sharpe = self.calculate_sharpe(current_portfolio, expected_returns, covariance_matrix, risk_free_rate)
        best_portfolio = current_portfolio
        best_sharpe = current_sharpe
        temperature = initial_temperature

        for _ in range(max_iter):
            new_portfolio = self.make_move(current_portfolio, min_allocation, max_allocation)
            new_portfolio = self.enforce_constraints(new_portfolio, min_allocation, max_allocation)
            new_sharpe = self.calculate_sharpe(new_portfolio, expected_returns, covariance_matrix, risk_free_rate)
            if accept_move(current_sharpe, new_sharpe, temperature):
                current_portfolio = new_portfolio
                current_sharpe = new_sharpe
            if new_sharpe > best_sharpe:
                best_portfolio = new_portfolio
                best_sharpe = new_sharpe
            temperature *= cooling_rate

        return best_portfolio, best_sharpe

    def calculate_risk_level(self, asset):
        """Obliczanie poziomu ryzyka dla aktywa na podstawie macierzy kowariancji."""
        # Na przykład możemy obliczyć ryzyko jako wariancję z macierzy kowariancji
        return self.covariance_matrix.loc[asset, asset]
    
    def calculate_sharpe(self, weights, expected_returns, covariance_matrix, risk_free_rate=0):
        """Function to calculate the Sharpe ratio of a portfolio."""
        portfolio_return = np.dot(weights, expected_returns)
        portfolio_risk = np.sqrt(np.dot(weights, np.dot(covariance_matrix, weights)))
        return (portfolio_return - risk_free_rate) / portfolio_risk
    
    def make_move(self, weights, min_weight=0.0, max_weight=1.0):
        """Function to make a random move in the search space."""
        new_weights = np.copy(weights)
        random_idx = random.randint(0, len(weights) - 1)
        change = np.random.uniform(-0.01, 0.01)
        new_weights[random_idx] += change
        # Zapewniamy, że suma wag jest równa 1 (portfel jest zrównoważony)
        new_weights = np.clip(new_weights, min_weight, max_weight)
        new_weights /= np.sum(new_weights)  # Normalizacja wag
        return new_weights
    
    def enforce_constraints(self, portfolio, min_allocation, max_allocation):
        """Function to enforce constraints on portfolio weights."""
        portfolio = np.clip(portfolio, min_allocation, max_allocation)
        epsilon = 1e-6
        weights_sum = np.sum(portfolio)
        if weights_sum < 1 - epsilon or weights_sum > 1 + epsilon:
            portfolio /= weights_sum    
        return portfolio

## ---------------------- Dialog for selecting assets ------------------
class SelectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Select Options")
        self.setGeometry(150, 150, 800, 400)
        self.dialog_layout = QHBoxLayout()
        self.categories = self.load_categories_from_json('config/tickers.json')

        for category, items in self.categories.items():
            new_layout = QVBoxLayout()
            category_label = QLabel(category)
            new_layout.addWidget(category_label)
            option_list = QListWidget()
            option_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
            option_list.addItems(items)
            new_layout.addWidget(option_list)
            self.dialog_layout.addLayout(new_layout)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.dialog_layout.addWidget(self.button_box)

        self.setLayout(self.dialog_layout)

    def load_categories_from_json(self, file_path):
        """Function to load categories and options from a JSON file."""
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                return data
        except Exception as e:
            print(f"Error loading Assets from JSON file: {e}")
            return {}
        
    def get_selected_options(self):
        """Function to get selected options from the dialog."""
        selected_options = {}

        for layout_index in range(self.dialog_layout.count() - 1):  # Ostatni element to przyciski
            category_layout = self.dialog_layout.itemAt(layout_index).layout()
            if not category_layout:
                continue
            category_label = category_layout.itemAt(0).widget() # QLabel
            category = category_label.text()

            option_list = category_layout.itemAt(1).widget()  #  QListWidget
            if not option_list:
                continue
            selected_items = [item.text() for item in option_list.selectedItems()]
            if selected_items:
                selected_options[category] = selected_items
        return selected_options

## ---------------------- Chart Widget ------------------
class DataWindow(QWidget):
    def __init__(self, data):
        super().__init__()
        
        self.setWindowTitle("Loaded Data")
        self.setGeometry(100, 100, 600, 400)
        
        # Tworzenie widgetu QTableWidget do wyświetlenia danych
        self.table_widget = QTableWidget(self)
        self.table_widget.setRowCount(len(data))
        self.table_widget.setColumnCount(len(data.columns))
        self.table_widget.setHorizontalHeaderLabels(data.columns)
        
        # Wypełnienie tabeli danymi
        for row in range(len(data)):
            for col in range(len(data.columns)):
                item = QTableWidgetItem(str(data.iloc[row, col]))
                self.table_widget.setItem(row, col, item)
        
        # Układ layoutu
        layout = QVBoxLayout(self)
        layout.addWidget(self.table_widget)
        self.setLayout(layout)
        

class PortfolioChartWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure()
        self.figure.set_facecolor("whitesmoke")
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.clear_chart()

    def update_chart(self, weights, tickers, sharpe_ratio):
        """Aktualizuje wykres kołowy na podstawie nowych danych."""
        self.clear_chart()
        ax = self.figure.add_subplot(111)

        ax.pie(
            weights, 
            labels=tickers, 
            autopct='%1.1f%%', 
            startangle=90
        )
        ax.text(
            0.0,0.0,
            f"Portfolio Sharpe Ratio: {sharpe_ratio:.4f}",
            horizontalalignment='left',  # do lewej
            verticalalignment='bottom',  # do dołu
            transform=ax.transAxes  # W układzie współrzędnych osi
        )
        self.canvas.draw()

    def save_chart(self, file_path="wallet\ results/chart.png"):
        """Zapisuje wykres do pliku."""
        if file_path is None:
            file_path = os.path.join("wallet results", "chart.png")
            
            # Tworzenie folderu, jeśli nie istnieje
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            self.figure.savefig(file_path)
            print(f"Chart saved to file: {file_path}")

    def clear_chart(self):
        """Czysci wykres."""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_title("Portfolio Distribution")
        ax.set_xticks([])
        ax.set_yticks([])
        self.canvas.draw()
