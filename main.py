import requests
import pandas as pd
from datetime import datetime, timedelta # Nhớ import timedelta
import os

# CẤU HÌNH
URL = "https://webgia.com/gia-xang-dau/petrolimex/"
FILE_NAME = 'lich_su_gia_xang.csv'

def lay_gia_xang_thong_minh():
    print(f"Dang ket noi den {URL}...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(URL, headers=headers)
        
        # --- KỸ THUẬT MỚI: DÙNG PANDAS QUÉT TOÀN BỘ BẢNG ---
        danh_sach_bang = pd.read_html(response.text)
        
        if len(danh_sach_bang) == 0:
            print("Khong tim thay bang gia nao tren web!")
            return None
        
        # Thường bảng giá nằm ở vị trí đầu tiên (index 0)
        df_bang_gia = danh_sach_bang[0]
        
        # Đổi tên cột cho dễ xử lý
        df_bang_gia = df_bang_gia.iloc[:, :2]
        df_bang_gia.columns = ['Loai_Xang', 'Gia_Vung_1']
        
        print("--- Tim thay bang gia ---")
        
        # LỌC DỮ LIỆU
        gia_ron95 = 0
        gia_e5 = 0
        
        # 1. Lấy giá RON 95
        try:
            dong_95 = df_bang_gia[df_bang_gia['Loai_Xang'].str.contains("RON 95", case=False, na=False)]
            if not dong_95.empty:
                gia_raw = str(dong_95.iloc[0]['Gia_Vung_1'])
                gia_ron95 = int(gia_raw.replace('.', '').replace(',', ''))
        except:
            pass

        # 2. Lấy giá E5
        try:
            dong_e5 = df_bang_gia[df_bang_gia['Loai_Xang'].str.contains("E5", case=False, na=False)]
            if not dong_e5.empty:
                gia_raw = str(dong_e5.iloc[0]['Gia_Vung_1'])
                gia_e5 = int(gia_raw.replace('.', '').replace(',', ''))
        except:
            pass

        print(f"KET QUA: RON 95 = {gia_ron95}, E5 = {gia_e5}")

        if gia_ron95 == 0:
            print("Van khong lay duoc gia. Web doi cau truc qua nhieu!")
            return None

        # --- PHẦN SỬA LỖI Ở ĐÂY ---
        # 1. Tính toán giờ TRƯỚC KHI tạo dictionary
        gio_vn = datetime.utcnow() + timedelta(hours=7)

        # 2. Đóng gói (Lưu ý: Tôi đã thêm lại cột RON_95 bị thiếu)
        du_lieu = {
            'Ngay': [gio_vn.strftime("%Y-%m-%d")],
            'Gio': [gio_vn.strftime("%H:%M:%S")],
            'RON_95': [gia_ron95], 
            'E5_RON_92': [gia_e5]
        }
        return pd.DataFrame(du_lieu)

    except Exception as e:
        print(f"Loi: {e}")
        return None

def luu_file(du_lieu_moi):
    if not os.path.isfile(FILE_NAME):
        du_lieu_moi.to_csv(FILE_NAME, index=False)
    else:
        du_lieu_moi.to_csv(FILE_NAME, mode='a', header=False, index=False)
    print("Da luu vao CSV!")

if __name__ == "__main__":
    df = lay_gia_xang_thong_minh()
    if df is not None:
        luu_file(df)