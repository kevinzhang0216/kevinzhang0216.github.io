from datetime import datetime
from datetime import timedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

data = pd.read_excel('妹妹的小日子.xlsx', index_col='日期', parse_dates = True)
data['平均间隔'] = np.nan
data['预测偏差'] = np.nan

for i in range(1, len(data.index)):
    data.iloc[i, 0] = (data.index[i] - data.index[i-1]).days
    data.iloc[i, 2] = data.iloc[1: i+1, 0].mean()
    data.iloc[i, 1] = data.index[i] + timedelta(data.iloc[i, 2])
    if i == len(data.index)-1:
        data.iloc[i, 3] = np.nan
    else:
        data.iloc[i, 3] = (data.index[i+1] - data.iloc[i, 1]).days
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False   # 解决保存图像是负号'-'显示为方块的问题
plt.figure(figsize=(13, 7))
plt.scatter(x=data.iloc[len(data.index)-1, 1], y=data.iloc[len(data.index)-1, 2], color='r')
plt.plot(data['间隔'], color='DarkBlue', marker='o')
plt.plot([data.index[len(data.index)-1], data.iloc[len(data.index)-1, 1]],
         [data.iloc[len(data.index)-1, 0], data.iloc[len(data.index)-1, 2]], 'r--')
plt.axis('tight')
plt.xlabel('时间：'+str(datetime.now().year)+'年'+str(datetime.now().month)+'月'+str(datetime.now().day)+'日',
                fontsize=12)
plt.ylabel('间隔天数', fontsize=15)
info = '平均间隔：{meantime} 天\n预测日期：{nexttime}\n距离今天：{leftdays} 天'.format(
        meantime=float('%.2f' % data.iloc[len(data.index)-1, 2]),
        nexttime=data.iloc[len(data.index)-1, 1].strftime('%Y-%m-%d %H:%M'),
        leftdays=(data.iloc[len(data.index)-1, 1] - datetime.now()).days)
plt.text(data.iloc[len(data.index)-1, 1], data.iloc[len(data.index)-1, 2] + 0.2, info)
plt.title('妹妹的小日子', fontsize=24)
plt.grid(True)
#plt.savefig("妹妹的小日子_"+str(datetime.now().year)+'年'+
#            str(datetime.now().month)+'月'+str(datetime.now().day)+'日'+".png")
plt.savefig("bodyhealth"+".png")
plt.show()