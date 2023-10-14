# https://goodthings4me.tistory.com/552


import Stock_main
import Tracking_main
from tkinter import *

window = Tk()
window.title('2028 Stock Project')
window.geometry('550x245')

#  Main_Frame

stockFrame=LabelFrame(window, text='Stock Main', width=480,height=120)
stockFrame.place(x=35,y=10)
# stockFrame.pack(padx=20,pady=20)

stock_nameLabel = Label(stockFrame,text='종목이름')
stock_nameLabel.place(x=130,y=50)

stock_codeLabel = Label(stockFrame,text='종목코드')
stock_codeLabel.place(x=130,y=75)

name_entry = Entry(stockFrame,width=20,relief='solid')
name_entry.place(x=200,y=50)

code_entry = Entry(stockFrame,width=20,relief='solid')
code_entry.place(x=200,y=75)

def call_getTodayData():
    Stock_main.getTodayData(name_entry.get(),code_entry.get())
def call_getAllChanges():
    Stock_main.getAllChanges(name_entry.get(),code_entry.get())
                
btn1=Button(stockFrame, text='금일 상한가', padx=20, command=Stock_main.today_upper)
btn2=Button(stockFrame, text='종목분석', padx=20, command=call_getTodayData)
btn3=Button(stockFrame, text='거래량전체', padx=20, command=call_getAllChanges)
btn4=Button(stockFrame, text='MyList 분석', padx=20, command=Stock_main.checkMyList)

btn1.place(x=10,y=5)
btn2.place(x=125,y=5)
btn3.place(x=225,y=5)
btn4.place(x=335,y=5)

#  Traking_Frame
trakingFrame=LabelFrame(window, text='Tracking', width=480,height=60)
trakingFrame.place(x=35,y=140)

btn5=Button(trakingFrame, text='Today_Tracking', padx=20, command=Tracking_main.tracking)
btn5.place(x=110,y=5)

btn6=Button(trakingFrame, text='MyList', padx=20)
btn6.place(x=250,y=5)

mainloop()