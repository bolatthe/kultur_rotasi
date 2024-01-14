import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QMessageBox
from pymongo import MongoClient

class DatabaseManager:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['users']
        self.users_collection = self.db['users']

    def is_valid_user(self, email, password):
        query = {'email': email, 'password': password}
        user = self.users_collection.find_one(query)
        return user is not None

class Login(QDialog):
    def __init__(self, main_window):
        super(Login, self).__init__()
        loadUi("login.ui", self)
        self.login_button.clicked.connect(self.loginfunction)
        self.signup_button.clicked.connect(self.gotocreate)
        self.main_window = main_window
        self.database_manager = DatabaseManager()

    def loginfunction(self):
        email = self.email.text()
        password = self.password.text()

        if self.database_manager.is_valid_user(email, password):
            print(email, "logged in with password:", password)
            self.show_successful_login_message()
            self.main_window.show()
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password!")

    def gotocreate(self):
        create = CreateAcc(self)
        if create.exec_() == QDialog.Accepted:
            self.show_successful_login_message()

    def show_successful_login_message(self):
        QMessageBox.information(self, "Login Successful", "You have successfully logged in!")

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("mainWindow.ui", self)

class CreateAcc(QDialog):
    def __init__(self, login_window):
        super(CreateAcc, self).__init__()
        loadUi("createacc.ui", self)
        self.signupbutton.clicked.connect(self.createaccfunction)
        self.backButton.clicked.connect(self.reject)
        self.login_window = login_window
        self.database_manager = DatabaseManager()

    def createaccfunction(self):
        email = self.email.text()
        if self.password.text() == self.confirmpass.text():
            password = self.password.text()
            print("Successfully created acc with email:", email, "and password:", password)
            self.database_manager.users_collection.insert_one({'email': email, 'password': password})
            self.accept()

if __name__ == "__main__":
    app = QApplication([])

    main_window = MainWindow()
    login = Login(main_window)
    login.show()

    sys.exit(app.exec_())
