
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)

    # Set global monospace font for the hacker aesthetic
    font = QFont("Consolas", 11)
    font.setStyleHint(QFont.StyleHint.Monospace)
    app.setFont(font)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
