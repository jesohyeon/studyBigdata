import sys
from PyQt5.QtWidgets import * # QApplication, QtWidgets
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import *

# 클래스 OOP
class qTemplate(QWidget):
    # 생성자
    def __init__(self) -> None:
        super( ).__init__( )
        self.initUI( )

    # 화면정의를 위해 사용자 함수
    def initUI(self) -> None:
        self.setGeometry(300,500,500,400 )
        self.setWindowTitle('QTemplate!!!')
        self.text='What a Wonderful world~'
        self.show( )

    def paintEvent(self, event) -> None:
        paint = QPainter()
        paint.begin(self)
        # 그리는 함수 추가
        self.drawText(event,paint)
        paint.end( )

    # 텍스트 그리기 위한 사용자 함수
    def drawText(self,event,paint):
        paint.setPen(QColor(50,50,50))
        paint.setFont(QFont('NanumGothic', 20))
        paint.drawText(105,100,'GOOD WORLD')  # 글자를 그린것
        paint.setPen(QColor(0,250,10))
        paint.setFont(QFont('Impact', 20))
        paint.drawText(event.rect(), Qt.AlignCenter, self.text)

if __name__=='__main__':
    app = QApplication(sys.argv)
    ins = qTemplate( )
    app.exec_( )

