import sys
from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 

# 클래스 oop
class qTemplate(QWidget):
    # 생성자
    def __init__(self) -> None:  
        super( ).__init__( ) 
        uic.loadUi('./pyqt02/Ttask.ui', self)
        self.initUI( )

    def initUI(self) -> None:
        self.addControls( )
        self.show( )

    def addControls(self) -> None:  
        self.btnStart.clicked.connect(self.btn1_clicked)   # 시그널 연결

    def btn1_clicked(self):                    # 시그널 연결 
        self.txbLog.append('실행!!!')
        self.pgbTask.setRange(0, 99)
        for i in range(0,100):                     # 응답없음 발생
            print(f'출력 : {i}')
            self.pgbTask.setValue(i)
            self.txbLog.append(f'출력>{i}')

if __name__=='__main__':
    app = QApplication(sys.argv)
    ins = qTemplate( )
    app.exec_( )