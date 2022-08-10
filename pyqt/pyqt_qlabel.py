from cProfile import label
import sys
from PyQt5.QtWidgets import  * # QApplication, QWidget, QLabel, QHBoxLayout
from PyQt5.QtGui import * # QPainter, QColor, QFont
# from PyQt5.QtCore import *

# 클래스 OOP
class qTemplate(QWidget):
    # 생성자
    def __init__(self) -> None:
        super( ).__init__( )
        self.initUI( )

    # 화면정의를 위해 사용자 함수
    def initUI(self) -> None:
        self.addControls( )
        self.setGeometry(300,500,500,400 )
        self.setWindowTitle('Qlabel')
        self.show( )

    def addControls(self) -> None:
        self.setWindowIcon(QIcon('./pyqt/image/dog.png'))  # 윈도우아이콘 지정
        label1 = QLabel(' ', self) # ' '안에 창에 띄울 문구 작성
        label2 = QLabel(' ', self)
        label1.setStyleSheet(
            ('border-width:3px;'
             'border-style: solid;'
             'border-color: yellow;'
             'image: url(./pyqt/image/image1.png)')
            )
        label2.setStyleSheet(
            ('border-width:3px;'
             'border-style: dot-dot-dash;'
             'border-color: green;'
             'image: url(./pyqt/image/image2.png)')
        )
        box = QHBoxLayout( )
        box.addWidget(label1)
        box.addWidget(label2)

        self.setLayout(box)

if __name__=='__main__':
    app = QApplication(sys.argv)
    ins = qTemplate( )
    app.exec_( )

