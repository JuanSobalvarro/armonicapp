from PySide6.QtWidgets import *
from PySide6.QtCore import Slot
import sys

@Slot()
def say(string):
    print(string)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    button0 = QPushButton('Dont press')
    button0.clicked.connect(lambda: say('Button pressed uwu nya'))
    button0.show()
    sys.exit(app.exec())


