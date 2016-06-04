# coding=utf-8
import xlrd
import re
import sys
import random
reload(sys) 
sys.setdefaultencoding('utf-8')


tjAll = xlrd.open_workbook('all.xls')
sheet=tjAll.sheets()[0]
yxAll = xlrd.open_workbook('yxAll.xls')
sheetYx=yxAll.sheets()[0]

data={}
contents={}
labelCount={}
label2Num={}

for row in range(8,sheet.nrows):
    line=sheet.row_values(row)
    idNum=line[5]
    data[idNum]={}
    contents[idNum]={}
#    if line[7]==u'男':
#        data[idNum]['male']=1
#    else:
#        data[idNum]['male']=0
#    data[idNum]['age']=int(line[8])
    texts=line[9].split('\n')
    for text in texts:
        req='^\d*\. (.*): (.+)$'
        tmp=re.search(req,text)
        if tmp==None:
            continue
        name=tmp.group(1)
        data[idNum][name]=0
        if not name in labelCount:
            labelCount[name]=0
        labelCount[name]+=1
        content=tmp.group(2)
        contents[idNum][name]=content

k=0
for lc in labelCount.keys():
    if labelCount[lc]==1:
        continue
    label2Num[lc]=k
    k+=1
print k

for row in range(8,sheetYx.nrows):
    line=sheetYx.row_values(row)
    idNum=line[5]
    texts=line[9].split('\n')
    for text in texts:
        req='^\d*\. (.*): (.+)$'
        tmp=re.search(req,text)
        if tmp==None:
            continue
        name=tmp.group(1)
        if not idNum in data:
            continue
        if not name in data[idNum]:
            continue
        data[idNum][name]=1

#trainFile=open('trainSet','wb')
testFile=open('testSet','wb')
testLabelFile=open('testLabelSet','wb')
trainRow=1
testRow=1
sampleNum=2000
num1=0
num0=0
i=1
for idNum,man in data.items():
    j=1
    #if i%5==3:
    tmpList=[]
    for name,flag in man.items():
        if not name in label2Num:
            continue
        tmpList.append((name,flag))
        j+=1
    if not j==1:
        labelIdx=random.randint(1,j)
        k=1
        for name,flag in tmpList:
            if k==labelIdx:
                if flag==1 and num1<sampleNum:
                    testLabelFile.write(str(testRow)+','+str(label2Num[name])+','+str(flag)+'\n')
                    num1+=1
                elif flag==0 and num0<sampleNum:
                    testLabelFile.write(str(testRow)+','+str(label2Num[name])+','+str(flag)+'\n')
                    num0+=1
                else:
                    testFile.write(str(testRow)+','+str(label2Num[name])+','+str(flag)+'\n')
            else:
                testFile.write(str(testRow)+','+str(label2Num[name])+','+str(flag)+'\n')
            k+=1
        i+=1
        testRow+=1
    #else:
    #    for name,flag in man.items():
    #        if not name in label2Num:
    #            continue
    #        trainFile.write(str(trainRow)+','+str(label2Num[name])+','+str(flag)+'\n')
    #        j+=1
    #    if not j==1:
    #        i+=1
    #        trainRow+=1

#trainFile.close()
testFile.close()
testLabelFile.close()

#resultFile=open('result','wb')
#k=0
#for idNum,man in data.items():
#    resultFile.write(idNum+'\n')
#    for name,flag in man.items():
#        content=contents[idNum][name]
#        resultFile.write('\t'+name+'\t'+content+'\t'+str(flag)+'\n')
#    resultFile.write('\n')
#
#resultFile.close()


