import os
import sys

# Get the absolute path of the project root directory
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PROJECT_ROOT)

from Admin_Dashboard.AD_main import main as admin_main
from E_Commerce.EC_main import main as ecommerce_main

def main():
    # CALL MY PROGRAM SCREENS
    admin_main()
    ecommerce_main()

if __name__ == "__main__":
    main()