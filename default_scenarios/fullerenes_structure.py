from scenario import Scenario
from PyQt6.QtWidgets import QPushButton, QTableWidget

class FullerenesStructureScenario(Scenario):
    def __init__(self, layout):
        super().__init__(layout)

        self.adjust_layout()

    def adjust_layout(self):
        """Set the view for the Structure of Fullerenes scenario"""
        # self.window.tit("Gradient Descent")

        # create table for variables
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["Variable Name", "Value"])
        self.table_widget.setRowCount(6)

        self.layout.addWidget(self.table_widget)


    def adjust_layout(self):
        # Implementacja dopasowania layoutu
        pass

    def run(self):
        # Implementacja logiki scenariusza
        pass