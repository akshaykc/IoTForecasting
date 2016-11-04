'''
Created on Oct 31, 2016

@author: achaluv
'''
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from math import sqrt

def movingAvgRMSE(train, m):
    temp = train[:m]
    #predictTrain = temp[:]
    i = m
    while i!= (len(train)):
        temp.append(sum(train[i-m:i])/m)
        i+=1
        #predictTrain = temp[:]
    return sqrt(mean_squared_error(train[m:],temp[m:]))

def bestMmovAvg(data):
    mRMSE = [10000]
    mMax = 30
    for i in range(1,mMax):
        trainData = data[:1485]
        mRMSE.append(movingAvgRMSE(trainData,i))
    fig = plt.figure()
    plt.plot(range(1,mMax),mRMSE[1:])
    fig.suptitle('RMSE values - Simple average')
    plt.xlabel('m values')
    plt.ylabel('RMSE')
    plt.show()
    return mRMSE.index(min(mRMSE))

def drange(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step

def exponenSmoothing(train, a = 0.2):
    temp = [train[0]]
    predExpSmooth = [train[0]]
    for i in range(1, len(train)):
        predExpSmooth.append(a*train[i-1] + (1-a)*temp[i-1])
        temp = predExpSmooth[:]
    RMSE = sqrt(mean_squared_error(train,predExpSmooth))
    return RMSE

def getBestExpSmooth(data):
    mRMSE = [10000]
    aRange = [float('%g'%i) for i in drange(0, 1, 0.001) ]
    for i in aRange:
        trainData = data[:1485]
        mRMSE.append(exponenSmoothing(trainData,i))
    fig = plt.figure()
    plt.plot(aRange,mRMSE[1:])
    fig.suptitle('RMSE values - Exponential smoothing')
    plt.xlabel('m values')
    plt.ylabel('RMSE')
    plt.show()
    return aRange[mRMSE.index(min(mRMSE))]
    
MOV_AVG = True
EXP_SMOOTH = True

def main():
    data = []
    with open('/home/achaluv/Documents/academics/IOT Analytics/IoTProject3/data.txt') as f:
        for line in f:
            data.append(line)
        '''Filter out inital data since it is completely increasing and not correct'''
        '''Data length = 1980 after split'''
        '''Train length = 1485, testing length = 495'''
        data = map(float,data[21:])
    '''Moving average'''
    if MOV_AVG:
        bestM = int(bestMmovAvg(data))
        #print bestM
        testData = data[1485:]
        temp = testData[:bestM]
        #predictTest = temp[:]
        i = bestM
        while i!= (len(testData)):
            temp.append(sum(testData[i-bestM:i])/bestM)
            i+=1
            #predictTest = temp[:]
        #print predictTest
        print sqrt(mean_squared_error(testData[bestM:], temp[bestM:]))
        fig = plt.figure()
        plt.plot(range(0,495),testData,'b',label = 'Actual test data')
        plt.plot(range(0,495),temp,'r',label = 'Predicted values')
        fig.suptitle('Simple average model - Predicted values for best M value vs Actual data')
        plt.xlabel('Time')
        plt.ylabel('Values')
        plt.legend()
        plt.show()
        
    if EXP_SMOOTH:
        bestAvalue = getBestExpSmooth(data)
        #print bestAvalue
        testData = data[1485:]
        temp = [testData[0]]
        predExpSmoothTestData = [testData[0]]
        for i in range(1, len(testData)):
            predExpSmoothTestData.append(bestAvalue*testData[i-1] + (1-bestAvalue)*temp[i-1])
            temp = predExpSmoothTestData[:]
        
        print sqrt(mean_squared_error(testData, predExpSmoothTestData))
        fig = plt.figure()
        plt.plot(range(0,495),testData,'b',label = 'Actual test data')
        plt.plot(range(0,495),predExpSmoothTestData,'r',label = 'Predicted values')
        fig.suptitle('Exponential smoothing - Predicted values for best M value vs Actual data')
        plt.xlabel('Time')
        plt.ylabel('Values')
        plt.legend()
        plt.show()
    
    

if __name__ == '__main__':
    main()