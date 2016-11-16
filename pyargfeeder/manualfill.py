'''
Created on 16 Nov 2016

@author: rob
'''

def manualfill(orderid, fill, fill_price, dbtype="LIVE", IBtype="LIVE"):
    """
    Do a manual fill in the trading system

    Manually apply a fill to an order; mark an order as completed; unlock the positions table.
    
    Dummy function to test pyargfeeder package
    """
    
    print("Done a fill of %d for order %d at price %f (%s, %s)" %(fill, orderid, fill_price, dbtype, IBtype))