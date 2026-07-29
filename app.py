import streamlit as st

# Thiết lập trang Streamlit
st.set_page_config(
    page_title="Công cụ tính Thuế TNCN",
    page_icon="🧮",
    layout="centered"
)

st.title("🧮 Công Cụ Tính Thuế Thu Nhập Cá Nhân (TNCN) Nguyễn Tấn Duy Đề tài 7")
st.caption("Cập nhật theo quy định biểu thuế lũy tiến từng phần hiện hành")

st.markdown("---")

# --- NHẬP DỮ LIỆU INPUT ---
st.subheader("1. Thông tin thu nhập & Giảm trừ")

col1, col2 = st.columns(2)

with col1:
    luong_gross = st.number_input(
        "Lương GROSS / Thu nhập hàng tháng (VNĐ):", 
        min_value=0, 
        value=20000000, 
        step=1000000,
        format="%d"
    )
    
    nguoi_phu_thuoc = st.number_input(
        "Số người phụ thuộc:", 
        min_value=0, 
        value=0, 
        step=1
    )

with col2:
    bao_hiem = st.number_input(
        "Tiền đóng BHXH, BHYT, BHTN (VNĐ):", 
        min_value=0, 
        value=int(luong_gross * 0.105) if luong_gross <= 36000000 else 3780000, # Ước tính 10.5% bảo hiểm bắt buộc
        step=10000,
        format="%d",
        help="Mặc định gợi ý 10.5% lương GROSS (tối đa theo trần lương cơ sở/lương tối thiểu vùng)."
    )
    
    giam_tru_khac = st.number_input(
        "Các khoản giảm trừ khác (Từ thiện, hưu trí...):", 
        min_value=0, 
        value=0, 
        step=100000,
        format="%d"
    )

# Mức giảm trừ gia cảnh cố định theo quy định
GIAM_TRU_BAN_THAN = 11000000  # 11 triệu/tháng
GIAM_TRU_PHU_THUOC = 4400000  # 4.4 triệu/người/tháng

# --- HÀM TÍNH THUẾ LŨY TIẾN ---
def tinh_thue_tncn(thu_nhap_tinh_thue):
    if thu_nhap_tinh_thue <= 0:
        return 0, []
    
    bac_thue = [
        (5000000, 0.05, "Bậc 1 (Đến 5 triệu - 5%)"),
        (10000000, 0.10, "Bậc 2 (Từ trên 5 tr đến 10 tr - 10%)"),
        (18000000, 0.15, "Bậc 3 (Từ trên 10 tr đến 18 tr - 15%)"),
        (32000000, 0.20, "Bậc 4 (Từ trên 18 tr đến 32 tr - 20%)"),
        (52000000, 0.25, "Bậc 5 (Từ trên 32 tr đến 52 tr - 25%)"),
        (80000000, 0.30, "Bậc 6 (Từ trên 52 tr đến 80 tr - 30%)"),
        (float('inf'), 0.35, "Bậc 7 (Trên 80 triệu - 35%)")
    ]
    
    tong_thue = 0
    muc_truoc = 0
    chi_tiet = []
    
    for han_muc, thue_suat, ten_bac in bac_thue:
        if thu_nhap_tinh_thue > muc_truoc:
            phan_chieu_thue = min(thu_nhap_tinh_thue, han_muc) - muc_truoc
            thue_bac_nay = phan_chieu_thue * thue_suat
            tong_thue += thue_bac_nay
            chi_tiet.append((ten_bac, phan_chieu_thue, thue_bac_nay))
            muc_truoc = han_muc
        else:
            break
            
    return tong_thue, chi_tiet

# --- XỬ LÝ TÍNH TOÁN ---
tong_giam_tru_phu_thuoc = nguoi_phu_thuoc * GIAM_TRU_PHU_THUOC
tong_giam_tru = GIAM_TRU_BAN_THAN + tong_giam_tru_phu_thuoc + bao_hiem + giam_tru_khac
