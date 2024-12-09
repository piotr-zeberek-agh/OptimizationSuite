from PyQt6.QtWidgets import QLabel, QFrame, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QComboBox, QTableWidget, QLineEdit
from PyQt6.QtGui import QFont

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.set_base_layout()
        self.combo_box.setCurrentIndex(-1)
        # tracks option changes in the combo box
        self.combo_box.currentTextChanged.connect(self.on_scenario_change)

    def set_base_layout(self, selected_scenario = None):
        """Sets up the base layout with combo box and table widget."""

        self.setWindowTitle("Optimization Suite")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.titlehbox = QHBoxLayout()
        
        title_label = QLabel("Simulated annealing")
        title_label.setFixedWidth(250)
        font = QFont("Arial", 18, QFont.Weight.Bold)
        title_label.setFont(font)
        self.titlehbox.addWidget(title_label)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        self.titlehbox.addWidget(line)

        self.combo_box = QComboBox()
        self.scenario = {"Structure Of Fullerenes", "Portfolio Optimization", "Gradient Descent"}
        
        if selected_scenario is None:
            cb_list = sorted(self.scenario)
            self.combo_box.addItems(cb_list)
        else:
            cb_list = [selected_scenario] + sorted(self.scenario - {selected_scenario})
            self.combo_box.addItems(cb_list)

        self.titlehbox.addWidget(self.combo_box)

        self.layout.addLayout(self.titlehbox)

        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)

        self.text_box = QLineEdit()
        self.layout.addWidget(self.text_box)

        self.central_widget.setLayout(self.layout)

    def clear_layout(self):
        """Clear all widgets in the current layout."""
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

    def on_scenario_change(self, selected_scenario: str):
        """Handle the scenario selection event."""
        print(f"Selected scenario: {selected_scenario}")

        self.clear_layout()
        self.set_base_layout(selected_scenario)
        self.combo_box.currentTextChanged.connect(self.on_scenario_change)

        if selected_scenario == "Structure Of Fullerenes":
            self.setup_fullerenes()
        elif selected_scenario == "Portfolio Optimization":
            self.setup_portfolio()
        elif selected_scenario == "Gradient Descent":
            self.setup_gradient()

    def setup_fullerenes(self):
        """Set up the Structure Of Fullerenes scenario."""
        from algorithms.structure_of_fullerenes import set_fullerenes_view
        set_fullerenes_view(self)

    def setup_portfolio(self):
        """Set up the Portfolio Optimization scenario."""
        from algorithms.portfolio_optimization import set_portfolio_view
        set_portfolio_view(self)

    def setup_gradient(self):
        """Set up the Gradient Descent scenario."""
        from algorithms.gradient_descent import set_gradient_descent_view
        set_gradient_descent_view(self)    
