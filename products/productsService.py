import pandas_ta as ta
from products.products import Products 
import pandas as pd
from functools import cache
import time
from datetime import datetime
from services.services import Services


class ProductsServices:  
    def __init__(self, mt5, timeFrame, ASSET, HOURSSTART, BUY_SELL_STOP):
        self.mt5 = mt5
        self.products = Products(self.mt5, timeFrame, ASSET, HOURSSTART)
        self.services = Services(mt5, timeFrame, ASSET, BUY_SELL_STOP)
        self.pd = pd
        self.futureNegative = 0
        self.futurePositive = 0
        self.positive = False
        self.negative = False

    def toTimeFrame(self):
        return self.products.tOtimeFrame()
              
    #name for dateframes func    
    def selectBar(self, valor):
        bar = self.products.selectBar(valor)
        return bar
    
    #mid price   
    def calcAMV(self, media):
        media = ta.midprice(self.selectBar('open'),self.selectBar('close'), media, 0 , 0)
        return media
        
    #Exponential Moving Average    
    def calcEma(self):
        mov = ta.ema(self.selectBar('close'), length=10)
        return mov
          
    #fixing  
    def vwap(self):
        vol = ta.vwap(self.selectBar('high'), self.selectBar('low'), 
              self.selectBar('close'), self.selectBar('real_volume'), anchor= 'W') 
        return vol
    
    #Accumulation/Distribution Index
    def adv(self):
        adVol = ta.ad(self.selectBar('high'), self.selectBar('low'), 
              self.selectBar('close'), self.selectBar('real_volume'),
              self.selectBar('open'), talib=False )
        return adVol
    
    #Price volume
    @cache
    def priceVol(self):
        pricevol = ta.pvol(self.selectBar('close'), self.selectBar('real_volume')) 
        #pricevolConv = pd.DataFrame(pricevol)
        return pricevol
    
    #last bar in market
    def lastbar(self):
        bar = self.products.lastBar()
        return bar
    
    #(mfi)volume force in buy and sell 
    def mfi(self):
        highNotConv = self.selectBar('high')
        high = pd.to_numeric(highNotConv, downcast='float')
        closeNotConv = self.selectBar('low')
        close = pd.to_numeric(closeNotConv, downcast='float') 
        mfiDataFrame = ta.mfi(high,closeNotConv,
                            self.selectBar('close'), self.selectBar('real_volume'))
        return mfiDataFrame
    
    def ad(self):
        adData = ta.ad(self.selectBar('high'), self.selectBar('low')
                       , self.selectBar('close'),  self.selectBar('real_volume'))
        return adData
    
    def eom(self):
        eomData = ta.eom(self.selectBar('high'), self.selectBar('low')
                       , self.selectBar('close'),  self.selectBar('real_volume') )
        return eomData
    
    
    def sma(self):
        smaData = ta.sma(self.priceVol())
        return smaData
    
    def volumeEma(self):
        mov = ta.ema(self.priceVol())
        return mov
    
    # calcv call method
    def calcVfunc(self):
        for i in range(1000):
            calc = self.convertToList(self.lastbar()) 
            self.calcV(calc)
            self.products.timeSleepNow()
        
    #Beta  calcV method
    @cache
    def calcV(self, data):
        if self.futureNegative == 0:
            self.futurePositive = data +  ((data * 0.69)/100)
            self.futureNegative = (data - (data * 0.69)/100)
        elif data < self.futurePositive and self.positive:
            self.futurePositive = 0
            self.positive = False
            return True
        elif data > self.futureNegative and self.negative:  
            self.futureNegative = 0
            self.negative = False  
            return True      
        elif data > self.futurePositive:
            if self.positive == False:
                self.futurePositive = (data - (data * 0.48)/100)
                self.positive = True
        elif data < self.futureNegative:
            if self.negative == False:
                self.futureNegative = (data + (data* 0.48)/100)
                print(self.futureNegative)
                self.negative = True        
                
    def calcAMVbroke(self, valueAMVnotSlice, valueClose, gainpoints):
        valueClose = self.selectBar(valueClose)[999]
        valueAMV= self.calcAMV(valueAMVnotSlice)[999]
        if (valueClose - valueAMV) < -100:
            print("Sell")
            self.services.sell()
            self.services.comeBackSell(gainpoints)
            return False
        elif (valueAMV - valueClose) > 100:
            print('Buy')
            self.services.buy()
            self.services.comeBackBuy(gainpoints)
            return False
        else:
            self.products.timeSleepNow()
            return True
            
    def volumeCheckSimple(self, valueAMVnotSlice, valueClose, gainpoints, volume):
        valueClose = self.selectBar(valueClose)[999]
        valueAMV= self.calcAMV(valueAMVnotSlice)[999]
        volumeBefore = volume[999]
        if (valueClose - valueAMV) < -100 and volumeBefore > volume:
            print("Sell")
            self.services.sell()
            self.services.comeBackSell(gainpoints)
            return False
        elif (valueAMV - valueClose) > 100 and volumeBefore < volume:
            print('Buy')
            self.services.buy()
            self.services.comeBackBuy(gainpoints)
            return False
        else:
            volumeBefore = volume
            self.products.timeSleepNow()
            return True
    
    #Beta
    def volumeCheckComplex(self, valueAMVnotSlice, valueClose, gainpoints, volume):
        valueClose = self.selectBar(valueClose)[999]
        valueAMV= self.calcAMV(valueAMVnotSlice)[999]
        volumeBefore = volume[999]
        if (valueClose - valueAMV) < -100 :
            volumeAfeter = 0
            for i in range(-5):
                volumeBefore += volume[i]
            volumeBefore = volumeBefore/5
            for i in range(5):
                volumeAfeter+= volume
                self.products.timeSleepNow()
            volumeAfeter= volumeAfeter/5
            if volumeBefore > volumeAfeter:
                print("Sell")
                self.services.sell()
                self.services.comeBackSell(gainpoints)
                return False
        elif (valueAMV - valueClose) > 100 :
            volumeAfeter = 0
            for i in range(-5):
                volumeBefore += volume[i]
            volumeBefore = volumeBefore/5
            for i in range(5):
                volumeAfeter+= volume
                self.products.timeSleepNow()
            volumeAfeter= volumeAfeter/5
            if volumeBefore < volumeAfeter:
                print('Buy')
                self.services.buy()
                self.services.comeBackBuy(gainpoints)
                return False
        else:
            volumeBefore = volume
            self.products.timeSleepNow()
            return True
        
   
            