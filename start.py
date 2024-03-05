import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from environment import DotEnvEnvironment
from src.app.view.WIN_Index import WIN_Index
from src.app.controller.IndexController import IndexController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    Window = QMainWindow()
    view = WIN_Index(Window)

    env = DotEnvEnvironment(".env")
    indexController = IndexController(env, view)
    indexController.init()

    sys.exit(app.exec_())