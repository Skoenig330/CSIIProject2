from controller import *


def main():
    readItems()
    readBoxes()
    app = QApplication([])
    window = Controller()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
