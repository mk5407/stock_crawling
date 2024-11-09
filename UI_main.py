# https://goodthings4me.tistory.com/552

import Stock_main
import Tracking_main
from tkinter import *


window = Tk()
window.title('2028 Stock Project')
window.geometry('600x330')

#  Main_Frame

stockFrame=LabelFrame(window, text='Stock Main', width=550,height=150)
stockFrame.place(x=35,y=10)
# stockFrame.pack(padx=20,pady=20)

stock_nameLabel = Label(stockFrame,text='종목이름')
stock_nameLabel.place(x=200,y=50)

stock_codeLabel = Label(stockFrame,text='종목코드')
stock_codeLabel.place(x=200,y=75)

name_entry = Entry(stockFrame,width=20,relief='solid')
name_entry.place(x=300,y=50)

code_entry = Entry(stockFrame,width=20,relief='solid')
code_entry.place(x=300,y=75)

def call_getTodayData():
    Stock_main.getTodayData(name_entry.get(),code_entry.get())
def call_getAllChanges():
    Stock_main.getAllChanges(name_entry.get(),code_entry.get())
def call_showChart():
    Stock_main.ShowStockChart(name_entry.get(),code_entry.get())
                
btn1=Button(stockFrame, text='금일 상한가', padx=20, command=Stock_main.today_upper)
btn2=Button(stockFrame, text='종목분석', padx=20, command=call_getTodayData)
btn3=Button(stockFrame, text='거래량전체', padx=20, command=call_getAllChanges)
btn4=Button(stockFrame, text='Chart보기', padx=20, command=call_showChart)
btn5=Button(stockFrame, text='금일 거래량', padx=20, command=Stock_main.today_top_trading)
btn6=Button(stockFrame, text='골든 크로스', padx=20, command=Stock_main.golden_cross)

btn1.place(x=10,y=5)
btn2.place(x=150,y=5)
btn3.place(x=270,y=5)
btn4.place(x=400,y=5)
btn5.place(x=10,y=40)
btn6.place(x=10,y=75)

#  Traking_Frame
trakingFrame=LabelFrame(window, text='Tracking', width=550,height=120)
trakingFrame.place(x=35,y=180)


def call_VerifyMyList():
    Stock_main.checkMyList("stock_list.txt")

def call_VerifyNewList():
    Stock_main.checkMyList("test_list.txt")

def call_AllinOne():
    Stock_main.today_upper()
    Stock_main.today_top_trading()
    Stock_main.golden_cross()
    # Tracking_main.tracking()

btn7=Button(trakingFrame, text='Today_Tracking', padx=20, command=Tracking_main.tracking)
btn7.place(x=30,y=5)

btn8=Button(trakingFrame, text='MyList 분석', padx=20, command=call_VerifyMyList)
btn8.place(x=200,y=5)

btn9=Button(trakingFrame, text='NewList 분석', padx=20, command=call_VerifyNewList)
btn9.place(x=340,y=5)

btn10=Button(trakingFrame, text='AllinOne', padx=10, width=46, command=call_AllinOne)
btn10.place(x=30,y=50)

mainloop()