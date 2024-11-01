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
    def __init__(self):
        db = connect_to_mongodb()
        if db is None:
            print("Không thể kết nối tới cơ sở dữ liệu.")
            messagebox.showerror("Lỗi", "Không thể kết nối tới cơ sở dữ liệu.")
            return 
        self.collection = db['family']

    # Thêm người dùng vào cơ sở dữ liệu
    def save(self,  ma_gia_dinh, tin_chu, chan_linh, thanh_vien):
        self.ma_gia_dinh = ma_gia_dinh
        self.tin_chu = tin_chu
        self.chan_linh = chan_linh
        self.thanh_vien = thanh_vien
        
        # Tạo document người dùng
        document = {
            "maGiaDinh": self.ma_gia_dinh,
            "tinChu": self.tin_chu,
            "chanLinh": self.chan_linh,
            "thanhVien": self.thanh_vien
        }

        try:
            self.collection.insert_one(document)
            print("Thông tin đã được lưu thành công!")
            messagebox.showinfo("Thành công", "Thông tin đã được lưu thành công!")
        except Exception as e:
            print(f"Lỗi khi lưu vào MongoDB: {e}")
            messagebox.showerror("Lỗi", "Lỗi khi lưu vào MongoDB: {e}")

    # Tìm kiếm gia đình dựa trên mã gia đình
    def search(self, ma_gia_dinh):    
        try:
            document = self.collection.find_one({"maGiaDinh": ma_gia_dinh})
            return document
        except Exception as e:
             print("Error delete!")
             messagebox.showwarning("Thông báo", "Không tìm thấy gia đình để xóa.")

    def delete(self, ma_gia_dinh):
        try:
            self.collection.delete_one({"maGiaDinh": ma_gia_dinh})
            print ("Delete success!")
            messagebox.showinfo("Thông báo", "Đã xóa thành công gia đình!")
        except Exception as e:
             print("Error delete!")
             messagebox.showwarning("Thông báo", "Không tìm thấy gia đình để xóa.")
            
    def edit(self,  ma_gia_dinh, tin_chu, chan_linh, thanh_vien):
        self.ma_gia_dinh = ma_gia_dinh
        self.tin_chu = tin_chu
        self.chan_linh = chan_linh
        self.thanh_vien = thanh_vien
        
        # Tạo document người dùng
        document = {
            "maGiaDinh": self.ma_gia_dinh,
            "tinChu": self.tin_chu,
            "chanLinh": self.chan_linh,
            "thanhVien": self.thanh_vien
        }

        try:
            self.collection.delete_one({"maGiaDinh": ma_gia_dinh})
            self.collection.insert_one(document)
            print("Thông tin đã được cập nhật thành công!")
            messagebox.showinfo("Thành công", "Thông tin đã được cập nhật thành công!")
        except Exception as e:
            print(f"Lỗi khi lưu vào MongoDB: {e}")
            messagebox.showerror("Lỗi", "Lỗi khi cập nhật vào MongoDB: {e}")