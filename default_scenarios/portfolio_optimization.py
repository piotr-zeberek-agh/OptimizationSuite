from scenario import Scenario
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QTableWidget, QPushButton, QHBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class PortfolioOptimizationScenario(Scenario):
    def __init__(self, layout):
        super().__init__(layout)
        
        self.adjust_layout()
        

    def adjust_layout(self):
        """Adjusts the layout to include elements for portfolio optimization."""

        # its because self.layout is a QVBoxLayout
        self.main_window = QHBoxLayout()

        # self.layout = QHBoxLayout()

        self.left_layout = QVBoxLayout()
        self.portfolio_table = QTableWidget()
        self.portfolio_table.setRowCount(5)
        self.portfolio_table.setColumnCount(3)
        self.portfolio_table.setHorizontalHeaderLabels(["Asset Name", "Expected Return", "Risk Level"])
        self.left_layout.addWidget(self.portfolio_table)
        self.run_button = QPushButton("Optimize Portfolio")
        self.left_layout.addWidget(self.run_button)
        self.main_window.addLayout(self.left_layout)

        self.right_layout = QVBoxLayout()
        self.chart_widget = PortfolioChartWidget()
        self.right_layout.addWidget(self.chart_widget)
        self.main_window.addLayout(self.right_layout)

        self.layout.addLayout(self.main_window)

        # run_button.clicked.connect(lambda: self.run(portfolio_table, chart_widget))


    def run(self, portfolio_table, chart_widget):
        """Simulates portfolio optimization and updates the chart."""


class PortfolioChartWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def update_chart(self, data):
        """Update the pie chart with new data."""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.pie(data.values(), labels=data.keys(), autopct='%1.1f%%', startangle=90)
        ax.set_title("Portfolio Distribution")
        self.canvas.draw()


# # ---------------------- Data ------------------

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
