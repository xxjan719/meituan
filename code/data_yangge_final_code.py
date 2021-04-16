# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 20:45:20 2021

@author: yangge
"""
import os
import requests
import pandas as pd
AK="***********************"
def yangge_get_special_location(data,name):
    string="finial_score_"+name
    data_sample=data[['经度',"纬度",string]]
    lat = list(data_sample['纬度'])
    lng = list(data_sample['经度'])
    final_score = list(data_sample[string])
    address_all=[]
    city_all =[]
    district_all =[]
    uri = "http://api.map.baidu.com"
    for i in range(len(lat)):
        url = '/reverse_geocoding/v3/?ak='+AK+'&output=json&coordtype=wgs84ll&location='+str(lat[i])+','+str(lng[i])
        url_use = uri+url
        res =requests.get(url_use)
        val =res.json()
        try:
            result=val['result']
            address=result['formatted_address']
            address_all.append(address)
            city = result['addressComponent']['city']
            city_all.append(city)
            district =result['addressComponent']['district']
            district_all.append(district)
        except:
            result=None
            if not result or'status' not in val or val['status']!=0:
                print("======Failure===========")
                pass
    data_all ={'地址':address_all,'具体区':district_all,'最终得分':final_score}
    data_all = pd.DataFrame(data_all)
    return data_all
def yangge_get_file_path():
    read_path =r"C:\Users\lenovo\Desktop\洋哥数据包"
    output_path =r"C:\Users\lenovo\Desktop\洋哥数据包"
    return read_path,output_path
def yangge_get_deal_files(name):
    read_path,output_path=yangge_get_file_path()
    files=os.listdir(read_path+"\\"+name)
    data_all =pd.DataFrame()
    for files_name in files:
        data = pd.read_csv(read_path+"\\"+name+"\\"+files_name,encoding='utf-8')
        data_other =  yangge_get_special_location(data,name)
        data_all = pd.concat([data_all,data_other])
    data_all=data_all.sort_values(by='最终得分',ascending = False).reset_index()
    data_all.to_csv(output_path+"\\"+name+"\\"+name+".csv")
    
yangge_get_deal_files("四星半")
