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

def main():   
    mt5.initialize() 
    service = services.ProductsServices(mt5, SELECTTIME, ASSET)
    products = Products(mt5, SELECTTIME, ASSET, HOURSSTART)
    productsServices = ProductsServices(mt5, SELECTTIME, ASSET, HOURSSTART)


if __name__ == "__main__":
    main()
      