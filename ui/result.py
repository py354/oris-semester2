from PyQt6.QtWidgets import *

from ui.qt_result import Ui_ResultForm


class ResultWidget(QWidget, Ui_ResultForm):
    def __init__(self, text, pid, callback):
        super().__init__()
        self.setupUi(self)

        self.result_label.setText(text)
        self.pid = pid
        self.callback = callback
        self.back.clicked.connect(self.back_handler)

    def back_handler(self):
        self.callback(self.pid)
