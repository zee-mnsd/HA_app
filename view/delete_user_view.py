import tkinter as tk
from tkinter import messagebox

class DeleteUserView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.place(relwidth=1, relheight=1)
        self.create_widgets()

    def create_label_entry(self, text, row):
        tk.Label(self, text=text).grid(row=row, column=0, sticky="e", padx=(5, 2), pady=2)
        entry = tk.Entry(self)
        entry.grid(row=row, column=1, sticky="w", pady=2)
        return entry

    # Tạo các widget nhập liệu
    def create_widgets(self):
        # Ô tìm kiếm
        self.search_entry = tk.Entry(self)
        self.search_entry.grid(row=0, column=1, sticky="w", pady=2)

        self.create_table_button = tk.Button(self, text="Tìm kiếm", command=self.search_family)
        self.create_table_button.grid(row=0, column=1, padx=(5, 2), pady=2)

        tk.Label(self, text="Mã gia đình:").grid(row=1, column=0, sticky="e", padx=(5, 2), pady=2)
        self.ma_gia_dinh_entry = tk.Entry(self)
        self.ma_gia_dinh_entry.grid(row=1, column=1, sticky="w", pady=2)

        tk.Label(self, text="Tín chủ:").grid(row=2, column=0, sticky="e", padx=(5, 2), pady=2)
        self.tin_chu_entry = tk.Entry(self)
        self.tin_chu_entry.grid(row=2, column=1, sticky="w", pady=2)

        # Bảng danh sách thành viên
        tk.Label(self, text="Thành viên:").grid(row=3, column=0, sticky="ne", padx=(5, 2), pady=2)
        self.member_table_frame = tk.Frame(self)
        self.member_table_frame.grid(row=3, column=1, sticky="nsew")
        
        # Placeholder cho bảng, sẽ được tạo trong hàm search_family
        self.member_frame = None

        tk.Label(self, text="Chân linh:").grid(row=4, column=0, sticky="ne", padx=(5, 2), pady=2)
        self.chan_linh_entry = tk.Text(self, height=10, width=70)
        self.chan_linh_entry.grid(row=4, column=1, sticky="w", pady=2)

        self.add_button = tk.Button(self, text="Xóa", command=self.on_delete_button_clicked)
        self.add_button.grid(row=5, column=1, pady=10, sticky="w")

        # Cấu hình để khung chính có thể mở rộng
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def search_family(self):
        # Lấy mã gia đình từ ô nhập
        search_ID = self.search_entry.get().strip()
        if not search_ID:
            messagebox.showerror("Lỗi", "Mã gia đình không được để trống.")
            return

        # Gọi phương thức tìm kiếm từ controller
        family = self.controller.search_user(search_ID)
        if family:
            # Hiển thị dữ liệu gia đình nếu tìm thấy
            self.search_entry.delete(0, tk.END)
            self.ma_gia_dinh_entry.delete(0, tk.END)
            self.ma_gia_dinh_entry.insert(0, family.get("maGiaDinh", ""))
            self.tin_chu_entry.delete(0, tk.END)
            self.tin_chu_entry.insert(0, family.get("tinChu", ""))
            
            self.chan_linh_entry.delete("1.0", tk.END)
            self.chan_linh_entry.insert("1.0", family.get("chanLinh", ""))

             # Tạo bảng thành viên
            self.create_member_table(family.get("thanhVien", []))
      
        else:
            messagebox.showinfo("Thông báo", "Không tìm thấy gia đình!")
            self.search_entry.delete(0, tk.END)

    def create_member_table(self, members):
        # Xóa bảng cũ nếu có
        if self.member_frame:
            self.member_frame.destroy()

        # Khung chứa bảng các thành viên
        self.member_frame = tk.Frame(self.member_table_frame)
        self.member_frame.grid(row=0, column=0, sticky="nsew")

        # Tiêu đề bảng
        headers = ["Họ và tên", "Năm sinh", "Con bán"]
        column_widths = [50, 15, 15]  # Đặt khoảng rộng cho từng cột

        for col, header in enumerate(headers):
            tk.Label(self.member_frame, text=header, borderwidth=1, relief="solid", width=column_widths[col], anchor='w').grid(row=0, column=col, sticky='nsew')

        # Thêm các hàng dữ liệu
        for row, member in enumerate(members, start=1):
            tk.Label(self.member_frame, text=member.get("ho_va_ten", ""), borderwidth=1, relief="solid", width=column_widths[0], anchor='w').grid(row=row, column=0, sticky='nsew')
            tk.Label(self.member_frame, text=member.get("nam_sinh", ""), borderwidth=1, relief="solid", width=column_widths[1], anchor='w').grid(row=row, column=1, sticky='nsew')
            tk.Label(self.member_frame, text=member.get("con_ban", ""), borderwidth=1, relief="solid", width=column_widths[2], anchor='w').grid(row=row, column=2, sticky='nsew')


    # Thêm phương thức để xóa dữ liệu các ô nhập
    def clear_entries(self):
        # Xóa toàn bộ dữ liệu trong các ô nhập
        self.ma_gia_dinh_entry.delete(0, tk.END)
        self.tin_chu_entry.delete(0, tk.END)
        self.chan_linh_entry.delete("1.0", tk.END)
        
        # Xóa bảng thành viên nếu có
        if self.member_frame:
            self.member_frame.destroy()
    
    def on_delete_button_clicked(self):
        # Lấy mã gia đình từ ô nhập
        ma_gia_dinh = self.ma_gia_dinh_entry.get().strip()
        if not ma_gia_dinh:
            messagebox.showerror("Lỗi", "Mã gia đình không được để trống.")
            return

        # Gọi phương thức xóa từ controller
        self.controller.delete_user(ma_gia_dinh)
        self.clear_entries()
