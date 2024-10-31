# PAU_Software
Admin Dashboard and E-commerce for "Productores Agrícolas Unidos"


# Dependencies:
pip install pygame pygame_gui numpy (json, os and math already incorporated)



- **`controllers/`**  
  *Files in this folder control the main tasks and decisions in the dashboard.*  
  Example files:  
  - `inventory_controller.py`: Manages adding and updating inventory items.
  - `product_controller.py`: Handles product and batch-related tasks for production.
  - `sales_controller.py`: Adjusts product sale statuses and promotions.
  - `user_controller.py`: Manages admin user access and permissions.

- **`models/`**  
  *Files in this folder define the structure for different types of data, like inventory items and products.*  
  Example files:  
  - `item.py`: Describes the attributes of inventory items.
  - `product.py`: Defines products and any recipes needed to make them.
  - `user.py`: Contains details about admin users and their permissions.

- **`services/`**  
  *Files in this folder perform the "heavy lifting" or complex tasks, like updating the database or calculating recipes.*  
  Example files:  
  - `inventory_service.py`: Updates and checks inventory details.
  - `product_service.py`: Manages production batches and recipe calculations.
  - `sales_service.py`: Applies discounts and promotions.
  - `database_service.py`: Reads and writes to the JSON database.

- **`views/`**  
  *Files in this folder manage the user interface, defining what each screen or section of the dashboard displays.*  
  Example files:  
  - `main_dashboard_view.py`: Shows the main admin dashboard screen.
  - `inventory_view.py`: Shows and lets users update inventory.
  - `production_view.py`: Shows production options and batch info.
  - `sales_view.py`: Shows sale and promotion options.

- **`utils/`**  
  *Files in this folder contain helper functions that simplify common tasks, like checking input formats or showing display elements.*  
  Example files:  
  - `input_validation.py`: Checks if inputs (like quantities) are valid.
  - `formatting_utils.py`: Formats units and other display elements.
  - `display_utils.py`: Helper functions to create common display elements for the UI.

- **`constants.py`**  
  *This file stores values that are used throughout the dashboard, like standard units of measure, to make them easy to change if needed.*  
