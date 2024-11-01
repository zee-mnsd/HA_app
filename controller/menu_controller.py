from view.menu_view import MenuView
from view.add_user_view import AddUserView
from controller.add_user_controller import AddUserController

class MainController:
    def __init__(self, db):
        self.db = db

        # Initialize AddUserController with self as the controller
        self.add_user_controller = AddUserController(self)

        # Initialize MenuView with self as the controller
        self.menu_view = MenuView(self)

    def show_menu_view(self):
        self.menu_view.mainloop()
