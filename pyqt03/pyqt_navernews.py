from ast import keyword
import json
import sys
from turtle import update
import webbrowser
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
    start = 1 # api호출할 때 시작하는 데이터 시작번호
    max_display = 100  # 한 페이지에 나올 데이터 수
    saveResult = [ ]   # 저장할 때 담을 데이터(딕셔너리 리스트) -> DataFrame

    # 생성자
    def __init__(self) -> None:  
        super( ).__init__( ) 
        uic.loadUi('./pyqt03/navernews_2.ui', self)  # 화면 UI 변경
        self.initUI( )

    def initUI(self) -> None:
        self.addControls( )
        self.show( )

    def addControls(self) -> None:  
        self.btnSearch.clicked.connect(self. btnSearchClicked)
        self.txtSearch.returnPressed.connect(self.btnSearchClicked)
        self.tblResult.itemSelectionChanged.connect(self.tblResultSelectted)
        # 22.08.18 추가버튼 이벤트(시그널) 확장
        self.btnNext.clicked.connect(self.btnNectClicked)
        self.btnSave.clicked.connect(self.btnSaveClicked)

    def btnNextClicked(self) -> None:
        self.start = self.start + self.max_display

    def btnSaveClicked(self) -> None:
        pass
    
    def tblResultSelectted(self) -> None:
        selected = self.tblResult.currentRow( ) # 현재 선택된 열의 인덱스
        link = self.tbnResult.item(selected, 1).text()
        webbrowser.open(link)

def btnSearchClicked(self) -> None:  #슬롯(이벤트핸들러)
    jsonResult = [ ]
    totalResult = [ ]
    keyword = 'news'
    search_word = self.txtSearch.txt()

    # QMessageBox.information(self, '결과', search_word, self.start, self.max_display)
    jsonResult = self.getNaverSearch(keyword, search_word, self.start, self.max_display)

    for post in jsonResult['items']:
        totalResult.append(self.getPostData(post))

    self.makeTable(totalResult)

    total = jsonResult['total']
    curr = self.start + self.max_display - 1

    self.lblStatus.setText(f'Data : {curr} / {total}')


if __name__=='__main__':
    app = QApplication(sys.argv)
    ins = qTemplate( )
    app.exec_( )


