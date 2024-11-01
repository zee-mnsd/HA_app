from model.user_model import UserModel

class EditUserController: 
    def __init__(self, view):
        self.view = view

    # cập nhật người dùng vào cơ sở dữ liệu
    def edit_user(self, ma_gia_dinh, tin_chu, chan_linh, thanh_vien):
        user_model = UserModel()
        user_model.edit(ma_gia_dinh, tin_chu, chan_linh, thanh_vien)

    def search_user(self, ma_gia_dinh):
        user_model = UserModel()
        return user_model.search(ma_gia_dinh)