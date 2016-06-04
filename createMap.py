# coding=utf-8
import xlrd
import re
import sys
reload(sys) 
sys.setdefaultencoding('utf-8')


tjAll = xlrd.open_workbook('tjAll.xls')
sheet=tjAll.sheets()[0]

usefulMap={}
def readLabel(filePath):
    f=open(filePath)
    result=[]
    for line in f:
        line=line.strip('\n')
        result.append(line)
    f.close()
    return result

usefulLabel=readLabel('labelDir/usefulLabel')
ignoreLabel=readLabel('labelDir/ignoreLabel')
complexLabel=readLabel('labelDir/complexLabel')

okContent=[u'正常', u'未见明显异常',u'未见异常',u'未见明确异常',u'未妇科检查见异常',u'未发现明显异常',u'健康']
ignoreContent=[u'详见..报告',u'弃检',u'拒检',u'未检']

def checkContent(text,contextList):
    for cl in contextList:
        if re.search(cl,text):
            return True
    return False

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
        if name in usefulLabel:
            if not usefulMap.has_key(name):
                usefulMap[name]={}
            if not usefulMap[name].has_key(content):
                if checkContent(content,okContent):
                    usefulMap[name][content]=0
                elif re.search(u'[↑高＋]',content):
                    usefulMap[name][content]=1
                elif re.search(u'[↓低]',content):
                    usefulMap[name][content]=-1
                elif content=='' or checkContent(content,ignoreContent):
                    usefulMap[name][content]=-2
                else:
                    usefulMap[name][content]=None

usefulMapFile=open('mapDir/usefulMap','wb')
k=0
for name in usefulMap:
    usefulMapFile.write(str(k)+'\t'+name+'\t1\n')
    for content in usefulMap[name]:
        usefulMapFile.write('\t\t'+content+'\t'+str(usefulMap[name][content])+'\n')
    usefulMapFile.write('\n')
    k+=1

usefulMapFile.close()
