import MetaTrader5 as mt5
from services import services


SELECTTIME = "1" #select time here, string type exp '2' or '3'
ASSET = "WINJ24" #Change name of ASSETS HERE exemple :"WDOc1"
SECONDS = 2 # seconds that the graphs will be shown here 
PHONENUMBER = "You watssap number"
HOURSSTART = '9:00:00' # IF you wish market start hours exemple '9:00:00'
STOP = 100 #define ou stoploss

def main():   
    mt5.initialize() 
    service = services.ProductsServices(mt5, SELECTTIME, ASSET)



if __name__ == "__main__":
    main()
      