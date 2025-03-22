import os  # Import os để kiểm tra và xóa tệp
from tkinter import messagebox  # Import messagebox từ tkinter để hiển thị thông báo

from pymongo import MongoClient

# Kết nối đến MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["cafeChill"]
collection = db["drinks"]

# Kiểm tra nếu database trống thì thêm dữ liệu mẫu
if collection.count_documents({}) == 0:
    default_drinks = [
        {
            "name": "Espresso",
            "price": 35000,
            "description": "Một ly espresso đậm đà với hương vị mạnh mẽ.",
            "image": "assets/images/espresso.jpg"
        },
        {
            "name": "Cappuccino",
            "price": 40000,
            "description": "Sự kết hợp giữa espresso, sữa nóng và bọt sữa.",
            "image": "assets/images/cappuccino.jpg"
        },
        {
            "name": "Latte",
            "price": 45000,
            "description": "Espresso hòa quyện với sữa tươi tạo nên hương vị nhẹ nhàng.",
            "image": "assets/images/latte.jpg"
        }
    ]
    collection.insert_many(default_drinks)
    print("✅ Đã thêm dữ liệu mặc định vào MongoDB!")

# Lấy danh sách đồ uống
def get_all_drinks():
    return list(collection.find({}, {"_id": 0}))

# Thêm đồ uống mới
def add_drink(name, price, description, image):
    collection.insert_one({
        "name": name,
        "price": price,
        "description": description,
        "image": image
    })

# Cập nhật món uống
def update_drink(original_name, new_name, price, description, image):
    """Cập nhật thông tin món uống"""
    collection.update_one(
        {"name": original_name},  # Tìm món uống theo tên cũ
        {"$set": {  # Thực hiện cập nhật các trường
            "name": new_name,  # Cập nhật tên mới
            "price": price,
            "description": description,
            "image": image
        }}
    )

# Xóa món uống
def delete_drink_from_db(name):
    """Xóa món uống khỏi cơ sở dữ liệu MongoDB"""
    drink_to_delete = collection.find_one({"name": name})  # Tìm món uống theo tên

    if drink_to_delete:
        # Xóa ảnh nếu cần
        image_path = drink_to_delete["image"]
        if os.path.exists(image_path):
            os.remove(image_path)  # Xóa ảnh trong thư mục uploads nếu cần

        # Xóa món uống khỏi collection
        collection.delete_one({"name": name})

        messagebox.showinfo("Thành công", f"Đã xóa {name}")
    else:
        messagebox.showwarning("Lỗi", "Không tìm thấy món uống!")
