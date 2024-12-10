import sys
import os
import random
import string
import sqlite3
import smtplib
import subprocess
import dns.resolver
import re
from datetime import datetime, timedelta
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QStackedWidget, QFrame, QMessageBox, QDialog, QComboBox
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from email.mime.text import MIMEText
from PyQt5.QtWidgets import QCheckBox, QInputDialog, QMessageBox
import smtplib
from email.mime.text import MIMEText

import bcrypt, hashlib

from suman import FirstUI  


# Predefined email sender and SMTP server details (for local use)
SENDER_EMAIL = "farid747870@gmail.com"
SENDER_PASSWORD = "eysz ytht jizb yfmt"# Or use App Password if 2FA is enabled in Gmail
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Check if the app is frozen (running as EXE)
if getattr(sys, 'frozen', False):
    # Path to the temporary folder containing the bundled files
    base_path = sys._MEIPASS
else:
    # Path to the current script during development
    base_path = os.path.dirname(os.path.abspath(__file__))

# Path to GT.py inside the bundled app
gt_path = os.path.join(base_path, 'GT2.py')
image_path = os.path.join(base_path, 'images', 'image.png')
db_path = os.path.join(base_path, 'database.db')
wkhtmltopdf_path = os.path.join(base_path, 'wkhtmltopdf')

# Create SQLite database and users table if they don't exist
def create_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS users")

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL UNIQUE, 
                    name TEXT NOT NULL,  -- Added 'name' field
                    email TEXT NOT NULL UNIQUE,  -- Email remains unique
                    department TEXT NOT NULL,  -- Added 'department' field
                    password TEXT NOT NULL,  -- Password remains required
                    temp_password TEXT,  -- Temporary password (if needed)
                    failed_attempts INTEGER DEFAULT 0,  -- Tracks failed login attempts
                    last_failed_attempt TIMESTAMP)''')

    
    # Add the temp_password column to the users table
    # cursor.execute("ALTER TABLE users ADD COLUMN temp_password TEXT")

    cursor.execute("DROP TABLE IF EXISTS verification")
    cursor.execute('''CREATE TABLE IF NOT EXISTS verification (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        name TEXT NOT NULL, 
                        email TEXT NOT NULL,
                        status TEXT DEFAULT 'pending',
                        FOREIGN KEY (user_id) REFERENCES users(user_id))''')
    conn.commit()
    conn.close()

# Function to save user data in the database
def save_user_data(user_id, name, email, department, password):
    # Hash the password before storing it
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Insert user data into the users table
    cursor.execute('''INSERT INTO users (user_id, name, email, department, password)
                  VALUES (?, ?, ?, ?, ?)''', (user_id, name, email, department, hashed_password.decode('utf-8')))

    conn.commit()
    user_id = cursor.lastrowid  # Get the last inserted user ID  

    # Insert a verification record with status "pending"
    cursor.execute("INSERT INTO verification (user_id, name, email, status) VALUES (?, ?, ?, ?)",
                   (user_id, name, email, 'pending'))

    conn.commit()
    conn.close()
    
# Function to generate a 4-digit OTP
def generate_otp():
    otp = random.randint(1000, 9999)  # Generate a 4-digit OTP
    return otp

# Function to send OTP via email
def send_otp_email(email, otp):
    subject = "Verify Your Email"
    body = f"Your email verification OTP is: {otp}\nPlease use this OTP to verify your email address."
    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = SENDER_EMAIL
    message["To"] = email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Encrypt the connection
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, email, message.as_string())
        QMessageBox.information(None, "OTP Sent", "A verification OTP has been sent to your email address.")
    except Exception as e:
        QMessageBox.critical(None, "Email Error", f"Error sending OTP email: {str(e)}")

# Function to verify the entered OTP
def verify_otp():
    entered_otp = otp_entry.text()

    # Check if the entered OTP matches the one stored in session
    if entered_otp == str(session_data.get('otp', None)):
        # Update verification status to 'verified' in the database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE verification SET status = 'verified' WHERE email = ?",
                       (session_data['email'],))
        conn.commit()
        conn.close()

        # Set a delay of 3-4 seconds before showing the OTP verified notification
        QTimer.singleShot(3000, lambda: show_otp_verified_notification())

    else:
        QMessageBox.critical(None, "Invalid OTP", "The OTP you entered is incorrect.")

def show_otp_verified_notification():
    # Show OTP verified notification
    QMessageBox.information(None, "OTP Verified", "Your email has been successfully verified!")
    
    # Switch to login page and fetch the user_id from session_data
    login_user_id = session_data.get('user_id')  # Fetching the user_id

    # Assuming your login form has a field like `userid_login_entry`
    userid_login_entry.setText(login_user_id)  # Set the user_id in the login form's field

    # After showing the notification, switch to the login screen
    stack.setCurrentWidget(login_page)

# Function to handle signup (generate OTP and send email)
def signup():
    
    user_id = userid_entry.text().strip()
    name = name_entry.text().strip()
    email = email_entry.text().strip()
    department = department_combo.currentText().strip() 
    password = password_entry.text().strip()
    confirm_password = confirm_password_entry.text().strip()


    # Simple validation (can add more checks for email format, password strength, etc.)
    if not user_id or not name or not email or not department or not password:
        QMessageBox.critical(None, "Input Error", "All fields are required!")
        return

    # Save the user data in the database
    save_user_data(user_id, name, email, department, password)

    # Store user_id and email in session data
    session_data['user_id'] = user_id  # Storing user_id in session

    # Generate OTP and send email for verification
    otp = generate_otp()
    send_otp_email(email, otp)

    # Store OTP in the session (using a variable here for simplicity)
    session_data['otp'] = otp
    session_data['email'] = email

    # Show success message
    QMessageBox.information(None, "Signup Successful", "Please check your email for OTP.")

    # Switch to the OTP verification screen
    stack.setCurrentWidget(verification_page)

# Login function
def login():
    user_id = userid_login_entry.text().strip()
    password = password_login_entry.text().strip()

    # Simple validation to ensure fields are filled
    if not user_id or not password:
        QMessageBox.critical(None, "Input Error", "Both fields are required!")
        print("Debug: User ID or Password is empty")  # Debug print
        return

    # Check if the entered user_id exists in the database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Search for the user with the entered user_id
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()

    # Debug: print the result to check if user_id is found
    print(f"Debug: result from DB lookup = {result}")

    conn.close()

    if result:
        # If the user_id exists, check for lockout
        can_login, lockout_time = check_user_lockout(user_id)
        if not can_login:
            if lockout_time:
                lockout_msg = f"You are locked out. Please try again after {lockout_time.strftime('%Y-%m-%d %H:%M:%S')}"
                QMessageBox.warning(None, "Account Locked", lockout_msg)
            print("Debug: Account is locked")  # Debug print
            return

        # Verify the password
        stored_password = result[5]  # Assuming password is the 6th field in the result tuple
        # Check if the entered password matches the hashed password
        if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
            # Reset failed attempts after successful login
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET failed_attempts = 0 WHERE user_id = ?", (user_id,))
            conn.commit()
            conn.close()

            QMessageBox.information(None, "Login Successful", "Welcome to the application!")
            # Open the billing software (GT.py)
            # subprocess.run(['python', gt_path])  # Modify the path if necessary
            ui = FirstUI()
            ui.show()
            
        else:
            # Incorrect password, update failed attempts
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET failed_attempts = failed_attempts + 1, last_failed_attempt = ? WHERE user_id = ?",
                           (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_id))
            conn.commit()
            conn.close()

            QMessageBox.critical(None, "Login Failed", "Invalid user ID or password.")
    else:
        # User ID does not exist
        print(f"Debug: User ID '{user_id}' not found in the database")  # Debugging line for missing user_id
        QMessageBox.critical(None, "Login Failed", "Invalid user ID or password.")

def hash_password(password):
    # Hash password for storage, replace with bcrypt for stronger security
    return hashlib.sha256(password.encode()).hexdigest()
    
# Function to check if the user is locked out
def check_user_lockout(user_id):
    # Connect to the database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Fetch the number of failed attempts and the last failed attempt time
    cursor.execute("SELECT failed_attempts, last_failed_attempt FROM users WHERE user_id = ?", (user_id,))
    user_data = cursor.fetchone()

    if user_data:
        failed_attempts, last_failed_attempt = user_data
        if failed_attempts >= 3:
            # Check if the last failed attempt was within 2 hours
            last_failed_time = datetime.strptime(last_failed_attempt, "%Y-%m-%d %H:%M:%S")
            lockout_time = last_failed_time + timedelta(hours=2)

            if datetime.now() < lockout_time:
                # User is locked out
                conn.close()
                return False, lockout_time
            else:
                # Reset failed attempts if more than 2 hours have passed
                cursor.execute("UPDATE users SET failed_attempts = 0 WHERE user_id = ?", (user_id,))
                conn.commit()
                conn.close()
                return True, None
        else:
            conn.close()
            return True, None
    else:
        conn.close()
        return False, None

# Function to toggle password visibility
def toggle_password_visibility(password_entry, checkbox):
    if checkbox.isChecked():
        password_entry.setEchoMode(QLineEdit.Normal)
    else:
        password_entry.setEchoMode(QLineEdit.Password)

# Function to handle "Forgot Password"
def forgot_password():
    # Create the Forgot Password dialog with custom design
    dialog = QDialog(window)
    dialog.setWindowTitle("Forgot Password")

    # Set a fixed size for the dialog
    dialog.setFixedSize(300, 200)  # Width: 400, Height: 300

    # Layout for dialog
    layout = QVBoxLayout()

    # Email input label and field
    email_label = QLabel("Enter Your Email Address:")
    email_label.setFont(label_font)
    email_label.setStyleSheet(label_style)
    email_label.setAlignment(Qt.AlignCenter)  # Center-align the label
    layout.addWidget(email_label)

    email_input = QLineEdit()
    email_input.setFont(input_font)
    email_input.setStyleSheet(input_style)
    layout.addWidget(email_input)

    # Submit button
    submit_button = QPushButton("Send Temporary Password")
    submit_button.setFont(button_font)
    submit_button.setStyleSheet(button_style)
    layout.addWidget(submit_button)

    # Function to handle the password reset process
    def handle_forgot_password():
        email = email_input.text()

        if email:
            # Check if the email exists in the database
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            user = cursor.fetchone()
            conn.close()

            if user:
                # Generate a temporary password
                temp_password = generate_temp_password()

                # Send the temporary password to the user's email
                send_temp_password_email(email, temp_password)
                
                # Update the database with the temporary password (hashed or as plain text for demo)
                conn = sqlite3.connect('database.db')
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET temp_password = ? WHERE email = ?", (temp_password, email))
                conn.commit()
                conn.close()

                QMessageBox.information(window, "Temporary Password Sent", "A temporary password has been sent to your email. Use it to log in and reset your password.")
                dialog.accept()  # Close the dialog after sending the password
                show_change_password_dialog(email)  # Open dialog to change password
            else:
                QMessageBox.warning(window, "Email Not Found", "No account is associated with this email address.")
        else:
            QMessageBox.warning(window, "Input Error", "Email address is required to reset the password.")

    submit_button.clicked.connect(handle_forgot_password)

    dialog.setLayout(layout)
    dialog.exec_()  # Execute the dialog

def forgot_user_id():
    # Create the Forgot User ID dialog with custom design
    dialog = QDialog(window)
    dialog.setWindowTitle("Forgot User ID")

    # Set a fixed size for the dialog
    dialog.setFixedSize(300, 200)

    # Layout for dialog
    layout = QVBoxLayout()

    # Email input label and field
    email_label = QLabel("Enter Your Email Address:")
    email_label.setFont(label_font)
    email_label.setStyleSheet(label_style)
    email_label.setAlignment(Qt.AlignCenter)  # Center-align the label
    layout.addWidget(email_label)

    email_input = QLineEdit()
    email_input.setFont(input_font)
    email_input.setStyleSheet(input_style)
    layout.addWidget(email_input)

    # Submit button
    submit_button = QPushButton("Retrieve User ID")
    submit_button.setFont(button_font)
    submit_button.setStyleSheet(button_style)
    layout.addWidget(submit_button)

    # Function to handle the user ID retrieval process
    def handle_forgot_user_id():
        email = email_input.text()

        if email:
            # Check if the email exists in the database
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM users WHERE email = ?", (email,))
            user = cursor.fetchone()
            conn.close()

            if user:
                user_id = user[0]
                QMessageBox.information(window, "User ID Retrieved", f"Your User ID is: {user_id}")
                dialog.accept()  # Close the dialog after showing the User ID
            else:
                QMessageBox.warning(window, "Email Not Found", "No account is associated with this email address.")
        else:
            QMessageBox.warning(window, "Input Error", "Email address is required to retrieve the User ID.")

    submit_button.clicked.connect(handle_forgot_user_id)

    dialog.setLayout(layout)
    dialog.exec()  # Execute the dialog

def send_temp_password_email(email, temp_password):
    # Configure email settings
    sender = "dshreyasi3003@gmail.com"
    password = "xpji oifw trrg lppv"
    message = MIMEText(f"Your temporary password is: {temp_password}")
    message['Subject'] = "Temporary Password"
    message['From'] = sender
    message['To'] = email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.sendmail(sender, email, message.as_string())
    except Exception as e:
        print("Error sending email:", e)

def generate_temp_password(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

def show_change_password_dialog(email):
    dialog = QDialog(window)
    dialog.setWindowTitle("Change Password")

    # Set a fixed size for the dialog
    dialog.setFixedSize(400, 300)  # Width: 400, Height: 300

    # Layout for dialog
    layout = QVBoxLayout()

    # Temporary password input
    temp_password_label = QLabel("Enter Temporary Password:")
    temp_password_label.setFont(label_font)
    temp_password_label.setStyleSheet(label_style)
    layout.addWidget(temp_password_label)
    
    temp_password_input = QLineEdit()
    temp_password_input.setFont(input_font)
    temp_password_input.setStyleSheet(input_style)
    temp_password_input.setEchoMode(QLineEdit.Password)
    layout.addWidget(temp_password_input)

    # New password input
    new_password_label = QLabel("Enter New Password:")
    new_password_label.setFont(label_font)
    new_password_label.setStyleSheet(label_style)
    layout.addWidget(new_password_label)
    
    new_password_input = QLineEdit()
    new_password_input.setFont(input_font)
    new_password_input.setStyleSheet(input_style)
    new_password_input.setEchoMode(QLineEdit.Password)
    layout.addWidget(new_password_input)

    # Confirm new password input
    confirm_password_label = QLabel("Confirm New Password:")
    confirm_password_label.setFont(label_font)
    confirm_password_label.setStyleSheet(label_style)
    layout.addWidget(confirm_password_label)
    
    confirm_password_input = QLineEdit()
    confirm_password_input.setFont(input_font)
    confirm_password_input.setStyleSheet(input_style)
    confirm_password_input.setEchoMode(QLineEdit.Password)
    layout.addWidget(confirm_password_input)

    # Show password checkbox
    show_password_checkbox = QCheckBox("Show Password")
    show_password_checkbox.setFont(label_font)
    layout.addWidget(show_password_checkbox)

    # Toggle password visibility when checkbox is checked
    def toggle_password_visibility():
        if show_password_checkbox.isChecked():
            temp_password_input.setEchoMode(QLineEdit.Normal)
            new_password_input.setEchoMode(QLineEdit.Normal)
            confirm_password_input.setEchoMode(QLineEdit.Normal)
        else:
            temp_password_input.setEchoMode(QLineEdit.Password)
            new_password_input.setEchoMode(QLineEdit.Password)
            confirm_password_input.setEchoMode(QLineEdit.Password)

    show_password_checkbox.stateChanged.connect(toggle_password_visibility)

    # Submit button
    submit_button = QPushButton("Submit")
    submit_button.setFont(button_font)
    submit_button.setStyleSheet(button_style)
    layout.addWidget(submit_button)

    dialog.setLayout(layout)

    # Function to handle password change
    def change_password():
        temp_password = temp_password_input.text().strip()
        new_password = new_password_input.text().strip()
        confirm_password = confirm_password_input.text().strip()

        # Check if temporary password is correct
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
        result = cursor.fetchone()
        conn.close()

        if result:
            old_password = result[0]  # Get the old password from the database (hashed)

            # Check if the entered temporary password is correct (we can skip this part if not using temp password logic)
            # For simplicity, you can assume temp_password has already been validated if needed
            # We can skip temp_password check as per your original logic, but you may still use it for extra security

            # Check if the new password and confirm password match
            if new_password != confirm_password:
                QMessageBox.warning(window, "Error", "New passwords do not match.")
                return

            # Compare the old password (hashed) with the new password
            if bcrypt.checkpw(new_password.encode('utf-8'), old_password.encode('utf-8')):
                QMessageBox.warning(window, "Error", "New password cannot be the same as the old password.")
                return

            # Hash the new password before saving it
            hashed_new_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            print("New hashed password:", hashed_new_password)  # Debugging line

            # Update the new password in the database
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET password = ?, temp_password = NULL WHERE email = ?", 
                           (hashed_new_password.decode('utf-8'), email))
            conn.commit()
            conn.close()

            QMessageBox.information(window, "Password Changed", "Your password has been successfully changed.")
            dialog.accept()  # Close the dialog
        else:
            QMessageBox.warning(window, "Error", "User not found in the database.")
            
    submit_button.clicked.connect(change_password)
    dialog.exec_()


def verify_login(email, entered_password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
    result = cursor.fetchone()
    conn.close()

    if result:
        stored_password_hash = result[0]
        
        # Check if the entered password matches the stored hash
        if bcrypt.checkpw(entered_password.encode('utf-8'), stored_password_hash.encode('utf-8')):
            return True
        else:
            return False
    else:
        return False


# Define colors and fonts
background_color = "#F7F9FC"
primary_color = "#4CAF50"
accent_color = "#1890FF"
font_color = "#333333"
heading_font = QFont("Arial", 18, QFont.Bold)
label_font = QFont("Arial", 12)
input_font = QFont("Arial", 12)
button_font = QFont("Arial", 12, QFont.Bold)

# Custom Styles
input_style = f"""
    QLineEdit{{
        background-color: white;
        border: 1px solid #BDBDBD;
        border-radius: 20px;
        padding: 3px;
        font-size: 14px;
        color: {font_color};
    }}
    QLineEdit:focus {{
        border: 2px solid {primary_color};
        background-color: #F1F1F1;
    }}
"""
error_style = "border: 1px solid red; padding: 5px;"  # Error style for input fields


button_style = f"""
    QPushButton {{
        background-color: {accent_color};
        color: white;
        border-radius: 20px;
        padding: 6px;
        font-size: 14px;
        font-weight: bold;
    }}
    QPushButton:hover {{
        background-color: #1465C0;
    }}
"""
link_style = f"color: {accent_color}; text-decoration: underline; font-size: 12px;"

# Setup the main application window
app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("Login & Signup System")
window.setFixedSize(620, 620)
window.setStyleSheet(f"background-color: {background_color};")

# Initialize session data for OTP storage (since PyQt5 doesn't have built-in session management)
session_data = {}

# Create stacked widget for page switching
stack = QStackedWidget(window)

# Define styling for the widgets
label_style = f"font-weight: bold; color: {font_color}; font-size: 14px;"
frame_style = f"border: 2px solid {primary_color}; border-radius: 15px; padding: 20px; background-color: #FFFFFF;"

# Signup Page
# Signup Page
signup_page = QWidget()
signup_layout = QVBoxLayout()
signup_layout.setContentsMargins(20, 20, 20, 20)

# Heading
signup_heading = QLabel("Create Account")
signup_heading.setFont(heading_font)
signup_heading.setAlignment(Qt.AlignCenter)
signup_layout.addWidget(signup_heading)


# def validate_input(field, pattern, error_label, error_message, custom_message=None, next_field: QLineEdit = None):
#     # Get the value from the field (QLineEdit or QComboBox)
#     field_value = field.currentText() if isinstance(field, QComboBox) else field.text()

#     # Check if the field is empty
#     if not field_value:
#         error_label.setText("This field cannot be empty.")
#         error_label.setStyleSheet("color: red; font-size: 12px;")
#         # field.setStyleSheet("border: 2px solid red;")
    
        
#     # USer id field validation 
#     elif field == userid_entry:
#         if len(field_value) < 8:
#             error_label.setText("User ID must be at least 8 characters.")
#             error_label.setStyleSheet("color: red; font-size: 12px;")
#             field.setStyleSheet("border: 2px solid red;")
#         elif not re.search(r"[a-z]", field_value):  # At least one lowercase letter
#             error_label.setText("User ID must contain at least 1 lowercase letter.")
#             error_label.setStyleSheet("color: red; font-size: 12px;")
#             field.setStyleSheet("border: 2px solid red;")
#         elif not re.search(r"\d", field_value):  # At least one number
#             error_label.setText("User ID must contain at least 1 number.")
#             error_label.setStyleSheet("color: red; font-size: 12px;")
#             field.setStyleSheet("border: 2px solid red;")
#         elif re.search(r"[A-Z]", field_value) or re.search(r"[^A-Za-z0-9]", field_value):  # No uppercase or special allowed
#             error_label.setText("No uppercase letters or special characters allowed.")
#             error_label.setStyleSheet("color: red; font-size: 12px;")
#             field.setStyleSheet("border: 2px solid red;")
#         else:
#             error_label.clear()  # Clear error message if input is valid
#             field.setStyleSheet("")  # Reset field style
    
    
#     # Validation for name field
#     elif field == name_entry:
#         # Check if the name contains only letters and spaces
#         if not field_value.replace(" ", "").isalpha():
#             error_label.setText("Name must contain only letters and spaces.")
#             error_label.setStyleSheet("color: red; font-size: 12px;")
#             field.setStyleSheet("border: 2px solid red;")
        
#         # Check if the name is at least 8 characters long
#         elif len(field_value) < 8:
#             error_label.setText("Name must be at least 8 characters.")
#             error_label.setStyleSheet("color: red; font-size: 12px;")
#             field.setStyleSheet("border: 2px solid red;")
        
#         # Check if the name contains at least one space (full name validation)
#         elif " " not in field_value:
#             error_label.setText("Name must contain at least one space.")
#             error_label.setStyleSheet("color: red; font-size: 12px;")
#             field.setStyleSheet("border: 2px solid red;")
        
#         # Check if the name matches the defined pattern (e.g., no numbers, special chars)
#         elif not re.match(pattern, field_value):
#             error_label.setText(error_message)
#             error_label.setStyleSheet("color: red; font-size: 12px;")
#             field.setStyleSheet("border: 2px solid red;")
        
#         else:
#             error_label.clear()  # Clear error message if input is valid
#             field.setStyleSheet("")  # Reset field style

#             # Move focus directly to the next field if validation is successful
#             if next_field is not None:
#                 next_field.setFocus()  # Directly set focus to next field


#     # Validation for email field
#     elif field == email_entry:
#         # Check for valid email format
#         if not re.match(pattern, field_value):
#             error_label.setText("Invalid email format.")
#             error_label.setStyleSheet("color: red; font-size: 12px;")
#             field.setStyleSheet("border: 2px solid red;")
#         # Check for uppercase letters in the email
#         elif any(char.isupper() for char in field_value):
#             error_label.setText("Email must contain only lowercase letters.")
#             error_label.setStyleSheet("color: red; font-size: 12px;")
#             field.setStyleSheet("border: 2px solid red;")
#         # Check if anything comes after '.in' in the domain part of the email
#         elif re.search(r"\.in\.(?!co|ac|gov)[a-z]", field_value):
#             error_label.setText("Email cannot have anything after '.in' in the domain.")
#             error_label.setStyleSheet("color: red; font-size: 12px;")
#             field.setStyleSheet("border: 2px solid red;")
#         else:
#             error_label.clear()  # Clear error message if input is valid
#             field.setStyleSheet("")  # Reset field style
            
#     # Password field validation (applies to both password and confirm password)
#     if field == password_entry or field == confirm_password_entry:
#         # Password must match the required pattern (at least 8 characters, 1 uppercase, 1 lowercase, 1 number, 1 special char)
#         if len(field_value) < 8:
#             error_label.setText("Password must be at least 8 characters.")
#             error_label.setStyleSheet("color: red; font-size: 12px;")
#             field.setStyleSheet("border: 2px solid red;")
#         elif not re.search(r"[A-Z]", field_value):  # At least one uppercase letter
#             error_label.setText("Password must contain at least 1 uppercase letter.")
#             error_label.setStyleSheet("color: red; font-size: 12px;")
#             field.setStyleSheet("border: 2px solid red;")
#         elif not re.search(r"[a-z]", field_value):  # At least one lowercase letter
#             error_label.setText("Password must contain at least 1 lowercase letter.")
#             error_label.setStyleSheet("color: red; font-size: 12px;")
#             field.setStyleSheet("border: 2px solid red;")
#         elif not re.search(r"\d", field_value):  # At least one number
#             error_label.setText("Password must contain at least 1 number.")
#             error_label.setStyleSheet("color: red; font-size: 12px;")
#             field.setStyleSheet("border: 2px solid red;")
#         elif not re.search(r"[^A-Za-z0-9]", field_value):  # At least one special character
#             error_label.setText("Password must contain at least 1 special character.")
#             error_label.setStyleSheet("color: red; font-size: 12px;")
#             field.setStyleSheet("border: 2px solid red;")
#         elif field == confirm_password_entry and field_value != password_entry.text():  # Check if passwords match
#             error_label.setText("Passwords do not match.")
#             error_label.setStyleSheet("color: red; font-size: 12px;")
#             field.setStyleSheet("border: 2px solid red;")
#         else:
#             error_label.clear()  # Clear error message if input is valid
#             field.setStyleSheet("")  # Reset field style

#     # Department field validation (only applicable to department_combo)
#     elif isinstance(field, QComboBox):
#         # Ensure that a valid department is selected (not empty)
#         if not field_value or field_value == "Select Department":  # Check if 'Select Department' is the default option
#             error_label.setText("Please select a department.")
#             error_label.setStyleSheet("color: red; font-size: 12px;")
#             field.setStyleSheet("border: 2px solid red;")
#         else:
#             error_label.clear()  # Clear error message if input is valid
#             field.setStyleSheet("")  # Reset field style

#     # Other fields (general validation)
#     else:
#         if len(field_value) < 8:
#             error_label.setText("Field must be at least 8 characters.")
#             error_label.setStyleSheet("color: red; font-size: 12px;")
#             field.setStyleSheet("border: 2px solid red;")
#         elif not re.match(pattern, field_value):
#             error_label.setText(error_message)
#             error_label.setStyleSheet("color: red; font-size: 12px;")
#             field.setStyleSheet("border: 2px solid red;")
#         else:
#             error_label.clear()  # Clear error message if input is valid
#             field.setStyleSheet("")  # Reset field style
      


def validate_input(field, pattern, error_label, error_message, custom_message=None, next_field= None):
    # Get the value from the field (QLineEdit or QComboBox)
    field_value = field.currentText() if isinstance(field, QComboBox) else field.text()
    is_valid = True  # Initialize the validation status

    # General field empty check
    if not field_value:
        error_label.setText("This field cannot be empty.")
        error_label.setStyleSheet("color: red; font-size: 12px;")
        field.setStyleSheet("border: 2px solid red;")
        is_valid = False

    # User ID validation
    elif field == userid_entry:
        # Check if the input contains spaces
        if " " in field_value:
            error_label.setText("No spaces allowed in User ID.")
            is_valid = False
        # Check length: between 4 and 8 characters
        elif len(field_value) < 4 or len(field_value) > 8:
            error_label.setText("User ID must be between 4 and 8 characters.")
            is_valid = False
        # Check for at least one lowercase letter
        elif not re.search(r"[a-z]", field_value):
            error_label.setText("User ID must contain at least 1 lowercase letter.")
            is_valid = False
        # Check for at least one number
        elif not re.search(r"\d", field_value):
            error_label.setText("User ID must contain at least 1 number.")
            is_valid = False
        # Check for uppercase letters
        elif re.search(r"[A-Z]", field_value):
            error_label.setText("No uppercase letters allowed.")
            is_valid = False
        # Check for special characters
        elif re.search(r"[^A-Za-z0-9]", field_value):
            error_label.setText("No special characters allowed.")
            is_valid = False
        else:
            # If all checks are passed, clear the error label and set is_valid to True
            error_label.clear()
            is_valid = True


    # Name field validation
    elif field == name_entry:
        # Check for length: Name must contain at least 8 characters
        if len(field_value) < 8:
            error_label.setText("Name must contain at least 8 characters.")
            is_valid = False
        # Check for digits in the input
        elif any(char.isdigit() for char in field_value):
            error_label.setText("Name must not contain numbers.")
            is_valid = False
        # Ensure that name contains at least one space (for first and last name)
        elif " " not in field_value:
            error_label.setText("Name must contain both first and last name with a space.")
            is_valid = False
        # Check for special characters (only allow letters and spaces)
        elif re.search(r"[^A-Za-z ]", field_value):  # No special characters allowed except space
            error_label.setText("No special characters allowed.")
            is_valid = False
        else:
            # If all checks are passed, clear the error label and set is_valid to True
            error_label.clear()
            is_valid = True




    # Email field validation
    elif field == email_entry:
        # Convert the email to lowercase
        field_value = field_value.lower()
        # Basic email format check using regex
        email_regex = r"^[a-z0-9]+[\._]?[a-z0-9]+[@][a-z0-9-]+\.[a-z]{2,}(?:\.[a-z]{2,})?$"
        if not re.match(email_regex, field_value):
            error_label.setText("Invalid email format.")
            error_label.setStyleSheet("color: red;")  # Red color for error
            is_valid = False  # Invalid email
        
        # Check if there are any uppercase letters in the email
        elif any(char.isupper() for char in field_value):
            error_label.setText("Email must contain only lowercase letters.")
            error_label.setStyleSheet("color: red;")  # Red color for error
            is_valid = False  # Invalid email
        
        # Check if the email domain contains '.in' with disallowed extensions
        elif re.search(r"\.in\.(?!co|ac|gov)[a-z]", field_value):
            error_label.setText("Email cannot have anything after '.in' in the domain.")
            error_label.setStyleSheet("color: red;")  # Red color for error
            is_valid = False  # Invalid email
        
        else:
            # Extract domain from the email and validate common email domains
            domain = field_value.split('@')[1]
            common_domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "geekthrive.com", "yahoo.co.in"]
            
            if domain not in common_domains:
                error_label.setText(f"Invalid or unrecognized email domain: {domain}.")
                error_label.setStyleSheet("color: red;")  # Red color for error
                is_valid = False  # Invalid email
            else:
                # Check MX records for the domain
                try:
                    dns.resolver.resolve(domain, 'MX')
                    # If MX records are found, the domain can receive emails
                    error_label.setText("Status: Valid")
                    error_label.setStyleSheet("color: green;")  # Green color for success
                    is_valid = True  # Valid email
                except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
                    # If no MX records or invalid domain
                    error_label.setText("Invalid email domain. No MX records found.")
                    error_label.setStyleSheet("color: red;")  # Red color for error
                    is_valid = False  # Invalid email

    # Password and Confirm Password validation
    elif field == password_entry:
        # Check if the password length is between 8 and 16 characters
        if len(field_value) < 8 or len(field_value) > 16:
            error_label.setText("Password must be between 8 and 16 characters.")
            is_valid = False
        elif not re.search(r"[A-Z]", field_value):
            error_label.setText("Password must contain at least 1 uppercase letter.")
            is_valid = False
        elif not re.search(r"[a-z]", field_value):
            error_label.setText("Password must contain at least 1 lowercase letter.")
            is_valid = False
        elif not re.search(r"\d", field_value):
            error_label.setText("Password must contain at least 1 number.")
            is_valid = False
        elif not re.search(r"[^A-Za-z0-9]", field_value):
            error_label.setText("Password must contain at least 1 special character.")
            is_valid = False
        elif field == confirm_password_entry and field_value != password_entry.text():
            error_label.setText("Passwords do not match.")
            is_valid = False
        else:
            # If confirm password matches, clear error label
            error_label.clear()
            is_valid = True

    elif field == confirm_password_entry:
    # Check if the confirm password matches the password
        if field_value != password_entry.text():
            error_label.setText("Confirm password does not match with password.")
            is_valid = False
        else:
            # If confirm password matches, clear error label
            error_label.clear()
            is_valid = True

    # Department field validation
    elif isinstance(field, QComboBox):
        if not field_value or field_value == "Select Department":
            error_label.setText("Please select a department.")
            is_valid = False

    # General validation for other fields
    elif len(field_value) < 8:
        error_label.setText("Field must be at least 8 characters.")
        is_valid = False
    elif not re.match(pattern, field_value):
        error_label.setText(error_message)
        is_valid = False

    # Finalize validation
    if is_valid:
        # error_label.clear()  # Clear any error messages
        field.setStyleSheet("")  # Reset field style
        if next_field is not None:
            next_field.setFocus()  # Move focus to the next field if specified
    else:
        error_label.setStyleSheet("color: red; font-size: 12px;")
        field.setStyleSheet("border: 2px solid red;")

    return is_valid

def validate_all_fields():
    fields_valid = True
    
    # Validate all fields using validate_input function
    fields_valid &= validate_input(name_entry, r"[a-zA-Z ]+", name_error, "Invalid Name", "Name should contain only letters and spaces", userid_entry)
    fields_valid &= validate_input(userid_entry, r"[a-z0-9]+", userid_error, "Invalid User ID", "User ID should be alphanumeric", email_entry)
    fields_valid &= validate_input(email_entry, r"^[a-z0-9]+@[a-z]+\.[a-z]{2,3}$", email_error, "Invalid Email Format", "Invalid Email", department_combo)
    fields_valid &= validate_input(password_entry, r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*\W).{8,}$", password_error, "Invalid Password", "Password must contain at least one uppercase, one lowercase, one number and one special character", confirm_password_entry)
    fields_valid &= validate_input(confirm_password_entry, r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*\W).{8,}$", confirm_password_error, "Passwords do not match", "Password confirmation does not match", None)
    fields_valid &= validate_input(department_combo, None, department_error, "Invalid Department", "Please select a department", password_entry)
    
    return fields_valid

# Name Label
name_label = QLabel("Name*")
name_label.setFont(label_font)
name_label.setStyleSheet(label_style)
        
# Requirement Label
requirement_label = QLabel("(Must contain 8 character's, no special character's, no number)")
requirement_label.setFont(label_font)
requirement_label.setStyleSheet("color: grey; font-size: 11px;")
        
# Horizontal layout to hold name label and requirement label
name_label_layout = QHBoxLayout()
name_label_layout.addWidget(name_label)
name_label_layout.addWidget(requirement_label, alignment=Qt.AlignRight)
        
# Name Entry
name_entry = QLineEdit()
name_entry.setFont(input_font)
name_entry.setStyleSheet(input_style)
        
# Add layouts and widgets to the main layout
signup_layout.addLayout(name_label_layout)
signup_layout.addWidget(name_entry)

# Error label for name
name_error = QLabel("")
signup_layout.addWidget(name_error)


# Connect focus-out event to validation
name_entry.editingFinished.connect(lambda : validate_input(
    name_entry, 
    r"^(?=.*\s)[A-Za-z\s]+$",  # Ensure name has at least 8 characters, only letters and spaces
    name_error, 
    "Name must contain one space",
    "Name must be at least 8 characters, no special characters.", next_field=userid_entry
))

# UserID Field
userid_label = QLabel("UserID*")
userid_label.setFont(label_font)
userid_label.setStyleSheet(label_style)
userid_requirement_label = QLabel("(Up to 8 characters, 1 lowercase, and 1 number; no special characters)")
userid_requirement_label.setFont(label_font)
userid_requirement_label.setStyleSheet("color: grey; font-size: 11px;")
userid_label_layout = QHBoxLayout()
userid_label_layout.addWidget(userid_label)
userid_label_layout.addWidget(userid_requirement_label, alignment=Qt.AlignRight)
userid_entry = QLineEdit()
userid_entry.setFont(input_font)
userid_entry.setStyleSheet(input_style)

signup_layout.addLayout(userid_label_layout)
signup_layout.addWidget(userid_entry)

# Error label for user ID
userid_error = QLabel("")
signup_layout.addWidget(userid_error)

# Connect focus-out event to validation for user ID
userid_entry.editingFinished.connect(lambda : validate_input(
    userid_entry, 
    r"^.{4,8}$",  # Ensure user ID is 8 characters, letters and numbers only
    userid_error, 
    "User ID must contain only letters and numbers", next_field= email_entry
))

# Email Field
email_label = QLabel("Email*")
email_label.setFont(label_font)
email_label.setStyleSheet(label_style)
        
# Email Requirement Label
email_requirement_label = QLabel("(Provide the correct email ,to receive OTP)")
email_requirement_label.setFont(label_font)
email_requirement_label.setStyleSheet("color: grey; font-size: 11px;")
        
# Horizontal layout for the email label and requirement label
email_label_layout = QHBoxLayout()
email_label_layout.addWidget(email_label)
email_label_layout.addWidget(email_requirement_label, alignment=Qt.AlignRight)
        
# Email Entry
email_entry = QLineEdit()
email_entry.setFont(input_font)
email_entry.setStyleSheet(input_style)
        
# Add all layouts and widgets to the main layout
signup_layout.addLayout(email_label_layout)
signup_layout.addWidget(email_entry)

# Error label for email
email_error = QLabel("")
# email_error.setFont(label_font)
signup_layout.addWidget(email_error)

# Connect focus-out event to validation
email_entry.editingFinished.connect(lambda : validate_input(
    email_entry, r"^[a-z0-9]+[\._]?[a-z0-9]+[@][a-z0-9-]+\.[a-z]{2,}(?:\.[a-z]{2,})?$", email_error, "Invalid email format", next_field= department_combo
))

# Department Dropdown
department_label = QLabel("Department*")
department_label.setFont(label_font)
department_label.setStyleSheet(label_style)
department_requirement_label = QLabel("(Choose the correct department)")
department_requirement_label.setFont(label_font)
department_requirement_label.setStyleSheet("color: grey; font-size: 11px;")
department_label_layout = QHBoxLayout()
department_label_layout.addWidget(department_label)
department_label_layout.addWidget(department_requirement_label, alignment=Qt.AlignRight)
        
# Create the department dropdown and apply custom styles
department_combo = QComboBox()
department_combo.setFont(input_font)
department_combo.setStyleSheet("""
    QComboBox {
        background-color: white;
        border: 1px solid #BDBDBD;
        padding: 2px;
        font-size: 14px;
        height: 20px;
    }
    QComboBox:focus {
        border: 2px solid #3498db;
        background-color: #F1F1F1;
    }
    QComboBox QAbstractItemView {
        background-color: white;
        border-radius: 10px;
        font-size: 14px;
        padding: 10px;
    }
""")

# Add department options
department_combo.addItem("Select Department")
department_combo.addItem("Admin")
department_combo.addItem("Developer")
department_combo.addItem("Sales")
department_combo.addItem("Support")
# Set the default "Select Department" option as unselectable
department_combo.setItemData(0, False, role=Qt.UserRole) 


signup_layout.addLayout(department_label_layout)
signup_layout.addWidget(department_combo)

# Error label for department
department_error = QLabel("")
signup_layout.addWidget(department_error)

# Connect focus-out event to department validation (example: no numbers or special characters)
department_combo.currentIndexChanged.connect(lambda : validate_input(
    department_combo, r"^[A-Za-z\s]+$", department_error, "Invalid output", next_field= password_entry
))

# Password Field
password_label = QLabel("Password*")
password_label.setFont(label_font)
password_label.setStyleSheet(label_style)
        
# Password Requirement Label
password_requirement_label = QLabel("(8 characters, including 1 uppercase, 1 lowercase, 1 number, and 1 special character)")
password_requirement_label.setFont(label_font)
password_requirement_label.setStyleSheet("color: grey; font-size: 11px;")
        
# Horizontal layout for the password label and requirement label
password_label_layout = QHBoxLayout()
password_label_layout.addWidget(password_label)
password_label_layout.addWidget(password_requirement_label, alignment=Qt.AlignRight)
        
# Password Entry
password_entry = QLineEdit()
password_entry.setEchoMode(QLineEdit.Password)
password_entry.setFont(input_font)
password_entry.setStyleSheet(input_style)
        
# Add all layouts and widgets to the main layout
signup_layout.addLayout(password_label_layout)
signup_layout.addWidget(password_entry)

# Error label for password
password_error = QLabel("")
signup_layout.addWidget(password_error)

# Connect focus-out event to password validation (example: minimum 8 characters, letters and numbers)
password_entry.editingFinished.connect(lambda : validate_input(
    password_entry, r"^.{8,}$", password_error, "Password must be at least 8 characters", next_field=confirm_password_entry
))

# Confirm Password Field
confirm_password_label = QLabel("Confirm Password*")
confirm_password_label.setFont(label_font)
confirm_password_label.setStyleSheet(label_style)
confirm_password_requirement_label = QLabel("(Same as password)")
confirm_password_requirement_label.setFont(label_font)
confirm_password_requirement_label.setStyleSheet("color: grey; font-size: 11px;")
confirm_password_label_layout = QHBoxLayout()
confirm_password_label_layout.addWidget(confirm_password_label)
confirm_password_label_layout.addWidget(confirm_password_requirement_label, alignment=Qt.AlignRight)
confirm_password_entry = QLineEdit()
confirm_password_entry.setEchoMode(QLineEdit.Password)
confirm_password_entry.setFont(input_font)
confirm_password_entry.setStyleSheet(input_style)

signup_layout.addLayout(confirm_password_label_layout)
signup_layout.addWidget(confirm_password_entry)

# Error label for confirm password
confirm_password_error = QLabel("")
signup_layout.addWidget(confirm_password_error)

# Connect focus-out event to confirm password validation (must match password)
confirm_password_entry.editingFinished.connect(lambda : validate_input(
    confirm_password_entry, r"^.{8,}$", confirm_password_error, "Confirm Password must match Password", next_field=None
))

# Show Password Checkbox
show_password_checkbox_signup = QCheckBox("Show Password")
show_password_checkbox_signup.setFont(label_font)
show_password_checkbox_signup.stateChanged.connect(
    lambda: toggle_password_visibility(password_entry, show_password_checkbox_signup)
)
show_password_checkbox_signup.stateChanged.connect(
    lambda: toggle_password_visibility(confirm_password_entry, show_password_checkbox_signup)
)
signup_layout.addWidget(show_password_checkbox_signup)

# Signup Button
signup_btn = QPushButton("Sign Up")
signup_btn.setFont(button_font)
signup_btn.setStyleSheet(button_style)
signup_btn.clicked.connect(signup)
signup_layout.addWidget(signup_btn)

# Switch to Login Button
switch_to_login_btn = QPushButton("Already have an account? Login")
switch_to_login_btn.setFont(button_font)
switch_to_login_btn.setStyleSheet(link_style)
switch_to_login_btn.clicked.connect(lambda: stack.setCurrentWidget(login_page))
signup_layout.addWidget(switch_to_login_btn)

signup_page.setLayout(signup_layout)


# OTP Verification Page
verification_page = QWidget()
verification_layout = QVBoxLayout()
verification_layout.setContentsMargins(20, 20, 20, 20)

otp_label = QLabel("Enter OTP")
otp_label.setFont(label_font)
otp_label.setStyleSheet(label_style)
otp_label.setAlignment(Qt.AlignCenter) 
verification_layout.addWidget(otp_label)

otp_entry = QLineEdit()
otp_entry.setFont(input_font)
otp_entry.setStyleSheet(input_style)
verification_layout.addWidget(otp_entry)

verify_btn = QPushButton("Verify OTP")
verify_btn.setFont(button_font)
verify_btn.setStyleSheet(button_style)
verify_btn.clicked.connect(verify_otp)
verification_layout.addWidget(verify_btn)

# Function to clear the signup form (reset all fields)
def clear_signup_form():
    # Clear all fields on the signup page
    userid_entry.clear()
    name_entry.clear()
    email_entry.clear()
    department_combo.setCurrentIndex(0)  # Reset combo box to default option
    password_entry.clear()
    confirm_password_entry.clear()


switch_to_signup_btn = QPushButton("Back to Signup")
switch_to_signup_btn.setFont(button_font)
switch_to_signup_btn.setStyleSheet(link_style)
# Connect the "Back to Signup" button to clear the form and switch to the signup page
switch_to_signup_btn.clicked.connect(lambda: (clear_signup_form(), stack.setCurrentWidget(signup_page)))

verification_layout.addWidget(switch_to_signup_btn)

verification_page.setLayout(verification_layout)

# Login Page
login_page = QWidget()
login_layout = QVBoxLayout()

# Set contents margins (left, top, right, bottom) to add side space
login_layout.setContentsMargins(50, 0, 50, 0)  # 50 pixels padding on the left and right sides

# Set the main layout alignment to center everything
login_layout.setAlignment(Qt.AlignCenter)

login_heading = QLabel("Welcome Back")
login_heading.setFont(heading_font)
login_heading.setAlignment(Qt.AlignCenter)  # Align the heading in the center
login_layout.addWidget(login_heading)

# Add vertical space after the heading (e.g., 20 pixels of space)
login_layout.addSpacing(20)

# "User ID"
user_id_login_label = QLabel("User ID")
user_id_login_label.setFont(label_font)
user_id_login_label.setStyleSheet(label_style)
user_id_login_label.setAlignment(Qt.AlignCenter)  # Center label
login_layout.addWidget(user_id_login_label)

# User ID input field
userid_login_entry = QLineEdit()  # Create the user ID input field
userid_login_entry.setFont(input_font)
userid_login_entry.setStyleSheet(input_style)
userid_login_entry.setAlignment(Qt.AlignCenter)  # Center the text in the field
login_layout.addWidget(userid_login_entry)

# Password Field
password_login_label = QLabel("Password")
password_login_label.setFont(label_font)
password_login_label.setStyleSheet(label_style)
password_login_label.setAlignment(Qt.AlignCenter)  # Center label
login_layout.addWidget(password_login_label)

password_login_entry = QLineEdit()
password_login_entry.setEchoMode(QLineEdit.Password)
password_login_entry.setFont(input_font)
password_login_entry.setStyleSheet(input_style)
password_login_entry.setAlignment(Qt.AlignCenter)  # Center the text in the field
login_layout.addWidget(password_login_entry)

# Centering the Show Password Checkbox using QHBoxLayout
show_password_checkbox = QCheckBox("Show Password")
show_password_checkbox.setFont(label_font)
show_password_checkbox.stateChanged.connect(lambda: toggle_password_visibility(password_login_entry, show_password_checkbox))

checkbox_layout = QHBoxLayout()
checkbox_layout.setAlignment(Qt.AlignCenter)  # Center the checkbox within the layout
checkbox_layout.addWidget(show_password_checkbox)
login_layout.addLayout(checkbox_layout)

# Add vertical space below the "Show Password" checkbox (e.g., 20 pixels of space)
login_layout.addSpacing(20)

# Layout for Forgot Password and Forgot User ID buttons
forgot_layout = QHBoxLayout()

# Forgot Password Button
forgot_password_btn = QPushButton("Forgot Password?")
forgot_password_btn.setFont(button_font)
forgot_password_btn.setStyleSheet(link_style)
forgot_password_btn.clicked.connect(forgot_password)
forgot_layout.addWidget(forgot_password_btn)

# Forgot User ID Button
forgot_user_id_btn = QPushButton("Forgot User ID?")
forgot_user_id_btn.setFont(button_font)
forgot_user_id_btn.setStyleSheet(link_style)
forgot_user_id_btn.clicked.connect(forgot_user_id)  # Now it works because the function is defined
forgot_layout.addWidget(forgot_user_id_btn)

# Add the layout for forgot buttons to the main login layout, centering the buttons
login_layout.addLayout(forgot_layout)

# Login Button
login_btn = QPushButton("Login")
login_btn.setFont(button_font)
login_btn.setStyleSheet(button_style)
login_btn.clicked.connect(login)  # Connect the login function
login_layout.addWidget(login_btn)

# Function to clear the signup form (reset all fields)
def clear_signup_form():
    # Clear all fields on the signup page
    userid_entry.clear()
    name_entry.clear()
    email_entry.clear()
    department_combo.setCurrentIndex(0)  # Reset combo box to default option
    password_entry.clear()
    confirm_password_entry.clear()

# Switch to Signup Button
switch_to_signup_from_login_btn = QPushButton("Create New Account")
switch_to_signup_from_login_btn.setFont(button_font)
switch_to_signup_from_login_btn.setStyleSheet(link_style)
switch_to_signup_from_login_btn.clicked.connect(lambda: stack.setCurrentWidget(signup_page))
# Connect the "Create New Account" button to clear the signup form and switch to the signup page
switch_to_signup_from_login_btn.clicked.connect(lambda: (clear_signup_form(), stack.setCurrentWidget(signup_page)))

login_layout.addWidget(switch_to_signup_from_login_btn)


# Set the layout for the login page
login_page.setLayout(login_layout)



# Add pages to stacked widget
stack.addWidget(signup_page)
stack.addWidget(verification_page)
stack.addWidget(login_page)

# Set the main layout
main_layout = QVBoxLayout()
main_layout.addWidget(stack)
window.setLayout(main_layout)

# Create the database if it doesn't exist
create_db()

# Show the window
window.show()

# Start the application event loop
sys.exit(app.exec_())
