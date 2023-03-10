# Form implementation generated from reading ui file 'qt_login.ui'
#
# Created by: PyQt6 UI code generator 6.1.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_LoginForm(object):
    def setupUi(self, LoginForm):
        LoginForm.setObjectName("LoginForm")
        LoginForm.resize(600, 800)
        self.horizontalLayoutWidget = QtWidgets.QWidget(LoginForm)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(-10, 200, 621, 201))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMaximumSize)
        self.verticalLayout.setContentsMargins(10, -1, 10, -1)
        self.verticalLayout.setSpacing(7)
        self.verticalLayout.setObjectName("verticalLayout")
        self.login_input = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.login_input.setObjectName("login_input")
        self.verticalLayout.addWidget(self.login_input)
        self.password_input = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.password_input.setEnabled(True)
        self.password_input.setObjectName("password_input")
        self.verticalLayout.addWidget(self.password_input)
        self.incorrect_data_layout = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.incorrect_data_layout.setMaximumSize(QtCore.QSize(16777215, 20))
        self.incorrect_data_layout.setStyleSheet("border: 2px solid red; background-color: rgb(255, 170, 0)")
        self.incorrect_data_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.incorrect_data_layout.setObjectName("incorrect_data_layout")
        self.verticalLayout.addWidget(self.incorrect_data_layout)
        self.wrong_password_layout = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.wrong_password_layout.setMaximumSize(QtCore.QSize(16777215, 20))
        self.wrong_password_layout.setStyleSheet("border: 2px solid red; background-color: rgb(255, 170, 0)")
        self.wrong_password_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.wrong_password_layout.setObjectName("wrong_password_layout")
        self.verticalLayout.addWidget(self.wrong_password_layout)
        self.wrong_password_repeat_layout = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.wrong_password_repeat_layout.setMaximumSize(QtCore.QSize(16777215, 20))
        self.wrong_password_repeat_layout.setStyleSheet("border: 2px solid red; background-color: rgb(255, 170, 0); visibility: hidden;")
        self.wrong_password_repeat_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.wrong_password_repeat_layout.setObjectName("wrong_password_repeat_layout")
        self.verticalLayout.addWidget(self.wrong_password_repeat_layout)
        self.bad_connect_layout = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.bad_connect_layout.setMaximumSize(QtCore.QSize(16777215, 20))
        self.bad_connect_layout.setStyleSheet("border: 2px solid red; background-color: rgb(255, 170, 0); visibility: hidden;")
        self.bad_connect_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.bad_connect_layout.setObjectName("bad_connect_layout")
        self.verticalLayout.addWidget(self.bad_connect_layout)
        self.login_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.login_btn.setObjectName("login_btn")
        self.verticalLayout.addWidget(self.login_btn)
        self.horizontalLayout.addLayout(self.verticalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)

        self.retranslateUi(LoginForm)
        QtCore.QMetaObject.connectSlotsByName(LoginForm)

    def retranslateUi(self, LoginForm):
        _translate = QtCore.QCoreApplication.translate
        LoginForm.setWindowTitle(_translate("LoginForm", "Form"))
        self.login_input.setPlaceholderText(_translate("LoginForm", "??????????"))
        self.password_input.setPlaceholderText(_translate("LoginForm", "????????????"))
        self.incorrect_data_layout.setText(_translate("LoginForm", "???????????????????????? ????????"))
        self.wrong_password_layout.setText(_translate("LoginForm", "???????????????? ??????????/????????????"))
        self.wrong_password_repeat_layout.setText(_translate("LoginForm", "???????????? ???? ??????????????????"))
        self.bad_connect_layout.setText(_translate("LoginForm", "?????????????????????? ????????????????????"))
        self.login_btn.setText(_translate("LoginForm", "??????????"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    LoginForm = QtWidgets.QWidget()
    ui = Ui_LoginForm()
    ui.setupUi(LoginForm)
    LoginForm.show()
    sys.exit(app.exec())
