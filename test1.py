import requests
from tkinter import *
from tkinter import font
from tkinter import messagebox
import xml.etree.ElementTree as ET
# 텔레그램
import time
import sqlite3
import telepot
from pprint import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta
import traceback

TOKEN = '6028126971:AAEY-4bSA1i_nQ0DuYoT_-VMVWzqnsFi-JY'

def search():
    keyword = e1.get()
    # API 요청에 필요한 정보
    url = "https://www.juso.go.kr/addrlink/addrLinkApi.do"  # API 엔드포인트 URL
    params = {
        "confmKey": "devU01TX0FVVEgyMDIzMDUyNjE1MDk0NjExMzgwNTA=",  # 발급받은 API 키
        "currentPage": "1",  # 조회할 페이지 번호
        "countPerPage": "10",  # 페이지당 결과 수
        "keyword": keyword,  # 검색할 키워드
        "resultType": "xml"  # 응답 형식 (json 또는 xml)
    }
    response = requests.get(url, params=params)
    root = ET.fromstring(response.text)
    
     # 기존에 생성된 버튼들을 제거
    for button in frame2.winfo_children():
        button.destroy()

    items = root.findall(".//juso")
    if items:
        for item in items:
            roadAddr = item.findtext("roadAddr")
            button = Button(frame2, text=roadAddr, font=TempFont)
            button.pack()
            button.configure(command=lambda r=item: show_hospital(r))
    else:  # 결과가 없는 경우
        messagebox.showinfo("검색 결과", "검색 결과가 없습니다.")

def show_hospital(result):
    url = 'http://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList'
    service_key = "sea100UMmw23Xycs33F1EQnumONR/9ElxBLzkilU9Yr1oT4TrCot8Y2p0jyuJP72x9rG9D8CN5yuEs6AS2sAiw=="
    # queryParams = {'serviceKey': service_key, 
    #                'pageNo': '1', 
    #                'numOfRows': '10', 
    #                'sidoCd': '110000', 
    #                'sgguCd': '110019'}

    # response = requests.get(url, params=queryParams)
    # root = ET.fromstring(response.text)

  

    # row_count = 1
    # for item in root.iter("item"):
    #     yadmNm = item.findtext("yadmNm")
    #     addr = item.findtext("addr")
    #     telno = item.findtext("telno")
        
    #     data = [yadmNm, addr, telno]
    #     for i, value in enumerate(data):
    #         label = Label(frame, text=value, font=TempFont2)
    #         label.grid(row=row_count, column=i)
    
    #     row_count += 1

    window2 = Toplevel(window)  # 병원 정보
    window2.geometry('800x600')
    window2.title("병원정보")
    TempFont2 = font.Font(window2, size=10, weight='bold', family='Consolas') # 윈도우2 기본 폰트 

   
    win2_frame = Frame(window2)
    win2_frame.pack()

    header = ["병원 이름", "주소", "Tel"]

    for i, col_name in enumerate(header):
        label = Label(win2_frame, text=col_name, font=TempFont2)
        label.grid(row=0, column=i)

    sidoCd = result.findtext("siCd")  # 시도 코드
    sgguCd = result.findtext("sggCd")  # 시군구 코드
    keyword = result.findtext("roadAddr")  # 검색할 키워드

    url = "http://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList"
    params = {
        "serviceKey": service_key,  # 발급받은 API 키
        "pageNo": "1",  # 조회할 페이지 번호
        "numOfRows": "10",  # 페이지당 결과 수
        "sidoCd": sidoCd,  # 시도 코드
        "sgguCd": sgguCd,  # 시군구 코드
        "emdongNm": keyword,  # 검색할 읍면동 이름
    }
    response = requests.get(url, params=params)
    root = ET.fromstring(response.text)

    hospitals = root.findall(".//item")
    if hospitals:
        for hospital in hospitals:
            name = hospital.findtext("yadmNm")  # 병원 이름
            address = hospital.findtext("addr")  # 병원 주소
            tel = hospital.findtext("telno")  # 병원 전화번호
        
def getData(juso):
    res_list = []
    keyword = juso # 인자로 받은 것으로 교체 
    # API 요청에 필요한 정보
    url = "https://www.juso.go.kr/addrlink/addrLinkApi.do"  # API 엔드포인트 URL
    params = {
        "confmKey": "devU01TX0FVVEgyMDIzMDUyNjE1MDk0NjExMzgwNTA=",  # 발급받은 API 키
        "currentPage": "1",  # 조회할 페이지 번호
        "countPerPage": "10",  # 페이지당 결과 수
        "keyword": keyword,  # 검색할 키워드
        "resultType": "xml"  # 응답 형식 (json 또는 xml)
    }
    response = requests.get(url, params=params)
    root = ET.fromstring(response.text)
    
    items = root.findall(".//juso")
    if items:
        for item in items:
            roadAddr = item.findtext("roadAddr")
            res_list.append(roadAddr)
        return res_list
    else:  # 결과가 없는 경우
        messagebox.showinfo("검색 결과", "검색 결과가 없습니다.")

    # res_list = []
    # url = baseurl+'&LAWD_CD='+loc_param+'&DEAL_YMD='+date_param
    # #print(url)
    # res_body = urlopen(url).read()
    # #print(res_body)
    # soup = BeautifulSoup(res_body, 'html.parser')
    # items = soup.findAll('item')
    # for item in items:
    #     item = re.sub('<.*?>', '|', item.text)
    #     parsed = item.split('|')
    #     try:
    #         row = parsed[3]+'/'+parsed[6]+'/'+parsed[7]+', '+parsed[4]+' '+parsed[5]+', '+parsed[8]+'m², '+parsed[11]+'F, '+parsed[1].strip()+'만원\n'
    #     except IndexError:
    #         row = item.replace('|', ',')

    #     if row:
    #         res_list.append(row.strip())
    # return res_list


    
window = Tk() # 부모 창
window.title("주소정보")
window.geometry('400x350')
TempFont = font.Font(size=10, weight='bold', family='Consolas') # 기본 폰트


frame1 = Frame(window) # 검색 프레임
frame1.pack()

frame2 = Frame(window) # 버튼 프레임
frame2.pack()

l1 = Label(frame1,text="주소를 입력하시오(최소 구까지)", font=TempFont)
l1.pack()  
b1 = Button(frame1,text="찾기", font=TempFont, command=search)
b1.pack(side="left")  
e1 = Entry(frame1,width=30, bg='white', fg='black')
e1.pack(side="left")  

window.mainloop()
