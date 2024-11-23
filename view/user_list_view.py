import tkinter as tk
from tkinter import messagebox

class UserListView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.place(relwidth=1, relheight=1)
        self.create_widgets()

    def create_widgets(self):
        # Khung tìm kiếm
        self.search_frame = tk.Frame(self)
        self.search_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Ô tìm kiếm trong khung search_frame
        tk.Label(self.search_frame, text="Tên Tín chủ:").grid(row=0, column=0, padx=(5, 2), pady=2)
        self.search_entry = tk.Entry(self.search_frame)
        self.search_entry.grid(row=0, column=1, sticky="w", pady=2)

        # Nút tìm kiếm trong khung search_frame
        self.search_button = tk.Button(self.search_frame, text="Tìm kiếm", command=self.search_families)
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
        if not families:
            messagebox.showwarning("Thông báo", "Không tìm thấy gia đình.")
            return
        self.display_family_table(families)

    def display_family_table(self, families):
        # Xóa bảng cũ nếu có
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        # Tiêu đề bảng
        headers = ["Mã gia đình", "Tên Tín chủ", "Thành viên 1", "Thành viên 2", "Thành viên 3"]
        column_widths = [20, 30, 30, 30, 30] 
        for col, header in enumerate(headers):
            label = tk.Label(self.result_frame, text=header, borderwidth=1, relief="solid", width=column_widths[col], anchor='center')
            label.grid(row=0, column=col, sticky='nsew', padx=1, pady=1)
            self.result_frame.grid_columnconfigure(col, weight=1)

        # Thêm dữ liệu vào bảng
        for row, family in enumerate(families, start=1):
            tk.Label(self.result_frame, text=family.get("maGiaDinh", ""), borderwidth=1, relief="solid", anchor='center', bg="#ffffff").grid(row=row, column=0, sticky='nsew', padx=1, pady=1)
            tk.Label(self.result_frame, text=family.get("tinChu", ""), borderwidth=1, relief="solid", anchor='center', bg="#ffffff").grid(row=row, column=1, sticky='nsew', padx=1, pady=1)

            # Lấy 3 thành viên đầu tiên
            members = family.get("thanhVien", [])
            for i in range(3):
                member_name = members[i].get("ho_va_ten", "") if i < len(members) else ""
                tk.Label(self.result_frame, text=member_name, borderwidth=1, relief="solid", anchor='center', bg="#ffffff").grid(row=row, column=2 + i, sticky='nsew', padx=1, pady=1)

        # Thiết lập tỉ lệ cho các hàng để tự động co giãn khi thay đổi kích thước cửa sổ
        for row in range(len(families) + 1):
            self.result_frame.grid_rowconfigure(row, weight=1)


