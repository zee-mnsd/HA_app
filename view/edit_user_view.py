import tkinter as tk
from tkinter import messagebox

class EditUserView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.place(relwidth=1, relheight=1)
        self.create_widgets()

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

        # Thêm ô nhập số lượng thành viên
        tk.Label(self, text="Số lượng cần thêm:").grid(row=5, column=0, sticky="e", padx=(5, 2), pady=2)
        self.so_luong_entry = tk.Entry(self)
        self.so_luong_entry.grid(row=5, column=1, sticky="w", pady=2)

        # Thêm nút để tạo bảng cạnh ô nhập số lượng thành viên
        self.create_table_button = tk.Button(self, text="Thêm", command=self.update_member_table)
        self.create_table_button.grid(row=5, column=1, padx=(5, 2), pady=2)

        self.add_button = tk.Button(self, text="Cập nhật", command=self.on_edit_button_clicked)
        self.add_button.grid(row=6, column=1, pady=10, sticky="w")

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

            # Tạo bảng thành viên với dữ liệu từ MongoDB
            self.create_member_table(family.get("thanhVien", []))
      
        else:
            messagebox.showinfo("Thông báo", "Không tìm thấy gia đình!")
            self.search_entry.delete(0, tk.END)

    def update_member_table(self):
        try:
            # Lấy số lượng hàng cần thêm từ ô nhập
            num_rows = int(self.so_luong_entry.get().strip())
            if num_rows <= 0:
                raise ValueError("Số lượng phải là số dương.")
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số lượng hàng hợp lệ.")
            return
        
        # Thêm hàng trống vào bảng hiện tại
        for _ in range(num_rows):
            row_entries = []
            for col, key in enumerate(["ho_va_ten", "nam_sinh", "con_ban"]):
                entry = tk.Entry(self.member_frame, borderwidth=1, relief="solid", width=15)
                entry.grid(row=len(self.member_entries) + 1, column=col, sticky='nsew')
                row_entries.append(entry)
            self.member_entries.append(row_entries)

    def create_member_table(self, members):
        # Xóa bảng cũ nếu có
        if self.member_frame:
            self.member_frame.destroy()

        # Khung chứa bảng các thành viên
        self.member_frame = tk.Frame(self.member_table_frame)
        self.member_frame.grid(row=0, column=0, sticky="nsew")

        # Tiêu đề bảng
        headers = ["Họ và tên", "Năm sinh", "Con bản"]
        column_widths = [50, 15, 15]

        for col, header in enumerate(headers):
            tk.Label(self.member_frame, text=header, borderwidth=1, relief="solid", width=column_widths[col], anchor='w').grid(row=0, column=col, sticky='nsew')

        # Thêm các hàng dữ liệu
        self.member_entries = []  # Lưu trữ các Entry để lấy dữ liệu sau này
        for row, member in enumerate(members, start=1):
            row_entries = []
            for col, key in enumerate(["ho_va_ten", "nam_sinh", "con_ban"]):
                entry = tk.Entry(self.member_frame, borderwidth=1, relief="solid", width=column_widths[col])
                entry.insert(0, member.get(key, ""))
                entry.grid(row=row, column=col, sticky='nsew')
                row_entries.append(entry)
            self.member_entries.append(row_entries)

    def on_edit_button_clicked(self):
        ma_gia_dinh = self.ma_gia_dinh_entry.get().strip()
        tin_chu = self.tin_chu_entry.get().strip()
        chan_linh = self.chan_linh_entry.get("1.0", tk.END).strip()

        if not ma_gia_dinh or not tin_chu:
            messagebox.showerror("Lỗi", "Mã gia đình và Tín chủ không được để trống.")
            return

        # Lấy thông tin từ bảng thành viên
        thanh_vien = []
        for row_entries in self.member_entries:
            ho_va_ten = row_entries[0].get().strip()
            nam_sinh = row_entries[1].get().strip()
            con_ban = row_entries[2].get().strip()
            if not ho_va_ten or not nam_sinh:
                messagebox.showerror("Lỗi", "Mỗi thành viên cần có Họ và Tên và Năm sinh.")
                return
            thanh_vien.append({"ho_va_ten": ho_va_ten, "nam_sinh": nam_sinh, "con_ban": con_ban})

        # Gọi controller để cập nhật dữ liệu
        self.controller.edit_user(ma_gia_dinh, tin_chu, chan_linh, thanh_vien)
