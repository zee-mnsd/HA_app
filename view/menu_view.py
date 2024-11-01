import tkinter as tk
from tkinter import Menu, Frame, Label

from view.add_user_view import AddUserView
from controller.add_user_controller import AddUserController

class MenuView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Quản lý thông tin tín chủ")
        self.geometry("900x550")

        # Khởi tạo các khung (frames) cho các chức năng
        self.add_frame = AddUserView(self, self.controller.add_user_controller)
        self.update_frame = Frame(self)
        self.delete_frame = Frame(self)
        self.print_frame = Frame(self)
        for frame in [self.add_frame, self.update_frame, self.delete_frame, self.print_frame]:
            frame.place(relwidth=1, relheight=1)
            Label(frame, font=("Arial", 24)).place(relx=0.5, rely=0.5, anchor="center") # text=frame.cget("bg").title() + " Frame",
            frame.lower()

        # Tạo thanh menu
        menu_bar = Menu(self)

        # Menu "Quản lý"
        quan_ly_menu = Menu(menu_bar, tearoff=0)
        quan_ly_menu.add_command(label="Nhập thông tin", command=self.show_add_frame)
        quan_ly_menu.add_command(label="Sửa thông tin", command=self.show_update_frame)
        quan_ly_menu.add_command(label="Xóa thông tin", command=self.show_delete_frame)
        menu_bar.add_cascade(label="Quản lý", menu=quan_ly_menu)

        # Menu "In thông tin"
        in_menu = Menu(menu_bar, tearoff=0)
        in_menu.add_command(label="In thông tin gia đình theo các ngày lễ", command=self.show_print_frame)
        menu_bar.add_cascade(label="In thông tin", menu=in_menu)

        self.config(menu=menu_bar)

    # Các phương thức hiển thị từng khung
    def show_add_frame(self):
        self.add_frame.lift()

    def show_update_frame(self):
        self.update_frame.lift()

    def show_delete_frame(self):
        self.delete_frame.lift()

    def show_print_frame(self):
        self.print_frame.lift()
