# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 10:23:39 2021

@author: lenovo
"""

import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
#============================用bokeh做交互========================================
from bokeh.io import output_file
from bokeh.plotting import figure,show
from bokeh.models import ColumnDataSource
from bokeh.layouts import gridplot
from bokeh.models import HoverTool
from bokeh.models.annotations import BoxAnnotation
#===========================数据读取===============================================
data_load = pd.read_csv("C:\\Users\\lenovo\\Desktop\\洋哥数据包\\2021所有信息加满数据.csv",encoding='gb18030')
def yange_classify(data):
    classfication = []
    for i in range(len(data['总评分'])):
        class_1 = data['总评分'][i]
        if class_1 >=4.80:
            classfication.append("五星店铺")
        if (class_1>=4.50) & (class_1<4.80):
            classfication.append("四星半店铺")
        if (class_1<4.50) & (class_1>=4.00):
            classfication.append("四星店铺")
        if (class_1<4.00) & (class_1>=3.50):
            classfication.append("三星半店铺")
        if (class_1<3.50):
            classfication.append("三星店铺")
    data_class = {"类别":classfication}
    data_class = pd.DataFrame(data_class)
    data_all = pd.concat([data,data_class],axis=1)
    return data_all
def yangge_get_location_csv(district):
    data = data_load
    data =  yange_classify(data)
    data =data[data['区县']==district]
    lng =data['经度']
    lat =data['纬度']
    name =data['标题']
    classify = data['类别']
    data_new={'类别':classify,'标题':name,"经度":lng,"纬度":lat}
    data_new = pd.DataFrame(data_new)
    data_new.to_csv("C:\\Users\\lenovo\\Desktop\\洋哥数据包\\区域餐饮数据\\"+district+"\\"+district+"经纬度数据.csv",encoding='utf-8')
    return data_new
#============================增加分类指标==========================================
def f2(data,col):
    col_name = col + '_norm'
    data_gp = data.groupby('类别').mean()
    data_gp[col_name] = (data_gp[col] - data_gp[col].min())/(data_gp[col].max()-data_gp[col].min())
    data_gp.sort_values(by = col_name, inplace = True, ascending=False)
    return data_gp
def yangge_dealing(district):
    path ="C:\\Users\\lenovo\\Desktop\\洋哥数据包\\区域餐饮数据\\"+ district
    data_load = pd.read_csv(path+"\\"+district+"处理数据.csv",encoding='utf-8')
    data_kw = data_load[['类别','评分口味']]
    data_rj = data_load[['类别','人均/元']]
    data_xjb = data_load[['类别','性价比']]
#==========================数据标准化==============================================
    data_kw_score = f2(data_kw,'评分口味')
    data_rj_score = f2(data_rj,'人均/元')
    data_xjb_score = f2(data_xjb,'性价比')
#==========================数据合并================================================
    data_final_q1 = pd.merge(data_kw_score,data_rj_score,left_index=True,right_index=True)    # 首先合并口味、人均消费指标得分
    data_final_q1 = pd.merge(data_final_q1,data_xjb_score,left_index=True,right_index=True)       # 接着合并性价比指标得分
    print(data_final_q1.head(15))
    data_final_q1['size'] = data_final_q1['评分口味_norm'] * 40  # 添加size字段
    data_final_q1.index.name = 'type_1'
    #data_final_q1['type_1'] =data_final_q1.index
    data_final_q1.columns = ['kw','kw_norm','price','price_norm','xjb','xjb_norm','size']
    output_file("C:\\Users\\lenovo\\Desktop\\洋哥数据包\\区域餐饮数据\\"+district+"店铺类型.html")#输出文件
    source_df = ColumnDataSource(data=dict(price=data_final_q1['price'],
                                         xjb_norm=data_final_q1['xjb_norm'],
                                         size=data_final_q1['size'],
                                         kw_norm = data_final_q1['kw_norm'],
                                         #type_1 = data_final_q1['type_1'],
                                         price_norm = data_final_q1['price_norm']))#创建数据
    source = ColumnDataSource(data_final_q1)
    data_type = data_final_q1.index.tolist()#横坐标为index，要先转化为列表
    hover = HoverTool(tooltips = [('餐饮类型','@type'),
    ('人均消费','@price'),('性价比得分','@xjb_norm'),('口味得分','@kw_norm'),])
    result = figure(plot_width = 800,plot_height = 300,title = '餐饮类型得分',
                    x_axis_label = '人均消费', y_axis_label = '性价比',tools = [hover, 'box_select, reset, xwheel_zoom,pan,crosshair'])
    result.circle(x = 'price', y = 'xjb_norm',source=source,line_color ='black',fill_alpha =0.6,size = 'size')
    price_mid = BoxAnnotation(left = 40, right = 80, fill_alpha = 0.1, fill_color = 'navy')
    result.add_layout(price_mid)#这里设置标记区
    kw = figure(plot_width = 800,plot_height = 300,title = '口味得分',x_range = data_type,
               tools = [hover, 'box_select, reset, xwheel_zoom,pan,crosshair'])
    kw.vbar(x = 'type_1', top = 'kw_norm', source = source, width = 0.8, alpha = 0.7,color = 'red')
    price = figure(plot_width = 800,plot_height = 300,title = '人均消费得分',x_range = data_type,
               tools = [hover, 'box_select, reset, xwheel_zoom,pan,crosshair'])
    price.vbar(x = 'type_1', top = 'price_norm', source = source, width = 0.8, alpha = 0.7,color = 'green')
    p = gridplot([[result],[kw],[price]])#将三个图放在一个画布上
    show(p)#一定要加show（p）,否则不显示
    return data_final_q1
#data_final_q1=yangge_dealing("中原区")
#print(data_final_q1)
