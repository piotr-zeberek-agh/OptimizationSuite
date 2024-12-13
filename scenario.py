from abc import ABC, abstractmethod

class Scenario(ABC):
    def __init__(self, layout):
        self.layout = layout
    
    @abstractmethod
    def adjust_layout(self):
        pass
    
    @abstractmethod
    def run(self):
        pass
    
    def clear_layout(self):
        """Clear all widgets in the current layout."""
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
    
    