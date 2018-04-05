import numpy as np
import xlwings as xw
from functools import reduce

pi=0.1
#连接到excel
workbook = xw.Book(r'E:/基尼系数测度数据.xlsx')
#连接到指定单元格
data_range = workbook.sheets('超效率').range('J1:J285')
data=data_range.value
data=sorted(data)
step=len(data)//10
split_d=[data[i*step+(5 if i>=5 else i):i*step+(5 if i>=5 else i)+step+(0 if i>=5 else 1)] for i in range(0,10,1)]
d_ce=[sum(split_d[i]) for i in range(0,len(split_d),1)]
def gini_coef(wealths):
    cum_wealths = np.cumsum(sorted(np.append(wealths, 0)))
    sum_wealths = cum_wealths[-1]
    xarray = np.array(range(0, len(cum_wealths))) / np.float(len(cum_wealths)-1)
    yarray = cum_wealths / float(sum_wealths)
    B = np.trapz(yarray, x=xarray)
    A = 0.5 - B
    return A / (A+B)

def gini_my(dd):
    # print(dd)
    d_sum=sum(dd)
    # print(d_sum)
    # Qi_l=[float('%.5f' % (dd[i]/d_sum)) for i in range(0,len(dd),1)]
    # print(Qi_l)
    Qi_l=dd[:]
    wi_l=[float('%.5f' % (sum(Qi_l[0:i+1])/d_sum)) for i in range(0,len(Qi_l),1)]
    print(wi_l)
    # print([(i+1)/10*(2*Qi_l[i]-wi_l[i]) for i in range(0,len(wi_l),1)])
    gini=1-sum([(i+1)/10*(2*wi_l[i]-Qi_l[i]) for i in range(0,len(wi_l),1)])
    return gini

# http://blog.sina.com.cn/s/blog_3ec2fda00100070c.html
def gini_my2(dd):
    print(dd)
    d_sum=sum(dd)
    print(d_sum)
    wi_l=[sum(dd[0:i+1])/d_sum for i in range(0,len(dd),1)]
    print(wi_l)
    gini=reduce(lambda ii,jj:ii+pi*(1-jj),wi_l)
    return gini
print(gini_my2(d_ce))
