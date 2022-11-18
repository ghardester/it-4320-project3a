'''
This web service extends the Alphavantage api by creating a visualization module, 
converting json query results retuned from the api into charts and other graphics. 
This is where you should add your code to function query the api
'''
import requests
from datetime import datetime
from datetime import date
import pygal
from flask import request

#Helper function for converting date


def convert_date(str_date):
    return datetime.strptime(str_date, '%Y-%m-%d').date()


def StockFunc():
    global StepData
    global symbol
    global time_series
    global URL
    StepData = ''
    symbol = request.form['symbol']
    time_series = request.form['time_series']
    Function = ['function=TIME_SERIES_INTRADAY','function=TIME_SERIES_DAILY_ADJUSTED','function=TIME_SERIES_WEEKLY','function=TIME_SERIES_MONTHLY']
    DictSeries =['Time Series (60min)', 'Time Series (Daily)', 'Weekly Time Series', 'Monthly Time Series']
    if int(time_series)-1 == 0:
        URL = 'https://www.alphavantage.co/query?'+ Function[int(time_series)-1] +'&interval=60min'+ '&symbol=' + symbol +'&apikey=7CKUYMD19R6Q9LKW'
    elif int(time_series)-1 == 1 or int(time_series)-1 == 2 or int(time_series)-1 == 3:
        URL = 'https://www.alphavantage.co/query?'+ Function[int(time_series)-1] + '&symbol=' + symbol +'&apikey=7CKUYMD19R6Q9LKW'
    DataDic = requests.get(URL)
    data = DataDic.json()
    StepData = data[DictSeries[int(time_series)-1]]
    print(URL)
    PopChart()

def PopChart():
    global chartvar
    global StepData
    global symbol
    global time_series
    global Close 
    global Date 
    global High
    global Low 
    global Open
    global chart_type
    global start_date
    global end_date
    global chart
    global Input
    global SecondInput
    Input=None
    SecondInput=None
    Index = ""
    Index2 =""
    chart_type = request.form['chart_type']
    chart = None
    Close =[]
    Date =[]
    High = []
    Low =[]
    Open =[]
    
    if int(time_series)-1 == 0: 
        Input = (request.form['start_date'] + ' 01:00:00')
        SecondInput = (request.form['end_date']+ ' 20:00:00')
        startDate()
        endDate()
        Index = startDate()
        Index2 = endDate()
        start_date = Input
        end_date = SecondInput
        Index = list(StepData).index(start_date)
        Index2 = list(StepData).index(end_date)
    elif int(time_series)-1 == 1 or int(time_series)-1 == 2 or int(time_series)-1 == 3:
        Input = request.form['start_date']
        if (Input in list(StepData)):
            start_date = Input
        else:
            while (Input in list(StepData)) == False:
                dateArray = Input.split('-')
                DayNum = int(dateArray[2])
                MonthNum = int(dateArray[1])
                if DayNum == 31:
                    DayNum = 0
                    MonthNum = MonthNum + 1
                    Input = (dateArray[0] + '-' + str(MonthNum).zfill(2) + '-' + str(DayNum).zfill(2))
                else:
                    DayNum = DayNum + 1
                    Input = (dateArray[0] + '-' + str(MonthNum).zfill(2) + '-' + str(DayNum).zfill(2))
            start_date = Input
        Index = list(StepData).index(start_date)
        SecondInput = request.form['end_date']
        if (SecondInput in list(StepData)):
            end_date = SecondInput
        else:
            while (SecondInput in list(StepData)) == False:
                dateArray = SecondInput.split('-')
                DayNum = int(dateArray[2])
                MonthNum = int(dateArray[1])
                if DayNum == 00:
                    DayNum = 31
                    MonthNum = MonthNum - 1
                    SecondInput = (dateArray[0] + '-' + str(MonthNum).zfill(2) + '-' + str(DayNum).zfill(2))
                else:
                    DayNum = DayNum - 1
                    SecondInput = (dateArray[0] + '-' + str(MonthNum).zfill(2) + '-' + str(DayNum).zfill(2))
            end_date = SecondInput
        Index2 = list(StepData).index(end_date)
        
    if Index > Index2:
        Value = list(StepData.values())[Index2]
    while Index2-1 < Index:
        Value = list(StepData.values())[Index2]
        Date.append(str(list(StepData.keys())[Index2]))
        Open.append(int(float(Value.get('1. open'))))
        High.append(int(float(Value.get('2. high'))))
        Low.append(int(float(Value.get('3. low'))))
        Close.append(int(float(Value.get('4. close'))))
        Index2 = Index2 + 1
    Index = list(StepData).index(start_date)
    Index2 = list(StepData).index(end_date)
    Date.reverse()
    Open.reverse()
    High.reverse()
    Low.reverse()
    Close.reverse()
    if int(chart_type)-1 == 0:
        chart = pygal.Bar(spacing=100, fill=True, x_label_rotation=40)
        chart.title = ('Stock Data for '+ symbol + ': ' + start_date +' to ' + end_date)
        chart.x_labels =('Red', 'Blue', 'Green', 'Yellow')
        chart.x_labels = Date
        chart.add('Open', Open)
        chart.add('High', Close)
        chart.add('Low', Low)
        chart.add('close', Close)
        chartvar = chart.render_data_uri()
        return chartvar
    elif int(chart_type)-1 == 1:
        chart = pygal.Line(spacing=100, fill=False, x_label_rotation=40)
        chart.title = ('Stock Data for '+ symbol + ': ' + start_date +' to ' + end_date)
        chart.x_labels =('Red', 'Blue', 'Green', 'Yellow')
        chart.x_labels = Date
        chart.add('Open', Open)
        chart.add('High', Close)
        chart.add('Low', Low)
        chart.add('close', Close)
        chartvar = chart.render_data_uri()
        return chartvar
    
def endDate():
    global SecondInput
    while (SecondInput in list(StepData)) == False:
        splitVar = SecondInput.split(' ')
        dateSegment = splitVar[0]
        dateArray = dateSegment.split('-')
        dayNum = int(dateArray[2])
        monthNum = int(dateArray[1])
        timeSegment = splitVar[1]
        hours = int(timeSegment.split(':')[0])
        if hours == 00:
            hours = 20
            dayNum = dayNum - 1
            if dayNum == 00:
                dayNum = 31
                monthNum = monthNum - 1
                SecondInput = (dateArray[0] + '-' + str(monthNum).zfill(2) + '-' + str(dayNum).zfill(2) + ' ' + str(hours).zfill(2) + ':00:00')
            else:
                dayNum = dayNum - 1
                SecondInput = (dateArray[0] + '-' + str(monthNum).zfill(2) + '-' + str(dayNum).zfill(2) + ' ' + str(hours).zfill(2) + ':00:00')
        else:
            hours = hours - 1
            SecondInput = (dateArray[0] + '-' + str(monthNum).zfill(2) + '-' + str(dayNum).zfill(2) + ' ' + str(hours).zfill(2) + ':00:00')
    return SecondInput


def startDate():
    global Input
    while (Input in list(StepData)) == False:
        splitVar = Input.split(' ')
        dateSegment = splitVar[0]
        dateArray = dateSegment.split('-')
        dayNum = int(dateArray[2])
        monthNum = int(dateArray[1])
        timeSegment = splitVar[1]
        hours = int(timeSegment.split(':')[0])
        if hours == 20:
            hours = 1
            dayNum = dayNum + 1
            if dayNum == 32:
                dayNum = 1
                monthNum = monthNum + 1
                Input = (dateArray[0] + '-' + str(monthNum).zfill(2) + '-' + str(dayNum).zfill(2) + ' ' + str(hours).zfill(2) + ':00:00')
            else:
                dayNum = dayNum + 1
                Input = (dateArray[0] + '-' + str(monthNum).zfill(2) + '-' + str(dayNum).zfill(2) + ' ' + str(hours).zfill(2) + ':00:00')
        else:
            hours = hours + 1
            Input = (dateArray[0] + '-' + str(monthNum).zfill(2) + '-' + str(dayNum).zfill(2) + ' ' + str(hours).zfill(2) + ':00:00')
    return Input
