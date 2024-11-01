'''
Chức năng: Định nghĩa các thao tác dữ liệu với người dùng.

    add_user(user_data): Thêm người dùng mới vào collection users.
    delete_user(user_id): Xóa người dùng khỏi collection users dựa trên user_id.
    get_all_users(): Trả về danh sách toàn bộ người dùng trong collection users.
    update_user(user_id, updated_data): Cập nhật thông tin của người dùng dựa trên user_id.

Mục đích: Xử lý tất cả các thao tác CRUD với người dùng, giúp Controller giao tiếp với MongoDB thông qua các phương thức đơn giản.
'''

from tkinter import messagebox
from model.mongodb_connection import connect_to_mongodb

class UserModel:
    def __init__(self, ma_gia_dinh, tin_chu, chan_linh, thanh_vien):
        self.ma_gia_dinh = ma_gia_dinh
        self.tin_chu = tin_chu
        self.chan_linh = chan_linh
        self.thanh_vien = thanh_vien

    # Thêm người dùng vào cơ sở dữ liệu
    def save(self):
        db = connect_to_mongodb()
        if db is None:
            print("Không thể kết nối tới cơ sở dữ liệu.")
            messagebox.showerror("Lỗi", "Không thể kết nối tới cơ sở dữ liệu.")
            return
        
        collection = db['family']
        # Tạo document người dùng
        document = {
            "maGiaDinh": self.ma_gia_dinh,
            "tinChu": self.tin_chu,
            "chanLinh": self.chan_linh,
            "thanhVien": self.thanh_vien
        }

        try:
            collection.insert_one(document)
            print("Thông tin đã được lưu thành công!")
            messagebox.showinfo("Thành công", "Thông tin đã được lưu thành công!")
        except Exception as e:
            print(f"Lỗi khi lưu vào MongoDB: {e}")
            messagebox.showerror("Lỗi", "Lỗi khi lưu vào MongoDB: {e}")
