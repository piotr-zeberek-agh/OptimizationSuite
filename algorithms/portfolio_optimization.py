from PyQt6.QtWidgets import QPushButton, QTableWidgetItem
import pandas as pd

def set_portfolio_view(window):
    """Set the view for the Portfolio Optimization scenario."""
    window.setWindowTitle("Portfolio Optimization")

    window.load_button = QPushButton("Load Data")
    window.load_button.clicked.connect(lambda: load_csv(window, "asset_data.csv"))
    window.layout.addWidget(window.load_button)

def load_csv(window, file_name: str):
    try:
        data = pd.read_csv(file_name)
        window.table_widget.setRowCount(len(data))
        window.table_widget.setColumnCount(len(data.columns))
        window.table_widget.setHorizontalHeaderLabels(data.columns)

        for row in range(len(data)):
            for col in range(len(data.columns)):
                item = QTableWidgetItem(str(data.iloc[row, col]))
                window.table_widget.setItem(row, col, item)
    except Exception as e:
        print(f"Error loading data: {e}")