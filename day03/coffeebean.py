# selenium사용 웹페이지 크롤링
# 패키지로드

from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import datetime
from selenium import webdriver
import time

def getCoffeeBeanStoreInfo(result):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    wd = webdriver.Chrome('./day03/chromedriver.exe', options=options)
    #크롬 웹드라이버 객체 생성
    # wd = webdriver.Chrome('./day03/chromedriver.exe') # 경로조심!

    for i in range(1,11): #매장 수만큼 반복
        wd.get('https://www.coffeebeankorea.com/store/store.asp')
        time.sleep(1)  # 팝업표시후에 크롤링이 안되서 브라우저가 닫히는 것을 방지

        try:
            wd.execute_script(f"storePop2('{i}')")
            time.sleep(0.5)
            html = wd.page_source
            soup = BeautifulSoup(html, 'html.parser')
            store_name = soup.select('div.store_txt > h2')[0].string
            print(store_name)
            store_info = soup.select('table.store_table > tbody > tr >td')
            store_address_list = list(store_info[2])
            store_address = store_address_list[0]
            store_contact = store_info[3].string
            result.append([store_name]+[store_address]+[store_contact]) 

        except Exception as e:
            print(e)
            continue
        
def main():
    result=[]
    print('커피빈 매장 크롤링 >>> ')
    getCoffeeBeanStoreInfo(result)

    #판다스 데이터프레임 생성
    columns = ['store','address', 'phone']
    coffeebean_df = pd.DataFrame(result, columns=columns)
    #csv 저장
    coffeebean_df.to_csv('./coffeeBean_info.csv', index=True, encoding='utf-8')
    # C:\studyBigdata\studyBigdata\day 03\chromedriver.exe

    del result[:]

if __name__ == '__main__':
    main()