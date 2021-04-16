# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 10:23:39 2021

@author: lenovo
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
import torch.utils.data as utils

#===========================数据读取===============================================
data_load = pd.read_csv("C:\\Users\\lenovo\\Desktop\\洋哥数据包\\2021所有信息加满数据.csv",encoding='gb18030')
#============================增加分类指标==========================================
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
#=========================Bootstrap Method =========================================
def yangge_bootstrap(data_number,n):
    print("要进行bootstrap方法的样本数为",data_number)
    np.random.seed(123)
    data_list_message = list(range(data_number))
    sample_record =[]
    for _ in range(10):
        sample_list_message = np.random.choice(data_list_message,size=n)
        sample_record.append(sample_list_message)
    return sample_record
def yangge_bootstrap_suit_train_data_neural_network(sample,data):
    #=====================former explanation ==============================
    data['index'] = data.index.tolist()
    data_operator = data[["index","评分口味","评分环境","评分服务","人均/元"]]
    #=====================get train_data===================================
    train_data_x ={}
    train_data_y={}
    for i in range(len(sample)):
        data_input_x = pd.DataFrame()
        data_input_y = pd.DataFrame()
        for j in range (len(sample[0])):
            data_sample = data_operator[data_operator['index']==sample[i][j]]
            data_sample = data_sample.reset_index()
            input_data =data_sample[['评分口味','评分环境','评分服务']]
            data_input_x =pd.concat([data_input_x,input_data])
            train_per_data = data_sample['人均/元']
            data_input_y = pd.concat([data_input_y,train_per_data])
        data_input_x = data_input_x.reset_index()
        data_input_y = data_input_y.reset_index()
        del data_input_x['index']
        del data_input_y['index']
        print(data_input_x)
        print(data_input_y)
        train_data_x[i]=data_input_x
        train_data_y[i]=data_input_y
    return train_data_x,train_data_y
def yangge_bootstrap_suit_test_data_neural_network(data):
    data_operator =data[["评分口味","评分环境","评分服务"]]   
    return data_operator
def yangge_bootstrap_suit_test_inverse(data):
    data_operator=data['人均/元']
    return data_operator
#=========================Neural Network=====================================
class NET_yangge_1(nn.Module):
    def __init__(self,num_layers=2,hidden_nodes=100,output_nodes=1,input_nodes=3):
        super(NET_yangge_1,self).__init__()
        h=hidden_nodes
        assert num_layers >=2
        self.fc=nn.ModuleList()
        self.fc.append(nn.Linear(input_nodes,h))#输入层
        for _ in range(num_layers -2):#去掉两层后运行隐藏层
            self.fc.append(nn.Linear(h,h))
        self.fc.append(nn.Linear(h,output_nodes))#输出层
    def forward(self,x):
        for layer in self.fc[:-1]:
            x=layer(x)
            x=F.relu(x)
        x=self.fc[-1](x)
        return x
#=========================dealing with data===================================

def yangge_separate_data(data): 
    data_load=yange_classify(data)
    data_filter_not_zero = data_load[(data_load['人均/元']!=0)&(data_load['评分口味']!=0)&(data_load['评分环境']!=0)&(data_load['评分服务']!=0)]
    data_filter_not_zero = data_filter_not_zero.reset_index()
    data_filter_zero = data_load[(data_load['人均/元']==0)&(data_load['评分口味']!=0)&(data_load['评分环境']!=0)&(data_load['评分服务']!=0)]
    data_filter_zero = data_filter_zero.reset_index()
    data_other = data_load[(data_load['人均/元']!=0)&(data_load['评分口味']==0)&(data_load['评分环境']==0)&(data_load['评分服务']==0)]
    data_other = data_other.reset_index()
    data_bad = data_load[(data_load['人均/元']==0)&(data_load['评分口味']==0)&(data_load['评分环境']==0)&(data_load['评分服务']==0)]
    data_bad = data_bad.reset_index()
    #=======================第一类数据处理==================================
    print("原始全部齐全数据记录为",len(data_filter_not_zero))
    data_filter_not_zero['性价比'] = (data_filter_not_zero['评分口味'] + data_filter_not_zero['评分环境'] + data_filter_not_zero['评分服务']) / data_filter_not_zero['人均/元']
    print("========================================")
    fig, axes = plt.subplots(1,3,figsize = (14,6))
    ls_columns = ['评分口味', '人均/元', "性价比"]
    for i in range(len(ls_columns)):
        data_filter_not_zero.boxplot(column=ls_columns[i], ax = axes[i] )
    print("=============箱线图已输出================")
    #=======================第一类数据继续过滤==============================
    data_filter_not_zero = data_filter_not_zero[data_filter_not_zero['人均/元']<300]
    data_filter_not_zero = data_filter_not_zero.reset_index()
    print("处理掉极大值后的数据记录为",len(data_filter_not_zero))
    del data_filter_not_zero['level_0']
    data_not_zero =data_filter_not_zero[['类别','评分口味','评分环境','评分服务','人均/元',"性价比"]] 
    #print(data_not_zero.head())
    print("========================================")
    #=======================第二类数据处理==================================
    print("原始只缺失人均数据的数据记录为",len(data_filter_zero))
    data_zero = data_filter_zero[['类别','评分口味','评分环境','评分服务','人均/元']]
    print("========================================")
    #=======================第三类数据处理==================================
    print("原始只有人均数据的数据记录为",len(data_other))
    data_inverse = data_other[['类别','评分口味','评分环境','评分服务','人均/元']] 
    print("========================================")
    #=======================第四类数据处理==================================
    print("原始数据全部缺失的数据记录为",len(data_bad)) 
    data_bad_replace_taste =[]
    data_bad_replace_circumstance=[]
    data_bad_replace_serve=[]
    data_bad_replace_per_people=[]
    data_bad_sample = data_not_zero[data_not_zero['类别']=='三星店铺']
    data_bad_sample =data_bad_sample.reset_index()
    min_taste =np.mean(data_bad_sample['评分口味'])
    min_circumstance = np.mean(data_bad_sample['评分环境'])
    min_serve = np.mean(data_bad_sample['评分服务'])
    min_per_people = np.mean(data_bad_sample['人均/元'])
    print("填补的缺失值数据值为",[min_taste,min_circumstance,min_serve,min_per_people])
    for i in range(len(data_bad)):
        justice = data_bad['评价/条'][i]
        if justice ==0:
            data_bad_replace_circumstance.append(3.0)
            data_bad_replace_taste.append(3.0)
            data_bad_replace_serve.append(3.0)
            data_bad_replace_per_people.append(50)
        else:
            data_bad_replace_circumstance.appned(0)
            data_bad_replace_serve.append(0)
            data_bad_replace_taste.append(0)
            data_bad_replace_per_people.append(0)
            
    data_bad_replace={'类别':list(data_bad['类别']),'评分口味':data_bad_replace_taste,
                      '评分环境':data_bad_replace_circumstance,'评分服务':data_bad_replace_serve,
                      '人均/元':data_bad_replace_per_people}
    data_bad_replace =pd.DataFrame(data_bad_replace)
    data_bad_replace =data_bad_replace[data_bad_replace['人均/元']!=0]
    data_bad_replace =data_bad_replace.reset_index()
    del data_bad_replace['index']
    data_bad_replace['性价比'] = (data_bad_replace['评分口味'] + data_bad_replace['评分环境'] + data_bad_replace['评分服务']) / data_bad_replace['人均/元']
    data_not_zero =pd.concat([data_not_zero,data_bad_replace])
    data_not_zero = data_not_zero.reset_index()
    del data_not_zero['index']
    #print(data_other['评价/条'])
    #print(data_bad['评价/条'])
    print("加上处理记录后现在需要跑神经网络的训练数据记录为",len(data_not_zero))
    return data_not_zero,data_zero,data_inverse

def yange_train_dealing(train_x,train_y):
    List={}
    for i in range(len(train_x)):
        List_train_x = []
        List_train_y = []
        for j in range(len(train_x[0])):
            taste = train_x[i]['评分口味'][j]
            circumstance = train_x[i]['评分环境'][j]
            serve = train_x[i]['评分服务'][j]
            dianping =[taste,circumstance,serve]
            List_train_x.append(dianping)
            per_people =train_y[i][0][j]
            List_train_y.append(per_people)
        List_train_x,List_train_y = np.asarray(List_train_x),np.asarray(List_train_y)
        List_train_x = List_train_x.astype(np.float32)
        List_train_y = List_train_y.astype(np.float32)
        List_train_x = List_train_x.reshape([-1,3])
        List_train_x = torch.from_numpy(List_train_x)
        List_train_y = torch.from_numpy(List_train_y)
        train_dataset = utils.TensorDataset(List_train_x,List_train_y)
        List[i] =train_dataset    
    return List
def yangge_test_dealing(test_x):
    List_test_x=[]
    List_test_y=[]
    for i in range(len(test_x)):
        taste = test_x['评分口味'][i]
        circumstance = test_x['评分环境'][i]
        serve = test_x['评分服务'][i]
        dianping =[taste,circumstance,serve]
        List_test_x.append(dianping)
        List_test_y.append(0)
    List_test_x = np.array(List_test_x)
    List_test_x = List_test_x.astype(np.float32)
    List_test_x = List_test_x.reshape([-1,3])
    List_test_x = torch.from_numpy(List_test_x)
    List_test_y =np.array(List_test_y)
    List_test_y = List_test_y.astype(np.float32)
    List_test_y = torch.from_numpy(List_test_y)
    test_dataset =List_test_x
    List=test_dataset
    return List

#=======================选择区域===========================================
def yangge_select_district(district):
    data_district = data_load[data_load['区县']==district]
    data_district = data_district.reset_index()
    del data_district['index']
    return data_district
#======================具体操作==============================================
#======================for example 二七区===================================
def yangge_finally(district):
    data_district = yangge_select_district(district)
    data_not_zero,data_zero,data_inverse=yangge_separate_data(data_district)
    sample = yangge_bootstrap(len(data_not_zero),len(data_zero)*10)
    #==================================训练集==============================
    train_data_x,train_data_y = yangge_bootstrap_suit_train_data_neural_network(sample,data_not_zero)
    train_data_list=yange_train_dealing(train_data_x,train_data_y)
    #==================================测试集===============================
    test_data_x = yangge_bootstrap_suit_test_data_neural_network(data_zero)
    test_dataset =yangge_test_dealing(test_data_x)
    #===================神经网络部分=======================================
    batch_size = 10
    epoch=51
    result={}
    for i in range(len(train_data_list)):
        train_dataset = train_data_list[i]        
        train_data_loader = DataLoader(train_dataset,batch_size=batch_size,shuffle=True)
        model_1=NET_yangge_1(num_layers=5,hidden_nodes=100)
        criterion=torch.nn.MSELoss()
        optimizer=torch.optim.Adam(model_1.parameters(),lr=0.005)
        scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.95)
        # 开始训练
        for epoch_number in range(epoch):
            for batch_idx, (input_batch,epsilon_batch) in enumerate(train_data_loader):
                optimizer.zero_grad()
                pred = model_1(input_batch)
                loss = criterion(pred, epsilon_batch)
                loss.backward()
                optimizer.step()
        
        pred_per_people = model_1(test_dataset)
        pred_per_people = pred_per_people.cpu().detach().numpy()
        result[i] =pred_per_people
    List_all =[]
    for i in range(len(result)):
        List_mean =[]
        for j in range(len(result[0])):
            List_mean.append(float(result[i][j]))
        List_all.append(List_mean)
    List_all_1 =pd.DataFrame(List_all)
    List_fix=[]
    for i in range(len(List_all_1.columns)):
        mean_mean = np.mean(List_all_1[i])
        List_fix.append(mean_mean)
    print("================神经网络工作结束==============")
    data_zero['人均/元'] = List_fix
    data_zero['性价比'] = (data_zero['评分口味'] + data_zero['评分环境'] + data_zero['评分服务']) / data_zero['人均/元']
    data_final =pd.concat([data_not_zero,data_zero])
    data_final =data_final.reset_index()
    del data_final['index']
    return data_final

result=yangge_finally('惠济区')



