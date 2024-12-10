from pdfViewer import PDFViewer
from secondUi import SecondUI
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


class ValidatingLineEdit(QLineEdit):
    def __init__(self, validate_function, error_label, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validate_function = validate_function
        self.error_label = error_label

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.validate_function(self.text(), self.error_label)
