import sys
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 

# 클래스 oop
class qTemplate(QWidget):
    # 생성자
    def __init__(self) -> None:  
        super( ).__init__( )  
        self.initUI( )

    def initUI(self) -> None:
        self.addControls( )
        self.setGeometry(300,100,640,400 )  
        self.setWindowTitle('QPushbutton 예제')
        self.show( )

    def addControls(self) -> None:
        self.btn1 = QPushButton('메세지', self)
        self.btn1.setGeometry(10,10,600,40)
        self.btn1 = QPushButton('클릭', self)
        self.btn1.setGeometry(510,350,120,40)
        self.btn1.clicked.connect(self.btn1_clicked)   # 시그널 연결

    # event = signal (python)
    def btn1_clicked(self):                    # 시그널 연결 : 메세지박스 종류 3가지
        QMessageBox.information(self, 'signal', 'self.btn1_clicked!!!')  # 일반정보창
        # QMessageBox.warning(self, 'signal', 'self.btn1_clicked!!!')     # 경고창
        self.label.setText('메세지 : bnt1 버튼 클릭!!!')
        # QMessageBox.critical(self, 'signal', 'self.btn1_clicked!!!')        # 에러창

if __name__=='__main__':
    app = QApplication(sys.argv)
    ins = qTemplate( )
    app.exec_( )