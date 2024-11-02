import tkinter as tk
from tkinter import Menu, Frame, Label

from view.add_user_view import AddUserView
from controller.add_user_controller import AddUserController
from view.delete_user_view import DeleteUserView
from controller.delete_user_controller import DeleteUserController
from view.edit_user_view import EditUserView
from controller.edit_user_controller import EditUserController
from view.user_list_view import UserListView
from controller.user_list_controller import UserListController
from view.print_list_view import PrintListView
from controller.print_list_controller import PrintListController

class MenuView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("Quản lý thông tin tín chủ")
        self.geometry("1300x580")

        # Khởi tạo các khung (frames) cho các chức năng
        self.add_frame = AddUserView(self, AddUserController(self))
        self.update_frame = EditUserView(self, EditUserController(self))
        self.delete_frame = DeleteUserView(self, DeleteUserController(self))
        self.view_frame = UserListView(self, UserListController(self))
        self.print_frame = PrintListView(self, PrintListController(self))
        for frame in [self.add_frame, self.update_frame, self.delete_frame, self.view_frame, self.print_frame]:
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
        in_menu.add_command(label="Xem thông tin gia đình", command=self.show_view_frame)
        in_menu.add_command(label="In thông tin theo ngày lễ", command=self.show_print_frame)
        menu_bar.add_cascade(label="Xem và in", menu=in_menu)

        self.config(menu=menu_bar)

    # Các phương thức hiển thị từng khung
    def show_add_frame(self):
        self.add_frame.lift()

    def show_update_frame(self):
        self.update_frame.lift()

    def show_delete_frame(self):
        self.delete_frame.lift()

    def show_view_frame(self):
        self.view_frame.lift()

    def show_print_frame(self):
        self.print_frame.lift()
