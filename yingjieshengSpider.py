#!/usr/bin/env python
# coding: utf-8

# In[21]:


# 爬取校招2021信息 by 喝醉的龙猫

import pandas as pd #这是本次将数据保存为表格形式，进行数据清洗，与录入excel文件所需要的库
import requests #让python请求网页的库
from bs4 import BeautifulSoup #解析html代码的库
import re #正则表达式的库，爬取校招信息对应链接时用到
import time #生成日期，保存的时候用



# range: 第一页到第二十三页，页数范围可以自己改，信息由新到旧每页100个。

def get_data(page):
    url = 'http://www.yingjiesheng.com/2021/index-'+str(page)+'.html'
    #print('{}'.format(i))
    content = requests.get(url).content
    soup = BeautifulSoup(content,'html')
    #print('good to go')
    company = soup.find_all('div', class_='s_clear tit floatl')
    for i in company:
        namelist.append(i.text)

    for i in range(len(company)):
        link.append(company[i].find_all('a')[0]['href'])

    date = soup.find_all('div', class_='box1 bg1')
    for i in date:
        datelist.append(i.text)
    print('done for page {}'.format(page))
    return namelist, datelist, link


def data_cleaning(namelist, datelist, link):
    df = pd.DataFrame([namelist,datelist,link]).T #先把数据储存进表格里
    df.columns=['name','date','link']
    df['date'] = df.date.apply(lambda x: x.strip())
    df.drop([0,1],axis=0, inplace = True) #去掉前两行广告
    linklist = df['link'].tolist() #修改链接让它可以直接访问
    for i in range(len(linklist)):
        if re.search('^/job-',linklist[i]):
            linklist[i] = ('http://www.yingjiesheng.com'+linklist[i])
        else:
            pass
    df['link'] = linklist 
    df['date'] = df.date.apply(lambda x: x.replace('网申','')) #去除首尾的换行符和‘网申’二字
    return df

def save_df(df):
    timestamp = time.strftime('%m%d',time.localtime())
    filename = 'recruit'+timestamp+'.xlsx'
    df.to_excel(filename,index=False,encoding='utf-8-sig')
    return filename

if __name__ == '__main__':
    namelist=[]
    datelist=[]
    link=[]
    page = int(input('Enter the numbers of pages you want:'))
    for i in range(1,page+1):
        get_data(i)
    df = data_cleaning(namelist,datelist,link)
    filename = save_df(df)
    print('Data have been saved in excel file:"{}".The programe will shutdown in 5 seconds'.format(filename))
    time.sleep(5)
    print('88')

