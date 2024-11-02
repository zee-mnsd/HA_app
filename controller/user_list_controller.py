from model.user_model import UserModel

class UserListController:
    def __init__(self, view):
        self.view = view

    # Xem người dùng trong cơ sở dữ liệu
    def list_user(self, tin_chu):
        user_model = UserModel()
        families = user_model.list(tin_chu)
        return families if families is not None else []
