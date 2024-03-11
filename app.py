import MetaTrader5 as mt5
from services import services
from products.products import Products
from products.productsService import ProductsServices


SELECTTIME = "1" #select time here, string type exp '2' or '3'
ASSET = "WINJ24" #Change name of ASSETS HERE exemple :"WDOc1"
SECONDS = 2 # seconds that the graphs will be shown here 
PHONENUMBER = "You watssap number"
HOURSSTART = '' # IF you wish market start hours exemple '9:00:00'
STOP = 100 #define ou stoploss
MEDIA = 20 # Number o average media

def main():   
    mt5.initialize() 
    service = services.Services(mt5, SELECTTIME, ASSET, STOP)
    products = Products(mt5, SELECTTIME, ASSET, HOURSSTART)
    productsServices = ProductsServices(mt5, SELECTTIME, ASSET, HOURSSTART, STOP)
    #productsServices.eom()
    print(productsServices.calcAMV(MEDIA))
    print()
    print(productsServices.selectBar('close'))
    #print(productsServices.lastbar())
    print('\n\n\n')
    lastClosebar = productsServices.selectBar('close')[999]
    amv= productsServices.calcAMV(MEDIA)[999]
    
    exit = True
    print(lastClosebar)
    print(amv)
    
    while exit:
        exit = productsServices.calcAMVbroke(MEDIA, 'close')
        print("1")



if __name__ == "__main__":
    main()
      