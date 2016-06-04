from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel, Rating

sc.setCheckpointDir('checkpoint/')
ALS.checkpointInterval = 2

#dataValue=data.map(lambda l:l.split('\t')).map(lambda l:(l[0],l[1].strip(';'))).flatMap(lambda l:[(l[0],x) for x in l[1].split(';')])#(row,"col,flag")
#colWeight=dataValue.map(lambda l:(l[1].split(',')[0],1)).reduceByKey(lambda a,b:a+b)
#lowColWeight=colWeight.filter(lambda l: l[1]==1).map(lambda l:l[0])
#
#def chgRowCol(l):
#    row=l[0]
#    col,flag=l[1].split(',')
#    return (row,col),flag
#
#rowColFlag=dataValue.map(chgRowCol).filter(lambda l:l[0][1] not in lowColWeight.collect() )

data = sc.textFile("/Users/wing/Project/tj/yx2All/chgSrcData")
ratings = data.map(lambda l: l.split(',')).map(lambda l: Rating(int(l[0]), int(l[1]), float(l[2])))

# Build the recommendation model using Alternating Least Squares
rank = 10
numIterations = 10
model = ALS.train(ratings, rank, numIterations)


trainData = ratings.map(lambda p: (p[0], p[1]))
trainPred = model.predictAll(trainData).map(lambda r: ((r[0], r[1]), r[2]))
trainRatesAndPreds = ratings.map(lambda r: ((r[0], r[1]), r[2])).join(trainPred)
trainMSE = trainRatesAndPreds.map(lambda r: (r[1][0] - r[1][1])**2).mean()
print("Train Mean Squared Error = " + str(trainMSE))

testData = sc.textFile("/Users/wing/Project/tj/yx2All/testArr")
testRatings = testData.map(lambda l: l.split(',')).map(lambda l: Rating(int(l[0]), int(l[1]), float(l[2])))
testKeys = testRatings.map(lambda p: (p[0], p[1]))
testPred = model.predictAll(testKeys).map(lambda r: ((r[0], r[1]), r[2]))
testRatesAndPreds = testRatings.map(lambda r: ((r[0], r[1]), r[2])).join(testPred)
testMSE = testRatesAndPreds.map(lambda r: (r[1][0] - r[1][1])**2).mean()
print("Test Mean Squared Error = " + str(testMSE))

# Save and load model
#model.save(sc, "target/tmp/myCollaborativeFilter")
#sameModel = MatrixFactorizationModel.load(sc, "target/tmp/myCollaborativeFilter")

testArr=testRatings.collect()
predictArr=testPred.collect()

threshold=0.5
for i in range(11):
    rightNum=0
    wrongNum=0
    threshold=i*0.1
    for test,pre in zip(testArr,predictArr):
        if pre[1]>threshold and test[2]==1:
            rightNum+=1
        elif pre[1]<threshold and test[2]==0:
            rightNum+=1
        else:
            wrongNum+=1
    print threshold,float(rightNum)/(rightNum+wrongNum)

