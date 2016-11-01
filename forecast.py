'''
Created on Oct 31, 2016

@author: achaluv
'''
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from math import sqrt
from matplotlib.pyplot import ylabel

def movingAvg(train, test, m = 1):
    temp = train[:]
    i = 0
    while i!= len(test):
        train.append(sum(temp[-m:])/m)
        temp = train[:]
        i+=1
    predicted = temp[1485:]
    #errors = [a-b for a,b in zip(test,predicted)]
    RMSE = sqrt(mean_squared_error(test,predicted))
    return RMSE
    
def movAvgbestM(data):
    mRMSE = [10000]
    for i in range(1,1486):
        trainData = data[:1485]
        testData = data[1485:] 
        mRMSE.append(movingAvg(trainData,testData,i))
    fig = plt.figure()
    plt.plot(range(1,1486),mRMSE[1:])
    fig.suptitle('RMSE values')
    plt.xlabel('m values')
    plt.ylabel('RMSE')
    plt.show()
    return mRMSE.index(min(mRMSE))

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
    bestM = int(movAvgbestM(data))
    test = data[1485:]
    train = data[:1485]
    temp = train[:]
    i = 0
    while i!= len(test):
        train.append(sum(temp[-bestM:])/bestM)
        temp = train[:]
        i+=1
    predicted = temp[1485:]
    fig = plt.figure()
    plt.plot(range(0,495),test,'b')
    plt.plot(range(0,495),predicted,'r')
    fig.suptitle('Predicted for best M value vs Actual data')
    plt.xlabel('Time')
    plt.ylabel('Values')
    plt.show()
    print sqrt(mean_squared_error(test,predicted))
        
        
if __name__ == '__main__':
    main()