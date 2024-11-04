import random, sys

from PySide6 import QtCore, QtGui, QtWidgets

class LoginWidget(QtWidgets.QWidget):
    hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

    def __init__(self):
        super().__init__()

        

class GUI:
    def exec(self) -> int:
        app = QGuiApplication(sys.argv)

        engine = QQmlApplicationEngine()
        engine.addImportPath(sys.path[0])
        engine.loadFromModule("Main", "Main")

        if not engine.rootObjects():
            return -1

        exit_code = app.exec()
        del engine

        return exit_code
