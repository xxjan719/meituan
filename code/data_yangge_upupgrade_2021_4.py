# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 19:28:22 2021
@author: yangge
"""
#========================using package=========================
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
from bokeh.layouts import gridplot






#========================data reading===========================
data_load = pd.read_csv("C:\\Users\\lenovo\\Desktop\\洋哥数据包\\2021所有信息加满数据.csv",encoding='gb18030')
data_filter = data_load[data_load['人均/元']!=0]
data_filter = data_filter[["标题","评分口味","评分环境","评分服务","人均/元","评价/条"]]
data_filter['性价比'] = (data_filter['评分口味'] + data_filter['评分环境'] + data_filter['评分服务']) / data_filter['人均/元']
data_filter.dropna(inplace = True)
data_filter = data_filter[(data_filter['评分口味']>0) & (data_filter['人均/元']>0)].reset_index()
del data_filter['index']
#======================箱线图以及异常值清理========================
#fig, axes = plt.subplots(1,3,figsize = (14,6))
#ls_columns = [ '评分口味', '人均/元', "性价比"]
#for i in range(len(ls_columns)):
#    data_filter.boxplot(column=ls_columns[i], ax = axes[i] )
#======================异常值数据清理(1220)个数据==============================
def f1(data,col):
    q1 = data[col].quantile(q = 0.25)
    q3 = data[col].quantile(q = 0.75) 
    iqr = q3-q1
    t1 = q1 - 3 * iqr
    t2 = q3 + 3 * iqr
    return data[(data[col] > t1)&(data[col]<t2)][['标题',col]]
data_taste = f1(data_filter,'评分口味')
data_per_people = f1(data_filter,'人均/元')
data_d = f1(data_filter,'性价比')
def f2(data,col):
    col_name = col + '_norm'
    data_gp = data
    data_gp[col_name] = (data_gp[col] - data_gp[col].min())/(data_gp[col].max()-data_gp[col].min())
    data_gp.sort_values(by = col_name, inplace = True, ascending=False)
    return data_gp
data_taste_score = f2(data_taste,'评分口味')
data_per_people_score = f2(data_per_people,'人均/元')
data_d_score = f2(data_d,'性价比')
data_final_q1 = pd.merge(data_taste_score,data_per_people_score,left_index=True,right_index=True)    # 首先合并口味、人均消费指标得分
data_final_q1 = pd.merge(data_final_q1,data_d_score,left_index=True,right_index=True)       # 接着合并性价比指标得分
data_final_q1 =data_final_q1.reset_index()
#del data_final_q1['index']
del data_final_q1['标题_x']
del data_final_q1['标题_y']
print(data_final_q1)
#======================可视化图象==================================================
data_final_q1['size'] = data_final_q1['评分口味_norm'] * 40  # 添加size字段
data_final_q1.index.name = 'type'
data_final_q1.columns = ['kw','kw_norm','price','price_norm','xjb','xjb_norm','size']

#======================人均值没有的异常值回归填补并拼接(881个数据)====================
data_zero = data_load[(data_load['人均/元']==0) & (data_load['评分口味']!=0)]
data_zero_filter = data_zero[["标题","评分口味","评分环境","评分服务","人均/元","评价/条"]]

                              
#======================人均值有的但评分口味等的缺失的数据填补