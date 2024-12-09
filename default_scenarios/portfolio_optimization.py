from scenario import Scenario
from PyQt6.QtWidgets import QPushButton, QTableWidgetItem, QTableWidget
import pandas as pd
import yfinance as yf

class PortfolioOptimizationScenario(Scenario):
    def __init__(self, layout):
        super().__init__(layout)
        self.data = None
        self.isDataLoaded = False
        
    def adjust_layout(self):
        """Set the view for the Structure of Fullerenes scenario"""
        # self.window.tit("Gradient Descent")

        # create table for variables
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["Variable Name", "Value"])
        self.table_widget.setRowCount(8)

        self.layout.addWidget(self.table_widget)

        
# # ---------------------- Main Method -------------------
#     def anneal(self):
#         # Add your simulated annealing code here
#         print("Simulated annealing code goes here...")
# # ---------------------- GUI code -------------------

#     def set_portfolio_view(self, window):
#         """Set the view for the Portfolio Optimization scenario."""
#         window.setWindowTitle("Portfolio Optimization")

#         window.load_button = QPushButton("Load Data")
#         # window.load_button.clicked.connect(lambda: self.load_csv(window, "asset_data.csv"))
#         window.load_button.clicked.connect(lambda: self.load_csv(window, "data/asset_data.csv"))
#         window.layout.addWidget(window.load_button)

#         window.save_button = QPushButton("Save Data")
#         window.save_button.clicked.connect(
#             lambda: self.save_csv(self.data, "data/new_data.csv") if self.isDataLoaded else print("No data loaded!"))
#         window.layout.addWidget(window.save_button)

#         window.down_button = QPushButton("Download Data")
#         window.down_button.clicked.connect(lambda: self.download_data())
#         window.layout.addWidget(window.down_button)

# # ---------------------- Data -------------------


#     def download_data(self):
#         self.tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "NFLX", "SPY", "BABA"]
#         self.start_date = "2022-01-01"
#         self.end_date = "2024-10-31"
#         self.data = yf.download(self.tickers, start=self.start_date, end=self.end_date)['Adj Close']
#         if self.data is not None:
#             self.isDataLoaded = True
#         else:
#             print("Cannot download data!")

#     def save_csv(self, data, file_name: str):
#         data.to_csv(file_name)
#         print(f"Data saved in {file_name}")

#     def load_csv(self, window, file_name: str):
#         try:
#             self.data = pd.read_csv(file_name)
#             if self.data is not None:
#                 self.isDataLoaded = True
#             else:
#                 print("Cannot load data!")
#             window.table_widget.setRowCount(len(self.data))
#             window.table_widget.setColumnCount(len(self.data.columns))
#             window.table_widget.setHorizontalHeaderLabels(self.data.columns)

#             for row in range(len(self.data)):
#                 for col in range(len(self.data.columns)):
#                     item = QTableWidgetItem(str(self.data.iloc[row, col]))
#                     window.table_widget.setItem(row, col, item)
#         except Exception as e:
#             print(f"Error loading data: {e}")











#     def load_data(self, file_name: str):
#         try:
#             self.data = pd.read_csv(file_name)
#         except Exception as e:
#             print(f"Error loading data: {e}")
    
#     def optimize(self):
#         if self.data is None:
#             print("No data loaded!")
#             return
        
#         # Add your optimization code here
#         print("Optimization code goes here...")

#     def save_results(self, file_name: str):
#         # Add your code to save the results
#         print(f"Results saved in {file_name}")

#     def display_results(self):
#         # Add your code to display the results
#         print("Displaying results...")

#     def run(self):
#         self.optimize()
#         self.display_results()






