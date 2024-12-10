from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QColorDialog, QFileDialog,
    QVBoxLayout, QHBoxLayout, QWidget, QGroupBox, QLineEdit, QTableWidget, QTableWidgetItem,
    QMessageBox
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt
import sys
import pdfkit

# Global variables
templates = {
    "Template 1": """
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: {bg_color};
                color: {font_color};
            }}
            .invoice-container {{
                max-width: 800px;
                margin: 20px auto;
                padding: 20px;
                background: #ffffff;
                border: 1px solid #ddd;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                text-align: center;
                margin-bottom: 20px;
            }}
            .header h1 {{
                margin: 0;
                font-size: 24px;
            }}
            .header p {{
                margin: 5px 0 0;
                font-size: 14px;
                color: #666;
            }}
            .items th {{
                background-color: {table_heading_color};
                color: #ffffff;
            }}
        </style>
    </head>
    <body>
        <div class="invoice-container">
            <div class="header">
                <h1>Invoice</h1>
                <p>Thank you for doing business with us!</p>
            </div>
            <table class="items" border="1" width="100%">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Item</th>
                        <th>Qty</th>
                        <th>Price</th>
                    </tr>
                </thead>
                <tbody>
                    {services}
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """,
    "Template 2": """
    <html>
    <head>
      <style>
        body {{
            background-color: {bg_color};
            color: {font_color};
            font-family: Verdana, sans-serif;
        }}
        .header {{
            text-align: center;
            margin: 20px;
        }}
        .header h1 {{
            font-size: 32px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th {{
            background-color: {table_heading_color};
            color: white;
            padding: 10px;
        }}
        td {{
            padding: 10px;
            text-align: center;
        }}
      </style>
    </head>
    <body>
        <div class="header">
            <h1>Invoice</h1>
            <p>Template 2 Preview</p>
        </div>
        <table border="1">
            <thead>
                <tr>
                    <th>#</th>
                    <th>Description</th>
                    <th>Price</th>
                </tr>
            </thead>
            <tbody>
                {services}
            </tbody>
        </table>
    </body>
    </html>
    """
}


class BillingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.selected_template = "Template 1"
        self.selected_bg_color = "#ffffff"
        self.selected_font_color = "#000000"
        self.selected_table_heading_color = "#333333"
        self.services = []  # List to store the added services
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Billing Software")

        # Main layout
        central_widget = QWidget()
        main_layout = QVBoxLayout()

        # Template selection
        template_group = QGroupBox("Select Template")
        template_layout = QHBoxLayout()
        for template_name in templates.keys():
            button = QPushButton(template_name)
            button.clicked.connect(lambda _, name=template_name: self.select_template(name))
            template_layout.addWidget(button)
        template_group.setLayout(template_layout)
        main_layout.addWidget(template_group)

        self.template_label = QLabel("Selected Template: Template 1")
        main_layout.addWidget(self.template_label)

        # Color selection
        self.add_color_selection(main_layout)

        # Input for services
        self.add_service_input(main_layout)

        # Web preview
        self.web_preview = QWebEngineView()
        self.update_preview()
        main_layout.addWidget(self.web_preview)

        # Generate PDF button
        generate_button = QPushButton("Generate PDF")
        generate_button.clicked.connect(self.generate_pdf)
        main_layout.addWidget(generate_button)

        # Set the main layout
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def add_color_selection(self, layout):
        # Font color selection
        font_color_group = QGroupBox("Select Font Color")
        font_color_layout = QHBoxLayout()
        self.font_color_button = QPushButton("Select Font Color")
        self.font_color_button.clicked.connect(self.select_font_color)
        font_color_layout.addWidget(self.font_color_button)
        font_color_group.setLayout(font_color_layout)
        layout.addWidget(font_color_group)

        # Table heading color selection
        table_heading_color_group = QGroupBox("Select Table Heading Color")
        table_heading_color_layout = QHBoxLayout()
        self.table_heading_color_button = QPushButton("Select Table Heading Color")
        self.table_heading_color_button.clicked.connect(self.select_table_heading_color)
        table_heading_color_layout.addWidget(self.table_heading_color_button)
        table_heading_color_group.setLayout(table_heading_color_layout)
        layout.addWidget(table_heading_color_group)

    def add_service_input(self, layout):
        service_group = QGroupBox("Add Service")
        service_layout = QVBoxLayout()

        # Input fields
        self.service_name_input = QLineEdit()
        self.service_name_input.setPlaceholderText("Service Name")
        service_layout.addWidget(self.service_name_input)

        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Quantity")
        service_layout.addWidget(self.quantity_input)

        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Price")
        service_layout.addWidget(self.price_input)

        # Button to add service
        add_service_button = QPushButton("Add Service")
        add_service_button.clicked.connect(self.add_service)
        service_layout.addWidget(add_service_button)

        service_group.setLayout(service_layout)
        layout.addWidget(service_group)

    def add_service(self):
        service_name = self.service_name_input.text()
        quantity = self.quantity_input.text()
        price = self.price_input.text()

        if not service_name or not quantity or not price:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")
            return

        try:
            quantity = int(quantity)
            price = float(price)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Quantity must be an integer and Price must be a number.")
            return

        service_row = f"<tr><td>{len(self.services) + 1}</td><td>{service_name}</td><td>{quantity}</td><td>${price}</td></tr>"
        self.services.append(service_row)

        # Clear input fields
        self.service_name_input.clear()
        self.quantity_input.clear()
        self.price_input.clear()

        # Update the preview with the new service
        self.update_preview()

    def select_template(self, template_name):
        self.selected_template = template_name
        self.template_label.setText(f"Selected Template: {template_name}")
        self.update_preview()

    def select_font_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.selected_font_color = color.name()
            self.update_preview()

    def select_table_heading_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.selected_table_heading_color = color.name()
            self.update_preview()

    def update_preview(self):
        services_html = ''.join(self.services)
        html_content = templates[self.selected_template].format(
            bg_color=self.selected_bg_color,
            font_color=self.selected_font_color,
            table_heading_color=self.selected_table_heading_color,
            services=services_html
        )
        self.web_preview.setHtml(html_content)

    def generate_pdf(self):
        services_html = ''.join(self.services)
        html_content = templates[self.selected_template].format(
            bg_color=self.selected_bg_color,
            font_color=self.selected_font_color,
            table_heading_color=self.selected_table_heading_color,
            services=services_html
        )
        save_path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "", "PDF files (*.pdf)")
        if save_path:
            try:
                pdfkit.from_string(html_content, save_path)
                QMessageBox.information(self, "Success", f"PDF saved to {save_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save PDF: {str(e)}")


def main():
    app = QApplication(sys.argv)
    window = BillingApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
