from model.user_model import UserModel

class AddUserController:
    def __init__(self, view):
        self.view = view

    # Thêm người dùng vào cơ sở dữ liệu
    def add_user(self, ma_gia_dinh, tin_chu, chan_linh, thanh_vien):
        user_model = UserModel()
        user_model.save(ma_gia_dinh, tin_chu, chan_linh, thanh_vien)
