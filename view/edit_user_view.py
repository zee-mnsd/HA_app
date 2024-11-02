import tkinter as tk
from tkinter import messagebox

class EditUserView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.place(relwidth=1, relheight=1)
        self.create_widgets()
        # Initialize member table with no members
        # self.create_member_table([])

    def create_widgets(self):
        # Search area
        tk.Label(self, text="Mã gia đình:").grid(row=0, column=0, sticky="e", padx=(5, 2), pady=2)
        self.search_entry = tk.Entry(self, width=20)
        self.search_entry.grid(row=0, column=1, sticky="w", pady=2)

        self.search_button = tk.Button(self, text="Tìm kiếm", command=self.search_family)
        self.search_button.grid(row=0, column=1, padx=(5, 2), pady=2)

        # Family code
        tk.Label(self, text="Mã gia đình:").grid(row=1, column=0, sticky="e", padx=(5, 2), pady=2)
        self.ma_gia_dinh_entry = tk.Entry(self, state='readonly', width=30)
        self.ma_gia_dinh_entry.grid(row=1, column=1, sticky="w", pady=2, columnspan=2)

        # Family head
        tk.Label(self, text="Tín chủ:").grid(row=2, column=0, sticky="e", padx=(5, 2), pady=2)
        self.tin_chu_entry = tk.Entry(self, state='readonly', width=30)
        self.tin_chu_entry.grid(row=2, column=1, sticky="w", pady=2, columnspan=2)

        # Member table
        tk.Label(self, text="Thành viên:").grid(row=3, column=0, sticky="ne", padx=(5, 2), pady=2)
        self.member_table_frame = tk.Frame(self, bd=1, relief="sunken")
        self.member_table_frame.grid(row=3, column=1, columnspan=2, sticky="nsew")

        # Placeholder for the member frame
        self.member_frame = None

        # Ancestor text
        tk.Label(self, text="Chân linh:").grid(row=4, column=0, sticky="ne", padx=(5, 2), pady=2)
        self.chan_linh_entry = tk.Text(self, height=5, width=60)
        self.chan_linh_entry.grid(row=4, column=1, sticky="w", pady=2, columnspan=2)

        # Add member rows
        tk.Label(self, text="Số lượng cần thêm:").grid(row=5, column=0, sticky="e", padx=(5, 2), pady=2)
        self.so_luong_entry = tk.Entry(self, width=5)
        self.so_luong_entry.grid(row=5, column=1, sticky="w", pady=2)

        self.add_rows_button = tk.Button(self, text="Thêm", command=self.update_member_table)
        self.add_rows_button.grid(row=5, column=1, padx=(5, 2), pady=2)

        # Update button
        self.update_button = tk.Button(self, text="Cập nhật", command=self.on_edit_button_clicked)
        self.update_button.grid(row=6, column=1, pady=10, sticky="w", columnspan=2)

        # Configure grid weights
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def search_family(self):
        search_ID = self.search_entry.get().strip()
        if not search_ID:
            messagebox.showerror("Lỗi", "Mã gia đình không được để trống.")
            return

        family = self.controller.search_user(search_ID)
        if family:
            self.search_entry.delete(0, tk.END)
            self.ma_gia_dinh_entry.config(state='normal')
            self.ma_gia_dinh_entry.delete(0, tk.END)
            self.ma_gia_dinh_entry.insert(0, family.get("maGiaDinh", ""))
            self.ma_gia_dinh_entry.config(state='readonly')

            self.tin_chu_entry.config(state='normal')
            self.tin_chu_entry.delete(0, tk.END)
            self.tin_chu_entry.insert(0, family.get("tinChu", ""))
            self.tin_chu_entry.config(state='readonly')

            self.chan_linh_entry.delete("1.0", tk.END)
            self.chan_linh_entry.insert("1.0", family.get("chanLinh", ""))

            self.create_member_table(family.get("thanhVien", []))

        else:
            messagebox.showinfo("Thông báo", "Không tìm thấy gia đình!")
            self.search_entry.delete(0, tk.END)

    def update_member_table(self):
        try:
            num_rows = int(self.so_luong_entry.get().strip())
            if num_rows <= 0:
                raise ValueError("Số lượng phải là số dương.")
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số lượng hàng hợp lệ.")
            return

        # Add rows to the table
        for _ in range(num_rows):
            row_entries = []
            current_row = len(self.member_entries) + 1  # Headers are at row 0
            for col in range(3):
                entry = tk.Entry(self.table_fr, width=20)
                entry.grid(row=current_row, column=col, sticky='nsew', padx=1, pady=1)
                row_entries.append(entry)
            self.member_entries.append(row_entries)

        # Update canvas scrolling region
        self.table_fr.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def create_member_table(self, members):
        if self.member_frame:
            self.member_frame.destroy()

        # Create the frame and canvas
        self.member_frame = tk.Frame(self.member_table_frame)
        self.member_frame.pack(fill='both', expand=True)

        self.canvas = tk.Canvas(self.member_frame)
        self.canvas.pack(side=tk.LEFT, fill='both', expand=True)

        scrollbar = tk.Scrollbar(self.member_frame, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill='y')

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.table_fr = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.table_fr, anchor='nw')

        # Table headers
        headers = ["Họ và tên", "Năm sinh", "Con bản"]
        column_widths = [40, 10, 10]  # Adjusted widths
        for col, (header, width) in enumerate(zip(headers, column_widths)):
            tk.Label(self.table_fr, text=header, borderwidth=1, relief="solid", width=width, anchor='center').grid(row=0, column=col, sticky='nsew')

        # Member entries
        self.member_entries = []
        for row, member in enumerate(members, start=1):
            row_entries = []
            for col, (key, width) in enumerate(zip(["ho_va_ten", "nam_sinh", "con_ban"], column_widths)):
                entry = tk.Entry(self.table_fr, width=width)
                entry.insert(0, member.get(key, ""))
                entry.grid(row=row, column=col, sticky='nsew', padx=1, pady=1)
                row_entries.append(entry)
            self.member_entries.append(row_entries)

        # Configure canvas scrolling region
        self.table_fr.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def on_edit_button_clicked(self):
        ma_gia_dinh = self.ma_gia_dinh_entry.get().strip()
        tin_chu = self.tin_chu_entry.get().strip()
        chan_linh = self.chan_linh_entry.get("1.0", tk.END).strip()

        if not ma_gia_dinh or not tin_chu:
            messagebox.showerror("Lỗi", "Mã gia đình và Tín chủ không được để trống.")
            return

        thanh_vien = []
        for row_entries in self.member_entries:
            ho_va_ten = row_entries[0].get().strip()
            nam_sinh = row_entries[1].get().strip()
            con_ban = row_entries[2].get().strip()
            if not ho_va_ten or not nam_sinh:
                messagebox.showerror("Lỗi", "Mỗi thành viên cần có Họ và Tên và Năm sinh.")
                return
            thanh_vien.append({"ho_va_ten": ho_va_ten, "nam_sinh": nam_sinh, "con_ban": con_ban})

        self.controller.edit_user(ma_gia_dinh, tin_chu, chan_linh, thanh_vien)
