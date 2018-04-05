# import numpy as np
import xlwings as xw
# from functools import reduce

def gini_cal(pi,group,path):
    try:
        pi=float(pi) #0.1
        group=int(group)   #10
    except:
        return False,'pi或分组参数-格式错误，请填写数字'

    excel_path=path #r'E:/城镇化协调性数据.xlsx'
    if excel_path is None or excel_path.strip()=='' :
        return False,'路径不能为空或路径格式错误，正确格式如E:/城镇化协调性数据.xlsx'

    #连接到excel
    workbook = xw.Book(excel_path)
    sheet_names=[workbook.sheets[i].name for i in range(0,len(workbook.sheets),1)]
    rng=workbook.sheets[0].range('A1').expand()
    nrows=rng.rows.count-1
    ncols=rng.columns.count-1
    alpha='ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    cell_alpha=[ c for c in alpha[1:ncols+1]]

    result=[]

    def gini_my2(dd):
        # print(dd)
        d_sum=sum(dd)
        wi_l=[sum(dd[0:i+1])/d_sum for i in range(0,len(dd),1)]
        # print([pi*(1-wi_l[i]) for i in range(0,len(wi_l),1)])
        gini=1-sum([pi*(1-wi_l[i]) for i in range(0,len(wi_l),1)])
        return gini

    for si in range(0,len(sheet_names),1):
        for c in cell_alpha:
            # print(c+'2:'+c+str(nrows+1))
            data_range=workbook.sheets[sheet_names[si]].range(c+'2:'+c+str(nrows+1))
            data=data_range.value
            data=sorted(data)
            step=len(data)//group
            remainder=len(data)%group
            split_d=[data[i*step+(remainder if i>=remainder else i):i*step+(remainder if i>=remainder else i)+step+(0 if i>=remainder else 1)] for i in range(0,10,1)]
            d_ce=[sum(split_d[i]) for i in range(0,len(split_d),1)]
            rs=sheet_names[si]+':'+str(workbook.sheets[sheet_names[si]].range(c+'1').value)+':'+str(gini_my2(d_ce))
            result.append(rs)
            print(rs)
    return True,result

