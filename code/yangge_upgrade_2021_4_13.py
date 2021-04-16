# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 14:01:29 2021

@author: yangge
"""
import pandas as pd
from bokeh.io import output_file
from bokeh.plotting import figure,show
from bokeh.models import ColumnDataSource
from bokeh.layouts import gridplot
from bokeh.models import HoverTool
from bokeh.models.annotations import BoxAnnotation
#==========================================================================
def yangge_final_code(district):
    path="C:\\Users\\lenovo\\Desktop\\洋哥数据包\\区域餐饮数据\\"
    data_load = pd.read_csv(path+district+"\\yangge_郑州_"+district+".csv",encoding='gb18030')
    print('一共有的数据量为{}'.format(len(data_load)))
    print(data_load.head())
    print(data_load.isna().sum())
    df2 = data_load[['人口密度','长度','火锅店数','四星半计数','四星级计数','三星半计数','经度','纬度']]
    df2 = df2.copy()
    df2['rkmd_norm'] = (df2['人口密度'] - df2['人口密度'].min())/(df2['人口密度'].max() - df2['人口密度'].min())
    df2['cyrd_norm'] = (df2['火锅店数'] - df2['火锅店数'].min())/(df2['火锅店数'].max() - df2['火锅店数'].min())
    df2['四星半_norm'] = (df2['四星半计数'].max() - df2['四星半计数'])/(df2['四星半计数'].max() - df2['四星半计数'].min())
    df2['四星_norm'] = (df2['四星级计数'].max() - df2['四星级计数'])/(df2['四星级计数'].max() - df2['四星级计数'].min())
    df2['三星半_norm'] = (df2['三星半计数'].max() - df2['三星半计数'])/(df2['三星半计数'].max() - df2['三星半计数'].min())
    df2['dlmd_norm'] = (df2['长度'] - df2['长度'].min())/(df2['长度'].max() - df2['长度'].min())
    df2['finial_score_四星半'] = df2['rkmd_norm']*0.4 + df2['cyrd_norm']*0.3 +df2['四星半_norm']*0.1+df2['dlmd_norm']*0.2
    df2['finial_score_三星半'] = df2['rkmd_norm']*0.4 + df2['cyrd_norm']*0.3 +df2['三星半_norm']*0.1+df2['dlmd_norm']*0.2
    df2['finial_score_四星'] = df2['rkmd_norm']*0.4 + df2['cyrd_norm']*0.3 +df2['四星_norm']*0.1+df2['dlmd_norm']*0.2
    data_final_four_star_half = df2.sort_values(by='finial_score_四星半',ascending = False).reset_index()
    del data_final_four_star_half['index']
    data_final_four_star = df2.sort_values(by='finial_score_四星',ascending = False).reset_index()
    del data_final_four_star['index']
    data_final_three_star_half = df2.sort_values(by='finial_score_三星半',ascending = False).reset_index()
    del data_final_three_star_half['index']
    #单独确定散点图的大小
    #===================data_final_four_star_half============================
    data_final_four_star_half =data_final_four_star_half.copy()
    data_final_four_star_half['size_four_half'] = data_final_four_star_half['finial_score_四星半'] * 20
    data_final_four_star_half['color'] = 'green'
    data_final_four_star_half['color'].iloc[:20] = 'red'#设置好颜色后，再将前二十位的设置成为重要颜色，顺序不能反了
    #===================data_final_four_star=================================
    data_final_four_star =data_final_four_star.copy()
    data_final_four_star['size_four'] = data_final_four_star['finial_score_四星'] * 20
    
    data_final_four_star['color'] = 'green'
    color = data_final_four_star['color']
    color.iloc[:20] = 'red'#设置好颜色后，再将前二十位的设置成为重要颜色，顺序不能反了
    data_final_four_star['color'] = color
    #===================data_final_three_star_half============================
    data_final_three_star_half =data_final_three_star_half.copy()
    data_final_three_star_half['size_three_half'] = data_final_three_star_half['finial_score_三星半'] * 20
    data_final_three_star_half['color'] = 'green'
    data_final_three_star_half['color'].iloc[:20] = 'red'#设置好颜色后，再将前二十位的设置成为重要颜色，顺序不能反了
    #=======================================================================
    source_four_star_half = ColumnDataSource(data_final_four_star_half)
    source_four_star = ColumnDataSource(data_final_four_star)
    source_three_star_half = ColumnDataSource(data_final_three_star_half)
    output_file(path+district+"\\"+district+'餐馆地址.html')
    hover = HoverTool(tooltips = [('经度','@lng'),('纬度','@lat'),
    ('最终得分','@finial_score'),])
    #============================四星半======================================
    four_star_half = figure(plot_width = 800,plot_height = 800,title = '四星半火锅空间散点图',
               tools = [hover, 'box_select, reset, wheel_zoom,pan,crosshair'])

    four_star_half.square(x = '经度',y ='纬度',source = source_four_star_half,line_color = 'black',fill_alpha = 0.8, color = 'color',size = 'size_four_half')
    #============================四星级======================================
    four_star = figure(plot_width = 800,plot_height = 800,title = '四星级火锅空间散点图',
               tools = [hover, 'box_select, reset, wheel_zoom,pan,crosshair'])

    four_star.square(x = '经度',y ='纬度',source = source_four_star,line_color = 'black',fill_alpha = 0.8, color = 'color',size = 'size_four')
    #============================三星半======================================
    three_star_half = figure(plot_width = 800,plot_height = 800,title = '四星级火锅空间散点图',
               tools = [hover, 'box_select, reset, wheel_zoom,pan,crosshair'])

    three_star_half.square(x = '经度',y ='纬度',source = source_three_star_half,line_color = 'black',fill_alpha = 0.8, color = 'color',size = 'size_three_half')
    p= gridplot([[four_star_half],[four_star],[three_star_half]])#将三个图放在一个画布上
    show(p)
    data_four_half = data_final_four_star_half[['经度','纬度','finial_score_四星半']]
    data_four_half = data_four_half.head(20)
    data_four_half.to_csv(path+district+"\\yangge_郑州_"+district+"四星半坐标得分.csv")
    data_four = data_final_four_star_half[['经度','纬度','finial_score_四星']]
    data_four = data_four_half.head(20)
    data_four.to_csv(path+district+"\\yangge_郑州_"+district+"四星级坐标得分.csv")
    data_three_half = data_final_three_star_half[['经度','纬度','finial_score_四星半']]
    data_three_half = data_three_half.head(20)
    data_three_half.to_csv(path+district+"\\yangge_郑州_"+district+"三星半坐标得分.csv")
yangge_final_code("管城回族区")
