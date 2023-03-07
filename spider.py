import requests
import json
import pandas as pd
import re
import time
import datetime
from fake_useragent import UserAgent
import random

ua = UserAgent()

for i in range(10):
    time.sleep(random.randint(4,30))
    print(ua.random)

# 假设有以下字符串
s = '这是一个 http://stock.hexun.com/abc/def.html 的链接，还有一个 http://stock.hexun.com/xyz.html 的链接'

def find_links(json_str):
    # 定义正则表达式
    pattern = r'http://stock\.hexun\.com/.*?\.html'

    # 使用 re.findall 方法匹配所有符合条件的字符串，并返回一个列表
    matched_strs = re.findall(pattern, json_str)

    # 输出匹配到的字符串列表
    return (matched_strs)

def now():
    # 获取当前日期和时间
    now = datetime.datetime.now()

    # 将日期时间对象格式化为MySQL datetime字符串
    datetime_str = now.strftime('%Y-%m-%d %H:%M:%S')
    return datetime_str


def get_table(date='2023-03-06',tempTime=55935794,count=-1):
    url=f'http://roll.hexun.com/roolNews_listRool.action?type=all&ids=108&date={date}&page=1&tempTime={tempTime}'
    count=int(count)
    response=requests.get(url)

    print(response)

    sum_str=str(response.content).split(",")[0]
    sum_str=sum_str.replace('"','').replace("'",'').split(":")[1]
    sum=int(sum_str)
    print(sum)

    links_g=find_links(str(response.content))
    # print(links_g)
    # print(len(links_g))

    pages=int(sum/30)+1
    print("pages:"+str(pages))

    result=[]
    page_count=0

    agent=ua.random
    for page in range(pages+1):
        links=[]
        now_str=now()
        request_url=f'http://roll.hexun.com/roolNews_listRool.action?type=all&ids=108&date=2023-03-05&page={page}&tempTime={tempTime}'
        print("request:")
        print(request_url)
        try:
            # 构造请求头部
            headers = {
                'User-Agent': agent
            }

            response_url=requests.get(request_url,headers=headers)
            links=links+(find_links(str(response_url.content)))
            temp=[{'link':temp_url,'time':now_str} for temp_url in links]
            result=result+temp
            time.sleep(2)
            print("page:"+str(page), flush=True)
            print("temp:"+str(temp), flush=True)
        except:
            agent=ua.random
            print("error")
        time.sleep(random.randint(2,4))
        page_count=page_count+1
        if(count>0 and page_count==count):
            break
        

    #print(result)
    df = pd.DataFrame(result, columns=['link','time'])

    print(df.head())

    csv_file="links.csv"
    try:
        csv_df=pd.read_csv(csv_file,index=False)
        csv_df.merge(df)
        csv_df.to_csv(csv_file)
    except:
        df.to_csv(csv_file,index=False)

    return csv_file