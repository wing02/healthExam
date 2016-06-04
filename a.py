# coding=utf-8
import xlrd
import re
import sys
reload(sys) 
sys.setdefaultencoding('utf-8')


tjAll = xlrd.open_workbook('tjAll.xls')
sheet=tjAll.sheets()[0]

labelMap={}
usefulLabel=[]
ignoreLabel=[u'体重',u'身高',u'腰围']
complexLabel=[]

for row in range(8,sheet.nrows):
    man=[]
    line=sheet.row_values(row)
    texts=line[9].split('\n')
    for text in texts:
        req='^\d*\. (.*): (.*)$'
        tmp=re.search(req,text)
        if tmp==None:
            continue
        name=tmp.group(1)
        if name in ignoreLabel2:
            continue
        content=tmp.group(2)
        if not labelMap.has_key(name):
            labelMap[name]={}
        if not labelMap[name].has_key(content):
            if content==u'正常' or re.search(u'未见明显异常',content) or re.search(u'未见异常',content):
                labelMap[name][content]=0
            elif re.search(u'[↑高]',content):
                labelMap[name][content]=1
            elif re.search(u'[↓低]',content):
                labelMap[name][content]=-1
            else:
                labelMap[name][content]=None

for name in labelMap.keys():
    if len(labelMap[name])==1:
        labelMap.pop(name)

labelFile=open('label.txt','wb')
k=0
for name in labelMap:
    labelFile.write(str(k)+'$'+' '+name+'\t1\n')
    for content in labelMap[name]:
        #labelFile.write('\t#'+j+'\t'+str(labelMap[name][j])+'\n')
        labelFile.write('\t#'+content+'\n')
    labelFile.write('\n')
    k+=1


labelFile.close()
