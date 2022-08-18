import imp
from os import link
from re import search # Pyqt위한 import
import sys
from tkinter.tix import Tree
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from urllib.parse import quote # 네이버 openAPI위한 import
import urllib.request
import json
import webbrowser
import pandas as pd # csv 저장용

# 클래스 OOP
class qTemplate(QWidget):
    start = 1 # API 호출할때 시작하는 데이터 번호 -> 그 다음은 101, 
    max_display = 100 # 한페이지에 나올 데이터 수
    saveResult = [] # 저장할 때 담을 데이터리스트(딕셔너리) -> DateFrame으로 변경될 것
    
    # 생성자
    def __init__ (self) -> None: # 생성자
        super().__init__() 
        uic.loadUi('./pyqt03/navernews_2.ui', self) # 화면UI 변경
        self.initUI()
    
    def initUI(self) -> None:
        self.addControls()
        self.show()
    
    # 위젯 정의, 이벤트(signal) 처리
    def addControls(self) -> None:
        self.btnSearch.clicked.connect(self.btnSearchClicked)
        self.txtSearch.returnPressed.connect(self.btnSearchClicked) # enter키로 검색 실행하기
        self.tblResult.itemSelectionChanged.connect(self.tblResultSelected)
        # 220818 추가버튼 이벤트(signal) 처리
        self.btnNext.clicked.connect(self.btnNextClicked)
        self.btnSave.clicked.connect(self.btnSaveClicked)

    # 화살표버튼 누를때마다 다음페이지의 데이터를 가져오는 것
    def btnNextClicked(self) -> None:
        self.start = self.start + self.max_display
        self.btnSearchClicked()

    def btnSaveClicked(self) -> None:
        if len(self.saveResult) > 0:
            df = pd.DataFrame(self.saveResult)
            df.to_csv(f'./pyqt03/{self.txtSearch.text()}_뉴스검색결과.csv', encoding='utf-8', index=True)

        QMessageBox.information(self, '저장', '저장완료!')
        # 저장후 모든변수 초기화
        self.saveResult = [ ]
        self.start = 1
        self.txtSearch.setText(' ')
        self.lblStatus.setText('Data : ')
        self.lblStatus2.setText('저장할 데이터 > 0개')
        self.tblResult.setRowCount(0)
        self.btnNext.setEnabled(True)

    # tblResult창 클릭하면 해당 기사링크로 이동하는 함수
    def tblResultSelected(self) -> None:
        selected = self.tblResult.currentRow() # 현재 선택된 열의 인덱스
        link = self.tblResult.item(selected, 1).text() # tblResult창에서 index[1]인 주소를 가져오는 것
        webbrowser.open(link)     

    # 슬롯(이벤트핸들러)
    def btnSearchClicked(self) -> None:  
        jsonResult = []
        totalResult = []
        keyword = 'news'
        search_word = self.txtSearch.text()
        # QMessageBox.information(self, '결과', search_word)
        jsonResult = self.getNaverSearch(keyword, search_word, self.start, self.max_display)
        # print(jsonResult)

        for post in jsonResult['items']:
            totalResult.append(self.getPostData(post))
        # print(totalResult)
        self.makeTable(totalResult)

        # saveResult 값 할당, lblStatus,lblStatus2에 상태값 표시
        total = jsonResult['total']
        curr = self.start + self.max_display - 1
        self.lblStatus.setText(f'Data : {curr} / {total}')

        # saveResult 변수에 저장할 데이터 복사
        for post in totalResult:
            self.saveResult.append(post[0])

        self.lblStatus2.setText(f'저장할데이터 > {len(self.saveResult)}개')

        # 불러온 데이터가 1000건 이상이 될때 버튼 비활성화(UI오류 막기)
        if curr >= 1000:
            self.btnNext.setDisabled(True) # 화살표버튼 비활성화
        else: 
            self.btnNext.setEnabled(True) # 화살표버튼 활성화

        return 

    # 테이블위젯 설정
    def makeTable(self, result):
        self.tblResult.setSelectionMode(QAbstractItemView.SingleSelection) #pyqtDesigner에서 처리해도 가능
        self.tblResult.setColumnCount(2)
        self.tblResult.setRowCount(len(result)) # result가 50개면 50개 출력(displayCount에 따라서 변경, 현재는 50개로 고정)
        self.tblResult.setHorizontalHeaderLabels(['기사제목', '뉴스링크'])
        self.tblResult.setColumnWidth(0, 350)
        self.tblResult.setColumnWidth(1, 100)
        self.tblResult.setEditTriggers(QAbstractItemView.NoEditTriggers) # read only(읽기만 가능)

        i = 0
        for item in result:
            title = self.strip_tag(item[0]['title'])
            link = item[0]['originallink']
            self.tblResult.setItem(i, 0, QTableWidgetItem(title))
            self.tblResult.setItem(i, 1, QTableWidgetItem(link))
            i += 1

    # html tag 없애는 함수
    def strip_tag(self, title):
        ret = title.replace('&lt;', '<')
        ret = ret.replace('&gt;', '>')
        ret = ret.replace('&quot;', '"')
        ret = ret.replace('&apos;', "'")
        ret = ret.replace('&amp;', '&')
        ret = ret.replace('<b>', '')
        ret = ret.replace('</b>', '')
        return ret

    def getPostData(self, post):
        temp = []
        title= self.strip_tag(post['title'])
        originallink = post['originallink']
        link = post['link']
        description = post['description']
        pubDate = post['pubDate']

        temp.append({'title':title, 'originallink':originallink, 'link':link, 'description':description, 'pubDate':pubDate})

        return temp 

    # 핵심함수(Naver API 크롤링을 위한 함수)
    def getNaverSearch(self, keyword, search, start, display):
        url = f'https://openapi.naver.com/v1/search/{keyword}.json' \
              f'?query={quote(search)}&start={start}&display={display}'
        print(url)
        req = urllib.request.Request(url)
        # 네이버 인증 추가
        req.add_header('X-Naver-Client-Id', 'w2SrjIcbPlRew2exM0l8')
        req.add_header('X-Naver-Client-Secret', 'ZAkULrp9Ve')

        res = urllib.request.urlopen(req)
        if res.getcode() == 200:
            print('URL request Succeed')
        else:
            print('URL request Failed')

        ret = res.read().decode('utf-8')
        if ret == None:
            return None
        else:
            return json.loads(ret)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ins = qTemplate()
    app.exec_()