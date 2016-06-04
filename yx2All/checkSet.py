
f=open('testSet','r')
oldNum=0
for line in f:
    num=int(line.split(',')[0])
    if num==oldNum or num==oldNum+1:
        oldNum=num
        continue
    else:
        print oldNum
        oldNum=num
