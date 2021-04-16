# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 13:51:22 2021

@author: yangge
"""
import pandas as pd
import requests
#===========================================================================
data_sample = pd.read_csv("C:\\Users\\lenovo\\Desktop\\洋哥数据包\\2021_4_7.code_table\\sample.csv",encoding='gb18030')
AK="*******************"
#============================================================================
def yangge_getlocation(lat,lng):
    print(lat,"ss",lng)
    if int(lat)==0 &int (lng)==0:
        address='无'
        country='中国'
        province='河南省'
        city = '郑州市'
        district='未知'
        street='未知'
        adcode='未知'
    else:
        url = '/reverse_geocoding/v3/?ak='+AK+'&output=json&coordtype=wgs84ll&location='+str(lat)+','+str(lng)
        uri = "http://api.map.baidu.com"
        url_use = uri+url
        res =requests.get(url_use)
        val =res.json()
        try:
            result=val['result']
            address=result['formatted_address']
            country=result['addressComponent']['country']
            province = result['addressComponent']['province']
            city = result['addressComponent']['city']
            district =result['addressComponent']['district']
            street = result['addressComponent']['street']
            adcode = result['addressComponent']['adcode']
        except:
            result=None
            if not result or'status' not in val or val['status']!=0:
                print("======Failure===========")
                pass
    return address,country,province,city,district,street,adcode
#=======================experiment========================================
latitude = list(data_sample['纬度'])
longitude = list(data_sample['经度'])
address_all=[]
city_all=[]
district_all=[]
street_all=[]
adcode_all=[]
for i in range(len(longitude)):
    lat=latitude[i]
    lng=longitude[i]
    address_single,country_single,province_single,city_single,district_single,street_single,adcode_single = yangge_getlocation(lat,lng)
    address_all.append(address_single)
    city_all.append(city_single)
    district_all.append(district_single)
    street_all.append(street_single)
    adcode_all.append(adcode_single)
data_yangge_other={'具体地址':address_all,'城市':city_all,'区县':district_all,'街道':street_all,'邮政编码':adcode_all}
data_yangge_other = pd.DataFrame(data_yangge_other)
#============================全部数据大汇总===================================
data_all=pd.concat([data_sample,data_yangge_other],axis=1)
