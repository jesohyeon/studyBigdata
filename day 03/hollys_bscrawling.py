# 할리스 커피숍 매장정보 크롤링

from bs4 import BeautifulSoup
import urllib.request  # url에 요청
import pandas as pd
import datetime

def getHollysStoreInfo(result):

    for page in range(1, 54):
        Hollys_url = f'https://www.hollys.co.kr/store/korea/korStore2.do?pageNo={page}'
        # print(Hollys_url)
        html = urllib.request.urlopen(Hollys_url)
        soup = BeautifulSoup (html, 'html.parser')
        tbody = soup.find ('tbody')

        for store in tbody.find_all ('tr'):
                if len(store) <= 3: break

                store_td = store.find_all('td')

                store_name = store_td[1].string
                store_sido = store_td[0].string
                store_address = store_td[3].string
                store_phone = store_td[5].string
                result.append([store_name]+[store_sido]+[store_address]+[store_phone])

# result
print('완료!')

#작업결과 저장 리스트 준비
def main():
    result = [ ]
    print('할리스 매장 크롤링 >>>')
    getHollysStoreInfo(result)

    # 판다스 데이터프레임 생성
    columns = ['store', 'sido-gu', 'address', 'phone']
    hollys_df = pd.DataFrame(result, columns=columns)

    # csv 저장
    hollys_df.to_csv('./hollys_shop_info.csv', index=True, encoding='utf-8') # 상대경로
    # hollys_df.to_csv('C:/studyBigdata/studyBigdata/day 03/hollys_shop_info.csv', index=True, encoding='utf-8') # 절대경로

    print('저장완료')

    del result[:]

if __name__ == '__main__':
    main()