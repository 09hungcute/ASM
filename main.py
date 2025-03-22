import tkinter as tk
from views import CoffeeShopApp  # Import giao diện từ views.py

if __name__ == "__main__":
    root = tk.Tk()
    app = CoffeeShopApp(root)  # Khởi tạo ứng dụng
    root.mainloop()  # Chạy ứng dụng
