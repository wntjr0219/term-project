import requests
from tkinter import *
from tkinter import font
from tkinter import messagebox
import json

def search():
    keyword = e1.get()
    # Juso API 요청에 필요한 정보
    juso_url = "https://www.juso.go.kr/addrlink/addrLinkApi.do"
    juso_params = {
        "confmKey": "devU01TX0FVVEgyMDIzMDUyNjE1MDk0NjExMzgwNTA=",  # 발급받은 Juso API 키
        "currentPage": "1",
        "countPerPage": "10",
        "keyword": keyword,
        "resultType": "json"
    }
    juso_response = requests.get(juso_url, params=juso_params)
    juso_data = json.loads(juso_response.text)

    # 필요한 정보 추출
    results = juso_data.get("results")
    if results and results.get("common"):
        sidoCd = results["common"].get("sidoCd")
        sgguCd = results["common"].get("sgguCd")

        # 병원 정보 API 요청에 필요한 정보
        hospital_url = "http://apis.data.go.kr/B551182/hospInfoServicev2/getHospBasisList"
        hospital_params = {
            "serviceKey": "sea100UMmw23Xycs33F1EQnumONR/9ElxBLzkilU9Yr1oT4TrCot8Y2p0jyuJP72x9rG9D8CN5yuEs6AS2sAiw==",  # 발급받은 병원 정보 API 키
            "pageNo": "1",
            "numOfRows": "10",
            "sidoCd": sidoCd,
            "sgguCd": sgguCd
        }
        hospital_response = requests.get(hospital_url, params=hospital_params)
        hospital_data = json.loads(hospital_response.text)

        # 기존에 생성된 버튼들을 제거
        for button in frame2.winfo_children():
            button.destroy()

        hospitals = hospital_data.get("response").get("body").get("items").get("item")
        if hospitals:
            for hospital in hospitals:
                name = hospital.get("yadmNm")
                address = hospital.get("addr")
                tel = hospital.get("telno")
                info = f"병원 이름: {name}\n주소: {address}\n전화번호: {tel}\n"

                button = Button(frame2, text=info, font=TempFont, wraplength=300, justify="left")
                button.pack()
        else:
            messagebox.showinfo("검색 결과", "검색 결과가 없습니다.")
    else:
        messagebox.showinfo("검색 결과", "검색 결과가 없습니다.")

    



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

