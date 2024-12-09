def set_fullerenes_view(self):
    """Set the view for the Structure Of Fullerenes scenario."""
    self.setWindowTitle("Structure Of Fullerenes")    

    # tracks option changes in the combo box
    self.combo_box.currentTextChanged.connect(self.on_scenario_change)
