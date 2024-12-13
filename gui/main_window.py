from PyQt6.QtWidgets import QLabel, QFrame, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QComboBox, QTableWidget, QPushButton
from PyQt6.QtGui import QFont
from default_scenarios import (gradient_descent, fullerenes_structure, portfolio_optimization)

DEFAULT_SCENARIO_CLASSES = {
    "Gradient Descent": gradient_descent.GradientDescentScenario,
    "Structure Of Fullerenes": fullerenes_structure.FullerenesStructureScenario,
    "Portfolio Optimization": portfolio_optimization.PortfolioOptimizationScenario
}

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_scenario = None
        self.scenario_classes = DEFAULT_SCENARIO_CLASSES
        self.imported_scenario_classes = {}
        
        self.set_base_layout()
        self.scenario_combo_box.setCurrentIndex(-1)
        # tracks option changes in the combo box
        self.scenario_combo_box.currentTextChanged.connect(self.on_scenario_change)

    def set_base_layout(self):
        """Sets up the base layout with scenario label and combo box and combo box."""

        self.setWindowTitle("Optimization Suite")
        self.setGeometry(100, 100, 1000, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.scenario_choosing_layout = QHBoxLayout()
        
        self.scenario_label = QLabel("Choose scenario")
        self.scenario_label.setFixedWidth(250)
        font = QFont("Arial", 16, QFont.Weight.Bold)
        self.scenario_label.setFont(font)
        self.scenario_choosing_layout.addWidget(self.scenario_label)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.VLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        self.scenario_choosing_layout.addWidget(line)

        self.scenario_combo_box = QComboBox()
        self.scenario_combo_box.addItems(self.scenario_classes.keys())
        self.scenario_choosing_layout.addWidget(self.scenario_combo_box)
        
        # modified by scenario
        self.scenario_input_layout = QVBoxLayout()
        self.scenario_input_layout.addWidget(QTableWidget())
        
        self.window_layout = QVBoxLayout()

        self.window_layout.addLayout(self.scenario_choosing_layout)
        self.window_layout.addLayout(self.scenario_input_layout)
        
        self.run_button = QPushButton()
        self.run_button.setText("Run")
        self.window_layout.addWidget(self.run_button)

        # self.table_widget = QTableWidget()
        # self.layout.addWidget(self.table_widget)

        # self.text_box = QLineEdit()
        # self.layout.addWidget(self.text_box)

        self.central_widget.setLayout(self.window_layout)

    def on_scenario_change(self):
        """Handle the scenario selection event."""
        scenario_name = self.scenario_combo_box.currentText()
        self.scenario_label.setText(scenario_name)
        self.current_scenario = self.scenario_classes[scenario_name](self.scenario_input_layout)
        self.run_button.clicked.connect(self.current_scenario.run)

    def setup_fullerenes(self):
        """Set up the Structure Of Fullerenes scenario."""
        from default_scenarios.fullerenes_structure import FullerenesStructureScenario
        # self.current_scenario = FullerenesStructureScenario(self)

    def setup_portfolio(self):
        """Set up the Portfolio Optimization scenario."""
        from default_scenarios.portfolio_optimization import PortfolioOptimizationScenario
        self.current_scenario = PortfolioOptimizationScenario(self)

    def setup_gradient(self):
        """Set up the Gradient Descent scenario."""
        from default_scenarios.gradient_descent import GradientDescentScenario
        self.current_scenario = GradientDescentScenario(self)
        
