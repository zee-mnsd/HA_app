import tkinter as tk
from tkinter import messagebox

class UserListView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.place(relwidth=1, relheight=1)
        self.create_widgets()

    def create_widgets(self):
        # Ô tìm kiếm
        tk.Label(self, text="Tên Tín chủ:").grid(row=0, column=0, padx=(5, 2), pady=2)
        self.search_entry = tk.Entry(self)
        self.search_entry.grid(row=0, column=1, sticky="w", pady=2)

        # Nút tìm kiếm
        self.search_button = tk.Button(self, text="Tìm kiếm", command=self.search_families)
        self.search_button.grid(row=0, column=2, padx=(5, 2), pady=2)

        # Bảng kết quả
        self.result_frame = tk.Frame(self)
        self.result_frame.grid(row=1, column=0, columnspan=3, sticky="nsew")

    def search_families(self):
        tin_chu = self.search_entry.get().strip()
        if not tin_chu:
            messagebox.showerror("Lỗi", "Tên Tín chủ không được để trống.")
            return

        # Gọi controller để tìm kiếm
        families = self.controller.list_user(tin_chu)
        self.display_family_table(families)

    def display_family_table(self, families):
        # Xóa bảng cũ nếu có
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        if not families:
            return
        
        # Tiêu đề bảng
        headers = ["Mã gia đình", "Tên Tín chủ", "Thành viên 1", "Thành viên 2", "Thành viên 3"]
        for col, header in enumerate(headers):
            tk.Label(self.result_frame, text=header, borderwidth=1, relief="solid", anchor='w').grid(row=0, column=col, sticky='nsew')

        # Thêm dữ liệu vào bảng
        for row, family in enumerate(families, start=1):
            tk.Label(self.result_frame, text=family.get("maGiaDinh", ""), borderwidth=1, relief="solid").grid(row=row, column=0, sticky='nsew')
            tk.Label(self.result_frame, text=family.get("tinChu", ""), borderwidth=1, relief="solid").grid(row=row, column=1, sticky='nsew')

            # Lấy 3 thành viên đầu tiên
            members = family.get("thanhVien", [])
            for i in range(3):
                member_name = members[i].get("ho_va_ten", "") if i < len(members) else ""
                tk.Label(self.result_frame, text=member_name, borderwidth=1, relief="solid").grid(row=row, column=2 + i, sticky='nsew')
