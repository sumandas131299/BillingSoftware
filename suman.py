from pdfViewer import PDFViewer
from farid import SecondUI
from validating import ValidatingLineEdit
import sys
import random
import string
import os
import pdfkit
import webbrowser
import tempfile
import fitz  # PyMuPDF
import dns.resolver
from PyQt5.QtWidgets import QGraphicsScene,  QGraphicsView, QScrollArea, QMainWindow, QPushButton, QComboBox, QListWidget, QMessageBox, QHBoxLayout, QCheckBox ,    QApplication, QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit
import phonenumbers
from phonenumbers import parse, is_valid_number, geocoder, carrier, NumberParseException
from email_validator import validate_email, EmailNotValidError
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
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
from PyQt5.QtGui import QIcon, QPixmap, QImage
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

# Placeholder for additional imports (like phonenumbers, dns)
try:
    import phonenumbers
    import dns.resolver
except ImportError:
    phonenumbers = None
    dns = None




class FirstUI(QWidget):
    address=""
    name=""
    contact_number=""
    email=""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("User Information")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()
        formLayout = QFormLayout()

        # Name
        self.name_error = QLabel()
        self.name_error.setStyleSheet('color: red;')
        self.name_input = ValidatingLineEdit(self.validate_name, self.name_error)

        # Company Name
        self.company_name_error = QLabel()
        self.company_name_error.setStyleSheet('color: red;')
        self.company_name_input = ValidatingLineEdit(self.validate_company_name, self.company_name_error)

        # Address
        self.address_error = QLabel()
        self.address_error.setStyleSheet('color: red;')
        self.address_input = ValidatingLineEdit(self.validate_address, self.address_error)

        # Phone Number
        self.phone_error = QLabel()
        self.phone_error.setStyleSheet('color: red;')
        self.phone_input = ValidatingLineEdit(self.validate_phone_number, self.phone_error)

        # Email
        self.email_error = QLabel()
        self.email_error.setStyleSheet('color: red;')
        self.email_entry = ValidatingLineEdit(self.validate_email, self.email_error)

        # Add widgets to the form layout
        formLayout.addRow("Name:", self.name_input)
        formLayout.addRow(self.name_error)
        formLayout.addRow("Company Name:", self.company_name_input)
        formLayout.addRow(self.company_name_error)
        formLayout.addRow("Address:", self.address_input)
        formLayout.addRow(self.address_error)
        formLayout.addRow("Phone Number:", self.phone_input)
        formLayout.addRow(self.phone_error)
        formLayout.addRow("Email:", self.email_entry)
        formLayout.addRow(self.email_error)

        layout.addLayout(formLayout)

        # Continue Button
        self.continue_button = QPushButton("Continue")
        self.continue_button.clicked.connect(self.validate_all_fields)
        layout.addWidget(self.continue_button)

        self.setLayout(layout)

    def validate_name(self, text, error_label):
        if not text.strip():
            error_label.setText("Name cannot be empty.")
            return False
        if not re.match(r"^[a-zA-Z ]+$", text):
            error_label.setText("Name must contain only letters and spaces.")
            return False
        if " " not in text:
            error_label.setText("Name must contain at least one space.")
            return False
        error_label.clear()
        return True

    def validate_company_name(self, text, error_label):
        if not text.strip():
            error_label.setText("Company Name cannot be empty.")
            return False
        if not re.match(r"^[a-zA-Z0-9 ]+$", text):
            error_label.setText("Company Name must contain only letters, numbers, and spaces.")
            return False
        error_label.clear()
        return True

    def validate_address(self, text, error_label):
        if not text.strip():
            error_label.setText("Address cannot be empty.")
            return False
        if not re.match(r"^[a-zA-Z0-9\s,.-]+$", text):
            error_label.setText("Address contains invalid characters.")
            return False
        error_label.clear()
        return True

    def validate_phone_number(self, text, error_label):
        if not text or len(text) != 10 or not text.isdigit():
            error_label.setText("Phone number must be exactly 10 numeric digits.")
            return False
        if text[0] not in "6789":
            error_label.setText(f"Phone number cannot start with {text[0]}.")
            return False

        # Advanced validation using phonenumbers library
        try:
            from phonenumbers import parse, is_valid_number, geocoder, carrier
            parsed_number = parse(f"+91{text}", "IN")
            if not is_valid_number(parsed_number):
                error_label.setText("Invalid phone number.")
                return False

            location = geocoder.description_for_number(parsed_number, "en")
            provider = carrier.name_for_number(parsed_number, "en")
            if not location or not provider:
                error_label.setText("Unable to detect location or service provider.")
                return False

            # Valid phone number
            error_label.setText(f"<font color='green'>Status: Valid: {location} | {provider} </font>")
        except ImportError:
            error_label.setText("phonenumbers library is not installed.")
            return False
        except Exception:
            error_label.setText("An error occurred during validation.")
            return False

        return True

    def validate_email(self, text, error_label):
        text = text.strip().lower()
        if not text.strip():
            error_label.setText("Email cannot be empty.")
            return False

        # Ensure email is lowercase
        if any(char.isupper() for char in text):
            error_label.setText("Email address cannot contain uppercase letters.")
            return False

        email_regex = r"^[a-z0-9]+[\._]?[a-z0-9]+[@][a-z0-9-]+\.[a-z]{2,}(?:\.[a-z]{2,})?$"
        if not re.match(email_regex, text):
            error_label.setText("Invalid email format.")
            return False

        # Validate email domain
        try:
            domain = text.split('@')[1]
            common_domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com"]
            if domain not in common_domains:
                error_label.setText(f"Invalid or unrecognized email domain: {domain}.")
                return False

            import dns.resolver
            dns.resolver.resolve(domain, 'MX')
        except ImportError:
            error_label.setText("DNS resolver library is not installed.")
            return False
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            error_label.setText("Invalid email domain. No MX records found.")
            return False

        error_label.setText("<font color='green'>Status: Valid</font>")
        return True

    def validate_all_fields(self):
        valid = True
        valid &= self.validate_name(self.name_input.text(), self.name_error)
        valid &= self.validate_company_name(self.company_name_input.text(), self.company_name_error)
        valid &= self.validate_address(self.address_input.text(), self.address_error)
        valid &= self.validate_phone_number(self.phone_input.text(), self.phone_error)
        valid &= self.validate_email(self.email_entry.text(), self.email_error)

        if valid:
            self.open_second_ui()

    # def open_second_ui(self):
    #     self.second_ui = SecondUI()
    #     self.second_ui.show()
    #     self.close()

    def open_second_ui(self):
        # Get input data from FirstUI
        address = self.address_input.text()
        name = self.name_input.text()
        contact_number = self.phone_input.text()
        email = self.email_entry.text()


        print(address , name , contact_number , email)

        # Create and show the SecondUI, passing the data
        self.second_ui = SecondUI(address, name, contact_number, email)
        self.second_ui.show()
        self.close()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    main_window = FirstUI()
    # main_window = SecondUI("address", "name", "contact_number", "email")
    main_window.show()
    sys.exit(app.exec_())
