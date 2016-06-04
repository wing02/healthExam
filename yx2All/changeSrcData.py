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
    int2Label={}
    k=0
    for i in colW.keys():
        if colW[i]>1:
            label2Int[i]=k
            int2Label[k]=i
            k+=1
    print k

    id2Int={}
    int2Id={}
    k=0
    for i in data.keys():
        if len(data[i])>2:
            id2Int[i]=k
            int2Id[k]=i
            k+=1
    print k

    falseArr=[]
    trueArr=[]
    sampleNum=2000
    for i in data.keys():
        if not i in id2Int:
            data.pop(i)
            continue
        for j in data[i].keys():
            if not j in label2Int:
                data[i].pop(j)
        labelNum=len(data[i])
        if labelNum>2:
            j=data[i].keys()[random.randint(0,labelNum-1)]
            flag=data[i][j]
            if flag==1 and len(trueArr)<sampleNum:
                trueArr.append((id2Int[i],label2Int[j],flag))
                data[i].pop(j)
            elif flag==0 and len(falseArr)<sampleNum:
                falseArr.append((id2Int[i],label2Int[j],flag))
                data[i].pop(j)

    f=open('testArr','wb')
    for line in trueArr:
        f.write(','.join(map(str,line)))
        f.write('\n')
    for line in falseArr:
        f.write(','.join(map(str,line)))
        f.write('\n')
    f.close()

    f=open('chgSrcData','wb')
    for i in data.keys():
        row=id2Int[i]
        for j in data[i].keys():
            col=label2Int[j]
            flag=data[i][j]
            line=(row,col,flag)
            f.write(','.join(map(str,line)))
            f.write('\n')
    f.close()

if __name__=="__main__":
    getSrcData()
