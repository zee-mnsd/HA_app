import tkinter as tk
from tkinter import messagebox
import os
from pathlib import Path

class PrintListView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.stt_count = 0
        self.list_ma = []
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
        self.ma_gia_dinh_entry = tk.Entry(self, state='readonly')
        self.ma_gia_dinh_entry.grid(row=1, column=1, sticky="w", pady=2)

        tk.Label(self, text="Tín chủ:").grid(row=2, column=0, sticky="e", padx=(5, 2), pady=2)
        self.tin_chu_entry = tk.Entry(self, state='readonly')
        self.tin_chu_entry.grid(row=2, column=1, sticky="w", pady=2)

        # Placeholder cho bảng thành viên
        self.member_table_frame = None

        tk.Label(self, text="Chân linh:").grid(row=4, column=0, sticky="ne", padx=(5, 2), pady=2)
        self.chan_linh_entry = tk.Text(self, height=10, width=70, state='disabled')
        self.chan_linh_entry.grid(row=4, column=1, sticky="w", pady=2)

        # Cấu hình để khung chính có thể mở rộng
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(1, weight=0)

        # Tạo khung chứa các nút chức năng đặc biệt
        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=5, column=1, sticky="news")

        # Các nút cho các chức năng đặc biệt, đặt vào button_frame
        self.button_chon = tk.Button(self.button_frame, text="Chọn", command=self.chon)
        self.button_chon.grid(row=0, column=0, pady=5, sticky="n")

        self.button_cung_1_15 = tk.Button(self.button_frame, text="Cúng 1 và 15", command=self.cung_1_15)
        self.button_cung_1_15.grid(row=1, column=0, pady=5, sticky="n")

        self.button_vu_lan = tk.Button(self.button_frame, text="Cúng Vu Lan", command=self.cung_vu_lan)
        self.button_vu_lan.grid(row=1, column=1, pady=5, sticky="n")

        self.button_dau_nam = tk.Button(self.button_frame, text="Cúng đầu năm", command=self.cung_dau_nam)
        self.button_dau_nam.grid(row=1, column=2, pady=5, sticky="n")

        self.button_con_ban = tk.Button(self.button_frame, text="Cúng con bán", command=self.cung_con_ban)
        self.button_con_ban.grid(row=1, column=3, pady=5, sticky="n")

        self.button_con_ban = tk.Button(self.button_frame, text="Cúng sao", command=self.cung_sao)
        self.button_con_ban.grid(row=1, column=4, pady=5, sticky="n")

        # Tạo Frame mới chiếm từ row=0 đến row=4 và column=2
        self.right_frame = tk.Frame(self)
        self.right_frame.grid(row=0, column=2, rowspan=6, sticky="nsew")

        self.list_frame = None

        self.create_frame()
        # Cấu hình lưới để cột 2 có thể mở rộng
        self.grid_columnconfigure(2, weight=1)  

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
            self.ma_gia_dinh_entry.config(state='normal')
            self.ma_gia_dinh_entry.delete(0, tk.END)
            self.ma_gia_dinh_entry.insert(0, family.get("maGiaDinh", ""))
            self.ma_gia_dinh_entry.config(state='readonly')

            self.tin_chu_entry.config(state='normal')
            self.tin_chu_entry.delete(0, tk.END)
            self.tin_chu_entry.insert(0, family.get("tinChu", ""))
            self.tin_chu_entry.config(state='readonly')

            self.chan_linh_entry.config(state='normal')
            self.chan_linh_entry.delete("1.0", tk.END)
            self.chan_linh_entry.insert("1.0", family.get("chanLinh", ""))
            self.chan_linh_entry.config(state='disabled')

            # Tạo bảng thành viên
            self.create_member_table(family.get("thanhVien", []))

        else:
            messagebox.showinfo("Thông báo", "Không tìm thấy gia đình!")
            self.search_entry.delete(0, tk.END)

    def create_member_table(self, members):
        # Xóa bảng cũ nếu có
        if self.member_table_frame:
            self.member_table_frame.destroy()

        # Khung chứa bảng và thanh cuộn
        self.member_table_frame = tk.Frame(self)
        self.member_table_frame.grid(row=3, column=1, sticky="nsew") #, columnspan=2

        # Đảm bảo khung có thể co giãn
        self.member_table_frame.rowconfigure(1, weight=1)
        self.member_table_frame.columnconfigure(0, weight=1)

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
        headers = ["Họ và tên", "Năm sinh", "Con bán"]
        column_widths = [30, 15, 15]  # Đặt khoảng rộng cho từng cột

        for col, header in enumerate(headers):
            tk.Label(headers_frame, text=header, borderwidth=1, relief="solid", width=column_widths[col],
                     anchor='w').grid(row=0, column=col, sticky='nsew')

        # Hiển thị dữ liệu thành viên
        for row, member in enumerate(members):
            ho_va_ten = member.get("ho_va_ten", "")
            nam_sinh = member.get("nam_sinh", "")
            con_ban = member.get("con_ban", "")

            tk.Entry(self.member_frame, borderwidth=1, relief="solid", width=column_widths[0], state='readonly',
                     textvariable=tk.StringVar(value=ho_va_ten)).grid(row=row, column=0, sticky='nsew')
            tk.Entry(self.member_frame, borderwidth=1, relief="solid", width=column_widths[1], state='readonly',
                     textvariable=tk.StringVar(value=nam_sinh)).grid(row=row, column=1, sticky='nsew')
            tk.Entry(self.member_frame, borderwidth=1, relief="solid", width=column_widths[2], state='readonly',
                     textvariable=tk.StringVar(value=con_ban)).grid(row=row, column=2, sticky='nsew')

        # Cập nhật kích thước của canvas
        self.member_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    # Thêm phương thức để xóa dữ liệu các ô nhập
    def clear_entries(self):
        # Xóa toàn bộ dữ liệu trong các ô nhập
        self.ma_gia_dinh_entry.config(state='normal')
        self.ma_gia_dinh_entry.delete(0, tk.END)
        self.ma_gia_dinh_entry.config(state='readonly')

        self.tin_chu_entry.config(state='normal')
        self.tin_chu_entry.delete(0, tk.END)
        self.tin_chu_entry.config(state='readonly')

        self.chan_linh_entry.config(state='normal')
        self.chan_linh_entry.delete("1.0", tk.END)
        self.chan_linh_entry.config(state='disabled')

        # Xóa bảng thành viên nếu có
        if self.member_table_frame:
            self.member_table_frame.destroy()
    
    def chon(self):
        # Tăng STT sau mỗi lần thêm vào bảng
        self.stt_count += 1
        ma_gia_dinh = self.ma_gia_dinh_entry.get().strip()
        tin_chu = self.tin_chu_entry.get().strip()

        # Kiểm tra xem có dữ liệu hợp lệ không
        if not ma_gia_dinh or not tin_chu:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ mã gia đình và tên tín chủ.")
            return

        self.add_to_table(self.stt_count, ma_gia_dinh, tin_chu)        

    def add_to_table(self, stt, ma_gia_dinh, tin_chu):
        row = self.table_fr.grid_size()[1]  # Đếm số dòng hiện có trong bảng (đã có header)
        self.list_ma.append(ma_gia_dinh)
        tk.Label(self.table_fr, text=str(stt), borderwidth=1, relief="solid", width=5).grid(row=row, column=0, sticky='nsew')
        tk.Label(self.table_fr, text=ma_gia_dinh, borderwidth=1, relief="solid", width=15).grid(row=row, column=1, sticky='nsew')
        tk.Label(self.table_fr, text=tin_chu, borderwidth=1, relief="solid", width=50).grid(row=row, column=2, sticky='nsew')

        # Update canvas scrolling region
        self.table_fr.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def create_frame(self):
        # Xóa bảng cũ nếu có
        if self.list_frame:
            self.list_frame.destroy()
    
        # Create the frame and canvas
        self.list_frame = tk.Frame(self.right_frame)
        self.list_frame.pack(fill='both', expand=True)

        self.canvas = tk.Canvas(self.list_frame)
        self.canvas.pack(side=tk.LEFT, fill='both', expand=True)

        scrollbar = tk.Scrollbar(self.list_frame, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill='y')

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.table_fr = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.table_fr, anchor='nw')
        #------------------
        # Tạo bảng tiêu đề
        headers = ["STT", "MÃ", "Tín chủ"]
        column_widths = [5, 15, 50]
        for col, (header, width) in enumerate(zip(headers, column_widths)):
            tk.Label(self.table_fr, text=header, borderwidth=1, relief="solid", width=width, anchor='center').grid(row=0, column=col, sticky='nsew')

        print("Headers, Canvas đã được tạo")

    @staticmethod
    def get_desktop_path():
        if os.name == 'nt':  # Windows
            return Path.home() / "Desktop"
        elif os.name == 'posix':  # macOS và Linux
            # Kiểm tra biến môi trường cho Linux nếu có
            desktop_path = os.getenv("XDG_DESKTOP_DIR", Path.home() / "Desktop")
            return Path(desktop_path)
        else:
            raise Exception("Hệ điều hành không được hỗ trợ")
    
    def cung_1_15(self):
        desktop_path = self.get_desktop_path() / "ngay1va15.docx"
        doc_list = self.controller.list_printed(self.list_ma)
        self.controller.ngay_print(desktop_path, doc_list)

    def cung_vu_lan(self):
        desktop_path = self.get_desktop_path() / "ngayVL.docx"
        doc_list = self.controller.list_printed(self.list_ma)
        self.controller.vu_lan_print(desktop_path, doc_list)

    def cung_dau_nam(self):
        desktop_path = self.get_desktop_path() / "ngayDN.docx"
        doc_list = self.controller.list_printed(self.list_ma)
        self.controller.dau_nam_print(desktop_path, doc_list)

    def cung_con_ban(self):
        desktop_path = self.get_desktop_path() / "ngayCB.docx"
        doc_list = self.controller.list_printed(self.list_ma)
        self.controller.con_ban_print(desktop_path, doc_list)

    def cung_sao(self):
        desktop_path = self.get_desktop_path() / "cungSAO.docx"
        doc_list = self.controller.list_printed(self.list_ma)
        self.controller.sao_print(desktop_path, doc_list)
