from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QListWidget, QMessageBox, QHBoxLayout, QCheckBox,QDateEdit,QDialog
)
class View():
    def __init__(self):
        pass

    

    def down(self):
        self.close()
        print("inside down")
        del self
        
        # from farid import SecondUI
        # from suman import FirstUI

        # # Close the current window
        

        # # Create a new instance of SecondUI with the required parameters
        # self.second_ui_window = SecondUI(
        #     FirstUI.address,
        #     FirstUI.name,
        #     FirstUI.contact_number,
        #     FirstUI.email
        # )

        # # Show the new window
        # self.second_ui_window.show()
        # self.second_ui_window.raise_()  # Raise the window to the top
        # self.second_ui_window.activateWindow()  # Give the new window focus    