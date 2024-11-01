from PyQt5 import QtWidgets
from app.View.ui import Ui_SQLCompiler
import sys

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_SQLCompiler()
ui.setupUi(MainWindow)

# Connections
from app.Controller.controllers import compile, execute
ui.combilebtn.clicked.connect(compile)
ui.excutebtn.clicked.connect(execute)

