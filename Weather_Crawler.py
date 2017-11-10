
import os.path
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import csv
import numpy as np
from datetime import datetime

def write_to_folder(yy):
    save_path = '/Users/JackTsai/Desktop/Civic_Weather_Crawler/{}/'.format(yy)
    return save_path
def download_weather(yy,mm,dd):
    # Like a human 1 : do not crawl too fast, it will let me recognize as a bot
    seed = np.random.randint(low = 2,high = 5, size = 1)
    seed = int(seed)
    time.sleep(seed)
    # Like a human 2 : Made me like a human rather than a bot, add header
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36', "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8","accept-encoding":"gzip, deflate, br","accept-language":"zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4,zh-CN;q=0.2"}
    session = requests.Session()
    re = session.get("https://www.wunderground.com/history/airport/KNYC/{}/{}/{}/DailyHistory.html?req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo=&MR=1".format(yy,mm,dd))

    soup = BeautifulSoup(re.text,"html.parser")
    div = soup.find(id = "observations_details")
    #print(div.get_text())
    text = div.get_text()
    text = text.strip("\n").split("\n")
    #print(text)
    return text

# Clean Data 1 : Remove the ""
def clean_data(text):
    for i in range (text.count("")):
        text.remove("")
    # Clean Data 2: remove "\t\xa0"
    for i in range(len(text)):
        if "\xa0" in text[i]:
            text[i] = text[i].replace("\xa0","")
    #text.remove("Events")
    return text
# Write the data to csv
def write_to_csv_20121031(yy,mm,dd,text):
    # Open the file
    if mm < 10:
        mm = "0"+str(mm)
    if dd < 10:
        dd = "0"+str(dd)
    save_path = write_to_folder(yy)
    f = open(save_path+'{}{}{}.csv'.format(yy,mm,dd), 'w')
    
    count = 0
    line = ""
    # Deal with the First column:
    for i in range(13):

        if i != 12 :
            line = line + text[i] +","
        else:
            line = line + text[i]+"\n"
            f.write(str(yy)+str(mm)+str(dd)+"\n")
            f.write(line+"\n")
            print(line)
            line = ""
# Deal the rest of data
    count = 0
    line = ""
    for i in range(13,len(text)):  
        if count != 12:
            line = line + text[i] +","
            count = count + 1
            #print(i,count)
        else:
            line = line + text[i]+"\n"
            f.write(line+"\n")
            #print(line)
            line = ""
            count = 0
def write_to_csv_20121030(yy,mm,dd,text):
    # Open the file
    if mm < 10:
        mm = "0"+str(mm)
    if dd < 10:
        dd = "0"+str(dd)
    save_path = write_to_folder(yy)

    f = open(save_path + '{}{}{}.csv'.format(yy,mm,dd), 'w')
    count = 0
    line = ""
    # Deal with the First column:
    for i in range(12):

        if i != 11 :
            line = line + text[i] +","
        else:
            line = line + text[i]+"\n"
            f.write(str(yy)+str(mm)+str(dd)+"\n")
            f.write(line+"\n")
            print(line)
            line = ""
# Deal the rest of data
    count = 0
    line = ""
    for i in range(12,len(text)):  
        if count != 11:
            line = line + text[i] +","
            count = count + 1
            #print(i,count)
        else:
            line = line + text[i]+"\n"
            
            f.write(line+"\n")
            #print(line)
            line = ""
            count = 0

def write_to_csv(yy,mm,dd,text):
    # Open the file
    if mm < 10:
        mm = "0"+str(mm)
    if dd < 10:
        dd = "0"+str(dd)
    save_path = write_to_folder(yy)

    f = open(save_path + '{}{}{}.csv'.format(yy,mm,dd), 'w')
    count = 0
    line = ""

    # Check the column of length
    if "Windchill" in text_clean or "Heat Index" in text_clean:
        len_column = 13
    else:
        len_column = 12

    # Deal with the First column:
    for i in range(len_column):

        if i != (len_column - 1) :
            line = line + text[i] +","
        else:
            line = line + text[i]+"\n"
            f.write(str(yy)+str(mm)+str(dd)+"\n")
            f.write(line+"\n")
            print(line)
            line = ""
    # Deal the rest of data
    count = 0
    day_counter = 0
    line = ""
    for i in range(len_column,len(text)):  
        if count != (len_column - 1):
            line = line + text[i] +","
            count = count + 1
            
            #print(i,count)
        else:
            line = line + text[i]+"\n"
            
            f.write(line+"\n")
            #print(line)
            line = ""
            count = 0
        



def check_mmdd(yy, mm):
    yy_not_normaol = [2012,2016]
    mm_31 = [1,3,5,7,8,10,12]
    mm_30 = [4,6,9,11]
    if (yy not in yy_not_normaol):
        if mm in mm_31:
            dd = 31
            return dd
        elif mm in mm_30:
            dd = 30
            return dd
        elif mm == 2:
            dd = 28
            return dd
    else:
        if mm in mm_31:
            dd = 31
            return dd
        elif mm in mm_30:
            dd = 30
            return dd
        elif mm == 2:
            dd = 29
            return dd
###TEST###
#text = download_weather(2012,12,1)
#text_clean = clean_data(text)
#write_to_csv(2012,12,1,text)


      
#print("Jack")
yy = int(input("Enter the year u want to explore:"))


#file_path = "/{}".format(yy)
#os.mkdir(file_path)
t0 = datetime.now()
day_counter = 0
for mm in range(1,13):
    dd = check_mmdd(yy, mm)
    for day in range(1,dd+1):
        try:
            text = download_weather(yy,mm,day)
            text_clean = clean_data(text)
            # Seperate 2 kinds of column number, for keeping csv in shape
        
            write_to_csv(yy,mm,day,text)
            day_counter = day_counter + 1
            print(yy,mm,day,"Done","Day of {}".format(yy),day_counter)
        except:
            print("Something Wrong !")
            break

dt1 = datetime.now() - t0
dt_miniute = dt1 // 60
dt_second = dt1 % 60
print ("Total use {} min {} sec".format(dt_miniute,dt_second), "and also collect {} days in {}".format(day_counter,yy))      
'''
for yy in range (2009,2017):
    for mm in range(13):
        dd = check_mmdd(yy,mm)
        for day in range(dd):
        #mm = "01"
            text = download_weather(yy,mm,dd)
            text_clean = clean_data(text)
            if yy >= 2012 & mm >=10 & day >=31:
                write_to_csv_20121031(yy,mm,dd,text)
            else:
                write_to_csv_20121030(yy,mm,dd,text)

#table = soup.findAll("tr")
#print (table)'''

#for i in range(len(table)):
#	print("++++++++++++")
#	print(table[i])