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
from PyQt5.QtWidgets import QGraphicsScene,  QGraphicsView, QScrollArea, QMainWindow, QPushButton, QComboBox, QListWidget, QMessageBox, QHBoxLayout, QCheckBox ,    QApplication, QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit
import phonenumbers
from phonenumbers import parse, is_valid_number, geocoder, carrier, NumberParseException
from email_validator import validate_email, EmailNotValidError
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QPainter
from PyQt5 import QtCore
from PyQt5.QtPrintSupport import QPrinter, QPrintPreviewDialog
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
    QApplication, QWidget, QVBoxLayout,  QFileDialog, QGraphicsView, QGraphicsScene, QSpacerItem, QSizePolicy, QFormLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QListWidget, QMessageBox, QHBoxLayout, QCheckBox,QDateEdit,QDialog
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
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog



class PDFViewer(QGraphicsView):
    # def __init__(self, pdf_path):
    #     super().__init__()
    #     self.setWindowTitle("Invoice Viewer")
    #     self.setGeometry(200, 100, 800, 600)

    #     # Create a QGraphicsScene to hold the PDF pages
    #     self.scene = QGraphicsScene(self)
    #     self.setScene(self.scene)

    #     # Render the PDF content
    #     self.load_pdf(pdf_path)
    # def __init__(self, pdf_path):
    #         super().__init__()
    #         self.pdf_path = pdf_path
    #         self.setWindowTitle("Invoice Viewer")
    #         self.setGeometry(200, 100, 800, 600)

    #         # Create the main layout for the widget
    #         layout = QVBoxLayout(self)

    #         # Create a QGraphicsView to hold the PDF pages
    #         self.graphics_view = QGraphicsView(self)
    #         self.scene = QGraphicsScene(self.graphics_view)
    #         self.graphics_view.setScene(self.scene)
    #         layout.addWidget(self.graphics_view)

    #         # Add a spacer to push the button to the bottom
    #         spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
    #         layout.addItem(spacer)

    #         # Add the "Download PDF" button fixed at the bottom
    #         self.download_button = QPushButton("Download PDF", self)
    #         self.download_button.clicked.connect(self.download_pdf)
    #         layout.addWidget(self.download_button)

    #         # Set the layout for the widget
    #         self.setLayout(layout)

    #         # Render the PDF content
    #         self.load_pdf(pdf_path)


    def __init__(self, pdf_path, contact_number="", email=""):
        super().__init__()
        
         # Load PDF
        self.doc = fitz.open(pdf_path)
        self.pdf_path = pdf_path  # Store the original PDF path

        # Current page and total pages
        self.current_page = 0
        self.total_pages = len(self.doc)
        
        self.contact_number = contact_number  # WhatsApp contact number
        self.email = email 
        self.setWindowTitle("Invoice")
        self.setGeometry(200, 100, 800, 700)
        
        # # Layout setup
        # self.label = QLabel(self)
        # self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create the main layout for the widget
        layout = QVBoxLayout(self)

        # Create a QGraphicsView to hold the PDF pages
        self.graphics_view = QGraphicsView(self)
        self.scene = QGraphicsScene(self.graphics_view)
        self.graphics_view.setScene(self.scene)
        layout.addWidget(self.graphics_view)

        # Add a spacer to push the buttons to the bottom
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)

        # Create a horizontal layout for the buttons
        button_layout = QHBoxLayout()

        # Buttons for navigation
        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.previous_page)
        self.prev_button.setEnabled(False)  # Disable initially
        button_layout.addWidget(self.prev_button)

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_page)
        button_layout.addWidget(self.next_button)

        # Button for downloading the PDF
        self.download_button = QPushButton("Download PDF")
        self.download_button.clicked.connect(self.download_pdf)
        button_layout.addWidget(self.download_button)

        # Add the "Print" button
        self.print_button = QPushButton("Print", self)
        self.print_button.clicked.connect(self.print_pdf)
        button_layout.addWidget(self.print_button)

         # Add the "Share" dropdown with WhatsApp and Email options
        self.share_option_combo = QComboBox(self)
        self.share_option_combo.addItems(["Select Share Option", "Email", "WhatsApp"])
        button_layout.addWidget(self.share_option_combo)

        # Add the "Share" button
        self.share_button = QPushButton("Share", self)
        self.share_button.clicked.connect(self.share)
        button_layout.addWidget(self.share_button)

        

        # Add the button layout to the main layout
        #layout.addWidget(self.label)
        layout.addLayout(button_layout)

        # Set the layout for the widget
        self.setLayout(layout)

        # Show the first page
        self.load_page(self.current_page)

  
    def load_page(self, page_number):
        """Loads the specified page number into the viewer."""
        pix = self.doc[page_number].get_pixmap()

        # Convert to QImage
        image = QImage(
            pix.samples,
            pix.width,
            pix.height,
            pix.stride,
            QImage.Format.Format_RGB888
        )

        # Display the QImage
        pixmap = QPixmap.fromImage(image)
        self.scene.addPixmap(pixmap)
        #self.label.setPixmap(pixmap)

        # Update button states
        self.prev_button.setEnabled(self.current_page > 0)
        self.next_button.setEnabled(self.current_page < self.total_pages - 1)

    def previous_page(self):
        """Navigate to the previous page."""
        if self.current_page > 0:
            self.current_page -= 1
            self.load_page(self.current_page)

    def next_page(self):
        """Navigate to the next page."""
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.load_page(self.current_page)

    def download_pdf(self):
        """Downloads the entire PDF to a user-specified location."""
        # Open a file dialog to choose the save location
        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save PDF As", "", "PDF Files (*.pdf);;All Files (*)"
        )
        if save_path:
            try:
                # Save the original PDF to the chosen location
                with open(self.pdf_path, "rb") as src_file:
                    with open(save_path, "wb") as dest_file:
                        dest_file.write(src_file.read())
                QMessageBox.information(self, "PDF saved successfully!", f"suman: {self.pdf_path}\nYou can open it from the     file system.")
                
            except Exception as e:
                QMessageBox.warning(self, "Error Saving PDF", str(e))

    # def print_pdf(self):
    #     """Handles the print functionality."""
    #     printer = QPrinter(QPrinter.HighResolution)
    #     printer.setPageSize(QPrinter.A4)
    #     printer.setOutputFormat(QPrinter.NativeFormat)

    #     # Create a QPrintPreviewDialog to preview before printing
    #     preview_dialog = QPrintPreviewDialog(printer, self)
    #     preview_dialog.paintRequested.connect(self.preview_print)  # Connect the print preview function
    #     preview_dialog.exec_()

    # def preview_print(self, printer):
    #     """Handles the actual print logic when preview is requested."""
    #     painter = QPainter(printer)
    #     self.scene.render(painter)  # Render the scene to the painter (the actual print process)
    #     painter.end()

    # def print_pdf(self):
    #     """Prints the entire PDF using the original file path."""
    #     print("Here")
    #     printer = QPrinter(QPrinter.PrinterMode.HighResolution)
    #     printer.setOutputFormat(QPrinter.OutputFormat.NativeFormat)
        
    #     # Show the print dialog
    #     dialog = QPrintDialog(printer, self)
    #     if dialog.exec() == QPrintDialog.DialogCode.Accepted:
    #         try:
    #             # Open the PDF file using the fitz library
    #             pdf_doc = fitz.open(self.pdf_path)
                
    #             painter = QPainter(printer)
    #             for page_number in range(len(pdf_doc)):
    #                 page = pdf_doc[page_number]
    #                 pix = page.get_pixmap()
    #                 image = QImage(
    #                     pix.samples, pix.width, pix.height, pix.stride, QImage.Format.Format_RGB888
    #                 )
    #                 pixmap = QPixmap.fromImage(image)

    #                 # Adjust page to printer
    #                 rect = painter.viewport()
    #                 scaled_pixmap = pixmap.scaled(
    #                     rect.width(), rect.height(), Qt.AspectRatioMode.KeepAspectRatio
    #                 )
    #                 painter.drawPixmap(rect, scaled_pixmap)

    #                 if page_number < len(pdf_doc) - 1:
    #                     printer.newPage()
    #             painter.end()
    #             pdf_doc.close()
    #             QMessageBox.information(
    #                 self, "PDF Printed", "PDF printed successfully!", QMessageBox.StandardButton.Ok)

    #         except:
    #             QMessageBox.critical(self, "Error Printing PDF", "Error printing PDF. Please check the PDF file.", QMessageBox.StandardButton.Ok)

    def print_pdf(self):
        """Prints the entire PDF using the original file path."""
        try:
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setOutputFormat(QPrinter.OutputFormat.NativeFormat)

            # Show the print dialog
            dialog = QPrintDialog(printer, self)
            if dialog.exec() == QPrintDialog.DialogCode.Accepted:
                pdf_doc = fitz.open(self.pdf_path)
                painter = QPainter(printer)

                for page_number in range(len(pdf_doc)):
                    page = pdf_doc[page_number]
                    pix = page.get_pixmap()
                    image = QImage(
                        pix.samples, pix.width, pix.height, pix.stride, QImage.Format.Format_RGB888
                    )
                    pixmap = QPixmap.fromImage(image)

                    # Adjust page to printer
                    rect = painter.viewport()
                    scaled_pixmap = pixmap.scaled(
                        rect.width(), rect.height(), Qt.AspectRatioMode.KeepAspectRatio
                    )
                    painter.drawPixmap(rect, scaled_pixmap)

                    if page_number < len(pdf_doc) - 1:
                        printer.newPage()

                painter.end()
                pdf_doc.close()
                QMessageBox.information(self, "PDF Printed", "PDF printed successfully!", QMessageBox.StandardButton.Ok)

        except Exception as e:
            QMessageBox.critical(self, "Error Printing PDF", f"Error printing PDF: {str(e)}")


    def share(self):
            """Handles the sharing functionality."""
            try:
                selected_option = self.share_option_combo.currentText()
                if selected_option == "Email":
                    self.send_email(self.pdf_path)
                elif selected_option == "WhatsApp":
                    self.send_whatsapp_pdf(self.contact_number, self.pdf_path)
                else:
                    QMessageBox.warning(self, "Warning", "Please select a valid sharing option.")

            except ValueError as e:
                QMessageBox.warning(self, "Warning", str(e))
                

    def send_email(self, pdf_filename):
        sender_email = "support@geekthrive.com"  # Replace with your email
        sender_password = "K}k,i^c+USss"  # Replace with your email password
        recipient_email = self.email

        # Validate recipient email
        if not recipient_email or "@" not in recipient_email:
            QMessageBox.warning(self, "Invalid Email", "Please provide a valid recipient email address.")
            return

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
            with smtplib.SMTP('mail.geekthrive.com', 587) as server:  # Update this for your email provider
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)
            QMessageBox.information(self, "Email Sent", f"Invoice sent to {recipient_email}")
        except Exception as e:
            QMessageBox.warning(self, "Email Sending Error", str(e))


    # def send_whatsapp_pdf(self, phone_number_input, pdf_filename):
    #     phone_number = phone_number_input.text().strip()
    #     phone_number = "91" + phone_number  # Add country code

    #     # Your WhatsApp API token
    #     token = 'EAAU3TESI1ZCgBOzQ0m4eTTCPShZBrOiAvSesXUH15x6snu1twu01fcna52o21wcbf8xfeJbbqoL1MigUksV1ual8McH0BRrS1tZBeLoan5s4p0Pbf6ZCyRg94H0QRP2mZAg4pyWNwKBGHwMDrUhk3jDWb6TcPBMY8U4bwH3ZC4pLFES9RqCbS2Gc6MKLnUhDL8'  # Replace with your actual token
    #     media_url = 'https://graph.facebook.com/v21.0/414904298379551/media'  # Your WhatsApp number

    #     headers = {
    #         'Authorization': f'Bearer {token}',
    #     }

    #     pdf_file_path = pdf_filename

    #     if not os.path.isfile(pdf_file_path):
    #         raise FileNotFoundError(f"The PDF file does not exist: {pdf_file_path}")

    #     # Step 1: Upload the document
    #     with open(pdf_file_path, 'rb') as f:
    #         files = {'file': f}
    #         # Adding 'messaging_product' parameter for upload
    #         payload = {
    #             'messaging_product': 'whatsapp'
    #         }
    #         response = requests.post(media_url, headers=headers, params=payload, files=files)

    #     if response.status_code != 200:
    #         error_message = f"Failed to upload PDF. Response: {response.text}"
    #         QMessageBox.warning(self, "Upload Error", error_message)
    #         print(error_message)
    #         return

    #     media_id = response.json().get('id')

    #     # Step 2: Send the document message
    #     message_url = 'https://graph.facebook.com/v21.0/me/messages'
    #     message_payload = {
    #         'messaging_product': 'whatsapp',
    #         'to': phone_number,
    #         'type': 'document',
    #         'document': {
    #             'id': media_id,
    #             'caption': 'Here is your PDF document.'
    #         }
    #     }

    #     message_response = requests.post(message_url, headers=headers, json=message_payload)

    #     if message_response.status_code != 200:
    #         error_message = f"Failed to send message. Response: {message_response.text}"
    #         QMessageBox.warning(self, "Send Error", error_message)
    #         print(error_message)
    #     else:
    #         success_message = f"PDF uploaded and sent successfully to {phone_number}."
    #         QMessageBox.information(self, "Success", success_message)
    #         print(success_message)

    def send_whatsapp_pdf(self, phone_number, pdf_filename):
        """Sends the PDF via WhatsApp."""
        if not phone_number or not phone_number.isdigit():
            QMessageBox.warning(self, "Invalid Phone Number", "Please enter a valid phone number.")
            return

        # WhatsApp API setup
        token = 'your-whatsapp-api-token'  # Replace with your actual token
        url = f"https://api.whatsapp.com/send?phone={phone_number}"
        
        try:
            # Save the PDF temporarily
            temp_pdf_path = os.path.join(tempfile.gettempdir(), os.path.basename(pdf_filename))
            with open(pdf_filename, 'rb') as f_in, open(temp_pdf_path, 'wb') as f_out:
                f_out.write(f_in.read())
            
            # Send file using WhatsApp API
            files = {'file': open(temp_pdf_path, 'rb')}
            data = {'token': token, 'phone': phone_number, 'caption': 'Here is your invoice.'}
            response = requests.post(url, files=files, data=data)

            if response.status_code == 200:
                QMessageBox.information(self, "WhatsApp", "PDF sent successfully via WhatsApp!")
            else:
                QMessageBox.warning(self, "WhatsApp Error", f"Failed to send PDF. {response.json()}")

        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")

    
    def go_back(self):
       pass
       #self.open()
       

    def open(self):
        from farid import SecondUI
        from suman import FirstUI

        # Close the current window
        

        # Create a new instance of SecondUI with the required parameters
        self.second_ui_window = SecondUI(
            FirstUI.address,
            FirstUI.name,
            FirstUI.contact_number,
            FirstUI.email
        )

        # Show the new window
        self.second_ui_window.show()
        self.second_ui_window.raise_()  # Raise the window to the top
        self.second_ui_window.activateWindow()  # Give the new window focus           


    # def go_back(self):
    #     """Handle the back button functionality."""
    #     QMessageBox.information(self, "Back", "Going back to the previous screen.")
    #     # self.hide()  # Close the current window
        
    #     from farid import SecondUI
    #     from suman import FirstUI

    #     # Clear the current content of the main window
    #     for i in reversed(range(self.layout().count())):
    #         widget = self.layout().itemAt(i).widget()
    #         if widget:
    #             widget.setParent(None)
        
    #     # Create an instance of SecondUI
    #     self.second_ui = SecondUI(FirstUI.address, FirstUI.name, FirstUI.contact_number, FirstUI.email)
        
    #     # Add SecondUI to the main window layout
    #     self.layout().addWidget(self.second_ui)
        

      
    
# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)  # Initialize the QApplication
    pdf_viewer = PDFViewer(pdf_path="sample.pdf")
    pdf_viewer.show()
    sys.exit(app.exec())



