from PyQt5 import QtWidgets
from app.view.ui import Ui_SQLCompiler
import sys

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_SQLCompiler()
ui.setupUi(MainWindow)

# Connections
from app.controller.controllers import compile, execute
ui.combilebtn.clicked.connect(compile)
ui.excutebtn.clicked.connect(execute)

