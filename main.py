import sys
from PyQt5.QtWidgets import QApplication
from gui.registrationPage import RegistrationPage

app = QApplication(sys.argv)

window = RegistrationPage()
window.show()
sys.exit(app.exec_())