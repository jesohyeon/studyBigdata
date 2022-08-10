# 가장 심플한 PyQt 실행방법
from cProfile import label
from PyQt5 import QtWidgets as qw

def run():
   app = qw.QApplication([])
   wnd = qw.QMainWindow()
   label = qw.QLabel('Hello Qt!')
   wnd.setCentralWidget(label) # 중간에 label을 넣음
   wnd.show()
   app.exec_() # 실행

if __name__ == '__main__':
   run()