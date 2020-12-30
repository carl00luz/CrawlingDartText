import bs4
import requests
import re
import pandas as pd
import os
from time import sleep


def getReportNumbers(key, crp_cd, date):
    url = "http://dart.fss.or.kr/api/search.xml?auth=" + key + "&crp_cd=" + crp_cd + "&start_dt=" + date + "&dsp_tp=A"
    request = requests.get(url)
    document = bs4.BeautifulSoup(request.content, 'lxml')
    lst = document.find_all('list')
    rcp_no_list = []
    for i in lst:
        if i.find('rpt_nm').text.startswith('사업보고서 ('):
            rcp_no_list.append(i.find('rcp_no').text)
    return rcp_no_list


def getReportParmas(ReportNumbers):
    request = requests.get("http://dart.fss.or.kr/dsaf001/main.do?rcpNo=" + ReportNumbers)
    html = bs4.BeautifulSoup(request.content, 'html.parser')
    JS = html.find_all('script', attrs={'type': 'text/javascript'})
    return JS


def getDocumentsURL(JS):
    for i in JS:
        if len(i.text.strip()) > 5000:
            idx = i.text.find("사업의 내용")
            idx = i.text.find('viewDoc', idx) + 8
            end = i.text.find(")", idx)
            temp = i.text[idx:end].replace("'", "").replace(" ", "")
            params = temp.split(",")

    innerURL = "http://dart.fss.or.kr/report/viewer.do?rcpNo=" + params[0] + "&dcmNo=" + params[1] + "&eleId=" + params[
        2] + "&offset=" + params[3] + "&length=" + params[4] + "&dtd=" + params[5]
    return innerURL


def getReport(innerURL):
    request = requests.get(innerURL)
    report = bs4.BeautifulSoup(request.content, 'html.parser')
    tag_a = report.find_all("p")
    tag_tr = report.find_all("tr")

    doc = ""
    for sen in tag_a:
        doc += sen.text

    for sen in tag_tr:
        doc += re.sub("[^ ㄱ-ㅣ가-힣]+", "", sen.text)

    return doc


def init(key, crp_cd, crp_name, date):
    list = getReportNumbers(key, crp_cd, date)
    if os.path.isdir(crp_name) == False:
        os.mkdir(crp_name)
    print(crp_name)
    for li in list:
        print(li)
        JS = getReportParmas(li)
        innerURL = getDocumentsURL(JS)
        report = getReport(innerURL)
        # reportList.append(report)
        fs = open("./" + crp_name + "/" + crp_cd + "_" + li[:8], 'w', encoding='utf-8')
        fs.write(report)
        fs.close()


if __name__ == "__main__":
    fs = pd.read_csv('Kospi.csv', header=0)
    companyCodeList, companyNameList = list(fs["종목코드"]), list(fs["기업명"])
    key = "api key를 발급받아 입력하세요"
    date = "20180101"

    for idx in range(len(companyCodeList)):
        if idx == 138:
            break
        if len(str(companyCodeList[idx])) < 6:
            companyCodeList[idx] = str(companyCodeList[idx]).zfill(6)
        init(key, str(companyCodeList[idx]), companyNameList[idx], date)
        # sleep(1)
