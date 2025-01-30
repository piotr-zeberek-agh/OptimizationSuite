from PyQt6.QtWidgets import QLabel, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QComboBox, QTableWidget, QPushButton
from default_scenarios import (gradient_descent, fullerenes_structure, portfolio_optimization)
from gui.help.help_portfolio import HelpWindowPortfolio
from gui.help.help_fullerenes import HelpWindowFullerenes
from gui.help.help_gradient import HelpWindowGradient
from gui.help.help_default import HelpWindowDefault

from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize

DEFAULT_SCENARIO_CLASSES = {
    "Gradient Descent": gradient_descent.GradientDescentScenario,
    "Structure Of Fullerenes": fullerenes_structure.FullerenesStructureScenario,
    "Portfolio Optimization": portfolio_optimization.PortfolioOptimizationScenario
}

class MainWindow(QMainWindow):
    """Main window of the application."""
    def __init__(self):
        super().__init__()

        self.current_scenario = None
        self.scenario_classes = DEFAULT_SCENARIO_CLASSES
        self.imported_scenario_classes = {}
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)
        self.timer.start(500) # 500 ms

        self.is_dark_mode = True
        self.autosave_enabled = True

        self.set_base_layout()
        self.scenario_combo_box.setCurrentIndex(-1)
        self.scenario_combo_box.currentTextChanged.connect(self.on_scenario_change) # tracks option changes in the combo box

    def set_base_layout(self):
        """Sets up the base layout with scenario label and combo box and combo box."""

        self.setWindowTitle("Optimization Suite")
        self.setGeometry(100, 100, 1280, 900)

        self.central_widget = QWidget()
        self.central_widget.setStyleSheet("background-color: #2f2f2f; color: white;")

        self.setCentralWidget(self.central_widget)
        self.scenario_choosing_layout = QHBoxLayout()
        
        self.scenario_label = QLabel("Choose scenario")
        self.scenario_label.setFixedWidth(310)
        font = QFont("Arial", 16, QFont.Weight.Bold)
        self.scenario_label.setFont(font)
        self.scenario_choosing_layout.addWidget(self.scenario_label)
        self.scenario_choosing_layout.setContentsMargins(0, 0, 0, 0)
        self.scenario_choosing_layout.setSpacing(5)

        self.scenario_combo_box = QComboBox()
        self.scenario_combo_box.setPlaceholderText("Select scenario")
        self.scenario_combo_box.setFixedWidth(300)
        self.scenario_choosing_layout.addStretch()
        self.scenario_choosing_layout.setAlignment(self.scenario_combo_box, Qt.AlignmentFlag.AlignRight)
        self.scenario_combo_box.addItems(self.scenario_classes.keys())

        self.help_button = QPushButton()
        self.help_button.setIcon(QIcon("resources/images/help.png"))
        self.help_button.setIconSize(QSize(32, 32))
        self.help_button.setToolTip("Show help")
        self.help_button.setFixedSize(40, 40)
        self.help_button.setStyleSheet("border: 2px solid transparent;")
        self.help_button.clicked.connect(self.help_button_clicked)

        self.dark_light_mode_button = QPushButton()
        self.dark_light_mode_button.setIcon(QIcon("resources/images/mode.png"))
        self.dark_light_mode_button.setIconSize(QSize(32, 32))
        self.dark_light_mode_button.setToolTip("Change to light mode")
        self.dark_light_mode_button.setFixedSize(40, 40)
        self.dark_light_mode_button.clicked.connect(self.toggle_dark_light_mode)

        self.autosave_button = QPushButton()
        # self.autosave_button.setCheckable(True)
        self.autosave_button.setIcon(QIcon("resources/images/autosave.svg"))
        self.autosave_button.setIconSize(QSize(32, 32))
        self.autosave_button.setToolTip("Autosave turned on")
        self.autosave_button.setFixedSize(40, 40)
        self.autosave_button.setStyleSheet("border: 2px solid transparent;")
        self.autosave_button.clicked.connect(self.toggle_autosave)
        self.autosave_button.setStyleSheet("border: 2px solid orange;")

        self.scenario_choosing_layout.addWidget(self.help_button)
        self.scenario_choosing_layout.addWidget(self.dark_light_mode_button)
        self.scenario_choosing_layout.addWidget(self.autosave_button)

        self.scenario_choosing_layout.addWidget(self.scenario_combo_box)
        self.window_layout = QVBoxLayout()
        self.window_layout.addLayout(self.scenario_choosing_layout)

        self.scenario_input_layout = QVBoxLayout()
        self.scenario_input_layout.addWidget(QTableWidget())
        self.window_layout.addLayout(self.scenario_input_layout)

        self.central_widget.setLayout(self.window_layout)

    def show_help_window(self):
        """Show the help window."""
        help_me_window = HelpWindowDefault(self)
        help_me_window.show_help()

    def update_status(self):
        """Method to update in loop the status of the autosave button."""
        if self.current_scenario != None and self.autosave_enabled != self.current_scenario.autosave_enabled:
            self.current_scenario.autosave_enabled = not self.current_scenario.autosave_enabled

    def on_scenario_change(self):
        """Handle the scenario selection event."""
        if self.current_scenario is not None:
            self.current_scenario.stop()
            
        scenario_name = self.scenario_combo_box.currentText()
        self.scenario_label.setText(scenario_name)
        self.current_scenario = self.scenario_classes[scenario_name](self.scenario_input_layout)

    def setup_fullerenes(self):
        """Set up the Structure Of Fullerenes scenario."""
        from default_scenarios.fullerenes_structure import FullerenesStructureScenario
        self.current_scenario = FullerenesStructureScenario(self)

    def setup_portfolio(self):
        """Set up the Portfolio Optimization scenario."""
        from default_scenarios.portfolio_optimization import PortfolioOptimizationScenario
        self.current_scenario = PortfolioOptimizationScenario(self)

    def setup_gradient(self):
        """Set up the Gradient Descent scenario."""
        from default_scenarios.gradient_descent import GradientDescentScenario
        self.current_scenario = GradientDescentScenario(self)

    def toggle_dark_light_mode(self):
        """Toggle the dark/light mode."""
        if self.is_dark_mode:
            self.central_widget.setStyleSheet("background-color: white; color: black;")
            self.dark_light_mode_button.setToolTip("Turn on dark mode")
            self.statusBar().showMessage("Light mode enabled", 2000)
        else:
            self.central_widget.setStyleSheet("background-color: #2f2f2f; color: white;")
            self.dark_light_mode_button.setToolTip("Turn on light mode")
            self.statusBar().showMessage("Dark mode enabled", 2000)
        self.is_dark_mode = not self.is_dark_mode

    def toggle_autosave(self):
        """Toggle the autosave feature."""
        if self.autosave_enabled:
            self.autosave_button.setToolTip("Autosave is disabled")
            self.autosave_button.setStyleSheet("border: 2px solid transparent;")
            self.statusBar().showMessage("Autosave has been disabled", 2000)
        else:
            self.autosave_button.setToolTip("Autosave is enabled")
            self.autosave_button.setStyleSheet("border: 2px solid orange;")
            self.statusBar().showMessage("Autosave has been enabled", 2000)
        self.autosave_enabled = not self.autosave_enabled

    def help_button_clicked(self):
        """Create and show the help window."""
        scenario_name = self.scenario_combo_box.currentText()
        if scenario_name == "Gradient Descent":
            self.help_window = HelpWindowGradient(self)
        elif scenario_name == "Structure Of Fullerenes":
            self.help_window = HelpWindowFullerenes(self)
        elif scenario_name == "Portfolio Optimization":
            self.help_window = HelpWindowPortfolio(self)
        else:
            self.help_window = HelpWindowDefault(self)
        self.help_window.show()

