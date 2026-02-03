import pandas as pd
from datetime import datetime
import random
import os

# 1. Hàm giả lập lấy giá xăng (Sau này mình sẽ thay bằng code cào web thật)
def lay_gia_xang():
    print("Dang ket noi den server...")
    # Giả vờ đợi 1 chút
    
    # Random giá để test
    gia_ron95 = 24000 + random.randint(-500, 500)
    gia_e5 = 23000 + random.randint(-500, 500)
    
    print(f"Da lay duoc gia: RON 95 = {gia_ron95}, E5 = {gia_e5}")
    
    # Tạo bảng dữ liệu
    du_lieu = {
        'Ngay': [datetime.now().strftime("%Y-%m-%d")],
        'Gio': [datetime.now().strftime("%H:%M:%S")],
        'RON_95': [gia_ron95],
        'E5_RON_92': [gia_e5]
    }
    
    return pd.DataFrame(du_lieu)

# 2. Hàm lưu vào file Excel/CSV
def luu_file(du_lieu_moi):
    ten_file = 'lich_su_gia_xang.csv'
    
    # Kiểm tra xem file đã có chưa
    if not os.path.isfile(ten_file):
        # Chưa có thì tạo mới, ghi cả tiêu đề cột
        du_lieu_moi.to_csv(ten_file, index=False)
    else:
        # Có rồi thì ghi nối tiếp vào đuôi (mode='a'), không ghi lại tiêu đề
        du_lieu_moi.to_csv(ten_file, mode='a', header=False, index=False)
    
    print(f"Da luu vao file {ten_file} thanh cong!")

# --- CHẠY CHƯƠNG TRÌNH ---
if __name__ == "__main__":
    df = lay_gia_xang()
    luu_file(df)
    print("--- Hoan tat ---")