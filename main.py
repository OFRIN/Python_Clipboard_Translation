# Copyright (C) 2019 * Ltd. All rights reserved.
# author : SangHyeon Jo <josanghyeokn@gmail.com>

import sys
import PyQt5
import ctypes
import pyperclip

from googletrans import Translator

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# Windows API
def get_mouse_position():
    class POINT(ctypes.Structure):
        _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

    pt = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y

# PyQt5
class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'ENG -> KOR Translation'

        self.translator = Translator()
        self.last_clip_text = pyperclip.paste()

        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 50

        self.initUI()

        # 1. Timer (translate)
        self.timer = QTimer()
        self.timer.setInterval(10) # 10ms - scan clipboard 
        self.timer.timeout.connect(self.translate)
        self.timer.start()
        
    def initUI(self):
        self.font = QFont()
        self.font.setBold(True)

        self.label_1 = QLabel()
        self.label_1.setText('Hello')
        self.label_1.setFont(self.font)
        self.setCentralWidget(self.label_1)

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.yellow)
        self.setPalette(p)
        
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

    def translate(self):
        self.timer.stop()

        clip_text = pyperclip.paste()
        if clip_text == self.last_clip_text:
            self.timer.start()
            return
        
        mouse_x, mouse_y = get_mouse_position()
        self.last_clip_text = clip_text

        words = clip_text.split()
        if len(words) == 0:
            self.timer.start()
            return

        search_string = ' '.join(words)
        if self.translator.detect(search_string).lang != 'en':
            self.timer.start()
            return

        output = self.translator.translate(search_string, src = 'en', dest = 'ko')
        translate_string = output.text

        f = open('histroy.csv', 'a+', encoding = 'utf-8')
        f.write('{},{}\n'.format(search_string, translate_string))
        f.close()

        self.label_1.setGeometry(QRect(0, 0, len(translate_string) * 2, 25))
        self.label_1.setText(output.text)
        
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setGeometry(mouse_x, mouse_y + 20, len(translate_string) * 2 + 10, 25)
        self.show()
        
        self.timer.start()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.hide()

# main
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    app.exec_()