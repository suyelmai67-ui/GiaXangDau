import streamlit as st
import pandas as pd

# 1. Tiêu đề trang web
st.title("⛽ Biểu đồ Theo Dõi Giá Xăng Việt Nam")
st.write("Dữ liệu được cập nhật tự động hàng ngày từ Petrolimex.")

# 2. Đọc dữ liệu từ file CSV
try:
    # Đọc file và chuyển cột 'Ngay' sang dạng thời gian để vẽ biểu đồ cho đẹp
    df = pd.read_csv('lich_su_gia_xang.csv', parse_dates=['Ngay'])
    
    # Sắp xếp theo ngày mới nhất lên đầu để xem bảng
    st.dataframe(df.sort_values(by='Ngay', ascending=False))

    # 3. Vẽ biểu đồ đường (Line Chart)
    st.subheader("Biểu đồ biến động giá")
    # Chọn cột Ngay làm trục hoành (ngang), giá làm trục tung (dọc)
    bieu_do = df.set_index('Ngay')[['RON_95', 'E5_RON_92']]
    st.line_chart(bieu_do)

except FileNotFoundError:
    st.error("Chưa có dữ liệu! Hãy chạy file main.py trước hoặc đợi Robot chạy.")