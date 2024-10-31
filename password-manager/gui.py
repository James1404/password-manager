import random, sys

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

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
