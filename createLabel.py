# coding=utf-8
import xlrd
import re
import sys
reload(sys) 
sys.setdefaultencoding('utf-8')

usefulLabel=[]
ignoreLabel=[u'体重',u'身高',u'腰围']
complexLabel=[]

tjAll = xlrd.open_workbook('tjAll.xls')
sheet=tjAll.sheets()[0]
labelMap={}
for row in range(8,sheet.nrows):
    line=sheet.row_values(row)
    texts=line[9].split('\n')
    for text in texts:
        req='^\d*\. (.*): (.*)$'
        tmp=re.search(req,text)
        if tmp==None:
            continue
        name=tmp.group(1)
        if name in ignoreLabel:
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
        ignoreLabel.append(name)
        labelMap.pop(name)

labelTxt=open('labelDir/labelMark','rb')
for line in labelTxt:
    tmp=re.search('\$ (.*)\t(\d)$',line)
    if tmp:
        name=tmp.group(1)
        typeNum=int(tmp.group(2))
        if typeNum==0:
            ignoreLabel.append(name)
        elif typeNum==1:
            usefulLabel.append(name)
        elif typeNum==2:
            complexLabel.append(name)

labelTxt.close()

def saveFile(fileName,listName):
    f=open(fileName,'wb')
    for l in listName:
        f.write(l+'\n')
    f.close()

saveFile('labelDir/ignoreLabel',ignoreLabel)
saveFile('labelDir/usefulLabel',usefulLabel)
saveFile('labelDir/complexLabel',complexLabel)
