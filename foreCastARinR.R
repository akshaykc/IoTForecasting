library(forecast)
library(ggplot2)
df <- read.table("data.txt",header = TRUE)
#head(df, n=30)
df=ts(df)
n<-dim(df)[1]
df<-df[21:n]
plot(df, type="b")

train<-df[1:1485]
test<-df[1486:(n-20)]

arMod3 <- Arima(train, order = c(3,0,0))
summary(arMod3)

pacf(train,lag.max = 20)

arMod <- Arima(train, order = c(3,0,0))
summary(arMod)

arMod$coef
arMod$coef['ar1']
arMod$coef['intercept']
options(scipen = 999)
intercept = (1-arMod$coef['ar1']-arMod$coef['ar2']-arMod$coef['ar3'])*arMod$coef['intercept']
intercept

testPredict = data.frame()
testPredict <- rbind(testPredict,test[1])
testPredict <- rbind(testPredict,test[2])
testPredict <- rbind(testPredict,test[3])

for (i in 2:length(test)){
  #print(test[i])
  testPredict <- rbind(testPredict,(test[i-1]*arMod$coef['ar1'])+(test[i-2]*arMod$coef['ar2'])+(test[i-3]*arMod$coef['ar3'])+intercept)      
}

testPredict

print(sqrt( mean( (testPredict-test)^2 , na.rm = TRUE ) ))
testPredict<-ts(testPredict)
plot(testPredict)


x = ts(test)
y = ts(testPredict)
ts.plot(x, y, gpars = list(col = c("blue", "red")))
