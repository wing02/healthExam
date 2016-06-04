# coding=utf-8
import xlrd
import re
import sys
import random
reload(sys) 
sys.setdefaultencoding('utf-8')

def getSrcData():
    #load data
    tjAll = xlrd.open_workbook('all.xls')
    sheet=tjAll.sheets()[0]
    yxAll = xlrd.open_workbook('yxAll.xls')
    sheetYx=yxAll.sheets()[0]
    data={}
    colW={}
    #
    for row in range(8,sheet.nrows):
        line=sheet.row_values(row)
        idNum=line[5]
        data[idNum]={}
        texts=line[9].split('\n')
        for text in texts:
            req='^\d*\. (.*): (.+)$'
            tmp=re.search(req,text)
            if tmp==None:
                continue
            label=tmp.group(1)
            data[idNum][label]=0
            if not label in colW:
                colW[label]=0
            colW[label]+=1

    for row in range(8,sheetYx.nrows):
        line=sheetYx.row_values(row)
        idNum=line[5]
        texts=line[9].split('\n')
        for text in texts:
            req='^\d*\. (.*): (.+)$'
            tmp=re.search(req,text)
            if tmp==None:
                continue
            label=tmp.group(1)
            if not idNum in data:
                continue
            if not label in data[idNum]:
                continue
            data[idNum][label]=1

    label2Int={}
    k=0
    for i in colW.keys():
        label2Int[i]=k
        k+=1
    print k
    id2Int={}
    k=0
    for i in data.keys():
        id2Int[i]=k
        k+=1
    print k
    f=open('srcData','wb')
    for idNum,man in data.items():
        row=id2Int[idNum]
        f.write(str(row)+'\t')
        for label,flag in man.items():
            f.write(str(label2Int[label])+','+str(flag)+';')
        f.write('\n')
    f.close()

if __name__=="__main__":
    getSrcData()
