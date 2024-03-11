from products.Adb import Adbconect
from products.products import Products
from enums.enumsGrafics import EnumsGraph

import time

class Apiconect():
    def __init__(self, mt5, timeframe, asset, phonenumber, ui, HOURSSTART) :
        self.product = Products(mt5, timeframe, asset, HOURSSTART)
        self.adb = Adbconect(phonenumber)
        self.enumsGrafics = EnumsGraph(ui)
        self.ui = ui
              
    def readTxt(self):
        #self.adb.readMsgOfChat()
        self.adb.readMsgOnChat()
    
    #send image in watssap web
    def sendImage(self):
        img = self.product.hoursImgName()
        self.adb.sendImagens(img) 
        self.product.deleteImg(img) 
              
    def apiConectZap(self):
        self.adb.adbConect()
        
    def closedPltEnums(self):
        self.enumsGrafics.pltClosed()
        

    
    
        
    
        
        
        
        
    
    
        
    
    