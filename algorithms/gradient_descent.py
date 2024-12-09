from PyQt6.QtWidgets import QPushButton

def set_gradient_descent_view(window):
    """Set the view for the Gradient Descent scenario."""
    window.setWindowTitle("Gradient Descent")

    # create table for variables
    window.table_widget.clear()
    window.table_widget.setColumnCount(2)
    window.table_widget.setHorizontalHeaderLabels(["Variable Name", "Value"])
    window.table_widget.setRowCount(3)

    save_button = QPushButton("Save variables")
    save_button.clicked.connect(lambda: save_variables(window))
    window.layout.addWidget(save_button)

    load_button = QPushButton("Load variables")
    load_button.clicked.connect(lambda: load_variables(window))
    window.layout.addWidget(load_button)

def save_variables(window):
    variables = {}
    try:
        for row in range(window.table_widget.rowCount()):
            var_name_item = window.table_widget.item(row, 0)
            var_value_item = window.table_widget.item(row, 1)

            if not var_name_item or not var_name_item.text():
                break

            var_name = var_name_item.text()
            var_value = float(var_value_item.text()) if var_value_item else 0.0

            if var_name not in variables:
                variables[var_name] = var_value
        
        window.text_box.setText(repr(variables))
    except Exception as e:
        print(f"Error saving variables: {e}")

def load_variables(window):
    print("Load variables")