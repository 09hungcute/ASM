import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk, Image
from data import get_all_drinks, add_drink, delete_drink_from_db, update_drink
import os

class CoffeeShopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Coffee Shop Manager")
        self.root.geometry("900x600")
        self.root.configure(bg="#f0f2f5")

        # Tạo style cho ttk với theme hiện đại
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", font=("Helvetica", 12, "bold"), padding=6, background="#0078D7", foreground="#fff")
        self.style.map("TButton", background=[("active", "#005a9e")])
        self.style.configure("TLabel", font=("Helvetica", 12), background="#f0f2f5")
        
        self.main_frame = tk.Frame(root, bg="#f0f2f5")
        self.main_frame.pack(fill="both", expand=True)

        self.order = []  # Danh sách đặt hàng
        self.create_home_screen()

    def create_home_screen(self):
        """Hiển thị trang chủ"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        header = tk.Label(self.main_frame, text="☕ Chào mừng đến Coffee Shop ☕", font=("Helvetica", 20, "bold"), bg="#f0f2f5", fg="#333")
        header.pack(pady=20)
        ttk.Button(self.main_frame, text="📜 Xem Menu", command=self.show_menu).pack(pady=10)
        ttk.Button(self.main_frame, text="📊 Dashboard", command=self.show_dashboard).pack(pady=10)
        ttk.Button(self.main_frame, text="🛒 Xem Đơn Hàng", command=self.show_order).pack(pady=10)

    def show_dashboard(self):
        """Hiển thị trang Dashboard"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        header = tk.Label(self.main_frame, text="📊 Dashboard", font=("Helvetica", 20, "bold"), bg="#f0f2f5", fg="#333")
        header.pack(pady=20)
        ttk.Button(self.main_frame, text="🆕 New Drink", command=self.add_new_drink).pack(pady=10)
        ttk.Button(self.main_frame, text="📋 List Drinks", command=self.list_drinks).pack(pady=10)
        ttk.Button(self.main_frame, text="🏠 Quay về Trang Chủ", command=self.create_home_screen).pack(pady=10)

    def add_new_drink(self):
        """Màn hình thêm món mới"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        header = tk.Label(self.main_frame, text="🆕 Thêm Đồ Uống", font=("Helvetica", 20, "bold"), bg="#f0f2f5", fg="#333")
        header.pack(pady=10)

        # Entry widgets cho món mới
        tk.Label(self.main_frame, text="Tên món:", font=("Helvetica", 12), bg="#f0f2f5").pack()
        self.name_entry = tk.Entry(self.main_frame, font=("Helvetica", 12))
        self.name_entry.pack(pady=5)

        tk.Label(self.main_frame, text="Giá (VNĐ):", font=("Helvetica", 12), bg="#f0f2f5").pack()
        self.price_entry = tk.Entry(self.main_frame, font=("Helvetica", 12))
        self.price_entry.pack(pady=5)

        tk.Label(self.main_frame, text="Mô tả:", font=("Helvetica", 12), bg="#f0f2f5").pack()
        self.desc_entry = tk.Entry(self.main_frame, font=("Helvetica", 12))
        self.desc_entry.pack(pady=5)

        tk.Label(self.main_frame, text="Đường dẫn ảnh:", font=("Helvetica", 12), bg="#f0f2f5").pack()
        self.img_entry = tk.Entry(self.main_frame, font=("Helvetica", 12), state="readonly")
        self.img_entry.pack(pady=5)

        def upload_image():
            file_path = filedialog.askopenfilename(
                title="Chọn ảnh",
                filetypes=[("Ảnh", "*.png;*.jpg;*.jpeg;*.gif;*.bmp"), ("Tất cả", "*.*")]
            )
            if file_path:
                self.img_entry.config(state="normal")
                self.img_entry.delete(0, tk.END)
                self.img_entry.insert(0, file_path)
                self.img_entry.config(state="readonly")

        ttk.Button(self.main_frame, text="📁 Chọn Ảnh", command=upload_image).pack(pady=5)

        def submit():
            name = self.name_entry.get()
            price = self.price_entry.get()
            desc = self.desc_entry.get()
            img = self.img_entry.get()

            if name and price:
                try:
                    price_int = int(price)
                except ValueError:
                    messagebox.showwarning("Lỗi giá", "Giá phải là số hợp lệ!")
                    return
                add_drink(name, price_int, desc, img)
                messagebox.showinfo("Thành công", "Đã thêm món mới!")
                self.show_dashboard()
            else:
                messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ thông tin!")

        ttk.Button(self.main_frame, text="✅ Thêm", command=submit).pack(pady=10)
        ttk.Button(self.main_frame, text="🔙 Quay lại", command=self.show_dashboard).pack(pady=10)

    def list_drinks(self):
        """Hiển thị danh sách đồ uống có ảnh, chi tiết, và chức năng sửa/xóa"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        header = tk.Label(self.main_frame, text="📋 Danh sách đồ uống", font=("Helvetica", 20, "bold"), bg="#f0f2f5", fg="#333")
        header.pack(pady=10)

        drinks = get_all_drinks()
        # Create a canvas and a scrollbar
        canvas = tk.Canvas(self.main_frame, bg="#f0f2f5")
        scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame that will hold all the drink items
        item_frame = tk.Frame(canvas, bg="#f0f2f5")
        canvas.create_window((0, 0), window=item_frame, anchor="nw")

        for drink in drinks:
            item = tk.Frame(item_frame, relief=tk.RAISED, borderwidth=2, padx=10, pady=10, bg="white")
            item.pack(fill="x", pady=5, padx=10)

            try:
                img = Image.open(drink["image"]).resize((80, 80))
                img = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Error opening image: {e}")
                img = Image.new('RGB', (80, 80), color='gray')
                img = ImageTk.PhotoImage(img)

            lbl_img = tk.Label(item, image=img)
            lbl_img.image = img
            lbl_img.pack(side="left", padx=10)

            details_frame = tk.Frame(item, bg="white")
            details_frame.pack(side="left", padx=10)
            tk.Label(details_frame, text=f"{drink['name']} - {drink['price']} VNĐ", font=("Helvetica", 12, "bold"), bg="white").pack(anchor="w")
            tk.Label(details_frame, text=drink['description'], font=("Helvetica", 10), bg="white").pack(anchor="w")

            btn_frame = tk.Frame(item, bg="white")
            btn_frame.pack(side="right", padx=10)
            ttk.Button(btn_frame, text="📝 Sửa", command=lambda d=drink: self.edit_drink(d)).pack(side="left", padx=5)
            ttk.Button(btn_frame, text="❌ Xóa", command=lambda d=drink: self.delete_drink(d)).pack(side="left", padx=5)

        item_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        
        canvas.pack(side="left", fill="both", expand=True, padx=10)
        scrollbar.pack(side="right", fill="y")
        ttk.Button(self.main_frame, text="🔙 Quay lại", command=self.show_dashboard).pack(pady=10)

    def edit_drink(self, drink):
        """Mở màn hình chỉnh sửa đồ uống"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        container = ttk.Frame(self.main_frame, padding=20)
        container.pack(expand=True)

        header = tk.Label(container, text=f"📝 Chỉnh sửa {drink['name']}", font=("Helvetica", 20, "bold"), bg="#f0f2f5", fg="#333")
        header.grid(row=0, column=0, columnspan=2, pady=10)

        original_name = drink['name']
        original_image = drink['image']

        # Các input field
        fields = [
            ("Tên đồ uống", drink['name']),
            ("Giá tiền", drink['price']),
            ("Mô tả", drink['description']),
            ("Ảnh", drink['image'])
        ]

        entries = {}
        for i, (label_text, value) in enumerate(fields):
            ttk.Label(container, text=label_text, font=("Helvetica", 12, "bold")).grid(row=i+1, column=0, sticky="w", padx=5, pady=5)
            entry = ttk.Entry(container, width=40, font=("Helvetica", 12))
            entry.insert(0, value)
            entry.grid(row=i+1, column=1, padx=5, pady=5)
            entries[label_text] = entry

        def select_image():
            file_path = filedialog.askopenfilename(
                title="Chọn ảnh mới",
                filetypes=[("Image files", "*.jpg;*.png;*.jpeg;*.gif")]
            )
            if file_path:
                entries["Ảnh"].delete(0, tk.END)
                entries["Ảnh"].insert(0, file_path)

        ttk.Button(container, text="📷 Chọn ảnh", command=select_image).grid(row=5, column=1, sticky="w", padx=5, pady=5)

        def submit():
            new_name = entries["Tên đồ uống"].get()
            new_price = entries["Giá tiền"].get()
            new_desc = entries["Mô tả"].get()
            new_img = entries["Ảnh"].get()

            if not new_price.isdigit():
                messagebox.showwarning("Lỗi giá", "Giá phải là một số hợp lệ!")
                return
            new_price = int(new_price)

            if new_name and new_price:
                if new_img != original_image and os.path.exists(original_image):
                    os.remove(original_image)

                update_drink(original_name, new_name, new_price, new_desc, new_img)
                messagebox.showinfo("Thành công", "Món đồ uống đã được cập nhật!")
                self.show_dashboard()
            else:
                messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ thông tin!")

        button_frame = ttk.Frame(container)
        button_frame.grid(row=6, column=0, columnspan=2, pady=15)

        ttk.Button(button_frame, text="✅ Cập nhật", command=submit, width=15).grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text="🔙 Quay lại", command=self.show_dashboard, width=15).grid(row=0, column=1, padx=10)

    def delete_drink(self, drink):
        """Xóa món uống"""
        confirm = messagebox.askyesno("Xóa món", f"Bạn có chắc chắn muốn xóa {drink['name']}?", icon="warning")
        if confirm:
            delete_drink_from_db(drink['name'])
            self.list_drinks()

    def show_menu(self):
        """Hiển thị menu dạng lưới với bộ lọc"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        header = tk.Label(self.main_frame, text="📜 Menu Cà Phê", font=("Helvetica", 20, "bold"), bg="#f0f2f5", fg="#333")
        header.pack(pady=10)
        ttk.Button(self.main_frame, text="🛒 Xem Giỏ Hàng", command=self.show_order).pack(pady=10)

        # Bộ lọc
        filter_frame = tk.Frame(self.main_frame, bg="#f0f2f5")
        filter_frame.pack(pady=5)

        tk.Label(filter_frame, text="🔎 Tìm kiếm:", font=("Helvetica", 12), bg="#f0f2f5").grid(row=0, column=0, padx=5)
        search_entry = tk.Entry(filter_frame, width=20, font=("Helvetica", 12))
        search_entry.grid(row=0, column=1, padx=5)

        tk.Label(filter_frame, text="💰 Lọc giá:", font=("Helvetica", 12), bg="#f0f2f5").grid(row=0, column=2, padx=5)
        price_filter = tk.StringVar(value="Tất cả")
        price_options = ["Tất cả", "Dưới 50.000", "50.000 - 100.000", "Trên 100.000"]
        ttk.Combobox(filter_frame, textvariable=price_filter, values=price_options, state="readonly", width=15, font=("Helvetica", 12)).grid(row=0, column=3, padx=5)

        ttk.Button(filter_frame, text="📌 Lọc", command=lambda: apply_filter()).grid(row=0, column=4, padx=5)

        frame = tk.Frame(self.main_frame, bg="#f0f2f5")
        frame.pack()

        drinks = get_all_drinks()
        columns = 3
        row, col = 0, 0

        def display_drinks(filtered_drinks):
            for widget in frame.winfo_children():
                widget.destroy()
            nonlocal row, col
            row, col = 0, 0
            for drink in filtered_drinks:
                item_frame = tk.Frame(frame, relief=tk.RAISED, borderwidth=2, padx=10, pady=10, bg="white")
                item_frame.grid(row=row, column=col, padx=10, pady=10)

                try:
                    img = Image.open(drink["image"]).resize((100, 100))
                    img = ImageTk.PhotoImage(img)
                except Exception as e:
                    print(f"Error opening image: {e}")
                    img = Image.new('RGB', (100, 100), color='gray')
                    img = ImageTk.PhotoImage(img)

                lbl_img = tk.Label(item_frame, image=img, bg="white")
                lbl_img.image = img
                lbl_img.pack()

                lbl_name = tk.Label(item_frame, text=f"{drink['name']}", font=("Helvetica", 12, "bold"), bg="white")
                lbl_name.pack()

                lbl_price = tk.Label(item_frame, text=f"{drink['price']} VNĐ", font=("Helvetica", 12), bg="white")
                lbl_price.pack()

                btn_add = ttk.Button(item_frame, text="➕ Thêm", command=lambda d=drink: self.add_to_order(d))
                btn_add.pack()

                col += 1
                if col >= columns:
                    col = 0
                    row += 1

        def apply_filter():
            keyword = search_entry.get().strip().lower()
            selected_price = price_filter.get()
            filtered_drinks = [drink for drink in drinks if keyword in drink["name"].lower()]
            if selected_price == "Dưới 50.000":
                filtered_drinks = [drink for drink in filtered_drinks if drink["price"] < 50000]
            elif selected_price == "50.000 - 100.000":
                filtered_drinks = [drink for drink in filtered_drinks if 50000 <= drink["price"] <= 100000]
            elif selected_price == "Trên 100.000":
                filtered_drinks = [drink for drink in filtered_drinks if drink["price"] > 100000]
            display_drinks(filtered_drinks)

        display_drinks(drinks)
        ttk.Button(self.main_frame, text="🔙 Quay lại", command=self.create_home_screen).pack(pady=10)

    def add_to_order(self, drink):
        """Thêm món vào giỏ hàng"""
        self.order.append(drink)
        messagebox.showinfo("Giỏ hàng", f"Đã thêm {drink['name']} vào giỏ hàng!")

    def show_order(self):
        """Hiển thị giỏ hàng với giao diện có ảnh và thông tin chi tiết cho từng món"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        header = tk.Label(self.main_frame, text="🛒 Giỏ Hàng", font=("Helvetica", 20, "bold"), bg="#f0f2f5", fg="#333")
        header.pack(pady=10)
        top_frame = tk.Frame(self.main_frame, bg="#f0f2f5")
        top_frame.pack(fill="x", pady=5)
        ttk.Button(top_frame, text="🔙 Quay về Menu", command=self.show_menu).pack(expand=True)

        if not self.order:
            tk.Label(self.main_frame, text="Giỏ hàng của bạn đang trống!", font=("Helvetica", 12), bg="#f0f2f5").pack()
        else:
            order_frame = tk.Frame(self.main_frame, bg="#f0f2f5")
            order_frame.pack(fill="both", expand=True, padx=10, pady=10)

            total_price = 0
            for drink in self.order:
                item_frame = tk.Frame(order_frame, relief=tk.RIDGE, borderwidth=2, padx=10, pady=10, bg="white")
                item_frame.pack(fill="x", pady=5)

                image_path = drink["image"]
                try:
                    if os.path.exists(image_path):
                        img = Image.open(image_path).resize((80, 80))
                        img = ImageTk.PhotoImage(img)
                    else:
                        raise Exception("File not found")
                except Exception as e:
                    print(f"Error opening image: {e}")
                    img = Image.new('RGB', (80, 80), color='gray')
                    img = ImageTk.PhotoImage(img)
                lbl_img = tk.Label(item_frame, image=img, bg="white")
                lbl_img.image = img
                lbl_img.pack(side="left", padx=10)

                details_frame = tk.Frame(item_frame, bg="white")
                details_frame.pack(side="left", fill="x", expand=True)
                tk.Label(details_frame, text=drink['name'], font=("Helvetica", 12, "bold"), bg="white").pack(anchor="w")
                tk.Label(details_frame, text=f"{drink['price']} VNĐ", font=("Helvetica", 12), bg="white").pack(anchor="w")
                tk.Label(details_frame, text="Số lượng: 1", font=("Helvetica", 12), bg="white").pack(anchor="w")
                item_total = drink['price']
                total_price += item_total
                tk.Label(details_frame, text=f"Tổng: {item_total} VNĐ", font=("Helvetica", 12), bg="white").pack(anchor="w")

            tk.Label(self.main_frame, text=f"Tổng giỏ hàng: {total_price} VNĐ", font=("Helvetica", 14, "bold"), bg="#f0f2f5").pack(pady=10)

        button_frame = tk.Frame(self.main_frame, bg="#f0f2f5")
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Thanh toán", command=self.checkout).pack(side="left", padx=20)
        ttk.Button(button_frame, text="Quay lại", command=self.create_home_screen).pack(side="left", padx=20)

    def checkout(self):
        """Xử lý thanh toán"""
        messagebox.showinfo("Thanh toán", "Cảm ơn bạn đã mua hàng! Thanh toán thành công.")
        self.order.clear()
        self.create_home_screen()

if __name__ == "__main__":
    root = tk.Tk()
    app = CoffeeShopApp(root)
    root.mainloop()
