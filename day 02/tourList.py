import os
import sys
import urllib.request
import datetime
import time
import json
import pandas as pd

ServiceKey="Ody77GLuYeR%2FeFqbpduMN2Bi4Cka2fztbgnj6E2Eux1kUhy3e4epR28XKBUaObiqPoVzAizxXMBPXtMyuC9v9Q%3D%3D"

def getRequestUrl(url):
    req = urllib.request.Request(url)
    try:
        res = urllib.request.urlopen(req)  
        if res.getcode() == 200:
            print(f'[{datetime.datetime.now()}] Url Request success')
            return res.read().decode('utf-8')
    except Exception as e:
        print(e)
        print(f'[{datetime.datetime.now()}] Error for URL : {url}')
        return None

# 202201, 110, D(get값, post값)
def getTourismStatsItem(yyyymm, nat_cd, ed_cd):
    service_url = 'http://openapi.tour.go.kr/openapi/service/EdrcntTourismStatsService/getEdrcntTourismStatsList'
    params = f'?_type=json&serviceKey={ServiceKey}'  #?한번만 뒤에 다 &
    params += f'&YM={yyyymm}'
    params += f'&NAT_CD={nat_cd}'
    params += f'&ED_CD={ed_cd}'
    url = service_url + params

    # print(url)
    retData = getRequestUrl(url)

    if (retData == None):
        return None
    else:
         return json.loads(retData)

def getTourismStatsService(nat_cd, ed_cd, nStartYear, nEndYear):
    jsonResult = []  #리스트로 만듦
    result = []
    natName=''  #국가이름은 문자열로 응답
    dataEND = f"{nEndYear}{12:}0>2" #데이터 끝 초기화
    isDataEnd = False #데이터 끝 확인용 flag 초기화    
    
    for year in range(nStartYear, nEndYear+1):       # range는 마지막 -1에서 끝나서 
        for month in range(1, 13):
            if(isDataEnd == 1): break 

            yyyymm = f"{year}{str(month):0>2}"  # 2022 1월 202201          
            jsonData = getTourismStatsItem(yyyymm, nat_cd, ed_cd) 

            if jsonData['response']['header']['resultMsg'] == 'OK':               
                # 데이터가 없는 경우 수집종료
                if jsonData['response']['body']['items'] == ' ':    # 빈 값이면 끝
                    isDataEnd = True #데이터 끝 flag 설정
                    dataEND = f'{year}{str(month)-1:0>2}'
                    print(f"제공되는 통계 데이터는 {year}년 {month-1}월까지입니다.")
                    break                
                #jsonData를 출력하여 확인......................................................
                print (json.dumps(jsonData, indent=4, sort_keys=True, ensure_ascii=False))
                natName = jsonData['response']['body']['items']['item']['natKorNm']
                natName = natName.replace(' ', '')  # 중간 공백 2칸 없애줌
                num = jsonData['response']['body']['items']['item']['num']  
                ed = jsonData['response']['body']['items']['item']['ed']
                print('[ %s_%s : %s ]' %(natName, yyyymm, num))
                print('----------------------------------------------------------------------')                
                jsonResult.append({'nat_name': natName, 'nat_cd': nat_cd,
                                 'yyyymm': yyyymm, 'visit_cnt': num})
                result.append([natName, nat_cd, yyyymm, num])
                
    return (jsonResult, result, natName, ed, dataEND)

def main():
    jsonResult = []
    result = []
    natName=''
    print('<<국내 입국한 외국인 통계데이터를 수집합니다 >>')
    nat_cd = input('국가 코드를 입력하세요(중국: 112 / 일본: 130 / 미국: 275) : ')
    nStartYear =int(input('데이터를 몇 년부터 수집할까요? : '))
    nEndYear = int(input('데이터를 몇 년까지 수집할까요? : '))
    ed_cd = "E"     #E : 방한외래관광객, D : 한국인 해외 출국
    
    (jsonResult, result, natName, ed, dataEND) =\
    getTourismStatsService(nat_cd, ed_cd, nStartYear, nEndYear)

    if (natName=='') : #URL 요청은 성공하였지만, 데이터 제공이 안된 경우
        print('데이터가 전달되지 않았습니다. 공공데이터포털의 서비스 상태를 확인하기 바랍니다.')
    else:
        pass
    # #파일저장 1 : json 파일       
    # with open('./%s_%s_%d_%s.json' % (natName, ed, nStartYear, dataEND), 'w', 
    #             encoding='utf8') as outfile:
    #     jsonFile  = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)
    #     outfile.write(jsonFile)
    # #파일저장 2 : csv 파일   
    # columns = ["입국자국가", "국가코드", "입국연월", "입국자 수"]
    # result_df = pd.DataFrame(result, columns = columns)
    # result_df.to_csv('./%s_%s_%d_%s.csv' % (natName, ed, nStartYear, dataEND),
    #             index=False, encoding='cp949')


if __name__ == '__main__':
    main()