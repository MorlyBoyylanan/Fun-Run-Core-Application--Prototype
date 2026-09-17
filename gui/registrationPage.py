import os
import sys  

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import QDate

class RegistrationPage(QMainWindow):
    
    def __init__(self):
        super().__init__()

        uic.loadUi("gui/registrationFrontPage.ui", self)

        # Connect the buttons to their respective functions
        
        self.searchButton.clicked.connect(self.searchBtn)
        self.cancelButton.clicked.connect(self.cancelBtn)
        self.registerButton.clicked.connect(self.addBtn)
        self.updateButton.clicked.connect(self.updateBtn)
        self.deleteButton.clicked.connect(self.deleteBtn)
        self.clearButton.clicked.connect(self.clearBtn)

        self.tableWidget.itemSelectionChanged.connect(self.loadSelectedRow)

        self.headers = (
            "Name",
            "Age",
            "Sex",
            "Birthdate",
            "Email",
            "CP Number",
            "Address",
            "Category",
            "Distance",
            "Race Number"
        )

        self.tableWidget.setColumnCount(len(self.headers))
        self.tableWidget.setHorizontalHeaderLabels(self.headers)

        self.participants = []

        self.file_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "dataRecord",
            "participants_File"
        )

        self.file_path = os.path.abspath(self.file_path)

        self.loadFile()
    #Function to add a new row to the table

    def addBtn(self):

        try:
            # Get values from input fields
            name = self.fullnametxt.text().strip()
            age = self.agetxt.text().strip()
            sex = self.sexcomboBox.currentText()
            birthdate = self.birthdateEdit.date().toString(
                "yyyy-MM-dd"
            )
            email = self.emailtxt.text().strip()
            cpnumber = self.cptxt.text().strip()
            address = self.addresstxt.text().strip()
            category = self.categorycomboBox.currentText()
            distance = self.distancecomboBox.currentText()
            racenumber = self.racenumbertxt.text().strip()

            # Validate input fields
            if not name or not age or not email or not cpnumber \
                or not address or not racenumber:

                QMessageBox.warning(self,"Input Error","Please fill in all the fields.")
                return


            if self.raceNumberExists(racenumber):
                QMessageBox.warning(self,"Input Error","Race number already exists. "
                    "Please enter a unique race number."
                )
                return
        # Add the new row to the table
            participant = {
                "name": name,
                "age": age,
                "sex": sex,
                "birthdate": birthdate,
                "email": email,
                "cpnumber": cpnumber,
                "address": address,
                "category": category,
                "distance": distance,
                "race_number": racenumber
            }
    
            self.participants.append(participant)

            # Display participant in table
            self.displayParticipant(participant)

            # Save participant to file
            self.saveParticipant(participant)

            QMessageBox.information(
                self,
                "Registration Successful",
                "Participant registered successfully."
            )
            # Clear input fields
            self.clearBtn()

        except Exception as error:

            QMessageBox.critical(self,"Error",
                f"An error occurred:\n{error}")
            
    # Function to display a participant in the table
    def displayParticipant(self, participant):

        row = self.tableWidget.rowCount()

        self.tableWidget.insertRow(row)

        values = (
            participant["name"],
            participant["age"],
            participant["sex"],
            participant["birthdate"],
            participant["email"],
            participant["cpnumber"],
            participant["address"],
            participant["category"],
            participant["distance"],
            participant["race_number"]
        )
        for column, value in enumerate(values):
            self.tableWidget.setItem(
                row,
                column,
                QTableWidgetItem(value))
            
    # Function to check if a race number already exists in the participants
    def raceNumberExists(self, race_number):

        for participant in self.participants:
            if participant["race_number"] == race_number:
                return True

        return False    
    
    # Function to save a participant's data to the file
    def saveParticipant(self, participant):

        try:

            with open(self.file_path, "a") as file:

                file.write(
                    f"{participant['name']},"
                    f"{participant['age']},"
                    f"{participant['sex']},"
                    f"{participant['birthdate']},"
                    f"{participant['email']},"
                    f"{participant['cpnumber']},"
                    f"{participant['address']},"
                    f"{participant['category']},"
                    f"{participant['distance']},"
                    f"{participant['race_number']}\n"
                )

        except FileNotFoundError:
            QMessageBox.warning(
                self,
                "File Error",
                "The participant file could not be found.")

        except Exception as error:
            QMessageBox.critical(
                self,
                "File Error",
                f"Unable to save participant:\n{error}")
    # Function to load participants from the file and display them in the table
    def loadFile(self):

        try:

            if not os.path.exists(self.file_path):
                return

            with open(self.file_path, "r") as file:

                for line in file:

                    data = line.strip().split(",")

                    if len(data) != 10:
                        continue

                    participant = {
                        "name": data[0],
                        "age": data[1],
                        "sex": data[2],
                        "birthdate": data[3],
                        "email": data[4],
                        "cpnumber": data[5],
                        "address": data[6],
                        "category": data[7],
                        "distance": data[8],
                        "race_number": data[9]
                    }

                    # Add dictionary to list
                    self.participants.append(participant)

                    # Display it in the table
                    self.displayParticipant(participant)

        except FileNotFoundError:

            QMessageBox.warning(
                self,
                "File Error",
                "Participant file was not found."
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "File Error",
                f"Unable to load participants:\n{error}")
            
    # Function to load the selected row's data into the input fields
    def loadSelectedRow(self):

        selected_row = self.tableWidget.currentRow()

        if selected_row < 0:
            return

        try:

            self.fullnametxt.setText(
                self.tableWidget.item(selected_row, 0).text())

            self.agetxt.setText(
                self.tableWidget.item(selected_row, 1).text())

            self.sexcomboBox.setCurrentText(
                self.tableWidget.item(selected_row, 2).text())

            birthdate = self.tableWidget.item(
                selected_row, 3).text()

            date = QDate.fromString(
                birthdate,
                "yyyy-MM-dd")

            self.birthdateEdit.setDate(date)

            self.emailtxt.setText(
                self.tableWidget.item(selected_row, 4).text())

            self.cptxt.setText(
                self.tableWidget.item(selected_row, 5).text())

            self.addresstxt.setText(
                self.tableWidget.item(selected_row, 6).text())

            self.categorycomboBox.setCurrentText(
                self.tableWidget.item(selected_row, 7).text())

            self.distancecomboBox.setCurrentText(
                self.tableWidget.item(selected_row, 8).text())

            self.racenumbertxt.setText(
                self.tableWidget.item(selected_row, 9).text())

        except Exception as error:
            QMessageBox.warning(
                self,
                "Selection Error",
                f"Unable to load selected participant:\n{error}")

    # Function to update the selected participant's data in the list and table
    def updateBtn(self):

        selected_row = self.tableWidget.currentRow()

        if selected_row < 0:

            QMessageBox.warning(
                self,
                "Input Error",
                "Please select a participant to update."
            )
            return

        try:

            name = self.fullnametxt.text().strip()
            age = self.agetxt.text().strip()
            sex = self.sexcomboBox.currentText()
            birthdate = self.birthdateEdit.date().toString(
                "yyyy-MM-dd"
            )
            email = self.emailtxt.text().strip()
            cpnumber = self.cptxt.text().strip()
            address = self.addresstxt.text().strip()
            category = self.categorycomboBox.currentText()
            distance = self.distancecomboBox.currentText()
            racenumber = self.racenumbertxt.text().strip()

            if not name or not age or not email or not cpnumber \
                    or not address or not racenumber:

                QMessageBox.warning(
                    self,
                    "Input Error",
                    "Please fill in all the fields."
                )
                return

            # Check duplicate race number
            for index, participant in enumerate(self.participants):

                if index != selected_row:

                    if participant["race_number"] == racenumber:

                        QMessageBox.warning(
                            self,
                            "Input Error",
                            "Race number already exists."
                        )
                        return

            # Create updated dictionary
            updated_participant = {
                "name": name,
                "age": age,
                "sex": sex,
                "birthdate": birthdate,
                "email": email,
                "cpnumber": cpnumber,
                "address": address,
                "category": category,
                "distance": distance,
                "race_number": racenumber
            }

            # Update list
            self.participants[selected_row] = updated_participant

            # Update table
            values = (
                name,
                age,
                sex,
                birthdate,
                email,
                cpnumber,
                address,
                category,
                distance,
                racenumber
            )

            for column, value in enumerate(values):

                self.tableWidget.setItem(
                    selected_row,
                    column,
                    QTableWidgetItem(value))

            # Rewrite file
            self.saveAllParticipants()

            QMessageBox.information(
                self,
                "Update Successful",
                "Participant updated successfully.")

        except Exception as error:

            QMessageBox.critical(
                self,
                "Update Error",
                f"Unable to update participant:\n{error}")
            
    # Function to save all participants to the file
    def saveAllParticipants(self):

        try:

            with open(self.file_path, "w") as file:

                for participant in self.participants:

                    file.write(
                        f"{participant['name']},"
                        f"{participant['age']},"
                        f"{participant['sex']},"
                        f"{participant['birthdate']},"
                        f"{participant['email']},"
                        f"{participant['cpnumber']},"
                        f"{participant['address']},"
                        f"{participant['category']},"
                        f"{participant['distance']},"
                        f"{participant['race_number']}\n"
                    )

        except Exception as error:

            QMessageBox.critical(
                self,
                "File Error",
                f"Unable to save changes:\n{error}")
            
    # Function to delete a participant from the list and table
    def deleteBtn(self):

        selected_row = self.tableWidget.currentRow()

        if selected_row < 0:

            QMessageBox.warning(
                self,
                "No Selection",
                "Please select a participant to delete.")
            return

        confirm = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this participant?",
            QMessageBox.Yes | QMessageBox.No)

        if confirm == QMessageBox.Yes:

            try:

                # Remove from list
                self.participants.pop(selected_row)

                # Remove from table
                self.tableWidget.removeRow(selected_row)

                # Save updated list
                self.saveAllParticipants()

                QMessageBox.information(
                    self,
                    "Delete Successful",
                    "Participant deleted successfully.")

            except Exception as error:

                QMessageBox.critical(
                    self,
                    "Delete Error",
                    f"Unable to delete participant:\n{error}")

    # Function to search for a participant by race number and select the corresponding row in the table
    def searchBtn(self):

        search_txt = self.searchtxt.text().strip().lower()

        if not search_txt:

            QMessageBox.warning(
                self,
                "Input Error",
                "Please enter a race number or name to search.")
            return

        found = False

        for row in range(self.tableWidget.rowCount()):
            name_item = self.tableWidget.item(row, 0)
            race_number_item = self.tableWidget.item(row, 9)

            name = name_item.text().lower() if name_item else ""
            race_number = race_number_item.text().lower() if race_number_item else ""

            if search_txt in name or search_txt == race_number:

                self.tableWidget.selectRow(row)
                found = True
                QMessageBox.information(
                    self,
                    "Search Result",
                    f"Participant found: {name_item.text()} (Race Number: {race_number_item.text()})")
                break

        if not found:
            QMessageBox.information(
                self,
                "Search Result",
                "Participant not found.")
            
    #function to clear all input fields in the registration form
    def clearBtn(self):

        self.fullnametxt.clear()
        self.agetxt.clear()
        self.sexcomboBox.setCurrentIndex(0)
        self.birthdateEdit.setDate(
        self.birthdateEdit.minimumDate())
        self.emailtxt.clear()
        self.cptxt.clear()
        self.addresstxt.clear()
        self.categorycomboBox.setCurrentIndex(0)
        self.distancecomboBox.setCurrentIndex(0)
        self.racenumbertxt.clear()

    # function to cancel the participant processing registration
    def cancelBtn(self):

        self.close()

app = QApplication(sys.argv)
window = RegistrationPage()
window.setWindowTitle("Registration Page")
window.resize(1200, 800)  
window.show()
sys.exit(app.exec_())