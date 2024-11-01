# main.py
from controller.menu_controller import MainController

if __name__ == "__main__":
    db_connection = None  # Define the connection to MongoDB if required
    main_controller = MainController(db_connection)
    main_controller.show_menu_view()
