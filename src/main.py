from PyQt5.QtWidgets import QDesktopWidget, QApplication, QPlainTextEdit, QVBoxLayout, QWidget, QPushButton, QShortcut
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QEvent
from gtts import gTTS
import sys
import os

def process_text(text):
    text = text.replace(':', 'colon')
    return text

class PlainTextEditWithEnter(QPlainTextEdit):
    enterPressed = pyqtSignal()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.enterPressed.emit()
        else:
            super().keyPressEvent(event)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.textEdit = PlainTextEditWithEnter(self)
        self.textEdit.setPlaceholderText('Type something...')
        self.textEdit.setFocus()
        self.textEdit.enterPressed.connect(self.speak_text)

        self.button = QPushButton('Speak', self)
        self.button.clicked.connect(self.speak_text)

        layout = QVBoxLayout()
        layout.addWidget(self.textEdit)
        layout.addWidget(self.button)
        self.setLayout(layout)

        self.setGeometry(100, 100, 400, 200)
        self.setWindowTitle('TTS Input')

        # Setup shortcut to exit program
        exitShortcut = QShortcut(QKeySequence("Ctrl+Shift+K"), self)
        exitShortcut.activated.connect(self.exit_app)

    def exit_app(self):
        # Clean up and exit the application
        QApplication.quit()

    def speak_text(self):
        text = self.textEdit.toPlainText()

        text = process_text(text)

        if text:
            tts = gTTS(text, lang='en', tld='ca')
            tts.save('./out/message.mp3')
            os.system('paplay ./out/message.mp3 --device=mix-for-virtual-mic')
            self.textEdit.clear()

            # Exit the application after speaking text
            QApplication.quit()

def show_text_box():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    
    # Center window on current screen
    screen = QDesktopWidget().screenGeometry(QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos()))
    mainWindow.move(screen.center() - mainWindow.rect().center())

    mainWindow.show()

    sys.exit(app.exec_())

def main():
    show_text_box()

if __name__ == '__main__':
    main()
