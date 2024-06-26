from PyQt5.QtWidgets import QDesktopWidget, QApplication, QPlainTextEdit, QVBoxLayout, QWidget, QPushButton, QShortcut
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QEvent
from gtts import gTTS
import sys
import os
import re
import time
import subprocess

def process_text(text):
    text = text.replace(':3', 'colon3')
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
        self.modules = []
        self.initUI()

    def initUI(self):
        self.reset_button = QPushButton('Initialise/Reset', self)
        self.reset_button.clicked.connect(self.reset)

        self.remove_button = QPushButton('Remove Virtual Devices', self)
        self.remove_button.clicked.connect(self.unload_modules)


        self.textEdit = PlainTextEditWithEnter(self)
        self.textEdit.setPlaceholderText('Type something...')
        self.textEdit.setFocus()
        self.textEdit.enterPressed.connect(self.speak_text)

        self.button = QPushButton('Speak', self)
        self.button.clicked.connect(self.speak_text)

        layout = QVBoxLayout()
        layout.addWidget(self.reset_button)
        layout.addWidget(self.remove_button)
        layout.addWidget(self.textEdit)
        layout.addWidget(self.button)
        self.setLayout(layout)

        self.setGeometry(100, 100, 400, 200)
        self.setWindowTitle('TTS Input')

        # Setup shortcut to exit program
        exitShortcut = QShortcut(QKeySequence("Ctrl+Shift+K"), self)
        exitShortcut.activated.connect(self.exit_app)

        app = QApplication.instance()
        # app.aboutToQuit.connect(self.unload_modules)

    def exit_app(self):
        # Clean up and exit the application
        QApplication.quit()

    def unload_modules(self):
        while True:
            s = subprocess.run('pactl list modules short', shell=True, check=True, capture_output=True)
            modules_text = s.stdout.decode()
            
            pattern = rf'^(\d+).*text-to-speech-virtual-mic'
            match = re.search(pattern, modules_text, re.MULTILINE)
    
            if match:
                module_id = int(match.group(1))
                subprocess.run(f'pactl unload-module {module_id}', shell=True, check=True, capture_output=True)
            else:
                break

        print('Modules successfully unloaded')


    def reset(self):
        self.unload_modules()

        s = subprocess.run(f'pactl load-module module-null-sink sink_name=text-to-speech-virtual-mic-sink sink_properties=device.description=Mix-for-Virtual-TTS-Microphone', shell=True, check=True, capture_output=True)
        self.modules.append(int(s.stdout))

        s = subprocess.run(f'pactl load-module module-pipe-source source_name=text-to-speech-virtual-mic file=$HOME/dev/virtmic format=s16le rate=16000 channels=1', shell=True, check=True, capture_output=True)
        self.modules.append(int(s.stdout))

        s = subprocess.run(f'pactl load-module module-combine-sink sink_name=vext-to-speech-virtual-mic-combine-sink slaves=text-to-speech-virtual-mic-sink', shell=True, check=True, capture_output=True)
        self.modules.append(int(s.stdout))

        s = subprocess.run(f'pactl load-module module-remap-source master=text-to-speech-virtual-mic-sink.monitor source_properties=device.description=Text-to-Speech-Virtual-Microphone', shell=True, check=True, capture_output=True)
        # self.modules.append(int(s.stdout)) not needed as this gets deleted together with another module

        s = subprocess.run(f'pactl load-module module-loopback source=text-to-speech-virtual-mic-sink.monitor.remapped sink=@DEFAULT_SINK@', shell=True, check=True, capture_output=True)
        self.modules.append(int(s.stdout))

        print('Modules successfully initialised')


    def speak_text(self):
        text = self.textEdit.toPlainText()

        text = process_text(text)
        print(f'Saying: {text}')

        if text:
            tts = gTTS(text, lang='en', tld='ca')

            try:
                tts.save('./out/message.mp3')
            except Exception as e:
                print('Text failed with API', e)

            s = subprocess.run('paplay ./out/message.mp3 --device=text-to-speech-virtual-mic-sink', shell=True, capture_output=True)
            if 'No such entity' in s.stderr.decode():
                print('No virtual microphone found, initialising mic')
                self.reset()
                self.speak_text()
                return

            self.textEdit.clear()

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
