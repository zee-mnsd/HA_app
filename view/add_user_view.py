import tkinter as tk
from tkinter import messagebox

class AddUserView(tk.Frame):
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
        tk.Label(self, text="Mã gia đình:").grid(row=0, column=0, sticky="e", padx=(5, 2), pady=2)
        self.ma_gia_dinh_entry = tk.Entry(self)
        self.ma_gia_dinh_entry.grid(row=0, column=1, sticky="w", pady=2)

        tk.Label(self, text="Tín chủ:").grid(row=1, column=0, sticky="e", padx=(5, 2), pady=2)
        self.tin_chu_entry = tk.Entry(self)
        self.tin_chu_entry.grid(row=1, column=1, sticky="w", pady=2)

        # Thêm ô nhập số lượng thành viên
        tk.Label(self, text="Số lượng thành viên:").grid(row=2, column=0, sticky="e", padx=(5, 2), pady=2)
        self.so_luong_entry = tk.Entry(self)
        self.so_luong_entry.grid(row=2, column=1, sticky="w", pady=2)

        # Thêm nút để tạo bảng cạnh ô nhập số lượng thành viên
        self.create_table_button = tk.Button(self, text="Tạo bảng", command=self.create_member_table)
        self.create_table_button.grid(row=2, column=1, padx=(5,2), pady=2)

        # Placeholder cho bảng thành viên
        self.member_table_frame = None

        tk.Label(self, text="Chân linh:").grid(row=4, column=0, sticky="ne", padx=(5, 2), pady=2)
        self.chan_linh_entry = tk.Text(self, height=10, width=70)
        self.chan_linh_entry.grid(row=4, column=1, sticky="w", pady=2)

        self.add_button = tk.Button(self, text="Thêm", command=self.on_add_button_clicked)
        self.add_button.grid(row=5, column=1, pady=10, sticky="w")

        # Cấu hình để khung chính có thể mở rộng
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def create_member_table(self):
        # Xóa bảng cũ nếu có
        if self.member_table_frame:
            self.member_table_frame.destroy()

        try:
            num_rows = int(self.so_luong_entry.get())
            if num_rows <= 0:
                raise ValueError
        except ValueError:
            print("Vui lòng nhập số lượng thành viên hợp lệ (số nguyên dương).")
            messagebox.showerror("Lỗi", "Vui lòng nhập số lượng thành viên hợp lệ (số nguyên dương).")
            return

        # Khung chứa bảng và thanh cuộn
        self.member_table_frame = tk.Frame(self)
        self.member_table_frame.grid(row=3, column=1, columnspan=2, sticky="nsew")

        # Đảm bảo khung có thể co giãn
        self.member_table_frame.rowconfigure(1, weight=1)
        self.member_table_frame.columnconfigure(0, weight=0)

        # Tạo khung cho tiêu đề (headers)
        headers_frame = tk.Frame(self.member_table_frame)
        headers_frame.grid(row=0, column=0, sticky="ew")

        # Tạo Canvas để thêm thanh cuộn
        canvas = tk.Canvas(self.member_table_frame)
        canvas.grid(row=1, column=0, sticky="nsew")

        scrollbar = tk.Scrollbar(self.member_table_frame, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")

        canvas.configure(yscrollcommand=scrollbar.set)

        # Khung thực tế chứa các Entry
        self.member_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=self.member_frame, anchor='nw')

        # Tạo tiêu đề cho bảng trong headers_frame
        headers = ["Họ và tên", "Năm sinh", "Con bản (x)"]
        column_widths = [50, 15, 15]  # Đặt khoảng rộng cho từng cột

        for col, header in enumerate(headers):
            tk.Label(headers_frame, text=header, borderwidth=1, relief="solid", width=column_widths[col], anchor='w').grid(row=0, column=col, sticky='nsew')

        # Lưu trữ các Entry để lấy dữ liệu sau này
        self.member_entries = []

        for row in range(num_rows):
            row_entries = []
            for col in range(len(headers)):
                entry = tk.Entry(self.member_frame, borderwidth=1, relief="solid", width=column_widths[col])
                entry.grid(row=row, column=col, sticky='nsew')
                row_entries.append(entry)
            self.member_entries.append(row_entries)

        # Cập nhật kích thước của canvas
        self.member_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    # Thêm phương thức để xóa dữ liệu các ô nhập
    def clear_entries(self):
        self.ma_gia_dinh_entry.delete(0, tk.END)
        self.tin_chu_entry.delete(0, tk.END)
        self.so_luong_entry.delete(0, tk.END)
        self.chan_linh_entry.delete("1.0", tk.END)
        
        # Xóa toàn bộ dữ liệu trong bảng thành viên nếu có
        if hasattr(self, 'member_entries'):
            for row_entries in self.member_entries:
                for entry in row_entries:
                    entry.delete(0, tk.END)
    
    def on_add_button_clicked(self):
        ma_gia_dinh = self.ma_gia_dinh_entry.get().strip()
        tin_chu = self.tin_chu_entry.get().strip()
        chan_linh = self.chan_linh_entry.get("1.0", tk.END).strip()

        if not ma_gia_dinh or not tin_chu:
            messagebox.showerror("Lỗi", "Mã gia đình và Tín chủ không được để trống.")
            return

        thanh_vien = []
        if hasattr(self, 'member_entries'):
            for row_entries in self.member_entries:
                ho_va_ten = row_entries[0].get().strip()
                nam_sinh = row_entries[1].get().strip()
                con_ban = row_entries[2].get().strip()
                if not ho_va_ten or not nam_sinh:
                    messagebox.showerror("Lỗi", "Mỗi thành viên cần có Họ và Tên và Năm sinh.")
                    return
                thanh_vien.append({"ho_va_ten": ho_va_ten, "nam_sinh": nam_sinh, "con_ban": con_ban})

        self.controller.add_user(ma_gia_dinh, tin_chu, chan_linh, thanh_vien)
        # Sau khi thêm thành công, xóa dữ liệu trên view
        self.clear_entries()
