import sys
sys.path.append('../')
from Admin_Dashboard.AD_main import main as admin_main
from E_Commerce.EC_main import main as ecommerce_main

def main():
    #CALL MY PROGRAM SCREENS
    admin_main()
    ecommerce_main()

if __name__ == "__main__":
    main()