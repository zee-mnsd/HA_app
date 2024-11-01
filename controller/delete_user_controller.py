from model.user_model import UserModel

class DeleteUserController:
    def __init__(self, view):
        self.view = view

    # Xoa người dùng vào cơ sở dữ liệu
    def delete_user(self, ma_gia_dinh):
        user_model = UserModel()
        user_model.delete(ma_gia_dinh)

    def search_user(self, ma_gia_dinh):
        user_model = UserModel()
        return user_model.search(ma_gia_dinh)