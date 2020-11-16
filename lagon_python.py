# Author: Mélodie - Lagou.com - Python positions - 北上广深杭
import requests
import json
import random
import time
import math
from openpyxl import Workbook

# Request URL: https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false
# Request Method: POST
# Form DATA:
#   first: true
#   pn: 1
#   kd: python

def get_json(url, url_html, page, key_word):

    headers = {
       'Host': 'www.lagou.com',
       'Connection': 'keep-alive',
       'Content-Length': '23',
       'Origin': 'https://www.lagou.com',
       'X-Anit-Forge-Code': '0',
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
       'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
       'Accept': 'application/json, text/javascript, */*; q=0.01',
       'X-Requested-With': 'XMLHttpRequest',
       'X-Anit-Forge-Token': 'None',
       'Referer': 'https://www.lagou.com/jobs/list_python?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput=',
       'Accept-Encoding': 'gzip, deflate, br',
       'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
    }
    
    if page == 1:
        data = {'first': 'true', 'pn': page, 'kd': key_word}
    else:
        data = {'first': 'false', 'pn': page, 'kd': key_word}

    #Get the cookies
    s = requests.Session()
    s.get(url_html, headers = headers, data = data, timeout = 4)
    cookies = s.cookies
    response = s.post(url, headers = headers, data = data, timeout = 4)
    # print(response)
    response.encoding = response.apparent_encoding
    text = json.loads(response.text)
    print(text)

    result = text['content']['positionResult']['result']
    info_list = []
    for item in result:
        info = [] 
        info.append(item.get('positionId', 'N/A'))
        info.append(item.get('positionName', 'N/A'))
        info.append(item.get('city', 'N/A'))
        info.append(item.get('industryField', 'N/A'))
        info.append(item.get('companyFullName', 'N/A'))
        info.append(item.get('companySize', 'N/A'))
        info.append(item.get('financeStage', 'N/A'))
        info.append(item.get('salary', 'N/A'))
        info.append(item.get('positionAdvantage', 'N/A'))
        info.append(item.get('workYear', 'N/A'))
        info.append(item.get('education', 'N/A'))
        info_list.append(info)
    return info_list

def get_page(url, url_html, params, key_word):
    headers = {
       'Host': 'www.lagou.com',
       'Connection': 'keep-alive',
       'Content-Length': '23',
       'Origin': 'https://www.lagou.com',
       'X-Anit-Forge-Code': '0',
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
       'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
       'Accept': 'application/json, text/javascript, */*; q=0.01',
       'X-Requested-With': 'XMLHttpRequest',
       'X-Anit-Forge-Token': 'None',
       'Referer': 'https://www.lagou.com/jobs/list_python?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput=',
       'Accept-Encoding': 'gzip, deflate, br',
       'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
    }
    s = requests.Session()
    s.get(url_html, headers = headers, data = params, timeout = 4)
    cookies = s.cookies
    response = s.post(url, headers = headers, data = params, timeout = 4)
    response.encoding = response.apparent_encoding
    text = json.loads(response.text)
    total_Count = text['content']['positionResult']['totalCount']
    if int(math.ceil(total_Count/15)) < 30 :
        page_number = int(math.ceil(total_Count/15))
    else:
        page_number = 30
    return page_number

def main():
    key_word = 'python'
    xls_wb = Workbook()
    xls_sheet = xls_wb.active
    xls_sheet.title = key_word
    xls_sheet.append(['ID','职位','地点','行业','公司','公司规模','融资情况','薪酬','岗位优势','经验要求','学历要求'])
    # Check from lagou website: 
    # Beijing = %E5%8C%97%E4%BA%AC
    # Shanghai = %E4%B8%8A%E6%B5%B7
    # Guangzhou = %E5%B9%BF%E5%B7%9E
    # Shenzhen = %E6%B7%B1%E5%9C%B3
    # Hangzhou = %E6%9D%AD%E5%B7%9E
    
    for i in ['北京', '上海', '广州', '深圳', '杭州']:
        page = 1
        params = {'first': 'true', 'pn': page, 'kd': key_word}
        if i == '北京':
            url_html = 'https://www.lagou.com/jobs/list_python/p-city_2?px=default#filterBox'
        elif i == '上海':
            url_html = 'https://www.lagou.com/jobs/list_python/p-city_3?px=default#filterBox'
        elif i == '广州':
            url_html = 'https://www.lagou.com/jobs/list_python/p-city_213?px=default#filterBox'
        elif i == '深圳':
            url_html = 'https://www.lagou.com/jobs/list_python/p-city_215?px=default#filterBox'
        else:
            url_html = 'https://www.lagou.com/jobs/list_python/p-city_6?px=default#filterBox'

        url = 'https://www.lagou.com/jobs/positionAjax.json?city={}&needAddtionalResult=false'.format(i) 
        page_number = get_page(url, url_html, params, key_word)
        while page < page_number + 1:
            info_list = get_json(url, url_html, page, key_word)
            page += 1
            time.sleep(random.randint(10,15))
            for row in info_list: 
                xls_sheet.append(row)
   
    xls_wb.save('Lagou-{}职位信息.xlsx'.format(key_word))

if __name__ == '__main__':
   main()






