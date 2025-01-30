from abc import ABC, abstractmethod

class Scenario(ABC):
    """Abstract class for a scenario."""
    def __init__(self, layout):
        self.layout = layout
        self.clear_layout()
    
    @abstractmethod
    def adjust_layout(self):
        """Adjust the layout of the scenario."""
        pass

    @abstractmethod
    def run(self):
        """Run the scenario."""
        pass
    
    @abstractmethod
    def stop(self):
        """Stop the scenario."""
        pass

    def clear_layout(self):
        """Clear all widgets and layouts in the current layout."""
        for i in reversed(range(self.layout.count())):
            item = self.layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout_of_nested(item.layout())
                item.layout().deleteLater()

    def clear_layout_of_nested(self, layout):
        """Recursively clear all widgets and layouts in a nested layout."""
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout_of_nested(item.layout())
                item.layout().deleteLater()