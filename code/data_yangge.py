# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 15:09:42 2021

@author: lenovo
"""
import pandas as pd
import numpy as np
import requests
from pyecharts.charts import Geo
from pyecharts import options
from pyecharts.globals import GeoType
data_hotpot = pd.read_excel("C:\\Users\\lenovo\\Desktop\\郑州火锅 - 副本.xlsx")
data_origin=data_hotpot.drop_duplicates(subset='标题')
data_origin=data_origin.reset_index()
data_origin=data_origin.drop(['index'], axis=1)
#============================Baidu Map API Ak key password========================================================
AK ="9uaS7LlQy66FVitEOYVay3Pv0I0AHGGN"
#=============================dealing with original data================================================================
def Yangge_data_washing(data):
    name=[]
    url_connect=[]
    personal_average=[]
    score_all=[]
    number_critizify=[]
    taste =[]
    serve =[]
    circumstance=[]
    Recommend_1=[]
    Recommend_2=[]
    Recommend_3=[]
    for i in range(len(data)):
#===============================标题,总评分,链接的处理==================================================================        
        d=  data['总评分'][i]
        name.append("郑州"+data['标题'][i])
        url_connect.append(data['链接'][i])
        if str(d) =='nan':
            d=0
        score_all.append(d)
#===============================评分的处理====================================================================
        c=data['评分'][i]
        c=str(c)
        if c=='nan':
            c='0'
            c1='0'
            c2='0'
            c3='0'
        else:
            x=c.split()
            c1=x[0]
            c1=c1.strip("口味")
            c2=x[1]
            c2=c2.strip("环境")
            c3=x[2]
            c3=c3.strip("服务")
        taste.append(c1)
        circumstance.append(c2)
        serve.append(c3)
#===============================评价的处理====================================================================
        b=data['评价'][i].strip("条评价")
        if b=="我要":
            b=b.replace("我要",'0')
        else:
            b=b.strip()
        b=int(b)
        number_critizify.append(b)
#=================================人均的处理==================================================================
        a=data['人均'][i].strip()
        a=a.strip("人均")
        a=a.replace("￥","")
        a=a.replace(" ","")
        a=a.strip()
        if a =='-':
            a='0'
        a=int(a)
        personal_average.append(a)
#==============================推荐菜的处理====================================================================
        ee=str(data['推荐菜'][i])
        ee=ee.strip("推荐菜")
        if ee=="nan":
            ee="无"
        else:
            ee=ee.split()
            if len(ee)==4:
                ee1=ee[1]
                ee2=ee[2]
                ee3=ee[3]
            else:
                ee1=ee
        Recommend_1.append(ee1)
        Recommend_2.append(ee2)
        Recommend_3.append(ee3)
    index_wrong=[]
    for j in range(len(Recommend_2)-1):
        if (Recommend_2[j]==Recommend_2[j+1]) and (Recommend_2[j]!="无"):
            index_wrong.append(j+1)
    for index in index_wrong:
        Recommend_1[index]="无"
        Recommend_2[index]="无"
        Recommend_3[index]="无"
    data_washing = {"标题":name,"总评分":score_all,"评分口味":taste,'评分环境':circumstance,'评分服务':serve,'人均/元':personal_average,'评价/条':number_critizify
                       ,"链接":url_connect,"推荐菜1":Recommend_1,"推荐菜2":Recommend_2,"推荐菜3":Recommend_3}
    data_done =pd.DataFrame(data_washing)
    return data_done
def get_position(name,AK):
    url2='http://api.map.baidu.com/geocoding/v3/?address='
    output='json'
    add = name#本文城市变量为中文，为防止乱码，先用quote进行编码
    url=url2+add+'&output='+output+"&ak="+AK
    res =requests.get(url)
    val =res.json()
    return val
def Yangge_dealing_Lng_Lat_Data(data,AK):
    lat=[]
    lng=[]
    for i in range(len(data)):
        val = get_position(data["标题"][i], AK)
        print(i)
        print("========================================")
        print(val)
        if val['status']==0:
            longitude = val['result']['location']['lng']
            latitude = val['result']['location']['lat']
            
        else:
            longitude =0
            latitude =0
        lng.append(longitude)
        lat.append(latitude)
    name=list(data["标题"])
    data_geo ={"标题":name,"经度":lng,"纬度":lat}
    data_geo = pd.DataFrame(data_geo)
    #other_data = pd.concat([data,data_geo],axis=1,how="outer")
    return data_geo

data_done=Yangge_data_washing(data_origin)
data_done_data=data_done[data_done['总评分']!=0]
data_done_data=data_done_data.reset_index()
data_done_data=data_done_data.drop(['index'], axis=1)
data_geo_1 =Yangge_dealing_Lng_Lat_Data(data_done_data,AK)
data_geo_1=data_geo_1.drop(['标题'],axis=1)
other_data = pd.concat([data_done_data,data_geo_1],axis=1)
other_data.to_csv("C:\\Users\\lenovo\\Desktop\\sample.csv")