# -*- coding: utf-8 -*-

import requests as req
import xml.etree.ElementTree as ET
from datetime import datetime
import csv
import configparser
import sys

args=sys.argv
filename=args[0]
inifile = configparser.ConfigParser()

r=filename.replace('.py','.ini')
inifile.read(r)
if len(args)>1:
    router_addr=args[1]
else:
    router_addr=inifile.get('settings','router_address')
print("router="+router_addr)
reportfile=inifile.get('report','file')
session=req.Session()
session.get('http://'+router_addr+'/html/home.html')
r=session.get('http://'+router_addr+'/api/monitoring/month_statistics')

root = ET.fromstring(r.text)
CheckDate=datetime.now().strftime("%Y/%m/%d %H:%M:%S")
CurrentMonthDownload=root.find("CurrentMonthDownload").text
CurrentMonthUpload=root.find("CurrentMonthUpload").text
MonthLastClearTime=root.find("MonthLastClearTime").text
datas=[]
datas.append(CheckDate)
datas.append(CurrentMonthDownload)
datas.append(CurrentMonthUpload)
datas.append(MonthLastClearTime)
print("got:")
print(datas)
f=open(reportfile,"a",newline='')
writer = csv.writer(f)
writer.writerow(datas)
