import imp
import os
import re
import sys
from unittest import result
import urllib.request
import datetime
import time
import json
from colorama import Cursor
from debugpy import connect
from numpy import column_stack
import pandas as pd
import pymysql


ServiceKey="eNbNqklUmut9QHy%2FK%2FF42wH0tsx0YOWDDBy1ZAOwRXJrRTPOtDl%2Fiv7fHCZqEdODXCHrHQd4h2pws7FeJRGTaA%3D%3D"

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
def getGalmatgiInfo():
    service_url = 'http://apis.data.go.kr/6260000/fbusangmgcourseinfo/getgmgcourseinfo'
    params = f'?serviceKey={ServiceKey}'  #?한번만 뒤에 다 &
    params += f'&numOfRows=10'  #한번에 볼수있는 페이지 수
    params += f'&pageNo=1'
    params += f'&resultType=json'
    url = service_url + params

    retData = getRequestUrl(url)

    if (retData == None):
        return None
    else:
         return json.loads(retData)

def getGalmatgilService():
    result = []
    
    jsonData = getGalmatgiInfo()
    # print(jsonData)
    if jsonData['getgmgcourseinfo']['header']['code'] == '00':
        if jsonData['getgmgcourseinfo']['item'] == '':
            print('서비스 오류!!')
        else:
            for item in jsonData['getgmgcourseinfo']['item']:
                seq =item['seq']
                course_nm = item['course_nm']
                gugan_nm =  item['gugan_nm']
                gm_range = item['gm_range']
                gm_degree = item['gm_degree']
                start_pls = item['start_pls']
                start_addr = item['start_addr']
                middle_pls = item['middle_pls']
                middle_adr =  item['middle_adr']
                end_pls =  item['end_pls']
                end_addr =  item['end_addr']
                gm_course =  item['gm_course']
                gm_text =  item['gm_text']

                result.append([seq, course_nm, gugan_nm, gm_range, gm_degree, 
                                        start_pls, start_addr, middle_pls, middle_adr, end_pls, end_addr, gm_course, gm_text])

    return result

def main():
    result = []

    print('부산 갈맷길 정보 조회합니다.')
    result = getGalmatgilService()

    if len(result) >0:
        # csv 파일저장
        columns = ['seq', 'course_nm','gugan_nm', 'gm_range', 'gm_degree', 'start_pls', 'start_addr', 'middle_pls', 'middle_adr','end_pls', 'end_addr', 'gm_course', 'gm_text']
        result_df = pd.DataFrame(result, columns = columns)
        result_df.to_csv(f'./부산갈맷길 정보.csv', index=False, encoding='cp949')

    #DB 저장
    connection = pymysql.connect(host='localhost',
                                                    user='root',
                                                    password='1234',
                                                    db='test')
    Cursor = connection.cursor()

    #컬럼명 동적으로 만들기
    cols='`,`'.join([str(i) for i in result_df.columns.tolist()])

    for i, row in result_df.iterrows():
        sql = 'INSERT INTO `galmatgil_info` (`'+ cols +'`)  VALUES ('+' %s, '*(len(row)-1) + "%s) "
        Cursor.execute(sql, tuple(row))

    connection.commit()

    print('DB 저장완료')
    connection.close()

if __name__ == '__main__':
    main()
