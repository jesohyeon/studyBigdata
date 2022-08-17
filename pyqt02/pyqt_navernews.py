import sys
from turtle import update
from PyQt5 import uic
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import time

# UI 스레드와 작업스레드 분리
class Worker(QThread):
    # QThread는 화면을 그릴 권한이 없음.
    # 대신 통신을 통해서 UI스레드가 그림을 그릴 수 있도록 통신수행
    valChangeSignal = pyqtSignal(int)

    def __init__(self, parent):  
        super( ).__init__(parent)
        self.parent = parent
        self.working = True

    def run(self):
        while self.working:
            for i in range(0, 100000):
                print(f'출력 : {i}')
                # self.pgbTask.setValue(i)
                # self.txbLog.append(f'출력>{i}') 
                self.valChangeSignal.emit(i)  # UI스레드야 화면은 너가 그려줘~
                time.sleep(0.0001) # 1micro sec

# 클래스 oop
class qTemplate(QWidget):
    # 생성자
    def __init__(self) -> None:  
        super( ).__init__( ) 
        uic.loadUi('./pyqt02/navernews.ui', self)
        self.initUI( )

    def initUI(self) -> None:
        self.addControls( )
        self.show( )

    def addControls(self) -> None:  
        pass

if __name__=='__main__':
    app = QApplication(sys.argv)
    ins = qTemplate( )
    app.exec_( )