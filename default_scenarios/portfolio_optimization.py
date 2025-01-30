from utilities.scenario import Scenario
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QVBoxLayout, QDialog, QListWidget, QLabel, QGridLayout, QStackedWidget, QFileDialog, QDialogButtonBox, QTableWidgetItem, QFrame, QLineEdit, QTableWidget, QPushButton, QHBoxLayout, QWidget

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import json
from utilities.portfolio_data import fetch_data
from utilities.annealing import accept_move
import numpy as np
import pandas as pd
import random
import re
import os
from PyQt6.QtGui import QPixmap, QIcon
from pathlib import Path

class PortfolioOptimizationScenario(Scenario):
    """Scenario for portfolio optimization."""
    def __init__(self, layout):
        super().__init__(layout)
        self.selected_options = None
        self.data = None
        self.risk_free_rate = 0
        self.autosave_enabled = False
        self.run_button_clicked = False
        self.chart_widget = PortfolioChartWidget()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)
        self.timer.timeout.connect(self.handle_data)
        self.timer.start(500)  # 500 ms

        self.adjust_layout()
            
    def adjust_layout(self):
        """Adjusts the layout to include elements for portfolio optimization."""

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

        self.open_dialog_button = QPushButton("Choose assets")
        self.open_dialog_button.clicked.connect(self.open_selection_window)
        self.date_row.addWidget(self.open_dialog_button)

        self.left_layout.addLayout(self.date_row)

        self.download_data_button = QPushButton()
        self.download_data_button.setText("Download data")
        self.download_data_button.setEnabled(False)
        self.download_data_button.clicked.connect(self.download_data)
        self.left_layout.addWidget(self.download_data_button)

        self.download_layout = QHBoxLayout()
        self.filename_line = QLineEdit()
        self.filename_line.setPlaceholderText("Enter filename")
        self.download_layout.addWidget(self.filename_line)
        self.filename_line.textChanged.connect(self.check_filename_input)
        self.save_data_button = QPushButton()
        self.save_data_button.setText("Save data")
        self.save_data_button.setEnabled(False)
        self.save_data_button.clicked.connect(self.save_data)
        self.download_layout.addWidget(self.save_data_button)
        self.left_layout.addLayout(self.download_layout)

        self.line_download = QFrame()
        self.line_download.setFrameShape(QFrame.Shape.HLine)
        self.line_download.setFrameShadow(QFrame.Shadow.Sunken)
        self.left_layout.addWidget(self.line_download)
        
        self.selected_table = QTableWidget()
        self.left_layout.addWidget(self.selected_table)

        self.assets_buttons_layout = QHBoxLayout()

        self.open_dialog_button = QPushButton("Load data")
        self.open_dialog_button.clicked.connect(self.load_data)
        self.assets_buttons_layout.addWidget(self.open_dialog_button)
        self.clear_data_button = QPushButton("Clear data")
        self.clear_data_button.clicked.connect(self.clear_data)
        self.assets_buttons_layout.addWidget(self.clear_data_button)
        self.left_layout.addLayout(self.assets_buttons_layout)

        self.save_chart_button = QPushButton("Save chart")
        self.save_chart_button.clicked.connect(self.chart_widget.save)
        self.left_layout.addWidget(self.save_chart_button)

        self.risk_free_rate_input = QLineEdit()
        self.max_iter_input = QLineEdit()
        self.initial_temperature_input = QLineEdit()
        self.cooling_rate_input = QLineEdit()
        self.max_allocation_input = QLineEdit()
        self.min_allocation_input = QLineEdit()
        
        self.risk_free_rate_input.setText("0")
        self.max_iter_input.setText("30000")
        self.initial_temperature_input.setText("100")
        self.cooling_rate_input.setText("0.95")
        self.max_allocation_input.setText("0.25")
        self.min_allocation_input.setText("0.0")
            
        layout = QGridLayout()
        layout.addWidget(QLabel("Risk-Free Rate:"), 0, 0)
        layout.addWidget(self.risk_free_rate_input, 0, 1)
        layout.addWidget(QLabel("Max Iterations:"), 1, 0)
        layout.addWidget(self.max_iter_input, 1, 1)
        layout.addWidget(QLabel("Initial Temperature:"), 2, 0)
        layout.addWidget(self.initial_temperature_input, 2, 1)
        layout.addWidget(QLabel("Cooling Rate:"), 0, 2)
        layout.addWidget(self.cooling_rate_input, 0, 3)
        layout.addWidget(QLabel("Max Allocation:"), 1, 2)
        layout.addWidget(self.max_allocation_input, 1, 3)
        layout.addWidget(QLabel("Min Allocation:"), 2, 2)
        layout.addWidget(self.min_allocation_input, 2, 3)
        self.left_layout.addLayout(layout)

        self.run_button = QPushButton("Run")
        self.run_button.setEnabled(False)
        self.run_button.clicked.connect(self.run)
        self.left_layout.addWidget(self.run_button)

        self.mid_layout = QVBoxLayout()
        self.middle_line = QFrame()
        self.middle_line.setFrameShape(QFrame.Shape.VLine)
        self.middle_line.setFrameShadow(QFrame.Shadow.Sunken)
        self.mid_layout.addWidget(self.middle_line)

        self.right_layout = QVBoxLayout()
        self.right_layout.addWidget(self.chart_widget)

        self.portfolio_table = QTableWidget()
        self.portfolio_table.setRowCount(0)
        self.portfolio_table.setColumnCount(8)
        self.portfolio_table.setHorizontalHeaderLabels(["Asset Name", "Allocation", "Expected Return", "Correlation", "Risk", "Beta", "Sharpe Ratio", "Treynor Ratio"])
        self.portfolio_table.resizeColumnsToContents()

        self.right_layout.addWidget(self.portfolio_table)

        self.container_widget = QWidget()
        self.container_widget.setLayout(self.left_layout)
        self.container_widget.setFixedWidth(530)
        self.main_window.addWidget(self.container_widget)
        # self.main_window.addLayout(self.left_layout)

        self.main_window.addLayout(self.mid_layout)
        self.main_window.addLayout(self.right_layout, stretch=1)
        self.layout.addLayout(self.main_window)

    def update_status(self):
        """Method to update in loop the status of the autosave button."""
        if self.autosave_enabled != self.chart_widget.autosave_enabled:
            self.chart_widget.autosave_enabled = not self.chart_widget.autosave_enabled

    def handle_data(self):
        """Method to handle the data input."""
        try:
            self.risk_free_rate = float(self.risk_free_rate_input.text())
            self.max_iter = int(self.max_iter_input.text())
            self.initial_temperature = float(self.initial_temperature_input.text())
            self.cooling_rate = float(self.cooling_rate_input.text())
            self.max_allocation = float(self.max_allocation_input.text())
            self.min_allocation = float(self.min_allocation_input.text())
        except ValueError as e:
            print(f"Error: Please enter valid numbers. {e}")

    def check_date_input(self):
        """ Function to check if the date input is correct."""
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

    def open_selection_window(self):
        """Function to open a dialog for selecting assets"""
        try:
            dialog = SelectionDialog()
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.selected_options = dialog.get_selected_options()

                if self.selected_options:
                    column_headers = []
                    for category, selected_assets in self.selected_options.items():
                        column_headers.extend(selected_assets)

                    self.selected_table.setColumnCount(len(column_headers))
                    self.selected_table.setHorizontalHeaderLabels(column_headers)
                    self.selected_table.setRowCount(0)

                    for i, asset in enumerate(column_headers):
                        q_item = QTableWidgetItem(asset)
                        q_item.setFlags(q_item.flags() & ~Qt.ItemFlag.ItemIsEditable) 
                        self.selected_table.setItem(0, i, q_item)
                    self.selected_table.resizeColumnsToContents()
                    self.check_date_input()
        except Exception as e:
            print(f"Error opening selection window: {e}")

    def download_data(self):
        """Function to download data from the API."""
        try:
            start_date = self.start_date_line.text()
            end_date = self.end_date_line.text()
            self.data = fetch_data(self.selected_options, start_date, end_date)
            self.run_button.setEnabled(True)

            if self.data is None:
                print("Error: No data returned from API!")
                return

            date_column = self.data.index
            row_count = len(date_column)
            self.selected_table.setRowCount(row_count)

            column_headers = []
            for category, selected_assets in self.selected_options.items():
                for asset in selected_assets:
                    column_headers.append(asset)

            self.selected_table.setColumnCount(len(column_headers))
            self.selected_table.setHorizontalHeaderLabels(column_headers)

            for i, category in enumerate(self.selected_options.keys()):
                for j, asset in enumerate(self.selected_options[category]):
                    column_index = column_headers.index(asset)

                    for day_index, date in enumerate(date_column):
                        data_value = self.data.loc[date, asset] if asset in self.data.columns else None
                        q_item = QTableWidgetItem(f"{data_value:.2f}" if data_value is not None else "")
                        q_item.setFlags(q_item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Block editing
                        self.selected_table.setItem(day_index, column_index, q_item)

            self.selected_table.resizeColumnsToContents()
        except Exception as e:
            print(f"Error downloading data: {e}")

    def switch_tab(self, index):
        """Function to switch between tabs in the stacked widget."""
        self.stacked_widget.setCurrentIndex(index)

    def show_widget_visibility(self):
        """Function to show the visibility of the current widget."""
        current_widget = self.stacked_widget.currentWidget()
        visibility = "visible" if current_widget.isVisible() else "hidden"
        print(f"Current widget visibility: {visibility}")        

    def check_filename_input(self):
        """Function to check if the filename input is correct."""
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
        """Function to check if the run button should be enabled."""
        if self.data is not None:
            self.run_button.setEnabled(True)
        else:
            self.run_button.setEnabled(False)

    def save_data(self):
        """Function to save the data to a CSV file."""
        folder_path = "data/portfolio_optimization/"
        Path(folder_path).mkdir(parents=True, exist_ok=True)

        filename = self.filename_line.text()
        if not filename.endswith('.csv'):
            filename += '.csv'
        self.data.to_csv(folder_path+filename)
        print(f"Chart saved to file: {folder_path + filename}")

    def clear_data(self):
        """Function to clear the data and reset the UI."""
        self.selected_table.setColumnCount(0)
        self.selected_table.setRowCount(0)
        self.selected_table.clear()
        self.portfolio_table.setRowCount(0)
        self.portfolio_table.clear()
        self.portfolio_table.setHorizontalHeaderLabels(["Asset Name", "Allocation", "Expected Return", "Correlation", "Risk", "Beta", "Sharpe Ratio", "Treynor Ratio"])
        self.portfolio_table.resizeColumnsToContents()
        self.download_data_button.setEnabled(False)
        self.save_data_button.setEnabled(False) 
        self.run_button.setEnabled(False)
        self.selected_options = None
        self.data = None
        self.chart_widget.clear_chart()
        self.run_button_clicked = False
# q_item.setFlags(q_item.flags() & ~Qt.ItemFlag.ItemIsEditable)   # block editing
    def load_data(self):
        """Function to load data from a CSV file."""
        folder_path = "data/portfolio_optimization/"
        Path(folder_path).mkdir(parents=True, exist_ok=True)
        try:
            file_name, _ = QFileDialog.getOpenFileName(
                None, "Select CSV File", folder_path, "CSV Files (*.csv);;All Files (*)"
            )
            if not file_name:
                print("No file selected!")
                return

            file_data = pd.read_csv(file_name)

            if file_data.columns[0] == 'Date':
                self.data = file_data.iloc[:, 1:]
                self.date = file_data.iloc[:, 0]

            # convert data to numeric
            self.data = self.data.apply(pd.to_numeric, errors='coerce')

            self.selected_table.setRowCount(len(self.data))
            self.selected_table.setColumnCount(len(self.data.columns))
            self.selected_table.setHorizontalHeaderLabels(self.data.columns)

            for row in range(len(self.data)):
                for col in range(len(self.data.columns)):
                    # item = QTableWidgetItem(str(self.data.iloc[row, col]))
                    item = QTableWidgetItem(f"{self.data.iloc[row, col]:.2f}")
                    self.selected_table.setItem(row, col, item)
            self.selected_table.resizeColumnsToContents()
            print(f"Data successfully loaded from {file_name}!")

        except Exception as e:
            print(f"Error loading data: {e}")

        if self.data is not None:
            self.run_button.setEnabled(True)

    def run(self):
        """Simulates portfolio optimization and updates the chart."""
        self.run_button_clicked = True

        self.num_days = len(self.data)
        self.returns = self.data.pct_change(fill_method=None).dropna()
        self.expected_returns = self.returns.mean() * self.num_days
        self.covariance_matrix = self.returns.cov() * self.num_days

        tickers = self.data.columns

        while True:
            optimal_portfolio, optimal_sharpe, asset_details = self.simulated_annealing_portfolio(
                assets=tickers,
                expected_returns=self.expected_returns.values,
                covariance_matrix=self.covariance_matrix.values,
                risk_free_rate=self.risk_free_rate,
                max_iter=self.max_iter,
                initial_temperature=self.initial_temperature,
                cooling_rate=self.cooling_rate,
                max_allocation=self.max_allocation,
                min_allocation=self.min_allocation
            )
            if optimal_sharpe > 0:
                break

        tickers_cut = [label for label, value in zip(tickers, optimal_portfolio) if value >= 1e-4]
        values_cut = [value for value in optimal_portfolio if value >= 1e-4]
        self.chart_widget.update_chart(values_cut, tickers_cut, optimal_sharpe)

        self.portfolio_table.setRowCount(len(asset_details))
        for i, asset_data in enumerate(asset_details):
            self.portfolio_table.setItem(i, 0, QTableWidgetItem(asset_data["Asset Name"]))
            self.portfolio_table.setItem(i, 1, QTableWidgetItem(f"{asset_data['Allocation']:.6f}"))
            self.portfolio_table.setItem(i, 2, QTableWidgetItem(f"{asset_data['Expected Return']:.6f}"))
            self.portfolio_table.setItem(i, 3, QTableWidgetItem(f"{asset_data['Correlation']:.6f}"))
            self.portfolio_table.setItem(i, 4, QTableWidgetItem(f"{asset_data['Risk']:.6f}"))
            self.portfolio_table.setItem(i, 5, QTableWidgetItem(f"{asset_data['Beta']:.6f}"))
            self.portfolio_table.setItem(i, 6, QTableWidgetItem(f"{asset_data['Sharpe Ratio']:.6f}"))
            self.portfolio_table.setItem(i, 7, QTableWidgetItem(f"{asset_data['Treynor Ratio']:.6f}"))
        self.portfolio_table.resizeColumnsToContents()

        if self.autosave_enabled:
            self.chart_widget.save()

    def calculate_beta(self, covariance_matrix, asset_index):
        """Calculate Beta for an individual asset."""
        market_variance = np.sum(covariance_matrix) / covariance_matrix.shape[0]  # approximating market variance
        covariance_with_market = np.sum(covariance_matrix[asset_index])
        return covariance_with_market / market_variance if market_variance != 0 else 0

    def calculate_sharpe_individual(self, expected_return, risk, risk_free_rate):
        """Calculate Sharpe Ratio for an individual asset."""
        return (expected_return - risk_free_rate) / risk if risk != 0 else 0

    def calculate_correlation(self, covariance_matrix, asset_index, portfolio_weights):
        """Calculate correlation of an asset with the portfolio."""
        portfolio_variance = np.dot(portfolio_weights, np.dot(covariance_matrix, portfolio_weights))
        asset_variance = covariance_matrix[asset_index, asset_index]
        covariance = np.dot(covariance_matrix[asset_index], portfolio_weights)
        if portfolio_variance == 0 or asset_variance == 0:
            return 0
        return covariance / np.sqrt(portfolio_variance * asset_variance)

    def calculate_treynor(self, expected_return, risk_free_rate, beta):
        """Calculate the Treynor Ratio for a single asset."""
        if beta == 0:
            return float('inf')
        return (expected_return - risk_free_rate) / beta

    def stop(self):
        """Function to stop the simulation."""
        pass

    def simulated_annealing_portfolio(self, assets, expected_returns, covariance_matrix, 
            risk_free_rate=0, max_iter=10000, initial_temperature=100, 
            cooling_rate=0.99, max_allocation=0.5, min_allocation=0.0):
        """Optimize a portfolio using simulated annealing."""
        num_assets = len(assets)
        current_portfolio = np.random.dirichlet(np.ones(num_assets))  # Random portfolio weights (sum to 1)
        current_portfolio = self.enforce_constraints(current_portfolio, min_allocation, max_allocation)
        current_sharpe = self.calculate_sharpe(current_portfolio, expected_returns, covariance_matrix, risk_free_rate)
        best_portfolio = current_portfolio
        best_sharpe = current_sharpe
        temperature = initial_temperature

        for _ in range(max_iter):
            new_portfolio = self.make_move(current_portfolio, min_allocation, max_allocation)
            new_sharpe = self.calculate_sharpe(new_portfolio, expected_returns, covariance_matrix, risk_free_rate)
            if accept_move(current_sharpe, new_sharpe, temperature):
                current_portfolio = new_portfolio
                current_sharpe = new_sharpe
            if new_sharpe > best_sharpe:
                best_portfolio = new_portfolio
                best_sharpe = new_sharpe
            temperature *= cooling_rate

        asset_details = []
        for idx, asset in enumerate(assets):
            allocation = best_portfolio[idx]
            expected_return = expected_returns[idx]
            risk = np.sqrt(covariance_matrix[idx, idx])
            beta = self.calculate_beta(covariance_matrix, idx)
            sharpe_ratio = self.calculate_sharpe_individual(expected_return, risk, risk_free_rate)
            treynor_ratio = self.calculate_treynor(expected_return, risk_free_rate, beta)
            correlation = self.calculate_correlation(covariance_matrix, idx, best_portfolio)

            asset_details.append({
                "Asset Name": asset,
                "Allocation": allocation,
                "Expected Return": expected_return,
                "Risk": risk,
                "Beta": beta,
                "Sharpe Ratio": sharpe_ratio,
                "Treynor Ratio": treynor_ratio,
                "Correlation": correlation,
            })

        return best_portfolio, best_sharpe, asset_details

    def calculate_risk_level(self, asset):
        """Calculate the risk level of an asset."""
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
        new_weights = np.clip(new_weights, min_weight, max_weight) # Clip to [0, 1]
        new_weights /= np.sum(new_weights)
        return new_weights
    
    def enforce_constraints(self, portfolio, min_allocation, max_allocation):
        """Function to enforce constraints on portfolio weights."""
        portfolio = np.clip(portfolio, min_allocation, max_allocation)
        epsilon = 1e-6
        weights_sum = np.sum(portfolio)
        if weights_sum < 1 - epsilon or weights_sum > 1 + epsilon:
            portfolio /= weights_sum    
        return portfolio

class SelectionDialog(QDialog):
    """Dialog for selecting assets."""
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

        for layout_index in range(self.dialog_layout.count() - 1):
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

class DataWindow(QWidget):
    """Widget for displaying loaded data."""
    def __init__(self, data):
        super().__init__()
        
        self.setWindowTitle("Loaded Data")
        self.setGeometry(100, 100, 600, 400)
        
        self.table_widget = QTableWidget(self)
        self.table_widget.setRowCount(len(data))
        self.table_widget.setColumnCount(len(data.columns))
        self.table_widget.setHorizontalHeaderLabels(data.columns)
        
        for row in range(len(data)):
            for col in range(len(data.columns)):
                item = QTableWidgetItem(str(data.iloc[row, col]))
                self.table_widget.setItem(row, col, item)
        
        layout = QVBoxLayout(self)
        layout.addWidget(self.table_widget)
        self.setLayout(layout)
        
class PortfolioChartWidget(QWidget):
    """Widget for displaying a pie chart of portfolio distribution."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure()
        self.figure.set_facecolor("whitesmoke")
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.clear_chart()
        self.autosave_enabled = True

    def update_chart(self, weights, tickers, sharpe_ratio):
        """Updates the pie chart with new data."""
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
            horizontalalignment='left',
            verticalalignment='bottom',
            transform=ax.transAxes
        )
        self.canvas.draw()

    def save(self):
        """Save the chart"""
        folder_path = "results/portfolio_optimization/"
        Path(folder_path).mkdir(parents=True, exist_ok=True)     # Create directory if it doesn't exist
        # os.makedirs(os.path.dirname(file_path), exist_ok=True) # Create directory if it doesn't exist
        # file_path, _ = QFileDialog.getSaveFileName( None, "Save Chart", folder_path, "PNG Files (*.png);;All Files (*)") # Ask user for file path
        if self.autosave_enabled:
            self.figure.savefig(folder_path + "wallet.png") # Save chart to file
            print(f"Chart saved to file: {folder_path + 'wallet.png'}")
        else:
            file_path, _ = QFileDialog.getSaveFileName( None, "Save Chart", folder_path, "PNG Files (*.png);;All Files (*)") # Ask user for file path
            if file_path:
                self.figure.savefig(file_path) # Save chart to file
                print(f"Chart saved to file: {file_path}") 

    def clear_chart(self):
        """Clears the chart."""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_title("Portfolio Distribution")
        ax.set_xticks([])
        ax.set_yticks([])
        self.canvas.draw()
