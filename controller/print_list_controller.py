from model.user_model import UserModel
from tkinter import messagebox
import docx

class PrintListController:
    def __init__(self, view):
        self.view = view


    def search_user(self, ma_gia_dinh):
        user_model = UserModel()
        return user_model.search(ma_gia_dinh)

    # def ngay_print(self):
    #     self.create_doc_file("ngay1va15.docx")

    # def vu_lan_print(self):
    #     self.create_doc_file("ngayVL.docx")

    # def dau_nam_print(self):
    #     self.create_doc_file("ngayDN.docx")

    # def con_ban_print(self):
    #     self.create_doc_file("ngayCB.docx")

    # def create_doc_file(self, filename):
    #     document = docx.Document()
    #     for doc in self.search_user():
    #         para = document.add_paragraph()
    #         para.add_run(f"Tín Chủ: {doc.get('tinChu')}\n")
    #         para.add_run("Thành Viên: ")
    #         for member in doc.get("thanhVien", []):
    #             para.add_run(f"{member.get('hoTen')} ")
    #     document.save(filename)
    #     messagebox.showinfo("Thông báo", f"Xuất file thành công: {filename}")