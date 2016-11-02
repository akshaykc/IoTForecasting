'''
Created on Oct 31, 2016

@author: achaluv
'''
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from math import sqrt

def movingAvg(train, m = 1):
    temp = train[:m]
    predictTrain = temp[:]
    i = 0
    while i!= (len(train)-m):
        temp.append(sum(predictTrain[-m:])/m)
        i+=1
        predictTrain = temp[:]
    RMSE = sqrt(mean_squared_error(train,predictTrain))
    return RMSE

def bestMmovAvg(data):
    mRMSE = [10000]
    mMax = 20
    for i in range(1,mMax):
        trainData = data[:1485]
        testData = data[1485:] 
        mRMSE.append(movingAvg(trainData,i))
    fig = plt.figure()
    plt.plot(range(1,mMax),mRMSE[1:])
    fig.suptitle('RMSE values')
    plt.xlabel('m values')
    plt.ylabel('RMSE')
    plt.show()
    return mRMSE.index(min(mRMSE))

MOV_AVG = True
    
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
        testData = data[1485:]
        temp = testData[:bestM]
        predictTest = temp[:]
        i = 0
        while i!= (len(testData)-bestM):
            temp.append(sum(predictTest[-bestM:])/bestM)
            i+=1
            predictTest = temp[:]
        print predictTest
        print sqrt(mean_squared_error(testData, predictTest))
        fig = plt.figure()
        plt.plot(range(0,495),testData,'b',label = 'Actual test data')
        plt.plot(range(0,495),predictTest,'r',label = 'Predicted values')
        fig.suptitle('Predicted values for best M value vs Actual data')
        plt.xlabel('Time')
        plt.ylabel('Values')
        plt.legend()
        plt.show()

    
    



if __name__ == '__main__':
    main()