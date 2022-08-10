import sys
from PyQt5.QtWidgets import * # QApplication, QtWidgets

# 클래스 oop
class qTemplate(QWidget):
    # 생성자:기본적으로 return값이 없어 none임
    def __init__(self) -> None:  # return하는 것 없음
        super( ).__init__( )  #q리젯을 상속받아 사용
        self.initUI( )

    def initUI(self) -> None:
        self.setGeometry(300,500,500,400 )  # 윈도우 자체가 축,,디스플레이 창도 x,y축으로 이루어짐
        self.setWindowTitle('QTemplate!!!')
        self.show( )

if __name__=='__main__':
    app = QApplication(sys.argv)
    ins = qTemplate( )
    app.exec_( )