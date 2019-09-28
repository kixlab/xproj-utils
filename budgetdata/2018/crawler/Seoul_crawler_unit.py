from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
import csv
import re
import os
import time


options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")

driver=webdriver.Chrome('/Users/eunyoungko/Downloads/chromedriver',chrome_options=options)

startaddr='http://openfinance.seoul.go.kr/budgetbybusiness?curPage='
midaddr='&mngId=4&localGovCd=00&init=n&fisYear=2018'
endaddr='&cate=&deptNm=&deptCd=&bNm=&won=1'

maxp=403

j=0
for i in range(maxp):
    addr=startaddr+str(i+1)+midaddr+endaddr
    page=requests.get(addr)
    soup=BeautifulSoup(page.content,"lxml")
    table=soup.find('tbody')
    rows=table.findAll('tr')
    for row in rows:
        cols=row.findAll('td')
        no=cols[0].text
        acc=cols[1].text
        dep=cols[2].text
        service=cols[3].text
        subsidy=cols[4].text
        budget=cols[5].text.split()[0]
        spending=cols[6].text.split()[0]
        balance=cols[7].text.split()[0]
        docdiv=cols[8]
        servhref=docdiv.find('a')['href']
        servhreflist=servhref.replace("'", "-")
        servhref=re.split(':|;|-',servhreflist)
        servuid=servhref[-3]
        inforaddr='http://lofin.mois.go.kr/websquare/websquare.jsp?w2xPath=/ui/portal/stat/local/apply/sd002_be202_01.xml&accnutYear=2017&sfrndCode=1100000&detailBsnsCode='+servuid+'&excutDe=20171221'
        driver.get(inforaddr)
        time.sleep(3)
        infofunc=driver.find_element_by_id("wq_uuid_53").get_attribute("innerText")
        infopol=driver.find_element_by_id("textbox5").get_attribute("innerText")
        infounit=driver.find_element_by_id("textbox6").get_attribute("innerText")
        infopurpose=driver.find_element_by_id("wq_uuid_68").get_attribute("innerHTML")
        infocontent=driver.find_element_by_id("wq_uuid_84").get_attribute("innerHTML")
        infoevidence=driver.find_element_by_id("wq_uuid_102").get_attribute("innerText")
        infocontext=driver.find_element_by_id("wq_uuid_105").get_attribute("innerHTML")
        infoplan=driver.find_element_by_id("wq_uuid_108").get_attribute("innerHTML")
        arow=[dep,service,budget,spending,servuid, infofunc, infopol, infounit, infopurpose, infocontent, infoevidence, infocontext, infoplan]
        filename='Seoul_Service_2018_'+str(j)+'.txt'
        budgetfile=open(filename,'a',encoding="utf-8")
        wr=csv.writer(budgetfile,delimiter=',')
        titles=["부서부서부서","사업사업사업","예산예산예산","지출지출지출","유아이디","기능기능기능","정책정책정책","단위단위단위","목적목적목적","내용내용내용","근거근거근거","경위경위경위","계획계획계획"]
        k=0
        for item in arow:
            wr.writerow([titles[k]])
            wr.writerow([item])
            k=k+1                        
        j=j+1
        print(j)
        budgetfile.flush()
print(str(fisyear)+' Done!!')
        
