from pdfViewer import PDFViewer
from viewer import View
import sys
import random
import string
import os
import pdfkit
import webbrowser
import tempfile
import fitz  # PyMuPDF
import dns.resolver
from PyQt5.QtWidgets import QColorDialog, QFrame, QGraphicsScene,  QGraphicsView, QScrollArea, QMainWindow, QPushButton, QComboBox, QListWidget, QMessageBox, QHBoxLayout, QCheckBox ,    QApplication, QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit,QDialog
import phonenumbers
from phonenumbers import parse, is_valid_number, geocoder, carrier, NumberParseException
from email_validator import validate_email, EmailNotValidError
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5.QtGui import QColor
from PyQt5.QtWebEngineWidgets import QWebEngineView
import smtplib
import json
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import sys
import random
import string
import subprocess
import os
import re
import pdfkit
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QListWidget, QMessageBox, QHBoxLayout, QCheckBox,QDateEdit
)
from PyQt5.QtGui import QIcon, QPixmap, QImage, QFont
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtCore import Qt, QUrl
import smtplib
import json
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from num2words import num2words
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtGui import QRegExpValidator, QDoubleValidator

class ZoomableLabel(QLabel):
    def __init__(self, text=""):
        super().__init__(text)
        self.setAlignment(Qt.AlignCenter)
        self.setFixedSize(350, 420)
        self.setStyleSheet("border: 1px solid black; background-color: white;")
        self.setFont(QFont("Arial", 10))  # Set initial font size
    
    def wheelEvent(self, event):
        delta = event.angleDelta().y()  # Get the scroll amount
        current_font = self.font()
        font_size = current_font.pointSize()
        
        # Zoom in (wheel up) or zoom out (wheel down)
        if delta > 0:
            new_font_size = font_size + 1  # Increase font size
        else:
            new_font_size = max(5, font_size - 1)  # Decrease font size, but don't go below 5
        
        # Apply the new font size
        current_font.setPointSize(new_font_size)
        self.setFont(current_font)


class SecondUI(QWidget):
    global balance_in_words , total_installments ,total_receive,selected_template
    selected_template="Template 1"
    balance_in_words=0
    total_receive=0.00
    total_installments=0
    fontColorHex="#000000"
    tableHeaderFontColorHex="#000000"
    tableHeaderColorHex="#c700ff"
    hexCode="#ffffff"
    def __init__(self, address, name, contact_number, email):
        self.services_info = []
        self.total_discounted_price = 0.00
        super().__init__()

        

        # Store passed data
        self.address = address
        self.name = name
        self.contact_number = contact_number
        self.email = email

        self.services = {
                "Web Development": {
                    "Select": [
                        
                    ],
                    "On Demand": [
                        "₹2000", "₹5000", "₹10000", "₹20000"
                    ],
                    "Static": [
                        "Basic - ₹5999", "Standard - ₹8999", "Premium - ₹10999"
                    ],
                    "Dynamic": [
                        "Basic - ₹24999", "Standard - ₹44999", "Premium - ₹74999"
                    ],
                    "E-Commerce": [
                        "Basic - ₹24999", "Standard - ₹44999", "Premium - ₹74999"
                    ]
                },
                "Mobile App Development": {
                    "Select": [
                        
                    ],
                    "On Demand": [
                        "₹50000"
                    ],
                    "Basic": [
                        "₹100000"
                    ],
                    "Standard": [
                        "₹350000"
                    ],
                    "Premium": [
                        "₹550000"
                    ],
                    "Premium Pro": [
                        "₹850000"
                    ]
                },
                "Software Development": {
                    "Select": [
                        
                    ],
                    "On Demand": [
                        "₹10000","₹20000","₹30000"
                    ],
                    "Basic": [
                        "₹40000","₹45000"
                    ],
                    "Standard": [
                        "₹500000","₹60000","₹70000"
                    ],
                    "Premium": [
                        "₹80000","₹90000"
                    ],
                    "Premium Pro": [
                        "₹1000000"
                    ]
                },
                "Domain": {
                    "Select": [
                        
                    ],
                    "Basic": [
                        "₹2000"
                    ],
                    "Standard": [
                        "₹4000"
                    ]
                },
                "Hosting": {
                    "Select": [
                        
                    ],
                    "On Demand": [
                        "₹1000","₹2000","₹5000","₹8000","₹10000"
                    ],
                    "Starter": [
                        "12 months - ₹1788", "24 months - ₹2856", "36 months - ₹2844", "60 months - ₹4740"
                    ],
                    "Economy": [
                        "1 month - ₹549", "12 months - ₹3948", "24 months - ₹6456", "36 months - ₹7164"
                    ]
                },
                "Graphic Design": {
                    "Select": [
                        
                    ],
                    "Logo": [
                        "₹2000", "₹4000", "₹6000", "₹6000", "₹10000"
                    ],
                    "Banner": [
                        "₹1000"
                    ],
                    "Bill": [
                        "₹500"
                    ],
                    "Visiting Card": [
                        "₹500"
                    ],
                    "Brochure": [
                        "₹2000"
                    ],
                    "Company Profile": [
                        "₹2000"
                    ],
                    "Pamphlet": [
                        "₹500"
                    ],
                    "Package": [
                        "Logo + Bill + Banner + Visiting Card + Brochure + Company Profile - ₹6000"
                    ]
                },
                "Ecommerce Listing": {
                    "Select": [
                        
                    ],
                    "5 Products": [
                        "₹4999"
                    ],
                    "10 Products": [
                        "₹10999"
                    ]
                },
                "Google Listing": {
                    "Select": [
                        
                    ],
                    "Listing": [
                        "₹2499"
                    ],
                    "Google Product Listing": [
                        "₹2499"
                    ]
                },
                "SEO": {
                    "Select": [
                        
                    ],
                    "Organic": [
                        "₹10000"
                    ],
                    "Paid": [
                        "₹10000"
                    ]
                },
                "Email": {
                    "Select": [
                        
                    ],
                    "Per Email basic": [
                        "₹99"
                    ],
                    "Per Email standard": [
                        "₹199"
                    ]
                },
                "Security": {
                    "Select": [
                        
                    ],
                    "SSL Certificate Yearly": [
                        "₹5999"
                    ],
                    "Web Security": [
                        "Contact for Price"
                    ]
                },
            }
            
            
        
        self.discount_options = [str(i) for i in range(0, 101)]
        
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Geek Thrive Billing Software")
        self.setFixedSize(700, 700)  # Increased height for new field

        # Main Layout
        self.main_layout = QVBoxLayout()

        layout = QVBoxLayout()

        # Create a horizontal layout for the Advance Received field
        advance_layout = QHBoxLayout()

        # Advance Received Input Field
        self.advance_received_input = QLineEdit()
        self.advance_received_input.setPlaceholderText("Enter Advance Received Amount")
        self.advance_received_input.setValidator(QDoubleValidator(0.99, 99999.99, 2))

        # Set a fixed width for the Advance Received input field
        self.advance_received_input.setFixedWidth(350)  # Adjust width as needeed

        # Add the label and input field to the horizontal layout
        advance_layout.addWidget(QLabel("Advance Received:"))
        advance_layout.addWidget(self.advance_received_input)

        # Add the horizontal layout to the main layout
        layout.addLayout(advance_layout)

       # Create a horizontal layout for Service and Plan Dropdowns
        service_plan_layout = QHBoxLayout()


        # Service Dropdown
        self.service_combo = QComboBox()
        self.service_combo.addItems(self.services.keys())
        self.service_combo.currentTextChanged.connect(self.update_plan_combo)
        service_plan_layout.addWidget(QLabel("Select Service:"))
        service_plan_layout.addWidget(self.service_combo)

        
        # Plan Dropdown
        self.plan_combo = QComboBox()
        self.plan_combo.currentTextChanged.connect(self.update_pricing_combo)
        service_plan_layout.addWidget(QLabel("Select Plan:"))
        service_plan_layout.addWidget(self.plan_combo)

        # Pricing Dropdown
        self.price_combo = QComboBox()
        service_plan_layout.addWidget(QLabel("Select Pricing:"))
        service_plan_layout.addWidget(self.price_combo)

        # Add the horizontal layout to the main layout
        layout.addLayout(service_plan_layout)


        # Create a horizontal layout for Discount Amount Input, Checkbox, and Service Discount Combo
        discount_layout = QHBoxLayout()

        # Editable Discounted Amount Input
        self.discounted_amount_input = QLineEdit()
        self.discounted_amount_input.setPlaceholderText("Enter Discounted Amount")
        self.discounted_amount_input.setValidator(QDoubleValidator(0.99, 99999.99, 2))
        self.discounted_amount_input.setEnabled(False)  # Disable by default
        discount_layout.addWidget(self.discounted_amount_input)

        # Checkbox to enable discounted amount input
        self.enable_discount_checkbox = QCheckBox("Enable Discounted Amount")
        self.enable_discount_checkbox.stateChanged.connect(self.toggle_discount_options)
        discount_layout.addWidget(self.enable_discount_checkbox)

        # Discount for specific service
        self.service_discount_combo = QComboBox()
        self.service_discount_combo.addItems([str(d) for d in self.discount_options])
        self.service_discount_combo.setEnabled(False)  # Enabled by default
        discount_layout.addWidget(QLabel("Select Service Discount (%):"))
        discount_layout.addWidget(self.service_discount_combo)

        # Checkbox to enable the service discount combo
        self.enable_service_discount_checkbox = QCheckBox("Enable Service Discount")
        self.enable_service_discount_checkbox.stateChanged.connect(self.toggle_discount_options)
        discount_layout.addWidget(self.enable_service_discount_checkbox)

        # Custom Amount Input
        self.custom_amount_input = QLineEdit()
        self.custom_amount_input.setPlaceholderText("Enter Custom Discount Amount")
        self.custom_amount_input.setValidator(QDoubleValidator(0.99, 99999.99, 2))
        self.custom_amount_input.setEnabled(False)  # Disable by default
        discount_layout.addWidget(self.custom_amount_input)

        # Checkbox to enable the custom amount input
        self.enable_custom_amount_checkbox = QCheckBox("Enable Custom Amount")
        self.enable_custom_amount_checkbox.stateChanged.connect(self.toggle_discount_options)
        discount_layout.addWidget(self.enable_custom_amount_checkbox)


        # Add the horizontal layout to the main layout
        layout.addLayout(discount_layout)
        

        # Create a horizontal layout for Service List and Buttons (Left side)
        left_layout = QVBoxLayout()

        # Service List and Buttons
        left_layout.addWidget(QLabel("Added Services:"))
        self.selected_services_list = QListWidget()
        left_layout.addWidget(self.selected_services_list)

        # Add and Delete Service Buttons
        service_button_layout = QHBoxLayout()
        self.add_service_button = QPushButton("Add Service")
        self.add_service_button.clicked.connect(self.add_service)
        service_button_layout.addWidget(self.add_service_button)

        self.delete_service_button = QPushButton("Delete Service")
        self.delete_service_button.clicked.connect(self.delete_service)
        service_button_layout.addWidget(self.delete_service_button)

        left_layout.addLayout(service_button_layout)

        # Create a horizontal layout for Installment Entry Section (Right side)
        # right_layout = QVBoxLayout()

        # Create a horizontal layout for the Installment Amount, Select Date, and Add Installment button
        installment_layout = QHBoxLayout()

        # Installment Amount Input
        self.installment_input = QLineEdit()
        self.installment_input.setPlaceholderText("Enter Installment Amount")

        # Date input for installment
        self.installment_date_input = QDateEdit()
        self.installment_date_input.setDisplayFormat("dd-MM-yy")  # Set date format
        self.installment_date_input.setCalendarPopup(True)  # Enable calendar popup
        self.installment_date_input.setDate(QDate.currentDate())  # Set current date as default

        # Add Installment Button
        self.add_installment_button = QPushButton("Add")
        self.add_installment_button.clicked.connect(self.add_installment)

        # Delete Installment Button
        self.delete_installment_button = QPushButton("Delete")
        self.delete_installment_button.clicked.connect(self.delete_installment)


        # Add widgets to the horizontal layout
        installment_layout.addWidget(self.installment_input)  # Installment Amount
        installment_layout.addWidget(self.installment_date_input)  # Select Date
        installment_layout.addWidget(self.add_installment_button)  # Add Installment Button
        installment_layout.addWidget(self.delete_installment_button)  # Delete Installment Button


        # Installment List
        self.installment_list = QListWidget()

        # Add everything to the right_layout
        left_layout.addWidget(QLabel("Installments Received:"))
        left_layout.addLayout(installment_layout)  # Add the horizontal layout
        left_layout.addWidget(self.installment_list)

        # Create a horizontal layout for Template and Color Selection (Right side)
        template_layout = QVBoxLayout()

        # Template Selection ComboBox
        self.template_combo = QComboBox()
        self.template_combo.addItems(["Template 1", "Template 2", "Template 3", "Template 4", "Template 5"])
        self.template_combo.currentTextChanged.connect(self.update_template)
        template_layout.addWidget(QLabel("Select Template:"))
        template_layout.addWidget(self.template_combo)

        # Color Picker Button
        # self.color_button = QPushButton("Pick Template Color")
        # self.color_button.clicked.connect(self.select_color)
        # template_layout.addWidget(self.color_button)

        # Font Color Picker Button
        self.font_color_button = QPushButton("Pick Font Color")
        self.font_color_button.clicked.connect(self.select_font_color)
        template_layout.addWidget(self.font_color_button)

        # Table Heading Color Picker Button
        self.table_heading_color_button = QPushButton("Pick Table Heading Color")
        self.table_heading_color_button.clicked.connect(self.select_table_heading_color)
        template_layout.addWidget(self.table_heading_color_button)


        # Table Heading Text Color Picker Button
        self.table_heading_text_color_button = QPushButton("Pick Table Heading Text Color")
        self.table_heading_text_color_button.clicked.connect(self.select_table_heading_text_color)
        template_layout.addWidget(self.table_heading_text_color_button)

        # Template Preview Label
        self.template_preview_label = ZoomableLabel("Template Preview will be shown here.")
        self.template_preview_label.setAlignment(Qt.AlignCenter)
        self.template_preview_label.setFixedSize(350, 420)
        self.template_preview_label.setStyleSheet("border: 1px solid black; background-color: white;")
        template_layout.addWidget(self.template_preview_label)

        # Add Template options to the right layout
        right_layout = QVBoxLayout()
        right_layout.addLayout(template_layout)

        # Create a horizontal layout for the left and right sections
        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout)  # Left layout (Services)
        main_layout.addLayout(right_layout)  # Right layout (Installments)


        # Add main layout to the window
        layout.addLayout(main_layout)

        # Add labels for dynamic data display
        self.address_label = QLabel(f"Address: {self.address}", self)
        self.name_label = QLabel(f"Name: {self.name}", self)
        self.contact_label = QLabel(f"Contact: {self.contact_number}", self)
        self.emai_label = QLabel(f"Email: {self.email}", self)


        # Add labels to the layout
        layout.addWidget(self.address_label)
        layout.addWidget(self.name_label)
        layout.addWidget(self.contact_label)
        layout.addWidget(self.emai_label)



        # GST Checkbox
        self.gst_checkbox = QCheckBox("Apply 18% GST")
        layout.addWidget(self.gst_checkbox)

        # Amount labels
        self.subtotal_label = QLabel("Subtotal: ₹0.00")
        self.discount_amount_label = QLabel("Discount Amount: ₹0.00")
        self.cgst_amount_label = QLabel("CGST Amount: ₹0.00")
        self.sgst_amount_label = QLabel("SGST Amount: ₹0.00")
        self.total_label = QLabel("Total Amount: ₹0.00")
        self.balance_label = QLabel("Balance: ₹0.00")
        self.total_installments_label = QLabel("Total Installments Received: ₹0.00")
        
        layout.addWidget(self.subtotal_label)
        layout.addWidget(self.discount_amount_label)
        layout.addWidget(self.cgst_amount_label)
        layout.addWidget(self.sgst_amount_label)
        layout.addWidget(self.total_label)
        layout.addWidget(self.balance_label)
        layout.addWidget(self.total_installments_label)

        # Buttons and Share Option Dropdown in a single layout
        button_layout = QHBoxLayout()

        # Calculate Total Button
        calculate_button = QPushButton("Calculate Total")
        calculate_button.clicked.connect(self.calculate_total)
        button_layout.addWidget(calculate_button)

        # Generate Invoice Button
        generate_invoice_button = QPushButton("Preview")
        generate_invoice_button.clicked.connect(self.generate_invoice)
        button_layout.addWidget(generate_invoice_button)

        # Generate Invoice Button
        generate_invoice_button = QPushButton("Live Preview")
        generate_invoice_button.clicked.connect(self.generate_invoice)
        button_layout.addWidget(generate_invoice_button)
        
        

        # # Generate Quotation Button
        # generate_quotation_button = QPushButton("Generate Quotation")
        # generate_quotation_button.clicked.connect(self.generate_quotation)
        # button_layout.addWidget(generate_quotation_button)

        # Share Option Dropdown
        self.share_option_combo = QComboBox()
        self.share_option_combo.addItems(["Select Share Option", "Email", "WhatsApp"])
        button_layout.addWidget(self.share_option_combo)

        # Share Button
        self.share_button = QPushButton("Share")
        self.share_button.clicked.connect(self.share)
        button_layout.addWidget(self.share_button)

        # Exit Button (to redirect to login)
        self.exit_button = QPushButton("Logout")
        self.exit_button.clicked.connect(self.exit_application)
        button_layout.addWidget(self.exit_button)

        button_layout.addStretch()
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Initialize the plan and pricing dropdowns using the currently selected service
        self.update_plan_combo(self.service_combo.currentText())

        # List to store installment due dates
        self.installment_due_dates = []


    def update_template(self, template_name):
        """Update template preview based on selection"""
        selected_template = self.template_combo.currentText()  # Get the selected template
        print(selected_template, "SELECTED TEMPLATE IS THIS ")
        if selected_template == "Template 1":
            self.apply_template_1()
        elif selected_template == "Template 2":
            self.apply_template_2()
        elif selected_template == "Template 3":
            self.apply_template_3()
        elif selected_template == "Template 4":
            self.apply_template_4()
        elif selected_template == "Template 5":
            self.apply_template_5()

    def apply_template_1(self):
        """Apply template 1 style"""
        html_content = """
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Invoice</title>
        <style>
            body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            background-color: #f5f5f5;
            }
            .invoice-container {
            max-width: 350px; /* Adjusted for smaller screen */
            margin: 8px auto;
            border: 1px solid #ddd;
            padding: 10px;
            background-color: #fff;
            font-size: 10px; /* Reduced font size */
            }
            .header {
            text-align: center;
            margin-bottom: 10px;
            }
            .header h1 {
            font-size: 18px; /* Reduced header font size */
            letter-spacing: 1px;
            }
            .details {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            }
            .details div {
            font-size: 10px;
            }
            .details div p {
            margin: 2px 0;
            }
            .invoice-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 10px;
            }
            .invoice-table th,
            .invoice-table td {
            border: 1px solid #ddd;
            padding: 5px; /* Reduced padding */
            text-align: center;
            }
            .invoice-table th {
            background-color: #f8f8f8;
            }
            .total {
            text-align: right;
            font-size: 14px;
            font-weight: bold;
            }
            .footer {
            margin-top: 10px;
            font-size: 10px; /* Reduced footer font size */
            }
            .footer .signature {
            text-align: right;
            margin-top: 20px;
            }
            .footer .signature span {
            display: block;
            font-size: 9px;
            }
            .design {
            position: absolute;
            width: 30px;
            height: 30px;
            background-color: teal;
            top: 0;
            right: 0;
            z-index: -1;
            }
            .design-bottom {
            position: absolute;
            width: 30px;
            height: 30px;
            background-color: pink;
            bottom: 0;
            left: 0;
            z-index: -1;
            }
        </style>
        </head>
        <body>
        <div class="invoice-container">
            <div class="design"></div>
            <div class="design-bottom"></div>
            <div class="header">
            <h1>INVOICE</h1>
            </div>
            <div class="details">
            <div>
                <p><strong>Date Issued:</strong> 01 January 2030</p>
                <p><strong>Invoice No:</strong> 01234</p>
            </div>
            <div>
                <p><strong>Issued to:</strong></p>
                <p>Sacha Dubois</p>
                <p>123 Anywhere St, Any City, ST 12345</p>
            </div>
            </div>
            <table class="invoice-table">
            <thead>
                <tr>
                <th>Item Name</th>
                    <th>Description</th>
                    <th>Rate</th>
                    <th>Discount</th>
                    <th>Amount</th>
                </tr>
            """
         # Loop through the services_info list to add each service to the template
        for index, service in enumerate(self.services_info, start=1):
            html_content += f"""
                <tr>
                    <td>{service['service']}</td>
                    <td>{service['plan']}</td>
                    <td>₹{service['base_price']}</td>
                    <td>{service['discount_percentage']}%</td>
                    <td>₹{service['discounted_price']:.2f}</td>
                </tr>
            """

        html_content += """
            </table>
            
            <div class="total">GRAND TOTAL: $300</div>
            <div class="footer">
            <p><strong>Note:</strong></p>
            <p>Bank Name: Riberio</p>
            <p>Account No: 0123 4567 8901</p>
            <div class="signature">
                <p>Claudia</p>
                <span>Finance Manager</span>
            </div>
            </div>
        </div>
        </body>
        </html>

        """
        self.template_preview_label.setText(html_content)
        self.template_preview_label.setStyleSheet("background-color: lightblue; border: 1px solid black;")

    # def apply_template_2(self):
    #     """Apply template 2 style"""
    #     html_content = """
    #     <html>
    #     <head>
    #         <style>
    #             body {
    #                 font-family: Arial, sans-serif;
    #                 color: #333;
    #                 margin: 0;
    #                 padding: 7px;
    #                 width: 500px;  /* Set the overall width */
    #                 height: auto;  /* Adjust height as needed */
    #                 margin-left: auto;
    #                 margin-right: auto;

    #             }
    #             .invoice-header {
    #                 text-align: center;
    #                 margin-bottom: 10px;
    #             }
    #             .invoice-header h1 {
    #                 color: black;
    #                 font-size: 18px;  
    #             }
    #             .company-details {
    #                 text-align: left;
    #                 font-size: 10px;
    #                 margin-bottom: 10px;
    #             }
    #             table {
    #                 width: 100%;
    #                 border-collapse: collapse;
    #                 margin-top: 20px;
    #             }
    #             th, td {
    #                 border: 1px solid #000;
    #                 padding: 6px;
    #                 text-align: left;
    #                 font-size: 10px;
    #             }
    #             th {
    #                 background-color: #9400ff;
    #                 color: #fff;
    #             }
    #             .totals {
    #                 margin-top: 20px;
    #                 width: 50%;
    #                 float: right;
    #                 border-collapse: collapse;
    #             }
    #             .totals td {
    #                 border: 1px solid #000;
    #                 padding: 6px;
    #             }
    #             .totals tr:nth-child(1) td {
    #                 font-weight: bold;
    #             }
    #             .signature-section {
    #                 text-align: right;
    #                 margin-top: 20px;
    #             }
    #             .signature-section img {
    #                 height: 40px;
    #             }
    #             .footer {
    #                 text-align: center;
    #                 font-size: 3px;
    #                 margin-top: 5px;
    #             }
    #         </style>
    #     </head>
    #     <body>
    #         <div class="invoice-header">
    #             <h1>Invoice</h1>
    #             <p>Invoice No: ZSK5TYWIRE</p>
    #             <p>Date: 22/11/24</p>
    #         </div>
    #         <div class="company-details">
    #             <p>Company/Seller Name: Geek Thrive</p>
    #             <p>Address: 23 GGRA CHAND ROAD KOL-14</p>
    #             <p>Phone No.: 6261384312</p>
    #             <p>Email ID: support@geekthrive.com</p>
    #         </div>
    #         <table>
    #             <tr>
    #                 <th>Item Name</th>
    #                 <th>Description</th>
    #                 <th>Rate</th>
    #                 <th>Discount</th>
    #                 <th>Amount</th>
    #             </tr>
    #     """

    #     # Loop through the services_info list to add each service to the template
    #     for index, service in enumerate(self.services_info, start=1):
    #         html_content += f"""
    #             <tr>
    #                 <td>{service['service']}</td>
    #                 <td>{service['plan']}</td>
    #                 <td>₹{service['base_price']}</td>
    #                 <td>{service['discount_percentage']}%</td>
    #                 <td>₹{service['discounted_price']:.2f}</td>
    #             </tr>
    #         """

    #     html_content += """
    #         </table>
    #         <table class="totals">
    #             <tr>
    #                 <td>Total:</td>
    #                 <td>₹2000.00</td>
    #             </tr>
    #             <tr>
    #                 <td>Received:</td>
    #                 <td>₹0.00</td>
    #             </tr>
    #             <tr>
    #                 <td>Balance:</td>
    #                 <td>₹0.00</td>
    #             </tr>
    #             <tr>
    #                 <td><strong>Grand Total:</strong></td>
    #                 <td><strong>₹2000.00</strong></td>
    #             </tr>
    #         </table>
    #         <div class="signature-section">
    #             <p>For <strong>Geek Thrive</strong></p>
    #             <img src="signature.png" alt="Signature">
    #             <p>Authorized Signature</p>
    #         </div>
    #         <div class="footer">
    #             <p>Amount in words: Zero rupees only</p>
    #             <p>Thank you for choosing Geek Thrive for your business.</p>
    #         </div>
    #     </body>
    #     </html>
    #     """

    #     self.template_preview_label.setText(html_content)
    #     self.template_preview_label.setStyleSheet("background-color: beige; border: 1px solid black;")

    def apply_template_2(self):
        """Apply template 2 style with dynamic color selection"""
        # Retrieve selected colors or set defaults
        font_color = getattr(self, 'font_color', '#333')  # Default text color
        table_heading_color = getattr(self, 'table_heading_color', '#9400ff')  # Default table heading background color
        table_heading_text_color = getattr(self, 'table_heading_text_color', '#fff')  # Default heading text color
        

        html_content = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    color: {font_color};
                    margin: 0;
                    padding: 7px;
                    width: 500px;
                    height: auto;
                    margin-left: auto;
                    margin-right: auto;
                }}
                .invoice-header {{
                    text-align: center;
                    margin-bottom: 10px;
                }}
                .invoice-header h1 {{
                    color: black;
                    font-size: 18px;
                }}
                .company-details {{
                    text-align: left;
                    font-size: 10px;
                    margin-bottom: 10px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }}
                th, td {{
                    border: 1px solid #000;
                    padding: 6px;
                    text-align: left;
                    font-size: 10px;
                }}
                th {{
                    background-color: {table_heading_color};
                    color: {table_heading_text_color};
                }}
                .totals {{
                    margin-top: 20px;
                    width: 50%;
                    float: right;
                    border-collapse: collapse;
                }}
                .totals td {{
                    border: 1px solid #000;
                    padding: 6px;
                }}
                .totals tr:nth-child(1) td {{
                    font-weight: bold;
                }}
                .signature-section {{
                    text-align: right;
                    margin-top: 20px;
                }}
                .signature-section img {{
                    height: 40px;
                }}
                .footer {{
                    text-align: center;
                    font-size: 3px;
                    margin-top: 5px;
                }}
                .items{{
                    color: {font_color};
                }}
            </style>
        </head>
        <body>
            <div class="company-details" style="position:relative">
            <tableclass="header-table" style="width: 100%; border-collapse: collapse;">
            <tr>
            <td style="border: none;">
                <strong>Company/Seller Name: Geek Thrive</strong><br>
                            Address: 23 GORA CHAND ROAD KOL-14<br>
                            Phone No.: 6291843612<br>
                            Email ID: support@geekthrive.com<br>
            </td>
            </tr>
            </table>
            </div>
            
        """

        # Check if services_info exists and create a table if necessary
        if not self.services_info:
            # No services info, create a default table structure
            html_content += """
            <table>
                <tr>
                    <th>Item Name</th>
                    <th>Description</th>
                    <th>Rate</th>
                    <th>Discount</th>
                    <th>Amount</th>
                </tr>
                <tr>
                    <td>Example Item</td>
                    <td>Example Description</td>
                    <td>₹100.00</td>
                    <td>0%</td>
                    <td>₹100.00</td>
                </tr>
            </table>
            """
        else:
            # Add rows for existing services
            html_content += """
            <table>
                <tr class="items">
                    <th>Item Name</th>
                    <th>Description</th>
                    <th>Rate</th>
                    <th>Discount</th>
                    <th>Amount</th>
                </tr>
            """
            for index, service in enumerate(self.services_info, start=1):
                html_content += f"""
                    <tr>
                        <td>{service['service']}</td>
                        <td>{service['plan']}</td>
                        <td>₹{service['base_price']}</td>
                        <td>{service['discount_percentage']}%</td>
                        <td>₹{service['discounted_price']:.2f}</td>
                    </tr>
                """
            html_content += "</table>"

        # Add totals, signature section, and footer
        html_content += """
            <table class="totals">
                <tr>
                    <td>Total:</td>
                    <td>₹0.00</td>
                </tr>
                <tr>
                    <td>Received:</td>
                    <td>₹0.00</td>
                </tr>
                <tr>
                    <td>Balance:</td>
                    <td>₹0.00</td>
                </tr>
                <tr>
                    <td><strong>Grand Total:</strong></td>
                    <td><strong>₹0.00</strong></td>
                </tr>
            </table>
            <div class="signature-section">
                <img src="signature.png" alt="Signature">
                <p>Authorized Signature</p>
            </div>
            <div class="footer">
                <p>Amount in words: Zero rupees only</p>
                <p>Thank you for choosing Geek Thrive for your business.</p>
            </div>
        </body>
        </html>
        """

        # Update the preview label with the generated HTML
        self.template_preview_label.setText(html_content)
        self.template_preview_label.setStyleSheet("background-color: beige; border: 1px solid black;")


    def apply_template_3(self):
        """Apply template 3 style"""

        html_content = """
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Invoice</title>
        <style>
            body {
            font-family: Arial, sans-serif;
            font-size: 10px; /* Smaller base font size */
            margin: 0;
            padding: 0;
            background-color: #f9f9f9;
            }
            .invoice-container {
            max-width: 600px; /* Smaller container width */
            margin: 30px auto; /* Reduced margin */
            background: #fff;
            padding: 15px; /* Reduced padding */
            box-shadow: 0 0 8px rgba(0, 0, 0, 0.1);
            }
            .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px; /* Reduced spacing */
            }
            .header h1 {
            font-size: 18px; /* Smaller title font size */
            margin: 0;
            }
            .company-info {
            text-align: right;
            }
            .company-info h2 {
            margin: 0;
            font-size: 14px; /* Smaller font */
            }
            .company-info p {
            margin: 0;
            font-size: 10px; /* Smaller font */
            color: #555;
            }
            .invoice-to, .total-due {
            margin-bottom: 10px; /* Smaller spacing */
            }
            .invoice-to p, .total-due p {
            margin: 3px 0; /* Reduced paragraph spacing */
            }
            .invoice-details {
            margin: 15px 0; /* Reduced spacing */
            }
            .invoice-details table {
            width: 100%;
            border-collapse: collapse;
            }
            .invoice-details th, .invoice-details td {
            text-align: left;
            padding: 8px; /* Reduced padding */
            border: 1px solid #ddd;
            }
            .invoice-details th {
            background: #f4f4f4;
            }
            .total-section {
            text-align: right;
            margin-top: 15px; /* Reduced spacing */
            font-size:10px;
            }
            .total-section h3 {
            margin: 0;
            font-size: 8px; /* Smaller total font size */
            }
            .payment-method {
            margin-top: 10px; /* Reduced spacing */
            font-size: 10px; /* Smaller font */
            }
            .footer {
            margin-top: 20px; /* Reduced spacing */
            text-align: center;
            font-size: 10px; /* Smaller font */
            color: #555;
            }
            .footer p {
            margin: 3px 0; /* Reduced paragraph spacing */
            }
        </style>
        </head>
        <body>
        <div class="invoice-container">
            <div class="header">
            <div>
                <h1>INVOICE</h1>
            </div>
            <div class="company-info">
                <h2>Paucek and Lage</h2>
                <p>Your Business Partner</p>
            </div>
            </div>

            <div class="invoice-to">
            <p><strong>Invoice To:</strong> Marcellino Anderson</p>
            <p>P: +123-456-7890</p>
            <p>E: hello@example.com</p>
            <p>A: 123 Anywhere St, Any City, ST, 12345</p>
            </div>

            <div class="total-due">
            <p><strong>Total Due:</strong> <span>USD $12345</span></p>
            <p>Invoice No: 1234567890</p>
            <p>Date: 01/01/2023</p>
            </div>

            <div class="invoice-details">
            <table>
                <thead>
                <tr>
                    <th>Item Name</th>
                    <th>Description</th>
                    <th>Rate</th>
                    <th>Discount</th>
                    <th>Amount</th>
                </tr>
                """
        # Loop through the services_info list to add each service to the template
        for index, service in enumerate(self.services_info, start=1):
            html_content += f"""
                <tr>
                    <td>{service['service']}</td>
                    <td>{service['plan']}</td>
                    <td>₹{service['base_price']}</td>
                    <td>{service['discount_percentage']}%</td>
                    <td>₹{service['discounted_price']:.2f}</td>
                </tr>
            """

        html_content += """
            </table>
            </div>

            <div class="total-section">
            <h3>Subtotal: 0</h3>
            <h3>Tax (15%): 0</h3>
            <h3><strong>Total:0</strong></h3>
            </div>

            <div class="payment-method">
            <p><strong>Payment Method:</strong></p>
            <p>Bank Name: Francisco Andrade</p>
            <p>Bank Account: 1234567890</p>
            </div>

            <div class="footer">
            <p>Thank you for your purchase!</p>
            <p>Drew Feig</p>
            <p>Administrator</p>
            </div>
        </div>
        </body>
        </html>

        """
        self.template_preview_label.setText(html_content)
        self.template_preview_label.setStyleSheet("background-color: lightgray; border: 1px solid black;")


    def apply_template_4(self):
        invoice_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        total_amount = float(self.total_label.text().split("₹")[1])
        
        if(balance_in_words != None):
            total_amount_in_words = num2words(balance_in_words).title() 
        amount_received = float(self.advance_received_input.text() or 0)
        balance = float(self.balance_label.text().split("₹")[1])
        sub_total = float(self.subtotal_label.text().split("₹")[1])
        
        # Get the relative path to wkhtmltopdf
        current_directory = os.path.dirname(os.path.abspath(__file__))
        wkhtmltopdf_path = os.path.join(current_directory, 'wkhtmltopdf', 'bin', 'wkhtmltopdf.exe')

        # Set the PDFKit configuration with the correct wkhtmltopdf path
        self.pdfkit_config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)


        # Get the client details
        address = self.address
        name = self.name
        contact_number = self.contact_number
        current_date = QDate.currentDate().toString("dd/MM/yy")

        # Get the base path for the logo
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))

        logo_path = os.path.join(base_path, 'images', 'LOGO1.png')
        scanner_path = os.path.join(base_path, 'images', 'scanner.jpeg')
        signature_path = os.path.join(base_path, 'images', 'signature.png')

        # List of services and amounts
        selected_services = []
        for i in range(self.selected_services_list.count()):
            item_text = self.selected_services_list.item(i).text()
            parts = item_text.split(": ")
            if len(parts) >= 2:
                service = parts[0].strip()
                plan_info = parts[1]
                plan_parts = plan_info.split(" - ")
                plan_description = plan_parts[0].strip()
                amount_str = plan_parts[-1].strip()
                amounts = re.findall(r'\d+', amount_str)
                amount = int(amounts[0]) if amounts else 0
                selected_services.append((service, plan_description, amount))

        # Calculate totals
        total_service_amount = sum(amount for _, _, amount in selected_services)
        discount_rate = float(self.service_discount_combo.currentText()) / 100
        discount_amount = total_service_amount * discount_rate
        total_after_discount = total_service_amount - discount_amount

        # GST logic
        gst_applicable = self.gst_checkbox.isChecked()
        cgst_amount = float(self.cgst_amount_label.text().split("₹")[1]) if gst_applicable else 0.0
        sgst_amount = float(self.sgst_amount_label.text().split("₹")[1]) if gst_applicable else 0.0

        font_color = getattr(self, 'font_color', '#333')  # Default text color
        table_heading_color = getattr(self, 'table_heading_color', '#9400ff')  # Default table heading background color
        table_heading_text_color = getattr(self, 'table_heading_text_color', '#fff')  # Default heading text color

        selected_color = SecondUI.hexCode

        html_content = f"""
        <html>
        <head>
            <title>Tax Invoice</title>
            <style>
                @media print {{
                    body, .container {{
                        width: 793px;
                        height: 2500px;
                        margin: 0;
                        padding: 0;
                        page-break-before: always;
                    }}
                    .container {{
                        border: 1px solid #000;
                        padding: 20px;
                        box-sizing: border-box;
                        display: flex;
                        flex-direction: column;
                        justify-content: space-between;
                    }}
                }}
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #fff;
                }}
                .container {{
                    width: 893px;
                    height: auto;
                    margin: 0 auto;
                    padding: 20px;
                    border: 1px solid #000;
                    box-sizing: border-box;
                    display: flex;
                    flex-direction: column;
                    justify-content: space-between;
                    page-break-after: always;
                }}
                .header, .footer {{
                    text-align: center;
                }}
                .header h1 {{
                    background-color: #d3aefc;
                    padding: 10px;
                    font-size: 24px;
                }}
                .items th {{
                    background-color: {table_heading_color};
                }}
                .items, .summary, .installments {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                .items th, .items td, .summary td, .installments td {{
                    border: 1px solid #000;
                    padding: 8px;
                }}
                .items .description {{
                    text-align: left;
                }}
                .summary {{
                    margin-left: 60%;
                }}
                .summary td {{
                    text-align: right;
                    padding-right: 68px;
                }}
                .summary .label {{
                    text-align: left;
                }}
                .Signature {{
                    text-align: right;
                    font-weight: bold;
                }}
                .footer {{
                    margin-top: 20px;
                    text-align: center;
                    font-size: 15px;
                }}
                .fix {{
                    height: 350px;
                    width: 100%;
                    display: flex;
                }}
            </style>
        </head>
        <body>
        """

        # Replace `{table_heading_color}` with the actual color value
        html_content = html_content.replace("{table_heading_color}", table_heading_color)

        # Invoice Header
        html_content += f"""
        <div class="container">
            <table class="header-table" style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="border: none;">
                        <strong>Company/Seller Name: Geek Thrive</strong><br>
                        Address: 23 GORA CHAND ROAD KOL-14<br>
                        Phone No.: 6291843612<br>
                        Email ID: support@geekthrive.com<br>
                    </td>
                    <td style="border: none; position: absolute; left: 46%; top: 2%; ">
                        <img src="{logo_path}" alt="Company Logo" style="height: 80px;">
                    </td>
                    <td style="border: none; text-align: right;">
                        <img src="{scanner_path}" alt="Scanner Logo" style="height: 80px;">
                    </td>
                </tr>
            </table>
            <br>
            <h1 style="text-align: center">{"Tax Invoice" if gst_applicable else "Invoice"}</h1><br>
            <table class="details" style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td>
                        <strong>Billed To:</strong><br>
                        Name: {name}<br>
                        Address: {address}<br>
                        Contact No.: {contact_number}<br>
                    </td>
                    <td>
                        <strong>Shipping To:</strong><br>
                        Name: {name}<br>
                        Address: {address}<br>
                        Contact No.: {contact_number}
                    </td>
                    <td>
                        <strong>Invoice No.:</strong> {invoice_number}<br>
                        <strong>Date:</strong> {current_date}
                    </td>
                </tr>
            </table>
            <br>
            <div class="fix">
                <table class="items" style="width: 100%; border-collapse: collapse;">
                    <tr>
                        <th style="width: 5%;">Sl</th>
                        <th style="width: 25%;">Item Name</th>
                        <th style="width: 30%;">Description</th>
                        <th style="width: 10%;">Rate</th>
                        <th style="width: 15%;">Discount</th>
                        <th style="width: 15%;">Amount</th>
                    </tr>
        """

        # Adding items for the invoice
        sl_number = 1  # Start serial number from 1
        for service in self.services_info:
            if service["discount_percentage"] > 0:
                html_content += f"""
                <tr style="text-align: center;">
                    <td>{sl_number}</td>
                    <td>{service["service_name"]}</td>
                    <td>{service["plan"]}</td>
                    <td>&#8377;{service["base_price"]}</td>
                    <td>0</td>
                    <td>&#8377;{service["base_price"]}</td>
                </tr>
                """
            sl_number += 1

        html_content += f"""
            </table>
        </div>
        <br>
        """

        # Return the final HTML content
        self.template_preview_label.setText(html_content)
        self.template_preview_label.setStyleSheet("background-color: lightgray; border: 1px solid black;")



    # def select_color(self):
    #     """Open color dialog and update template preview color"""
    #     color = QColorDialog.getColor()
    #     if color.isValid():
    #         color_hex = color.name()
    #         print(f"Selected color: {color_hex}")
    #         self.update_color(color)

    def select_color(self):
        """Open color dialog, update template preview, and store the color."""
        # Open the color dialog and get the selected color
        color = QColorDialog.getColor()

        if color.isValid():
            # Get the hex color code (e.g., #RRGGBB)
            color_hex = color.name()

            # Update the color preview label (this is your template preview)
            self.template_preview_label.setStyleSheet(f"background-color: {color_hex};")

            # Store the selected color in a global variable for use in HTML template
            
            SecondUI.hexCode = color_hex
            print(f"Selected color: {SecondUI.hexCode}")
            return color_hex

    def select_font_color(self):
        """Open a color dialog to select font color."""
        color = QColorDialog.getColor()
        
        if color.isValid():
            self.font_color = color.name()  # Save the selected font color
            SecondUI.fontColorHex = self.font_color
        print(f"Selected font color: {SecondUI.fontColorHex}")
        self.update_template(selected_template)

    def select_table_heading_color(self):
        """Open a color dialog to select the table heading color."""
        color = QColorDialog.getColor()
        
        if color.isValid():
            self.table_heading_color = color.name()  # Save the selected table heading color
            SecondUI.tableHeaderColorHex = self.table_heading_color
        print(f"Selected table heading color: {SecondUI.tableHeaderColorHex}")
        self.update_template(selected_template)


    def select_table_heading_text_color(self):
        """Open a color dialog to select the table heading text color."""
        color = QColorDialog.getColor()
        
        if color.isValid():
            self.table_heading_text_color = color.name()  # Save the selected table heading text color
            SecondUI.tableHeaderFontColorHex = self.table_heading_text_color
        print(f"Selected table heading text color: {SecondUI.tableHeaderFontColorHex}")
        self.update_template(selected_template)            

    def update_color(self, color):
        """Update preview color"""
        self.template_preview_label.setStyleSheet(f"background-color: {color.name()}; border: 1px solid black;")
        self.update_template(selected_template)

    def validate_amount(self):
        amount = self.amount_received_input.text()
        if not amount or float(amount) <= 0:
            self.display_error("Invalid amount. Please enter a positive number.")
        else:
            self.clear_error()

    def display_error(self, message):
        # Create a simple popup or error label to display the error
        self.error_label = QLabel(message)
        self.error_label.setStyleSheet("color: red;")
        self.layout().addWidget(self.error_label)

    def clear_error(self):
        if hasattr(self, 'error_label'):
            self.error_label.clear()

    def exit_application(self):
        # Optionally, confirm with the user before logging out
        reply = QMessageBox.question(self, "Logout", "Are you sure you want to logout?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # Close the current window
            self.close()

            # Import the login script and open the login page
            # import login  # Import the login script
            # self.login_window = login.login_page()  # Assuming login_page is the class in login.py
            # self.login_window.show()
            
    def on_focus_out(self, event):
        email = self.email_entry.text()
        validate_email(email)
        QLineEdit.focusOutEvent(self.email_entry, event)  # Call the original focusOut event

    def toggle_discount_options(self):
        """
        Ensures only one checkbox can be ticked at a time. 
        Ticking a checkbox enables its corresponding input and disables the other two.
        """
        sender = self.sender()  # Get the checkbox that triggered the event

        if sender == self.enable_discount_checkbox:
            if self.enable_discount_checkbox.isChecked():
                # Enable discounted amount, disable the other two
                self.discounted_amount_input.setEnabled(True)
                self.enable_service_discount_checkbox.setChecked(False)
                self.enable_custom_amount_checkbox.setChecked(False)
                self.service_discount_combo.setEnabled(False)
                self.custom_amount_input.setEnabled(False)
            else:
                # Disable discounted amount if unchecked
                self.discounted_amount_input.setEnabled(False)

        elif sender == self.enable_service_discount_checkbox:
            if self.enable_service_discount_checkbox.isChecked():
                # Enable service discount, disable the other two
                self.service_discount_combo.setEnabled(True)
                self.enable_discount_checkbox.setChecked(False)
                self.enable_custom_amount_checkbox.setChecked(False)
                self.discounted_amount_input.setEnabled(False)
                self.custom_amount_input.setEnabled(False)
            else:
                # Disable service discount if unchecked
                self.service_discount_combo.setEnabled(False)

        elif sender == self.enable_custom_amount_checkbox:
            if self.enable_custom_amount_checkbox.isChecked():
                # Enable custom amount, disable the other two
                self.custom_amount_input.setEnabled(True)
                self.enable_discount_checkbox.setChecked(False)
                self.enable_service_discount_checkbox.setChecked(False)
                self.discounted_amount_input.setEnabled(False)
                self.service_discount_combo.setEnabled(False)
            else:
                # Disable custom amount if unchecked
                self.custom_amount_input.setEnabled(False)

    def delete_service(self):
        selected_item = self.selected_services_list.currentItem()
        if selected_item:
            # Find and remove the item from the UI list
            row = self.selected_services_list.row(selected_item)
            self.selected_services_list.takeItem(row)

            # Extract the text of the selected item
            selected_item_text = selected_item.text()

            # Find and remove the corresponding entry from the services_info list
            for service in self.services_info:
                service_text = (f"{service['service']}: {service['plan']} - ₹{service['base_price']} "
                                f"Discount: {service['discount_percentage']}% (₹{service['discount_amount']:.2f}) "
                                f"- Discounted ₹{service['discounted_price']:.2f}")
                service_text= service_text.replace("Discount: 0% (₹0.00) - Discounted" , "-")
                print(service_text ," <--2--> ", selected_item_text)
                if (service_text == selected_item_text):
                    print("before removal" , service)
                    self.services_info.remove(service)
                    print("after removal" , self.services_info)
                    break
                
                print (len(self.services_info))

            # Update the total_discounted_price after deletion
            self.total_discounted_price -= service['discounted_price']
            print(f"Updated total discounted price: {self.total_discounted_price}")
            self.update_template(selected_template)



    def update_plan_combo(self, service):
        self.plan_combo.clear()  # Clear existing items
        self.plan_combo.addItems(self.services[service].keys())  # Add plans for selected service
        self.price_combo.clear()  # Clear pricing when service changes
        self.discounted_amount_input.clear()  # Clear discounted amount input

    def update_pricing_combo(self, plan):
        service = self.service_combo.currentText()
        self.price_combo.clear()  # Clear existing prices
        if service in self.services and plan in self.services[service]:
            self.price_combo.addItems(self.services[service][plan])  # Add prices for selected plan
            # Set the discounted amount input to the selected price by default
            if self.price_combo.count() > 0:
                selected_price_text = self.price_combo.currentText()
                match = re.search(r"₹(\d+)", selected_price_text)
                if match:
                    base_price = int(match.group(1))
                    # Set the discounted amount input to the base price if not already filled
                    if not self.discounted_amount_input.text():
                        self.discounted_amount_input.setText(str(base_price))

    def add_service(self):
        selected_service = self.service_combo.currentText()
        selected_plan = self.plan_combo.currentText()
        selected_discount = int(self.service_discount_combo.currentText() or 0)
        selected_price_text = self.price_combo.currentText()

        if selected_price_text:
            match = re.search(r"₹(\d+)", selected_price_text)
            if match:
                base_price = int(match.group(1))

                # If custom amount checkbox is selected, override the price with the custom amount
                if self.enable_custom_amount_checkbox.isChecked():
                    custom_amount = self.custom_amount_input.text()
                    if custom_amount:
                        try:
                            discounted_price = float(custom_amount)  # Set custom amount as the final price
                            # No discount calculations will be made when using custom amount
                            discount_amount = 0
                            discount_percentage = 0
                        except ValueError:
                            QMessageBox.warning(self, "Input Error", "Please enter a valid custom amount.")
                            return
                    else:
                        QMessageBox.warning(self, "Input Error", "Custom amount cannot be empty.")
                        return
                else:

                    if self.enable_discount_checkbox.isChecked():
                        discounted_price = float(self.discounted_amount_input.text() or base_price)
                    else:
                        discount_amount = (selected_discount / 100) * base_price
                        discounted_price = base_price - discount_amount

                 # If custom amount is used, skip displaying the discount
                if self.enable_custom_amount_checkbox.isChecked():
                    item_text = (f"{selected_service}: {selected_plan} - ₹{discounted_price:.2f}")
                else:

                    discount_amount = base_price - discounted_price
                    discount_percentage = int((discount_amount / base_price) * 100) if base_price > 0 else 0
                    print(" discount",discount_percentage) 
                    

                    if discount_percentage > 0:
                        item_text = (f"{selected_service}: {selected_plan} - ₹{base_price} "
                                    f"Discount: {discount_percentage}% (₹{discount_amount:.2f}) "
                                    f"- Discounted ₹{discounted_price:.2f}")
                        
                    else:
                        item_text = (f"{selected_service}: {selected_plan} - ₹{base_price} "
                                    f"- ₹{discounted_price:.2f}")
                # Update the selected services list
                # self.selected_services_list.addItem(item_text)

                global discounted_percentage
                global discount_price
                global discounted_amount

                self.discounted_percentage= discount_percentage
                print(self.discounted_percentage)
                self.discount_price= discounted_price
                self.discounted_amount= discount_amount

                # Add the current discounted_price to total_discounted_price
                self.total_discounted_price += discounted_price

                self.selected_services_list.addItem(item_text)
                # Track this service's discount values locally
                service_info = {
                    "service": selected_service,
                    "plan": selected_plan,
                    "base_price": base_price,
                    "discount_percentage": discount_percentage,
                    "discount_amount": discount_amount,
                    "discounted_price": discounted_price
                }

                # Add this service's info to a list for later use (if needed)
                self.services_info.append(service_info)

                # Update HTML Template with New Service
                self.update_template(selected_template)

            else:
                QMessageBox.warning(self, "Input Error", "Could not find a valid price in the selected pricing.")
        else:
            QMessageBox.warning(self, "Selection Error", "Please select a pricing option.")
              
    def add_installment(self):
        installment_amount = self.installment_input.text()
        installment_date = self.installment_date_input.date().toString("dd-MM-yy")  # Get date in string format
        if installment_amount:
            self.installment_list.addItem(f"₹{installment_amount} Paid on {installment_date}")  # Add date to the list item
            self.installment_due_dates.append(installment_date)  # Store the due date
            self.installment_input.clear()  # Clear the input after adding
        else:
            QMessageBox.warning(self, "Input Error", "Please enter a valid installment amount.")
        self.update_template(selected_template)

        
    
    def delete_installment(self):
        # Get the selected item in the installment list
        selected_item = self.installment_list.currentItem()

        if selected_item:
            # Remove the selected item from the list
            row = self.installment_list.row(selected_item)
            self.installment_list.takeItem(row)
        else:
            # Optionally, show a message if no item is selected
            QMessageBox.warning(self, "Warning", "Please select an installment to delete.")

            self.update_template(selected_template)

        

    def calculate_total(self):
        try:
            subtotal = 0
            for i in range(self.selected_services_list.count()):
                item_text = self.selected_services_list.item(i).text()
                # Check if the service has a custom amount (Custom amount services won't have discounts)
                if "Discounted ₹" in item_text:
                    match = re.search(r"Discounted ₹(\d+(\.\d{1,2})?)", item_text)
                    if match:
                        amount = float(match.group(1))
                        subtotal += amount
                    else:
                        QMessageBox.warning(self, "Parse Error", "Could not find discounted amount in item text.")
                        return
                    
                # If the item has a custom amount, we don't apply any discount, just use the entered price
                elif "₹" in item_text:  # Check if item has ₹ symbol, implying it's a valid price format
                    match = re.search(r"₹(\d+(\.\d{1,2})?)", item_text)
                    if match:
                        # Extract custom price and add to subtotal
                        amount = float(match.group(1))
                        subtotal += amount
                    else:
                        QMessageBox.warning(self, "Parse Error", "Could not find valid price in item text.")
                        return
        
            # Calculate the discount
            discount_percentage = int(self.service_discount_combo.currentText() or 0)
            discount_amount = (discount_percentage / 100) * subtotal
            discounted_total = subtotal - discount_amount
            
            # Calculate GST
            gst_amount = 0
            if self.gst_checkbox.isChecked():
                gst_amount = discounted_total * 0.18
                
            cgst_amount = gst_amount / 2
            sgst_amount = gst_amount / 2
            total_amount = discounted_total + gst_amount
            print(total_amount)
            
            # Calculate total received and balance
            total_received = 0
            for i in range(self.installment_list.count()):
                print(self.installment_list.item(i).text())
                item_text = self.installment_list.item(i).text()
                match = re.search(r"₹(\d+(\.\d{1,2})?)", item_text)
                if match:
                    amount = int(match.group(1))
                    total_received += amount
            global total_installments
            total_installments = total_received
            print(total_installments,"total installment")
            advance_received = float(self.advance_received_input.text() or 0)
            
            global total_receive
            total_received += advance_received
            total_receive= total_received

            global balance_in_words
    
            balance = total_amount - total_received
            balance_in_words =balance
            # Update labels
            self.subtotal_label.setText(f"Subtotal: ₹ {subtotal:.2f}")
            self.discount_amount_label.setText(f"Discount Amount: ₹ {discount_amount:.2f}")
            self.cgst_amount_label.setText(f"CGST Amount: ₹ {cgst_amount:.2f}")
            self.sgst_amount_label.setText(f"SGST Amount: ₹ {sgst_amount:.2f}")
            self.total_label.setText(f"Total Amount: ₹ {total_amount:.2f}")
            self.balance_label.setText(f"Balance: ₹ {balance:.2f}")
            self.total_installments_label.setText(f"Total Installments Received: ₹ {total_installments:.2f}")
    
        except ValueError as e:
            QMessageBox.warning(self, "Input Error", str(e))
   
    def generate_invoice(self):
        invoice_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        total_amount = float(self.total_label.text().split("₹")[1])
        
        if(balance_in_words != None):
            total_amount_in_words = num2words(balance_in_words).title() 
        amount_received = float(self.advance_received_input.text() or 0)
        balance = float(self.balance_label.text().split("₹")[1])
        sub_total = float(self.subtotal_label.text().split("₹")[1])
        
        # Get the relative path to wkhtmltopdf
        current_directory = os.path.dirname(os.path.abspath(__file__))
        wkhtmltopdf_path = os.path.join(current_directory, 'wkhtmltopdf', 'bin', 'wkhtmltopdf.exe')

        # Set the PDFKit configuration with the correct wkhtmltopdf path
        self.pdfkit_config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)


        # Get the client details
        address = self.address
        name = self.name
        contact_number = self.contact_number
        current_date = QDate.currentDate().toString("dd/MM/yy")

        # Get the base path for the logo
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))

        logo_path = os.path.join(base_path, 'images', 'LOGO1.png')
        scanner_path = os.path.join(base_path, 'images', 'scanner.jpeg')
        signature_path = os.path.join(base_path, 'images', 'signature.png')

        # List of services and amounts
        selected_services = []
        for i in range(self.selected_services_list.count()):
            item_text = self.selected_services_list.item(i).text()
            parts = item_text.split(": ")
            if len(parts) >= 2:
                service = parts[0].strip()
                plan_info = parts[1]
                plan_parts = plan_info.split(" - ")
                plan_description = plan_parts[0].strip()
                amount_str = plan_parts[-1].strip()
                amounts = re.findall(r'\d+', amount_str)
                amount = int(amounts[0]) if amounts else 0
                selected_services.append((service, plan_description, amount))
                #print(selected_services)

        # Calculate totals
        total_service_amount = sum(amount for _, _, amount in selected_services)
        discount_rate = float(self.service_discount_combo.currentText()) / 100
        discount_amount = total_service_amount * discount_rate
        total_after_discount = total_service_amount - discount_amount

        # GST logic
        gst_applicable = self.gst_checkbox.isChecked()
        cgst_amount = float(self.cgst_amount_label.text().split("₹")[1]) if gst_applicable else 0.0
        sgst_amount = float(self.sgst_amount_label.text().split("₹")[1]) if gst_applicable else 0.0

        # Ensure self.selected_color has a valid value
        # if not hasattr(self, 'selected_color') or not self.selected_color:
        #     print("Color not selected or variable not set.")
        #     self.selected_color = "#ff0000"  # Set a fallback color (e.g., white)
        #selected_color= "#c700ff"

        font_color = SecondUI.fontColorHex
        selected_color = SecondUI.hexCode
        table_heading_color = SecondUI.tableHeaderColorHex
        table_heading_text_color = SecondUI.tableHeaderFontColorHex

        # Start generating HTML content for the invoice
        html_content = """
        <html>
        <head>
            <title>Tax Invoice</title>
            <style>
                @media print {{
                    body, .container {{
                        width: 793px;
                        height: 2500px;
                        margin: 0;
                        padding: 0;
                        page-break-before: always;
                        color: {font_color};
                        background-color: white;
                    }}
                    .container {{
                        border: 1px solid #000;
                        padding: 20px;
                        box-sizing: border-box;
                        display: flex;
                        flex-direction: column;
                        justify-content: space-between;
                    }}
                }}
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #fff;
                    color: {font_color};
                    background-color: white;
                }}
                .container {{
                    width: 893px;
                    height: auto;
                    margin: 0 auto;
                    padding: 20px;
                    border: 1px solid #000;
                    box-sizing: border-box;
                    display: flex;
                    flex-direction: column;
                    justify-content: space-between;
                    page-break-after: always;
                }}
                .header, .footer {{
                    text-align: center;
                }}
                .header h1 {{
                    background-color: #d3aefc;
                    padding: 10px;
                    font-size: 24px;
                }}
                .items th {{
                    background-color: {table_heading_color};
                    color: {table_heading_text_color};
                }}
                .items, .summary, .installments {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                .items th, .items td, .summary td, .installments td {{
                    border: 1px solid #000;
                    padding: 8px;
                }}
                .items .description {{
                    text-align: left;
                }}
                .summary {{
                    margin-left: 60%;
                }}
                .summary td {{
                    text-align: right;
                    padding-right: 68px;
                }}
                .summary .label {{
                    text-align: left;
                }}
                .Signature {{
                    text-align: right;
                    font-weight: bold;
                }}
                
                .footer {{
                    margin-top: 20px;
                    text-align: center;
                    font-size: 15px;
                }}
                .fix {{
                    height: 350px;
                    width: 100%;
                    display: flex;
                }}
            </style>
        </head>
        <body>
        """
        # Replace `{selected_color}` with the actual color value
        # html_content = html_content.format(selected_color=selected_color)
        html_content = html_content.format(selected_color=selected_color, font_color=font_color, table_heading_color=table_heading_color, table_heading_text_color=table_heading_text_color)

        sl_number = 1  # Start serial number from 1
        # Splitting services into pages of 8 items each
        for page_number, start_idx in enumerate(range(0, len(self.services_info), 8)):
            page_services = self.services_info[start_idx:start_idx + 8]
            
            html_content += f"""
            <div class="container" style="position:relative">
                <table class="header-table" style="width: 100%; border-collapse: collapse;">
                    <tr>
                        <td style="border: none;">
                            <strong>Company/Seller Name: Geek Thrive</strong><br>
                            Address: 23 GORA CHAND ROAD KOL-14<br>
                            Phone No.: 6291843612<br>
                            Email ID: support@geekthrive.com<br>
                        </td>
                        <td style="border: none; position: absolute; left: 46%; top: 2%; ">
                            <img src="{logo_path}" alt="Company Logo" style="height: 80px;">
                        </td>
                        <td style="border: none; text-align: right;">
                            <img src="{scanner_path}" alt="Company Logo" style="height: 80px;">
                        </td>
                    </tr>
                </table>
                <br>
                <h1 style="text-align: center">{"Tax Invoice" if gst_applicable else "Invoice"}</h1><br>
                <table class="details" style="width: 100%; border-collapse: collapse;">
                    <tr>
                        <td>
                            <strong>Billed To:</strong><br>
                            Name: {name} <br>
                            Address: {address}<br>
                            Contact No.: {contact_number}<br>
                        </td>
                        <td>
                            <strong>Shipping To:</strong><br>
                            Name: {name}<br>
                            Address: {address}<br>
                            Contact No.: {contact_number}
                        </td>
                        <td>
                            <strong>Invoice No.:</strong> {invoice_number}<br>
                            <strong>Date:</strong> {current_date}
                        </td>
                    </tr>
                </table>
                <br>
                <div class = "fix">
                <table class="items" style="width: 100%; border-collapse: collapse;">
                    <tr>
                        <th style="width: 5%;">Sl</th>
                        <th style="width: 25%;">Item Name</th>
                        <th style="width: 30%;">Description</th>
                        <th style="width: 10%;">Rate</th>
                        <th style="width: 15%;">Discount</th>
                        <th style="width: 15%;">Amount</th>
                    </tr>
            """

            
            item=0
            # Adding each service for this page
            
            for service_info in page_services:
                print("pgService",page_services)
                print(service_info)
                item+=1
                if service_info["discount_percentage"] > 0:
                    html_content += f"""
                        <tr style="text-align: center">
                            <td>{sl_number}</td>  <!-- Sl (Serial Number) -->
                            <td>{service_info["service"] or ""}</td>  <!-- Item Name (service) -->
                            <td>{service_info["plan"]or ""} ({service_info["discount_percentage"]or ""}% discount)</td>     <!-- Description (plan) -->
                            <td>&#8377;{service_info["base_price"]or ""}</td> <!-- Rate (base_price) -->
                            <td>&#8377;{service_info["discount_amount"] or 0:.2f}</td> <!-- Discount (discount_amount) -->
                            <td>&#8377;{service_info["discounted_price"] or 0:.2f}</td> <!-- Amount (discounted_price) -->            
                        </tr>
                    """
                else:  # No discount
                    html_content += f"""
                        <tr style="text-align: center">
                            <td>{sl_number}</td>  <!-- Sl (Serial Number) -->
                            <td>{service_info["service"]}</td>  <!-- Item Name (service) -->
                            <td>{service_info["plan"]}</td>     <!-- Description (plan) -->
                            <td>&#8377;{service_info["base_price"]}</td> <!-- Rate (base_price) -->
                            <td>&#8377;</td> <!-- Discount (no discount) -->
                            <td>&#8377;{service_info["discounted_price"]:.2f}</td> <!-- Amount (discounted_price) -->
                        </tr>
                    """
                sl_number += 1  # Increment serial number for next service

            switch_dict = {
                8: 7,
                7: 9,
                6: 11,
                5: 13,
                4: 15,
                3: 17,
                2: 19,
                1: 21,
                9: 7,
                10: 9,
                11: 11,
                12: 13,
                13: 15,
                14: 17,
                15: 19,
                16: 21,
                17: 7,
                18: 9,
                19: 11,
                20: 13,
                21: 15,
                22: 17,
                23: 19,
                24: 21
            }
            loopBr = switch_dict.get(item)
            print(loopBr)
            # Adding installments table
            html_content += """
                <table class="installments" style="width: 55%; border-collapse: collapse; border: 1px solid black;">
                    <tr>
                        <th style="width: 25%;">Installment Description</th>
                    </tr>
                  
                
            """
            if isinstance(loopBr, int) and loopBr > 0:
                html_content+=f'{"<br>" * loopBr}'
           
            

            # Initialize an empty list to hold all installment descriptions
            installments = []

            # Loop through the installments list
            for i in range(self.installment_list.count()):
                item_text = self.installment_list.item(i).text()
                
                if amount:
                    # Remove the ₹ symbol from the installment description
                    item_text_without_ruppee = item_text.replace("₹", "").strip()
                    
                    # Add the cleaned-up installment to the list
                    installments.append(item_text_without_ruppee)

            # Join all installments into a single string, separated by semicolons
            installments_str = " ; ".join(installments)

            # Add the combined string to a single table cell
            html_content += f"""
            <tr>
                <td>{installments_str or ""}</td>
            </tr>
              <tr>
                        <td><strong>Total : {total_installments or ""}/-</strong></td>
                    </tr>
            
            """

            html_content += "</table>"


            # Adding the summary to each page


            

            html_content += f"""
                </table>
                </div>
                """
                
            if not gst_applicable :
                print(gst_applicable )
                html_content += f"""
                <br><br><br>
                 <br><br>
                   
                """
                
            html_content += f"""
                <br><br><br>
                <table class="summary" style=" display: inline; width: 40%; border-collapse: collapse;">
                    <tr><td class="label"><strong>Total:</strong></td><td><strong>{self.total_discounted_price or 0  }</strong></td></tr>
                    {(f'<tr><td class="label">SGST:</td><td>{sgst_amount or 0:.2f  }</td></tr>' if gst_applicable else '')}
                    {(f'<tr><td class="label">CGST:</td><td>{cgst_amount or 0:.2f  }</td></tr>' if gst_applicable else '')}
                    <tr><td class="label">Received:</td><td>{total_receive or 0 }</td></tr>
                    <tr><td class="label">Balance:</td><td>{balance or 0  }</td></tr>
                    <tr><td class="label"><strong>Grand Total:</strong></td><td><strong>&#8377;{round(balance) or "" }/-</strong></td></tr>
                </table>
                <br><br>
                <br>
                <p><strong>Amount in words:</strong> {total_amount_in_words or "" } rupees only</p>
                <div class="Signature">
                    <p>For <strong>Geek Thrive</strong></p>
                    <img src="{signature_path}" alt="Signature" style="height: 60px;">
                    <p>Authorized Signature</p>
                </div>
                <div class="footer">
                    <br>
                    <p>Thank you for choosing Geek Thrive for your business. All payments must be completed before the final delivery of the product.</p>
                    </div>
                </div>
            </div>
            """
        html_content += "</body></html>"

        # Create a temporary file to store the generated PDF
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        temp_pdf_path = temp_file.name

        # Close the billing software window (SecondUi) before opening the PDF viewer
        self.close_billing_software()

        pdf_file = f"invoice_{invoice_number}.pdf"
        try:
            pdfkit.from_string(
                html_content,
                
                pdf_file,
                configuration=self.pdfkit_config,
                options={
                    'quiet': '',
                    'enable-local-file-access': '',
                    'no-stop-slow-scripts': '',
                    'debug-javascript': '',
                    'page-size': 'A4',
                    'margin-top': '10mm',
                    'margin-right': '10mm',
                    'margin-bottom': '10mm',
                    'margin-left': '10mm'
                }
            )

            global pdf_fileName
            pdf_path = f"{pdf_file}.pdf"
            pdf_fileName = pdf_file
    
            # Show information message with the path
            QMessageBox.information(self, "Invoice Generated", f"Invoice saved as: {pdf_path}\nYou can open it from the     file system.")
            
        

            # Create and show the PDF Viewer
            try:
                viewer = PDFViewer(pdf_file)
                print(viewer)
                self.showPdf(viewer)
            except Exception as e:
                QMessageBox.warning(self, "PDF Viewer Error", f"Could not display PDF: {e}")
                print(e)

            # Optionally, display a success message
            #self.show_invoice_generated_message(temp_pdf_path)
            
            #QMessageBox.information(self, "Invoice Generated", f"suman: {temp_pdf_path}\nYou can open it from the     file system.")
            
            # if(LivePreview):
            #     self.blank_box(viewer)
            # else:
            #View.showPdf(viewer)

        except Exception as e:
            QMessageBox.warning(self, "PDF Generation Error", str(e))

    
        
    def showPdf(self, viewer):
        main_window = QDialog()  # Create the dialog window

        main_window.setFixedSize(800, 700)  # Set the size of the window
        main_window.setWindowTitle("Invoice")  # Set the title of the window

        # Create a layout for the main window
        layout = QVBoxLayout()

        # Add the PDF viewer to the layout
        layout.addWidget(viewer)

        # Define the okay function to handle the Close button
        def okay():
            main_window.accept()  # Close the dialog
            PDFViewer.open(self)  # Call the PDFViewer.open() method

        # Add a Close button to the dialog
        close_button = QPushButton("Back")
        close_button.clicked.connect(okay)  # Connect the button to the okay function
        layout.addWidget(close_button)

        # Set the layout for the main window
        main_window.setLayout(layout)

        # Show the dialog
        main_window.exec_()

    def show_invoice_generated_message(self, pdf_path):
        """Show the invoice generated message."""
        # Create a message box
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(f"Invoice saved as: {pdf_path}\nYou can open it from the file system.")
        msg_box.setWindowTitle("Invoice Generated")
        msg_box.setStandardButtons(QMessageBox.Ok)

        # Set message box as non-blocking
        msg_box.setModal(False)

        # Show the message box asynchronously (non-blocking)
        msg_box.finished.connect(self.on_message_box_closed)
        msg_box.exec_()

    def on_message_box_closed(self):
        """Handle the event when the message box is closed."""
        # The PDF viewer window will remain open when the message box is closed.
        pass

    def close_billing_software(self):
        """Close the billing software (SecondUi)."""
        # Assuming SecondUi is the main window, use `close()` to close it
        self.close() 
    
    def generate_quotation(self):
        invoice_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        total_amount = float(self.total_label.text().split("₹")[1])
        total_amount_in_words = num2words(balance_in_words).title()
        amount_received = float(self.amount_received_input.text() or 0)
        balance = float(self.balance_label.text().split("₹")[1])
        sub_total = float(self.subtotal_label.text().split("₹")[1])
        
        # Get the relative path to wkhtmltopdf
        current_directory = os.path.dirname(os.path.abspath(__file__))
        wkhtmltopdf_path = os.path.join(current_directory, 'wkhtmltopdf', 'bin', 'wkhtmltopdf.exe')

        # Set the PDFKit configuration with the correct wkhtmltopdf path
        self.pdfkit_config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

        # Get client details
        address = self.address_input.text()
        name = self.name_input.text()
        contact_number = self.phone_input.text()
        current_date = QDate.currentDate().toString("dd/MM/yyyy")
    
        # Get the base path for the logo
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
    
        logo_path = os.path.join(base_path, 'images', 'LOGO1.png')
        scanner_path = os.path.join(base_path, 'images', 'scanner.jpeg')
        signnature_path = os.path.join(base_path, 'images', 'signature.png')
    
        # List of services and amounts
        selected_services = []

        for i in range(self.selected_services_list.count()):
            item_text = self.selected_services_list.item(i).text()
            print(item_text)
            
            # Split and handle the parts safely
            parts = item_text.split(": ")
            if len(parts) >= 2:
                service = parts[0].strip()  # The service name
                
                # Further split the plan info to separate description and amount
                plan =  parts[1].strip(": ")
                plan_parts = plan.split("-")
                plan_part = plan_parts[0]
                plan_info = parts[1].strip()  # Everything after ": "
                
                # Assuming the amount is at the end, we can use regex to find it
                amount_match = re.search(r'₹([\d,]+)', plan_info)
                if amount_match:
                    amount = int(amount_match.group(1).replace(',', ''))  # Convert found amount to int
                    # Now, we can get the plan description without the amount
                    plan_description = plan_info.replace(amount_match.group(0), '').strip()  # Remove amount to get         description
                else:
                    amount = 0  # Default value if no number is found
                    plan_description = plan_info.strip()  # If no amount, just keep the description
                
                selected_services.append((service, plan_part, amount))
                print(plan_parts)
            else:
                print(f"Unexpected item format: {item_text}")  # For debugging
            
        # Calculate totals
        total_service_amount = sum(amount for _, _, amount in selected_services)
        discount_rate = float(self.service_discount_combo.currentText()) / 100
        discount_amount = total_service_amount * discount_rate
        total_after_discount = total_service_amount - discount_amount
    
        # GST logic
        gst_applicable = self.gst_checkbox.isChecked()
        if gst_applicable:
            cgst_amount = float(self.cgst_amount_label.text().split("₹")[1])
            sgst_amount = float(self.sgst_amount_label.text().split("₹")[1])
        else:
            cgst_amount = sgst_amount = 0.0
    
        html_content = """
        <html>
        <head>
            <title>Tax Invoice</title>
            <style>
                @media print {
                    body, .container {
                        width: 793px; /* A4 width in pixels at 96 DPI */
                        height: 2500px; /* A4 height in pixels at 96 DPI */
                        margin: 0;
                        padding: 0;
                        page-break-before: always;
                    }
                    .container {
                        border: 1px solid #000; /* Fixed border for printing */
                        padding: 20px;
                        box-sizing: border-box;
                        display: flex;
                        flex-direction: column;
                        justify-content: space-between;
                    }
                }
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #fff;
                }

                .fix {
                    height: 300px;
                    width: 100%;

                    display: flex;
                }
                
                .container {
                    width: 893px; /* Fixed width for A4 size */
                    height: 1300px; /* Fixed height for A4 size */
                    margin: 0 auto;
                    padding: 20px;
                    border: 1px solid #000; /* Fixed border */
                    box-sizing: border-box;
                    display: flex;
                    flex-direction: column;
                    justify-content: space-between;
                    page-break-after: always;
                }
                .header, .footer {
                    text-align: center;
                }
                .header h1 {
                    background-color: #d3aefc;
                    padding: 10px;
                    font-size: 24px;
                }
                .items th {
                    background-color: #d3aefc;
                }
                .items, .summary {
                    width: 100%;
                    border-collapse: collapse;
                }
                .items th, .items td, .summary td {
                    border: 1px solid #000;
                    padding: 8px;
                }
                .items .description {
                    text-align: left;
                }
                .summary {
                    margin-left: 50%;
                }
                .summary td {
                    text-align: right;
                    padding-right: 68px;
                }
                .summary .label {
                    text-align: left;
                }
                .terms {
                    margin-top: 20px;
                }
                .Signature {
                    text-align: right;
                    font-weight: bold;
                }
                .footer {
                    margin-top: 20px;
                    text-align: center;
                    font-size: 15px;
                }
                .service{
                    text-align: center;
                }
                .fix {
                    height: 400px;
                    width: 100%;
                    display: flex;
                }

            </style>
        </head>
        <body>
        """
    
        for page_number, start_idx in enumerate(range(0, len(selected_services), 8)):
            page_services = selected_services[start_idx:start_idx + 8]
    
            html_content += f"""
            <div class="container" style="positional:relative">
                <table class="header-table" style="width: 100%; border-collapse: collapse;">
                    <tr>
                        <td style="border: none;">
                            <strong>Company/Seller Name: Geek Thrive</strong><br>
                            Address: 23 GORA CHAND ROAD KOL-14<br>
                            Phone No.: 6291843612<br>
                            Email ID: support@geekthrive.com<br>
                        </td>
                        <td style="border: none; position: absolute; left:46%; top:2%>
                            <img src="{logo_path}" alt="Company Logo" style="height: 80px;">
                        </td>
                        <td style="border: none; text-align: right;">
                            <img src="{scanner_path}" alt="Company Logo" style="height: 80px;">
                        </td>
                    </tr>
                </table>
                <br>
                <h1 style="text-align: center">Quotation</h1>
                <table class="details" style="width: 100%; border-collapse: collapse;"><br>
                    <tr>
                        <td>
                            <strong>Billed To:</strong><br>
                            Name: {name} <br>
                            Address: {address}<br>
                            Contact No.: {contact_number}<br>
                        </td>
                        <td>
                            <strong>Shipping To:</strong><br>
                            Name: {name}<br>
                            Address: {address}<br>
                            Contact No.: {contact_number}
                        </td>
                        <td>
                            <strong>Date:</strong> {current_date}
                        </td>
                    </tr>
                </table>
                <div class="fix">
                <table class="items" style="width: 100%; border-collapse: collapse;">
                    <tr>
                        <th style="width: 5%;">Sl</th>
                        <th style="width: 25%;">Item Name</th>
                        <th style="width: 30%;">Description</th>
                        <th style="width: 10%;">Rate</th>
                        <th style="width: 15%;">Discount</th>
                        <th style="width: 15%;">Amount</th>
                    </tr>
                    <br><br>.
            """
    
            # Adding each service for this page
            sl_number = 1  # Start serial number from 1
            for service_info in self.services_info:
                html_content += f"""
                    <tr style="text-align: center">
                        <td>{sl_number}</td>  <!-- Sl (Serial Number) -->
                        <td>{service_info["service"]}</td>  <!-- Item Name (service) -->
                        <td>{service_info["plan"]} ({service_info["discount_percentage"]}% discount)</td>     <!-- Description (plan) -->
                        <td>&#8377;{service_info["base_price"]}</td> <!-- Rate (base_price) -->
                        <td>&#8377;{service_info["discount_amount"]:.2f}</td> <!-- Discount (discount_amount) -->
                        <td>&#8377;{service_info["discounted_price"]:.2f}</td> <!-- Amount (discounted_price) -->
                    </tr>
                """
                sl_number += 1  # Increment serial number for next service

    
            # Adding the summary and footer to each page
            html_content += f"""
                </table>
                </div>
                <br><br>
                <table class="summary" style="width: 50%; border-collapse: collapse;">
                    <tr><td class="label"><strong>Total:</strong></td><td><strong>{self.total_discounted_price:.2f}</strong></td></tr>
                    {(f'<tr><td class="label">SGST:</td><td>{sgst_amount:.2f}</td></tr>' if gst_applicable else '')}
                    {(f'<tr><td class="label">CGST:</td><td>{cgst_amount:.2f}</td></tr>' if gst_applicable else '')}
                    <tr><td class="label">Received:</td><td>{total_receive:.2f}</td></tr>
                    <tr><td class="label">Balance:</td><td>{balance:.2f}</td></tr>
                    <tr><td class="label"><strong>Grand Total:</strong></td><td><strong>&#8377;{round(balance)}</strong></td></tr>
                </table>
                <br><br>
                <p><strong>Amount in words:</strong> {total_amount_in_words} rupees only</p>
                <br>
                <div class="Signature">
                    <p>For <strong>Geek Thrive</strong></p>
                    <img src="{signnature_path}" alt="Signature" style="height: 60px;">
                    <p>Authorized Signature</p>
                </div>
                <br>
                <div class="footer">
                    <p>Thank you for choosing Geek Thrive for your business. All payments must be completed before the  final delivery of the product.</p>
                    <br>
                </div>
            </div>
            """
        html_content += "</body></html>"
    
        pdf_file = f"QuotationAS{invoice_number}.pdf"
        try:
            pdfkit.from_string(
                html_content,
                pdf_file,
                configuration=self.pdfkit_config,
                options={
                    'quiet': '',
                    'enable-local-file-access': '', 
                    'no-stop-slow-scripts': '',
                    'debug-javascript': '',
                    'page-size': 'A4',
                    'margin-top': '10mm',
                    'margin-right': '10mm',
                    'margin-bottom': '10mm',
                    'margin-left': '10mm'
                }
            )
    
            # Generate a link to the PDF
            global pdf_fileName
            pdf_path = f"{pdf_file}.pdf"
            pdf_fileName = pdf_file
    
            # Show information message with the path
            QMessageBox.information(self, "Invoice Generated", f"Invoice saved as: {pdf_path}\nYou can open it from the     file system.")
    
        except Exception as e:
            QMessageBox.warning(self, "PDF Generation Error", str(e))
    
    def share(self):
        try:
            # Check if pdf_fileName is defined globally
            global pdf_fileName
            if 'pdf_fileName' not in globals() or not pdf_fileName:
                raise ValueError("You need to generate the invoice or quotation first.")

            selected_option = self.share_option_combo.currentText()
            if selected_option == "Email":
                self.send_email(pdf_fileName)
            elif selected_option == "WhatsApp":
                self.send_whatsapp_pdf(self.contact_number,pdf_fileName)
            else:
                QMessageBox.warning(self, "Warning", "Please select a valid sharing option.")

        except ValueError as e:
            QMessageBox.warning(self, "Warning", str(e))
     
    def send_email(self, pdf_filename):
        sender_email = "dshreyasi3003@gmail.com"  # Replace with your email
        sender_password = "xpji oifw trrg lppv"  # Replace with your email password
        recipient_email = self.email

            # Create the email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = "Invoice Attached"

            # Attach the PDF
        with open(pdf_filename, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={pdf_filename}')
            msg.attach(part)

            # Send the email
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:  # Update this for your email provider
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)
            QMessageBox.information(self, "Email Sent", f"Invoice sent to {recipient_email}")
        except Exception as e:
            QMessageBox.warning(self, "Email Sending Error", str(e))

    def send_whatsapp_pdf(self, phone_number_input, pdf_filename):
        phone_number = phone_number_input.text().strip()
        phone_number = "91" + phone_number  # Add country code

        # Your WhatsApp API token
        token = 'EAAU3TESI1ZCgBOzQ0m4eTTCPShZBrOiAvSesXUH15x6snu1twu01fcna52o21wcbf8xfeJbbqoL1MigUksV1ual8McH0BRrS1tZBeLoan5s4p0Pbf6ZCyRg94H0QRP2mZAg4pyWNwKBGHwMDrUhk3jDWb6TcPBMY8U4bwH3ZC4pLFES9RqCbS2Gc6MKLnUhDL8'  # Replace with your actual token
        media_url = 'https://graph.facebook.com/v21.0/414904298379551/media'  # Your WhatsApp number

        headers = {
            'Authorization': f'Bearer {token}',
        }

        pdf_file_path = pdf_filename

        if not os.path.isfile(pdf_file_path):
            raise FileNotFoundError(f"The PDF file does not exist: {pdf_file_path}")

        # Step 1: Upload the document
        with open(pdf_file_path, 'rb') as f:
            files = {'file': f}
            # Adding 'messaging_product' parameter for upload
            payload = {
                'messaging_product': 'whatsapp'
            }
            response = requests.post(media_url, headers=headers, params=payload, files=files)

        if response.status_code != 200:
            error_message = f"Failed to upload PDF. Response: {response.text}"
            QMessageBox.warning(self, "Upload Error", error_message)
            print(error_message)
            return

        media_id = response.json().get('id')

        # Step 2: Send the document message
        message_url = 'https://graph.facebook.com/v21.0/me/messages'
        message_payload = {
            'messaging_product': 'whatsapp',
            'to': phone_number,
            'type': 'document',
            'document': {
                'id': media_id,
                'caption': 'Here is your PDF document.'
            }
        }

        message_response = requests.post(message_url, headers=headers, json=message_payload)

        if message_response.status_code != 200:
            error_message = f"Failed to send message. Response: {message_response.text}"
            QMessageBox.warning(self, "Send Error", error_message)
            print(error_message)
        else:
            success_message = f"PDF uploaded and sent successfully to {phone_number}."
            QMessageBox.information(self, "Success", success_message)
            print(success_message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    #main_window = FirstUI()
    main_window = SecondUI("address", "name", "contact_number", "email")
    main_window.show()
    sys.exit(app.exec_())
