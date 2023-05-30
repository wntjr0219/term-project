import requests
from tkinter import *
from tkinter import font
from tkinter import messagebox
import xml.etree.ElementTree as ET

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
            button.configure(command=lambda r=item: show_hospital())
    else:  # 결과가 없는 경우
        messagebox.showinfo("검색 결과", "검색 결과가 없습니다.")

def show_hospital():
    pass

window = Tk() # 부모창
window.title("주소정보")
window.geometry('400x350')
TempFont = font.Font(size=10, weight='bold', family='Consolas') # 기본 폰트

frame1 = Frame(window) # 검색 프레임
frame1.pack()

frame2 = Frame(window) # 버튼 프레임
frame2.pack()

# 검색 프레임
l1 = Label(frame1,text="주소를 입력하시오(최소 구까지)", font=TempFont) # , font='helvetica 16 italic'
l1.pack()  
b1 = Button(frame1,text="찾기", font=TempFont, command=search)
b1.pack(side="left")  
e1 = Entry(frame1,width=30, bg='white', fg='black')
e1.pack(side="left")  


window.mainloop()