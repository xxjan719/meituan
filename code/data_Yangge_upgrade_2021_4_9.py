# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 20:32:58 2021
@author: yangge
"""
import requests
import pandas as pd
#=======================basic data support=========================================
#data_hotpot = pd.read_excel("C:\\Users\\lenovo\\Desktop\\郑州火锅 - 副本.xlsx")
#data_origin=data_hotpot.drop_duplicates(subset='标题')
#data_origin=data_origin.reset_index()

#===================================================================================
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
#===================================================================================
#百度地图API搜索
def baidu_search(query,region,data_check):
    url ='http://api.map.baidu.com/place/v2/search?'
    output='json'
    ak='9uaS7LlQy66FVitEOYVay3Pv0I0AHGGN'
    uri =url +'query='+query+'&tag=餐饮'+'&region='+region+'&output='+output+'&ak='+ak
    r=requests.get(uri)
    response_dict=r.json()
    status=response_dict["status"]
    name_all=[]
    location_all=[]
    longitude=[]
    latitude=[]    
    city_all=[]
    area_all=[]
    if status ==0:
        results =response_dict["results"]
        
        for adr in results:
            print("*********",i)            
            if ('location' in adr.keys())==True:
                name=adr['name']
                location=adr['location']
                lng=float(location['lng'])
                lat = float(location['lat'])
                address = adr['address']
                city=adr['city']
                area=adr['area']
                print('=================')
                print('名称：'+name)
                print('坐标：%f,%f' %(lat,lng))
                print('地址：'+address)
                print('城市：'+city)
                print('区县:'+area)
                print("===================")
                if (name==query) & (round(data_check,3)==round(lng,3)):
                    city_all.append(city)
                    area_all.append(area)
                    latitude.append(lat)
                    longitude.append(lng)
                    name_all.append(name)
                    location_all.append(address)
                else:
                    print("百度地图不能找到当前地址的信息")
            else:
                pass
            
    
    data_all={'标题':name_all,'经度':longitude,'纬度':latitude,
              '具体地址':location_all,'城市':city_all,'区名称':area_all}
    data_all=pd.DataFrame(data_all)
    return data_all
    
#data_all=baidu_search('海底捞','郑州')
#print(data_all)
#========================================================================
data_sample=pd.read_csv("C:\\Users\\lenovo\\Desktop\\洋哥数据包\\2021_4_7.code_table\\sample.csv",encoding='gb18030')
data_title=[]
for i in range(len(data_sample)):
    string=data_sample['标题'][i]
    string=string.replace('郑州','')
    if string.find("小龙坎火锅")!=-1:
        string=string.replace('小龙坎火锅','小龙坎老火锅')
    if string.find("yoyopark")!=-1:
        string=string.replace("yoyopark","YOYOPARK")
    data_title.append(string)
data_sample['标题']=data_title
#========================================================================
#data_original_done=Yangge_data_washing(data_origin)
data_other= pd.DataFrame(columns=['标题', '经度', '纬度', '具体地址','城市','区名称'])
data_title_list=[data_sample['标题'][0],data_sample['标题'][1],data_sample['标题'][2]]
#data_lng_list=[data_sample['经度'][0],data_sample['经度'][1],data_sample['经度'][2]]
#data_lat_list=[data_sample['纬度'][0],data_sample['纬度'][1],data_sample['纬度'][2]]
for i in range(len(data_title_list)):#data_sample)):
    #data_deal=baidu_search(data_sample['标题'][i],'郑州')
    data_deal=baidu_search(data_title_list[i], '郑州',data_sample['经度'][i])
    data_other=pd.concat([data_other,data_deal])
    data_other=data_other.reset_index()
    data_other=data_other.drop(['index'], axis=1)
print(data_other)

#data_other.to_csv("C:\\Users\\lenovo\\Desktop\\yangge_upgrade_data.csv")