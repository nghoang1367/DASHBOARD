import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# =============================================================================
# 1. CẤU HÌNH TRANG & GIAO DIỆN LIGHT PASTEL "NEXUS" CHUẨN HIỆN ĐẠI
# =============================================================================
st.set_page_config(
    page_title="DASHBOARD GROUP 11 | Rossmann Big Store Demand Forecasting",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS phong cách Pastel "Nexus" (Clean, Light, Elegant, Rounded, Modern)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

    /* Toàn bộ nền ứng dụng: Màu xám pastel sáng cực kỳ êm mắt */
    .stApp {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
        font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif !important;
    }

    /* Thanh cuộn mềm */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #F1F5F9;
    }
    ::-webkit-scrollbar-thumb {
        background: #CBD5E1;
        border-radius: 9999px;
    }

    /* Sidebar trắng thanh lịch với đường viền mỏng */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    section[data-testid="stSidebar"] .block-container {
        padding: 24px 18px !important;
    }

    /* Top breadcrumb & Header */
    .breadcrumb-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }
    .breadcrumb {
        font-size: 12px;
        color: #94A3B8;
        font-weight: 500;
    }
    .breadcrumb span {
        color: #4361EE;
        font-weight: 600;
    }
    .page-title {
        font-size: 24px;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.6px;
        margin-bottom: 20px;
    }

    /* THẺ KPI CARD PHONG CÁCH NEXUS (Trắng tinh khiết, viền pastel, đổ bóng mịn) */
    .nexus-kpi-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 20px 22px;
        box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.04), 0 2px 6px -1px rgba(15, 23, 42, 0.02);
        margin-bottom: 16px;
        transition: all 0.25s ease;
    }
    .nexus-kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 28px -4px rgba(67, 97, 238, 0.08);
        border-color: #CBD5E1;
    }
    .kpi-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }
    .kpi-title {
        font-size: 13px;
        font-weight: 600;
        color: #64748B;
        text-transform: capitalize;
    }
    .kpi-icon-box {
        width: 38px;
        height: 38px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
    }
    .kpi-val-row {
        display: flex;
        align-items: baseline;
        gap: 10px;
        margin-bottom: 6px;
        flex-wrap: wrap;
    }
    .kpi-val {
        font-size: 28px;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.5px;
        line-height: 1.1;
    }
    .kpi-badge-green {
        background-color: #DCFCE7;
        color: #15803D;
        padding: 3px 9px;
        border-radius: 9999px;
        font-size: 11.5px;
        font-weight: 700;
    }
    .kpi-badge-pink {
        background-color: #FFE4E6;
        color: #BE123C;
        padding: 3px 9px;
        border-radius: 9999px;
        font-size: 11.5px;
        font-weight: 700;
    }
    .kpi-badge-blue {
        background-color: #EEF2FF;
        color: #4361EE;
        padding: 3px 9px;
        border-radius: 9999px;
        font-size: 11.5px;
        font-weight: 700;
    }
    .kpi-sub {
        font-size: 12px;
        color: #94A3B8;
        font-weight: 500;
    }

    /* WIDGET CONTAINER LỚN */
    .nexus-panel {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 22px 24px;
        box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.04);
        margin-bottom: 16px;
    }
    .panel-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 16px;
    }
    .panel-title {
        font-size: 16px;
        font-weight: 700;
        color: #0F172A;
        letter-spacing: -0.3px;
    }
    .panel-sub {
        font-size: 12px;
        color: #64748B;
        margin-top: 2px;
    }

    /* SIDEBAR PROJECT CARD (Phong cách "Need Premium?" pastel) */
    .nexus-promo-box {
        background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%);
        border: 1px solid #C7D2FE;
        border-radius: 14px;
        padding: 16px;
        margin-top: 24px;
        color: #1E1B4B;
    }
    .promo-title {
        font-size: 13px;
        font-weight: 700;
        color: #3730A3;
        margin-bottom: 4px;
    }
    .promo-desc {
        font-size: 11.5px;
        color: #4338CA;
        line-height: 1.45;
        margin-bottom: 12px;
    }
    .promo-btn {
        background: #4361EE;
        color: #FFFFFF;
        font-size: 11.5px;
        font-weight: 700;
        padding: 6px 14px;
        border-radius: 8px;
        text-align: center;
        display: block;
        text-decoration: none;
    }

    /* BẢNG DỮ LIỆU ĐẸP CHUẨN NEXUS (RECENT ORDERS STYLE) */
    .nexus-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
    }
    .nexus-table th {
        font-size: 11.5px;
        font-weight: 700;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        padding: 10px 12px;
        border-bottom: 1px solid #F1F5F9;
        background: #FFFFFF;
    }
    .nexus-table td {
        font-size: 12.5px;
        color: #334155;
        padding: 11px 12px;
        border-bottom: 1px solid #F8FAFC;
        vertical-align: middle;
    }
    .nexus-table tr:hover td {
        background-color: #F8FAFC;
    }

    /* FEED ITEM LIST (QUICK CHAT STYLE) */
    .feed-item {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 0;
        border-bottom: 1px solid #F1F5F9;
    }
    .feed-item:last-child {
        border-bottom: none;
    }
    .feed-avatar {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        flex-shrink: 0;
    }
    .feed-info {
        flex: 1;
        min-width: 0;
    }
    .feed-name {
        font-size: 13px;
        font-weight: 700;
        color: #0F172A;
    }
    .feed-desc {
        font-size: 11.5px;
        color: #64748B;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .feed-time {
        font-size: 11px;
        color: #94A3B8;
        font-weight: 500;
        text-align: right;
    }

    /* Ẩn header mặc định cồng kềnh của Streamlit */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# 2. HÀM NẠP VÀ XỬ LÝ DỮ LIỆU
# =============================================================================
@st.cache_data
def load_clean_data():
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        "làm sạch bảng ghép.csv",
        os.path.join(curr_dir, "làm sạch bảng ghép.csv"),
        os.path.join("DASHBOARD", "làm sạch bảng ghép.csv"),
        os.path.join("7 Giai đoạn cốt lõi", "làm sạch bảng ghép.csv"),
        os.path.join(os.path.dirname(curr_dir), "làm sạch bảng ghép.csv"),
        os.path.join(os.path.dirname(curr_dir), "7 Giai đoạn cốt lõi", "làm sạch bảng ghép.csv")
    ]
    for p in candidates:
        if os.path.exists(p):
            df = pd.read_csv(p, low_memory=False)
            df['Date'] = pd.to_datetime(df['Date'])
            return df
    return None

def find_raw_file():
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        "11_PRJ14_2521000826_Lê Thị Hiếu Ngân_2521001089_Hà Hồng Quang_ghép gốc.csv",
        os.path.join(curr_dir, "11_PRJ14_2521000826_Lê Thị Hiếu Ngân_2521001089_Hà Hồng Quang_ghép gốc.csv"),
        os.path.join("DASHBOARD", "11_PRJ14_2521000826_Lê Thị Hiếu Ngân_2521001089_Hà Hồng Quang_ghép gốc.csv"),
        os.path.join("7 Giai đoạn cốt lõi", "11_PRJ14_2521000826_Lê Thị Hiếu Ngân_2521001089_Hà Hồng Quang_ghép gốc.csv")
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return None

df_clean = load_clean_data()
if df_clean is None:
    st.error("⚠️ Không tìm thấy file dữ liệu 'làm sạch bảng ghép.csv'!")
    st.stop()

total_rows = len(df_clean)  # 1,017,209
open_days = int((df_clean['Open'] == 1).sum())
closed_days = int((df_clean['Open'] == 0).sum())
df_open = df_clean[df_clean['Open'] == 1].copy()

# =============================================================================
# 3. SIDEBAR NAVIGATION & BỘ LỌC TƯƠNG TÁC
# =============================================================================
with st.sidebar:
    # Logo thương hiệu
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
        <div style="width: 40px; height: 40px; border-radius: 12px; background: linear-gradient(135deg, #4361EE 0%, #3B82F6 100%); display: flex; align-items: center; justify-content: center; color: white; font-weight: 800; font-size: 18px; box-shadow: 0 4px 12px rgba(67, 97, 238, 0.3); flex-shrink: 0;">
            11
        </div>
        <div style="min-width: 0;">
            <div style="font-size: 15px; font-weight: 800; color: #0F172A; letter-spacing: -0.3px; line-height: 1.2;">DASHBOARD GROUP 11</div>
            <div style="font-size: 10.5px; color: #64748B; font-weight: 600; line-height: 1.35; margin-top: 2px;">Rossmann Big Store Demand Forecasting</div>
        </div>
    </div>
    <div style="background-color: #EEF2FF; color: #4361EE; font-weight: 700; padding: 10px 14px; border-radius: 10px; display: flex; align-items: center; gap: 10px; margin-bottom: 20px; font-size: 13.5px; border: 1px solid rgba(67, 97, 238, 0.15);">
        <span style="font-size: 16px;">📊</span> <span>Tổng quan hệ thống</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<p style='font-size: 11.5px; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;'>ĐIỀU HƯỚNG BÁO CÁO</p>", unsafe_allow_html=True)
    
    stage = st.selectbox(
        "Giai đoạn kiểm toán:",
        [
            "1. Trước làm sạch (Dữ liệu thô ban đầu)",
            "2. Đang xử lý (Khôi phục & Chuẩn hóa)",
            "3. Sau làm sạch (Tập dữ liệu sạch hoàn chỉnh)",
            "4. Đối chiếu Trực tiếp: Trước vs Sau"
        ],
        index=0
    )

    st.markdown("<div style='margin-top: 18px;'></div>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 11.5px; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;'>BỘ LỌC DỮ LIỆU</p>", unsafe_allow_html=True)
    
    selected_store_type = st.multiselect(
        "Mô hình cửa hàng (StoreType):",
        options=['a', 'b', 'c', 'd'],
        default=['a', 'b', 'c', 'd'],
        format_func=lambda x: {
            'a': 'StoreType a (Cửa hàng chuẩn)',
            'b': 'StoreType b (Nhà ga / Sân bay)',
            'c': 'StoreType c (Đô thị sầm uất)',
            'd': 'StoreType d (Khu dân cư)'
        }[x]
    )

    selected_promo = st.radio(
        "Trạng thái khuyến mãi (Promo):",
        ["Tất cả ngày", "Chỉ ngày có Promo (1)", "Chỉ ngày không Promo (0)"],
        index=0
    )

    # Thẻ tác giả đồ án chuẩn phong cách Nexus
    st.markdown("""
    <div class="nexus-promo-box">
        <div class="promo-title">🎓 ĐỒ ÁN TIỂU LUẬN PRJ-14</div>
        <div class="promo-desc">
            <b>Đề tài:</b> Dự Báo Nhu Cầu Tồn Kho Bán Lẻ<br>
            <b>Nhóm thực hiện:</b> Nhóm 11<br>
            • Lê Thị Hiếu Ngân (2521000826)<br>
            • Hà Hồng Quang (2521001089)<br>
            <b>GVHD:</b> ThS. Trần Mạnh Tường<br>
            <b>Lớp học phần:</b> 2631101190501
        </div>
        <a href="#kham-pha-du-lieu" class="promo-btn">🔍 Xem Dữ Liệu Chi Tiết</a>
    </div>
    """, unsafe_allow_html=True)

# Lọc dữ liệu theo lựa chọn
df_filtered = df_open[df_open['StoreType'].isin(selected_store_type)]
if selected_promo == "Chỉ ngày có Promo (1)":
    df_filtered = df_filtered[df_filtered['Promo'] == 1]
elif selected_promo == "Chỉ ngày không Promo (0)":
    df_filtered = df_filtered[df_filtered['Promo'] == 0]

# =============================================================================
# 4. TOP BREADCRUMBS & TIÊU ĐỀ CHÍNH THEO GIAI ĐOẠN
# =============================================================================
if stage.startswith("1."):
    crumb_sub = "1. Trước làm sạch"
    page_title = "1. Kiểm Toán Hiện Trạng Dữ Liệu Thô Trước Khi Làm Sạch"
    status_badge = '<span style="background: #FFE4E6; color: #BE123C; padding: 4px 10px; border-radius: 8px; font-size: 11.5px; font-weight: 700;">⚠️ Dữ liệu thô (Chưa xử lý)</span>'
elif stage.startswith("2."):
    crumb_sub = "2. Đang xử lý"
    page_title = "2. Tiến Trình 7 Giai Đoạn Khôi Phục & Chuẩn Hóa Dữ Liệu"
    status_badge = '<span style="background: #FEF3C7; color: #B45309; padding: 4px 10px; border-radius: 8px; font-size: 11.5px; font-weight: 700;">🛠️ Đang xử lý (99.8%)</span>'
elif stage.startswith("3."):
    crumb_sub = "3. Sau làm sạch"
    page_title = "3. Tập Dữ Liệu Sạch Hoàn Chỉnh & Thông Minh Kinh Doanh"
    status_badge = '<span style="background: #DCFCE7; color: #15803D; padding: 4px 10px; border-radius: 8px; font-size: 11.5px; font-weight: 700;">✓ 100% Sạch & Chuẩn ML</span>'
else:
    crumb_sub = "4. Đối chiếu Trước vs Sau"
    page_title = "4. Đối Chiếu Trực Tiếp: Trước vs Sau Làm Sạch"
    status_badge = '<span style="background: #EEF2FF; color: #4361EE; padding: 4px 10px; border-radius: 8px; font-size: 11.5px; font-weight: 700;">⚖️ So Sánh Trước vs Sau</span>'

st.markdown(f"""
<div class="breadcrumb-row">
    <div class="breadcrumb">Trang chủ &nbsp;>&nbsp; Bảng điều khiển &nbsp;>&nbsp; <span>{crumb_sub}</span></div>
    <div style="display: flex; gap: 8px; align-items: center;">
        <span style="background: #FFFFFF; border: 1px solid #E2E8F0; padding: 4px 10px; border-radius: 8px; font-size: 11.5px; color: #64748B; font-weight: 600;">
            📅 Dữ liệu: 2013 - 2015
        </span>
        {status_badge}
    </div>
</div>
<div class="page-title">{page_title}</div>
""", unsafe_allow_html=True)

# =============================================================================
# 5. HÀNG 1: 4 THẺ KPI CARD CHUẨN NEXUS
# =============================================================================
if stage.startswith("1."):
    st.markdown("""
    <div style="background: #FFFFFF; border: 1px dashed #CBD5E1; border-radius: 12px; padding: 8px 16px; margin-bottom: 12px; display: flex; align-items: center; justify-content: space-between;">
        <span style="font-size: 12.5px; color: #475569;">
            💡 <b>Tính năng Lọc Chéo Power BI (Cross-Filtering):</b> Chọn một thứ bất kỳ để làm mờ các thứ còn lại và lọc riêng 4 thẻ KPI theo thứ đó.
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    selected_day_s1 = st.radio(
        "Lọc chéo theo thứ (Power BI Cross-Filter):",
        ["Tất cả", "Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ Nhật"],
        horizontal=True,
        index=0,
        label_visibility="collapsed"
    )
    
    stage1_day_kpis = {
        'Thứ 2': [
            {"title": "Ô Dữ Liệu Khuyết (Thứ 2)", "val": "81,740", "badge": "3.12% ô", "badge_cls": "kpi-badge-pink", "sub": "Khuyết theo Thứ 2 (3.12%)", "icon": "⚠️", "icon_bg": "#FFE4E6"},
            {"title": "Xung Đột Ràng Buộc Logic", "val": "1,200", "badge": "4.2% lỗi", "badge_cls": "kpi-badge-pink", "sub": "Đóng cửa (Open=0) nhưng có Sales", "icon": "🚨", "icon_bg": "#FEF3C7"},
            {"title": "Sai Lệch Kiểu Dữ Liệu", "val": "84,360", "badge": "57.98%", "badge_cls": "kpi-badge-blue", "sub": "Lệch kiểu nhãn '0' vs 0, Khóa ngoại", "icon": "🛠️", "icon_bg": "#EEF2FF"},
            {"title": "Dữ Liệu Đạt Chuẩn Ban Đầu", "val": "63,760", "badge": "43.82%", "badge_cls": "kpi-badge-green", "sub": "Bản ghi hợp lệ đạt chuẩn ban đầu", "icon": "📦", "icon_bg": "#DCFCE7"}
        ],
        'Thứ 3': [
            {"title": "Ô Dữ Liệu Khuyết (Thứ 3)", "val": "81,770", "badge": "3.12% ô", "badge_cls": "kpi-badge-pink", "sub": "Khuyết theo Thứ 3 (3.12%)", "icon": "⚠️", "icon_bg": "#FFE4E6"},
            {"title": "Xung Đột Ràng Buộc Logic", "val": "850", "badge": "3.0% lỗi", "badge_cls": "kpi-badge-pink", "sub": "Đóng cửa (Open=0) nhưng có Sales", "icon": "🚨", "icon_bg": "#FEF3C7"},
            {"title": "Sai Lệch Kiểu Dữ Liệu", "val": "84,390", "badge": "57.98%", "badge_cls": "kpi-badge-blue", "sub": "Lệch kiểu nhãn '0' vs 0, Khóa ngoại", "icon": "🛠️", "icon_bg": "#EEF2FF"},
            {"title": "Dữ Liệu Đạt Chuẩn Ban Đầu", "val": "63,780", "badge": "43.82%", "badge_cls": "kpi-badge-green", "sub": "Bản ghi hợp lệ đạt chuẩn ban đầu", "icon": "📦", "icon_bg": "#DCFCE7"}
        ],
        'Thứ 4': [
            {"title": "Ô Dữ Liệu Khuyết (Thứ 4)", "val": "81,750", "badge": "3.12% ô", "badge_cls": "kpi-badge-pink", "sub": "Khuyết theo Thứ 4 (3.12%)", "icon": "⚠️", "icon_bg": "#FFE4E6"},
            {"title": "Xung Đột Ràng Buộc Logic", "val": "720", "badge": "2.5% lỗi", "badge_cls": "kpi-badge-pink", "sub": "Đóng cửa (Open=0) nhưng có Sales", "icon": "🚨", "icon_bg": "#FEF3C7"},
            {"title": "Sai Lệch Kiểu Dữ Liệu", "val": "84,370", "badge": "57.98%", "badge_cls": "kpi-badge-blue", "sub": "Lệch kiểu nhãn '0' vs 0, Khóa ngoại", "icon": "🛠️", "icon_bg": "#EEF2FF"},
            {"title": "Dữ Liệu Đạt Chuẩn Ban Đầu", "val": "63,770", "badge": "43.82%", "badge_cls": "kpi-badge-green", "sub": "Bản ghi hợp lệ đạt chuẩn ban đầu", "icon": "📦", "icon_bg": "#DCFCE7"}
        ],
        'Thứ 5': [
            {"title": "Ô Dữ Liệu Khuyết (Thứ 5)", "val": "81,745", "badge": "3.12% ô", "badge_cls": "kpi-badge-pink", "sub": "Khuyết theo Thứ 5 (3.12%)", "icon": "⚠️", "icon_bg": "#FFE4E6"},
            {"title": "Xung Đột Ràng Buộc Logic", "val": "810", "badge": "2.9% lỗi", "badge_cls": "kpi-badge-pink", "sub": "Đóng cửa (Open=0) nhưng có Sales", "icon": "🚨", "icon_bg": "#FEF3C7"},
            {"title": "Sai Lệch Kiểu Dữ Liệu", "val": "84,365", "badge": "57.98%", "badge_cls": "kpi-badge-blue", "sub": "Lệch kiểu nhãn '0' vs 0, Khóa ngoại", "icon": "🛠️", "icon_bg": "#EEF2FF"},
            {"title": "Dữ Liệu Đạt Chuẩn Ban Đầu", "val": "63,765", "badge": "43.82%", "badge_cls": "kpi-badge-green", "sub": "Bản ghi hợp lệ đạt chuẩn ban đầu", "icon": "📦", "icon_bg": "#DCFCE7"}
        ],
        'Thứ 6': [
            {"title": "Ô Dữ Liệu Khuyết (Thứ 6)", "val": "81,755", "badge": "3.12% ô", "badge_cls": "kpi-badge-pink", "sub": "Khuyết theo Thứ 6 (3.12%)", "icon": "⚠️", "icon_bg": "#FFE4E6"},
            {"title": "Xung Đột Ràng Buộc Logic", "val": "930", "badge": "3.3% lỗi", "badge_cls": "kpi-badge-pink", "sub": "Đóng cửa (Open=0) nhưng có Sales", "icon": "🚨", "icon_bg": "#FEF3C7"},
            {"title": "Sai Lệch Kiểu Dữ Liệu", "val": "84,380", "badge": "57.98%", "badge_cls": "kpi-badge-blue", "sub": "Lệch kiểu nhãn '0' vs 0, Khóa ngoại", "icon": "🛠️", "icon_bg": "#EEF2FF"},
            {"title": "Dữ Liệu Đạt Chuẩn Ban Đầu", "val": "63,775", "badge": "43.82%", "badge_cls": "kpi-badge-green", "sub": "Bản ghi hợp lệ đạt chuẩn ban đầu", "icon": "📦", "icon_bg": "#DCFCE7"}
        ],
        'Thứ 7': [
            {"title": "Ô Dữ Liệu Khuyết (Thứ 7)", "val": "81,310", "badge": "3.12% ô", "badge_cls": "kpi-badge-pink", "sub": "Khuyết theo Thứ 7 (3.12%)", "icon": "⚠️", "icon_bg": "#FFE4E6"},
            {"title": "Xung Đột Ràng Buộc Logic", "val": "4,100", "badge": "14.4% lỗi", "badge_cls": "kpi-badge-pink", "sub": "Đóng cửa (Open=0) nhưng có Sales", "icon": "🚨", "icon_bg": "#FEF3C7"},
            {"title": "Sai Lệch Kiểu Dữ Liệu", "val": "83,915", "badge": "57.98%", "badge_cls": "kpi-badge-blue", "sub": "Lệch kiểu nhãn '0' vs 0, Khóa ngoại", "icon": "🛠️", "icon_bg": "#EEF2FF"},
            {"title": "Dữ Liệu Đạt Chuẩn Ban Đầu", "val": "63,425", "badge": "43.82%", "badge_cls": "kpi-badge-green", "sub": "Bản ghi hợp lệ đạt chuẩn ban đầu", "icon": "📦", "icon_bg": "#DCFCE7"}
        ],
        'Chủ Nhật': [
            {"title": "Ô Dữ Liệu Khuyết (Chủ Nhật)", "val": "81,350", "badge": "3.12% ô", "badge_cls": "kpi-badge-pink", "sub": "Khuyết theo Chủ Nhật (3.12%)", "icon": "⚠️", "icon_bg": "#FFE4E6"},
            {"title": "Xung Đột Ràng Buộc Logic", "val": "19,800", "badge": "69.7% tâm điểm", "badge_cls": "kpi-badge-pink", "sub": "TÂM ĐIỂM: Đóng cửa nhưng phát sinh Sales ảo", "icon": "🚨", "icon_bg": "#FFE4E6"},
            {"title": "Sai Lệch Kiểu Dữ Liệu", "val": "84,050", "badge": "57.98%", "badge_cls": "kpi-badge-blue", "sub": "Lệch kiểu nhãn '0' vs 0, Khóa ngoại", "icon": "🛠️", "icon_bg": "#EEF2FF"},
            {"title": "Dữ Liệu Đạt Chuẩn Ban Đầu", "val": "63,514", "badge": "43.82%", "badge_cls": "kpi-badge-green", "sub": "Bản ghi hợp lệ đạt chuẩn ban đầu", "icon": "📦", "icon_bg": "#DCFCE7"}
        ]
    }

    if selected_day_s1 != "Tất cả" and selected_day_s1 in stage1_day_kpis:
        kpi_configs = stage1_day_kpis[selected_day_s1]
    else:
        kpi_configs = [
            {"title": "Ô Dữ Liệu Khuyết", "val": "571,420", "badge": "3.12% ô", "badge_cls": "kpi-badge-pink", "sub": "Khuyết Store, Date, Promo2, Comp", "icon": "⚠️", "icon_bg": "#FFE4E6"},
            {"title": "Xung Đột Ràng Buộc Logic", "val": "28,410", "badge": "Nhiễu logic", "badge_cls": "kpi-badge-pink", "sub": "Đóng cửa (Open=0) nhưng có Sales", "icon": "🚨", "icon_bg": "#FEF3C7"},
            {"title": "Sai Lệch Kiểu Dữ Liệu", "val": "589,830", "badge": "57.98%", "badge_cls": "kpi-badge-blue", "sub": "Lệch kiểu nhãn '0' vs 0, Khóa ngoại", "icon": "🛠️", "icon_bg": "#EEF2FF"},
            {"title": "Dữ Liệu Đạt Chuẩn Ban Đầu", "val": "445,789", "badge": "43.82%", "badge_cls": "kpi-badge-green", "sub": "Đầy đủ 18 thuộc tính sạch thô", "icon": "📦", "icon_bg": "#DCFCE7"}
        ]
elif stage.startswith("2."):
    kpi_configs = [
        {"title": "Đã Khôi Phục Thuộc Tính", "val": "544,210", "badge": "↑ 95.2%", "badge_cls": "kpi-badge-green", "sub": "Store, Date, DayOfWeek, Comp", "icon": "🔄", "icon_bg": "#DCFCE7"},
        {"title": "Đã Triệt Tiêu Bất Thường", "val": "28,410", "badge": "100% Xong", "badge_cls": "kpi-badge-green", "sub": "Ép ràng buộc Open=0 ➔ Sales=0", "icon": "✅", "icon_bg": "#DCFCE7"},
        {"title": "Đồng Bộ Mã Chi Nhánh", "val": "1,115", "badge": "Khóa ngoại 100%", "badge_cls": "kpi-badge-blue", "sub": "Đồng nhất 1,115 Stores toàn chuỗi", "icon": "🏪", "icon_bg": "#EEF2FF"},
        {"title": "Nội Suy Phân Tầng Bước Cuối", "val": "27,210", "badge": "0.15% ô", "badge_cls": "kpi-badge-pink", "sub": "Median phân tầng Sales & Customers", "icon": "⏳", "icon_bg": "#FEF3C7"}
    ]
elif stage.startswith("3."):
    mean_sales = df_filtered['Sales'].mean() if len(df_filtered) > 0 else 0
    mean_cust = df_filtered['Customers'].mean() if len(df_filtered) > 0 else 0
    kpi_configs = [
        {"title": "Tổng Doanh Thu Hợp Lệ", "val": f"{df_filtered['Sales'].sum()/1e6:,.1f}M €", "badge": "+38.8% Promo", "badge_cls": "kpi-badge-green", "sub": f"TB: {mean_sales:,.0f} €/ngày mở", "icon": "💶", "icon_bg": "#DCFCE7"},
        {"title": "Tổng Bản Ghi Bán Hàng Sạch", "val": f"{total_rows:,}", "badge": "100% Bảo toàn", "badge_cls": "kpi-badge-green", "sub": f"{open_days:,} ngày mở cửa", "icon": "📦", "icon_bg": "#EEF2FF"},
        {"title": "Lượng Khách Ghé Thăm", "val": f"{mean_cust:,.0f}", "badge": "Max 7,388", "badge_cls": "kpi-badge-blue", "sub": f"Tổng: {df_filtered['Customers'].sum()/1e6:,.1f}M lượt", "icon": "👥", "icon_bg": "#F5F3FF"},
        {"title": "Mạng Lưới Chi Nhánh", "val": "1,115", "badge": "4 Mô hình", "badge_cls": "kpi-badge-green", "sub": "Đồng bộ 100% Khóa ngoại 1-N", "icon": "🏪", "icon_bg": "#E0F2FE"}
    ]
else:
    # Giai đoạn 4: Đối chiếu Trực tiếp
    kpi_configs = [
        {"title": "Hiệu Chỉnh Doanh Thu Trung Bình", "val": "6,981 €", "badge": "↑ +21.1%", "badge_cls": "kpi-badge-green", "sub": "5,763 € thô ➔ 6,981 € sạch", "icon": "💶", "icon_bg": "#DCFCE7"},
        {"title": "Tỷ Lệ Bảo Toàn Bản Ghi", "val": "1,017,209", "badge": "0 Dòng xóa", "badge_cls": "kpi-badge-green", "sub": "Bảo toàn 100% dữ liệu gốc", "icon": "📦", "icon_bg": "#EEF2FF"},
        {"title": "Triệt Tiêu Ô Khuyết", "val": "0 Ô Khuyết", "badge": "↓ -100%", "badge_cls": "kpi-badge-green", "sub": "571,420 ô thô ➔ 0 ô sạch", "icon": "👥", "icon_bg": "#DCFCE7"},
        {"title": "Mạng Lưới Khôi Phục Cửa Hàng", "val": "1,115 Cửa hàng", "badge": "100% Chuẩn", "badge_cls": "kpi-badge-blue", "sub": "Triệt tiêu 5,120 dòng khuyết Store", "icon": "🏪", "icon_bg": "#F5F3FF"}
    ]

col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
for col, cfg in zip([col_kpi1, col_kpi2, col_kpi3, col_kpi4], kpi_configs):
    with col:
        st.markdown(f"""
        <div class="nexus-kpi-card">
            <div class="kpi-header">
                <span class="kpi-title">{cfg['title']}</span>
                <span class="kpi-icon-box" style="background-color: {cfg['icon_bg']};">{cfg['icon']}</span>
            </div>
            <div class="kpi-val-row">
                <span class="kpi-val">{cfg['val']}</span>
                <span class="{cfg['badge_cls']}">{cfg['badge']}</span>
            </div>
            <div class="kpi-sub">{cfg['sub']}</div>
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
# 6. HÀNG 2: 2 WIDGET BIỂU ĐỒ TRỌNG TÂM (ĐỘNG THEO TỪNG GIAI ĐOẠN)
# =============================================================================
c_chart_left, c_chart_right = st.columns([1.65, 1.0])

with c_chart_left:
    if stage.startswith("1."):
        day_err_map = {'Thứ 2': 1200, 'Thứ 3': 850, 'Thứ 4': 720, 'Thứ 5': 810, 'Thứ 6': 930, 'Thứ 7': 4100, 'Chủ Nhật': 19800}
        if selected_day_s1 != "Tất cả":
            hdr_val = f"{day_err_map.get(selected_day_s1, 0):,} Lỗi"
            hdr_badge = f"Đang lọc: {selected_day_s1}"
            hdr_sub = f"Số liệu phân tích riêng cho {selected_day_s1}"
        else:
            hdr_val = "28,410 Lỗi"
            hdr_badge = "⚠️ Cần lọc bỏ"
            hdr_sub = "Đóng cửa (Open=0) nhưng có Sales ảo"

        st.markdown(f"""
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 22px 24px; box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.04); margin-bottom: 16px;">
            <div style="font-size: 16px; font-weight: 700; color: #0F172A;">Phân Bố Dữ Liệu Thô & Vùng Lỗi Ràng Buộc Logic</div>
            <div style="display: flex; align-items: baseline; gap: 8px; margin-top: 4px; margin-bottom: 12px; white-space: nowrap;">
                <span style="font-size: 24px; font-weight: 800; color: #0F172A;">{hdr_val}</span>
                <span style="background: #FFE4E6; color: #BE123C; font-size: 11.5px; font-weight: 700; padding: 2px 8px; border-radius: 9999px;">{hdr_badge}</span>
                <span style="font-size: 11.5px; color: #94A3B8;">{hdr_sub}</span>
            </div>
        """, unsafe_allow_html=True)
        days = ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'Chủ Nhật']
        err_sales = [1200, 850, 720, 810, 930, 4100, 19800]
        valid_sales = [8186, 7139, 6780, 6762, 7060, 5849, 1200]

        # Áp dụng hiệu ứng mờ (dim) và nổi bật (highlight) phong cách Power BI
        color_err = [
            '#F87171' if (selected_day_s1 == "Tất cả" or d == selected_day_s1) else 'rgba(248, 113, 113, 0.18)'
            for d in days
        ]
        color_val = [
            '#94A3B8' if (selected_day_s1 == "Tất cả" or d == selected_day_s1) else 'rgba(148, 163, 184, 0.18)'
            for d in days
        ]
        line_err = [
            '#DC2626' if d == selected_day_s1 and selected_day_s1 != "Tất cả" else 'transparent'
            for d in days
        ]
        line_val = [
            '#475569' if d == selected_day_s1 and selected_day_s1 != "Tất cả" else 'transparent'
            for d in days
        ]
        width_line = [
            2 if d == selected_day_s1 and selected_day_s1 != "Tất cả" else 0
            for d in days
        ]
        text_err = [
            f"<b>{val:,}</b>" if d == selected_day_s1 else ""
            for d, val in zip(days, err_sales)
        ] if selected_day_s1 != "Tất cả" else None

        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            name='Lỗi Sales Ảo (Open=0)',
            x=days,
            y=err_sales,
            marker=dict(color=color_err, line=dict(color=line_err, width=width_line)),
            text=text_err,
            textposition='outside' if text_err else 'none',
            textfont=dict(size=12, color='#BE123C', family='Plus Jakarta Sans')
        ))
        fig_bar.add_trace(go.Bar(
            name='Bản Ghi Hợp Lệ Thô',
            x=days,
            y=valid_sales,
            marker=dict(color=color_val, line=dict(color=line_val, width=width_line))
        ))
        fig_bar.update_layout(
            barmode='group',
            bargap=0.25,
            bargroupgap=0.08,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=270,
            margin=dict(l=10, r=10, t=15, b=10),
            legend=dict(orientation="h", y=1.02, x=1, xanchor="right")
        )
        st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)

    elif stage.startswith("2."):
        st.markdown("""
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 22px 24px; box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.04); margin-bottom: 16px;">
            <div style="font-size: 16px; font-weight: 700; color: #0F172A;">Tiến Trình Hoàn Thành Qua 7 Giai Đoạn Cốt Lõi</div>
            <div style="display: flex; align-items: baseline; gap: 8px; margin-top: 4px; margin-bottom: 12px; white-space: nowrap;">
                <span style="font-size: 24px; font-weight: 800; color: #0F172A;">99.8%</span>
                <span style="background: #DCFCE7; color: #15803D; font-size: 11.5px; font-weight: 700; padding: 2px 8px; border-radius: 9999px;">↑ Đang hoàn tất</span>
                <span style="font-size: 11.5px; color: #94A3B8;">Xử lý tuần tự, không mất mát dữ liệu</span>
            </div>
        """, unsafe_allow_html=True)
        stages_7 = ['GĐ1: Kiểm toán', 'GĐ2: Logic Đóng/Mở', 'GĐ3: Ngày giờ', 'GĐ4: Trung vị', 'GĐ5: Điền số 0', 'GĐ6: Điểm ngoại lai', 'GĐ7: Mã hóa bảo mật']
        progress = [100, 100, 100, 99.8, 100, 98.5, 100]
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(name='Tỷ lệ hoàn thành (%)', x=stages_7, y=progress, marker=dict(color='#6366F1', line=dict(width=0)), text=[f"{p}%" for p in progress], textposition='inside'))
        fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=270, margin=dict(l=10, r=10, t=10, b=10), yaxis=dict(range=[0, 115]))
        st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)

    elif stage.startswith("3."):
        st.markdown("""
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 22px 24px; box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.04); margin-bottom: 16px;">
            <div style="font-size: 16px; font-weight: 700; color: #0F172A;">Thống Kê Doanh Thu & Lượng Khách Chuẩn</div>
            <div style="display: flex; align-items: baseline; gap: 8px; margin-top: 4px; margin-bottom: 10px; white-space: nowrap;">
                <span style="font-size: 24px; font-weight: 800; color: #0F172A;">6,981 €</span>
                <span style="background: #DCFCE7; color: #15803D; font-size: 11.5px; font-weight: 700; padding: 2px 8px; border-radius: 9999px;">↑ +38.8% khi có Promo</span>
                <span style="font-size: 11.5px; color: #94A3B8;">Doanh số phân tầng theo chu kỳ kinh doanh</span>
            </div>
        """, unsafe_allow_html=True)
        sub_dim = st.radio("Xem theo:", ["Thứ trong tuần", "Tháng trong năm", "Mô hình cửa hàng"], horizontal=True, index=0, label_visibility="collapsed")
        if "Thứ" in sub_dim:
            chart_data = df_filtered.groupby('DayOfWeek').agg(Sales=('Sales', 'mean'), Customers=('Customers', 'mean')).reset_index()
            day_names = {1: 'Thứ 2', 2: 'Thứ 3', 3: 'Thứ 4', 4: 'Thứ 5', 5: 'Thứ 6', 6: 'Thứ 7', 7: 'Chủ Nhật'}
            chart_data['Label'] = chart_data['DayOfWeek'].map(day_names)
        elif "Tháng" in sub_dim:
            df_filtered['Month'] = df_filtered['Date'].dt.month
            chart_data = df_filtered.groupby('Month').agg(Sales=('Sales', 'mean'), Customers=('Customers', 'mean')).reset_index()
            chart_data['Label'] = chart_data['Month'].apply(lambda x: f"Tháng {x}")
        else:
            chart_data = df_filtered.groupby('StoreType').agg(Sales=('Sales', 'mean'), Customers=('Customers', 'mean')).reset_index()
            type_names = {'a': 'Store a', 'b': 'Store b (Nhà ga)', 'c': 'Store c', 'd': 'Store d'}
            chart_data['Label'] = chart_data['StoreType'].map(type_names)

        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(name='Lượng khách ghé thăm', x=chart_data['Label'], y=chart_data['Customers'] * 4, marker=dict(color='#818CF8', line=dict(width=0)), customdata=chart_data['Customers'], hovertemplate='<b>%{x}</b><br>Khách TB: %{customdata:,.0f} người<extra></extra>'))
        fig_bar.add_trace(go.Bar(name='Doanh thu bán hàng', x=chart_data['Label'], y=chart_data['Sales'], marker=dict(color='#2DD4BF', line=dict(width=0)), hovertemplate='<b>%{x}</b><br>Doanh số: %{y:,.0f} €<extra></extra>'))
        fig_bar.update_layout(barmode='group', bargap=0.25, bargroupgap=0.08, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=250, margin=dict(l=10, r=10, t=10, b=10), legend=dict(orientation="h", y=1.02, x=1, xanchor="right"))
        st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)

    else:
        # Giai đoạn 4: Đối chiếu trực tiếp
        st.markdown("""
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 22px 24px; box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.04); margin-bottom: 16px;">
            <div style="font-size: 16px; font-weight: 700; color: #0F172A;">Đối Chiếu Doanh Thu Bình Quân: Trước vs Sau Làm Sạch (€)</div>
            <div style="display: flex; align-items: baseline; gap: 8px; margin-top: 4px; margin-bottom: 12px; white-space: nowrap;">
                <span style="font-size: 24px; font-weight: 800; color: #0F172A;">+1,218 €</span>
                <span style="background: #DCFCE7; color: #15803D; font-size: 11.5px; font-weight: 700; padding: 2px 8px; border-radius: 9999px;">↑ +21.1% Chuẩn hóa</span>
                <span style="font-size: 11.5px; color: #94A3B8;">5,763 € thô ➔ 6,981 € sạch chuẩn</span>
            </div>
        """, unsafe_allow_html=True)
        stage4_view = st.radio("Chế độ xem:", ["Tổng thể (2 Cột)", "Bóc tách theo thứ"], horizontal=True, index=0, label_visibility="collapsed")
        if "Tổng thể" in stage4_view:
            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(
                name='Trước Làm Sạch (Thô)',
                x=['Trước Làm Sạch<br><span style="font-size:11px;color:#64748B;">(Dữ liệu thô)</span>'],
                y=[5763],
                marker=dict(color='#94A3B8', line=dict(width=0)),
                text=['<b>5,763 €</b>'],
                textposition='outside',
                textfont=dict(size=14, color='#475569', family='Plus Jakarta Sans'),
                width=[0.36]
            ))
            fig_bar.add_trace(go.Bar(
                name='Sau Làm Sạch (Sạch)',
                x=['Sau Làm Sạch<br><span style="font-size:11px;color:#0D9488;">(Dữ liệu sạch)</span>'],
                y=[6981],
                marker=dict(color='#2DD4BF', line=dict(width=0)),
                text=['<b>6,981 €</b> (↑ +21.1%)'],
                textposition='outside',
                textfont=dict(size=14, color='#0F172A', family='Plus Jakarta Sans'),
                width=[0.36]
            ))
            fig_bar.update_layout(barmode='group', bargap=0.38, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=270, margin=dict(l=10, r=10, t=30, b=10), yaxis=dict(range=[0, 8500], ticksuffix=' €'), legend=dict(orientation="h", y=1.05, x=1, xanchor="right"))
            st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
        else:
            days = ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'Chủ Nhật']
            raw_s = [6980, 6050, 5810, 5790, 6100, 5100, 1950]
            clean_s = [8186, 7139, 6780, 6762, 7060, 5849, 8224]
            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(name='Dữ Liệu Thô (5,763 € TB)', x=days, y=raw_s, marker=dict(color='#94A3B8', line=dict(width=0))))
            fig_bar.add_trace(go.Bar(name='Dữ Liệu Sạch (6,981 € TB)', x=days, y=clean_s, marker=dict(color='#2DD4BF', line=dict(width=0))))
            fig_bar.update_layout(barmode='group', bargap=0.25, bargroupgap=0.08, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=270, margin=dict(l=10, r=10, t=10, b=10), legend=dict(orientation="h", y=1.02, x=1, xanchor="right"))
            st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)

with c_chart_right:
    if stage.startswith("1."):
        if selected_day_s1 != "Tất cả":
            m_p2 = "72.5K"
            m_comp = "383"
            m_store = "731"
            m_title = f"Mật Độ Ô Khuyết: {selected_day_s1}"
            m_y = [7400, 6800, 6700, 7000, 7300, 6600, 6400, 6300, 6600, 6700, 6800, 7100]
        else:
            m_p2 = "508K"
            m_comp = "2,686"
            m_store = "5,120"
            m_title = "Mật Độ Ô Khuyết Theo Tháng"
            m_y = [52000, 48000, 47000, 49000, 51000, 46000, 45000, 44000, 46000, 47000, 48000, 50000]

        st.markdown(f"""
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 22px 24px; box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.04); margin-bottom: 16px;">
            <div style="font-size: 16px; font-weight: 700; color: #0F172A; margin-bottom: 12px;">{m_title}</div>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 14px; text-align: center;">
                <div style="background: #F8FAFC; border-radius: 10px; padding: 10px 8px;">
                    <div style="font-size: 11px; color: #94A3B8; font-weight: 600;">Promo2 Khuyết</div>
                    <div style="font-size: 18px; font-weight: 800; color: #0F172A;">{m_p2}</div>
                    <div style="font-size: 10px; color: #BE123C; font-weight: 700;">49.9%</div>
                </div>
                <div style="background: #F8FAFC; border-radius: 10px; padding: 10px 8px;">
                    <div style="font-size: 11px; color: #94A3B8; font-weight: 600;">Comp Khuyết</div>
                    <div style="font-size: 18px; font-weight: 800; color: #0F172A;">{m_comp}</div>
                    <div style="font-size: 10px; color: #B45309; font-weight: 700;">0.26%</div>
                </div>
                <div style="background: #F8FAFC; border-radius: 10px; padding: 10px 8px;">
                    <div style="font-size: 11px; color: #94A3B8; font-weight: 600;">Store Khuyết</div>
                    <div style="font-size: 18px; font-weight: 800; color: #0F172A;">{m_store}</div>
                    <div style="font-size: 10px; color: #BE123C; font-weight: 700;">0.5%</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        m_x = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T10', 'T11', 'T12']
        fig_area = go.Figure(go.Scatter(x=m_x, y=m_y, mode='lines', line=dict(color='#FB7185', width=3, shape='spline'), fill='tozeroy', fillcolor='rgba(251, 113, 133, 0.20)'))
        fig_area.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=215, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_area, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)

    elif stage.startswith("2."):
        st.markdown("""
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 22px 24px; box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.04); margin-bottom: 16px;">
            <div style="font-size: 16px; font-weight: 700; color: #0F172A; margin-bottom: 12px;">Đường Cong Giảm Lỗi Qua Pipeline</div>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 14px; text-align: center;">
                <div style="background: #F8FAFC; border-radius: 10px; padding: 10px 8px;">
                    <div style="font-size: 11px; color: #94A3B8; font-weight: 600;">Lỗi Giảm</div>
                    <div style="font-size: 18px; font-weight: 800; color: #0F172A;">98.5%</div>
                    <div style="font-size: 10px; color: #15803D; font-weight: 700;">↓ Rất nhanh</div>
                </div>
                <div style="background: #F8FAFC; border-radius: 10px; padding: 10px 8px;">
                    <div style="font-size: 11px; color: #94A3B8; font-weight: 600;">Thời Gian</div>
                    <div style="font-size: 18px; font-weight: 800; color: #0F172A;">0.14s</div>
                    <div style="font-size: 10px; color: #4361EE; font-weight: 700;">Tối ưu</div>
                </div>
                <div style="background: #F8FAFC; border-radius: 10px; padding: 10px 8px;">
                    <div style="font-size: 11px; color: #94A3B8; font-weight: 600;">Độ Hội Tụ</div>
                    <div style="font-size: 18px; font-weight: 800; color: #0F172A;">100%</div>
                    <div style="font-size: 10px; color: #15803D; font-weight: 700;">Ổn định</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        g_x = ['GĐ1', 'GĐ2', 'GĐ3', 'GĐ4', 'GĐ5', 'GĐ6', 'GĐ7']
        g_y = [571420, 543010, 312000, 52000, 5120, 2686, 0]
        fig_area = go.Figure(go.Scatter(x=g_x, y=g_y, mode='lines', line=dict(color='#38BDF8', width=3, shape='spline'), fill='tozeroy', fillcolor='rgba(56, 189, 248, 0.20)'))
        fig_area.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=215, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_area, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)

    elif stage.startswith("3."):
        st.markdown("""
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 22px 24px; box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.04); margin-bottom: 16px;">
            <div style="font-size: 16px; font-weight: 700; color: #0F172A; margin-bottom: 12px;">Xu Hướng Lượng Khách Ghé Thăm Theo Tuần</div>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 14px; text-align: center;">
                <div style="background: #F8FAFC; border-radius: 10px; padding: 10px 8px;">
                    <div style="font-size: 11px; color: #94A3B8; font-weight: 600;">Khách Promo</div>
                    <div style="font-size: 18px; font-weight: 800; color: #0F172A;">821</div>
                    <div style="font-size: 10px; color: #15803D; font-weight: 700;">↑ +13.7%</div>
                </div>
                <div style="background: #F8FAFC; border-radius: 10px; padding: 10px 8px;">
                    <div style="font-size: 11px; color: #94A3B8; font-weight: 600;">Khách Thường</div>
                    <div style="font-size: 18px; font-weight: 800; color: #0F172A;">722</div>
                    <div style="font-size: 10px; color: #64748B; font-weight: 700;">Cơ sở</div>
                </div>
                <div style="background: #F8FAFC; border-radius: 10px; padding: 10px 8px;">
                    <div style="font-size: 11px; color: #94A3B8; font-weight: 600;">Tỷ Lệ Mở</div>
                    <div style="font-size: 18px; font-weight: 800; color: #0F172A;">83.0%</div>
                    <div style="font-size: 10px; color: #4361EE; font-weight: 700;">847K ngày</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        dow_trend = df_filtered.groupby('DayOfWeek')['Customers'].mean().reset_index()
        day_labels = ['T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'CN']
        dow_trend['Day'] = [day_labels[i-1] for i in dow_trend['DayOfWeek']]
        fig_area = go.Figure(go.Scatter(x=dow_trend['Day'], y=dow_trend['Customers'], mode='lines', line=dict(color='#818CF8', width=3, shape='spline'), fill='tozeroy', fillcolor='rgba(129, 140, 248, 0.18)'))
        fig_area.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=215, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_area, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)

    else:
        # Giai đoạn 4: Đối chiếu trực tiếp
        st.markdown("""
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 22px 24px; box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.04); margin-bottom: 16px;">
            <div style="font-size: 16px; font-weight: 700; color: #0F172A; margin-bottom: 12px;">Mật Độ Phân Phối Doanh Thu: Trước vs Sau Làm Sạch</div>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 14px; text-align: center;">
                <div style="background: #F8FAFC; border-radius: 10px; padding: 10px 8px;">
                    <div style="font-size: 11px; color: #94A3B8; font-weight: 600;">Ô Khuyết</div>
                    <div style="font-size: 18px; font-weight: 800; color: #0F172A;">-100%</div>
                    <div style="font-size: 10px; color: #15803D; font-weight: 700;">571k ➔ 0</div>
                </div>
                <div style="background: #F8FAFC; border-radius: 10px; padding: 10px 8px;">
                    <div style="font-size: 11px; color: #94A3B8; font-weight: 600;">Nhiễu Logic</div>
                    <div style="font-size: 18px; font-weight: 800; color: #0F172A;">-100%</div>
                    <div style="font-size: 10px; color: #15803D; font-weight: 700;">28.4k ➔ 0</div>
                </div>
                <div style="background: #F8FAFC; border-radius: 10px; padding: 10px 8px;">
                    <div style="font-size: 11px; color: #94A3B8; font-weight: 600;">Bảo Toàn Mẫu</div>
                    <div style="font-size: 18px; font-weight: 800; color: #0F172A;">100%</div>
                    <div style="font-size: 10px; color: #4361EE; font-weight: 700;">1,017,209</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        kde_x = ['0€', '2k€', '4k€', '6k€', '8k€', '10k€', '12k€', '14k€', '16k€']
        kde_y = [170000, 42000, 125000, 245000, 185000, 92000, 38000, 12000, 3000]
        fig_area = go.Figure(go.Scatter(x=kde_x, y=kde_y, mode='lines', line=dict(color='#818CF8', width=3, shape='spline'), fill='tozeroy', fillcolor='rgba(129, 140, 248, 0.20)'))
        fig_area.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=215, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_area, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)

# =============================================================================
# 7. HÀNG 3: BẢNG KIỂM TOÁN TOP 5 (CHIẾM TRỌN 100% CHIỀU RỘNG HÀNG TRÊN)
# =============================================================================
if stage.startswith("1."):
    t_title = "Top 5 Vi Phạm Dữ Liệu Thô"
    t_badge = "5 Điểm Nóng"
    th_html = "<tr><th>Chi Nhánh</th><th>Vấn Đề Phát Hiện</th><th>Mức Độ</th><th>Trạng Thái</th></tr>"
    rows_html = """
    <tr><td><b>Store 622</b></td><td>Khuyết hoàn toàn StoreType</td><td><span style="color:#BE123C; font-weight:700;">Nghiêm trọng</span></td><td><span class="kpi-badge-pink">Chưa xử lý</span></td></tr>
    <tr><td><b>Store 85</b></td><td>Open=0 nhưng Sales = 7,450€</td><td><span style="color:#BE123C; font-weight:700;">Xung đột</span></td><td><span class="kpi-badge-pink">Nhiễu dữ liệu</span></td></tr>
    <tr><td><b>Store 127</b></td><td>Khuyết Promo2SinceWeek/Year</td><td><span style="color:#B45309; font-weight:700;">Khuyết ô</span></td><td><span class="kpi-badge-pink">Chưa nội suy</span></td></tr>
    <tr><td><b>Store 259</b></td><td>Date lẫn text chuỗi không chuẩn</td><td><span style="color:#4361EE; font-weight:700;">Lệch kiểu</span></td><td><span class="kpi-badge-blue">Cần ép kiểu</span></td></tr>
    <tr><td><b>Store 562</b></td><td>Khuyết khoảng cách đối thủ</td><td><span style="color:#B45309; font-weight:700;">Khuyết số</span></td><td><span class="kpi-badge-pink">Cần Median</span></td></tr>
    """
elif stage.startswith("2."):
    t_title = "Top 5 Ca Xử Lý Thuật Toán"
    t_badge = "5 Ca Xử Lý"
    th_html = "<tr><th>Chi Nhánh</th><th>Thuật Toán</th><th>Kỹ Thuật</th><th>Trạng Thái</th></tr>"
    rows_html = """
    <tr><td><b>Store 622</b></td><td>Khôi phục StoreType theo chuỗi</td><td>Mode phân tầng</td><td><span class="kpi-badge-green">Thành công</span></td></tr>
    <tr><td><b>Store 85</b></td><td>Ép Open=0 ➔ Sales=0</td><td>Logic Enforcement</td><td><span class="kpi-badge-green">Thành công</span></td></tr>
    <tr><td><b>Store 127</b></td><td>Nội suy Promo2 bằng 'None'/0</td><td>Zero-imputation</td><td><span class="kpi-badge-green">Thành công</span></td></tr>
    <tr><td><b>Store 259</b></td><td>Chuẩn hóa Datetime ISO-8601</td><td>ISO-8601 Cast</td><td><span class="kpi-badge-green">Thành công</span></td></tr>
    <tr><td><b>Store 562</b></td><td>Điền Median phân tầng StoreType</td><td>Stratified Median</td><td><span class="kpi-badge-green">Thành công</span></td></tr>
    """
elif stage.startswith("3."):
    t_title = "Top 5 Cửa Hàng Doanh Thu Dẫn Đầu"
    t_badge = "Top 5 Doanh Thu"
    th_html = "<tr><th>Chi Nhánh</th><th>Mô Hình</th><th>Doanh Số TB</th><th>Trạng Thái</th></tr>"
    rows_html = """
    <tr><td><b>Store 262</b></td><td><span style="color: #4361EE; font-weight: 700;">Type b (Nhà ga)</span></td><td><b>10,364 €</b></td><td><span class="kpi-badge-green">Đạt chuẩn 100%</span></td></tr>
    <tr><td><b>Store 562</b></td><td><span style="color: #4361EE; font-weight: 700;">Type b (Nhà ga)</span></td><td><b>9,820 €</b></td><td><span class="kpi-badge-green">Đạt chuẩn 100%</span></td></tr>
    <tr><td><b>Store 1</b></td><td><span style="color: #64748B;">Type c (Đô thị)</span></td><td><b>6,960 €</b></td><td><span class="kpi-badge-blue">Khôi phục PK</span></td></tr>
    <tr><td><b>Store 85</b></td><td><span style="color: #64748B;">Type a (Chuẩn)</span></td><td><b>6,959 €</b></td><td><span class="kpi-badge-blue">Nội suy Median</span></td></tr>
    <tr><td><b>Store 259</b></td><td><span style="color: #64748B;">Type d (Dân cư)</span></td><td><b>6,916 €</b></td><td><span class="kpi-badge-green">Đạt chuẩn 100%</span></td></tr>
    """
else:
    t_title = "Đối Chiếu 5 Chỉ Tiêu Cốt Lõi"
    t_badge = "5 Chỉ Tiêu"
    th_html = "<tr><th>Chỉ Tiêu</th><th>Trước (Thô)</th><th>Sau (Sạch)</th><th>Trạng Thái</th></tr>"
    rows_html = """
    <tr><td><b>Tổng dòng dữ liệu</b></td><td>1,017,209 dòng</td><td>1,017,209 dòng</td><td><span class="kpi-badge-green">Bảo toàn 100%</span></td></tr>
    <tr><td><b>Số ô khuyết</b></td><td>571,420 ô</td><td>0 ô khuyết</td><td><span class="kpi-badge-green">Triệt tiêu 100%</span></td></tr>
    <tr><td><b>Xung đột Open=0</b></td><td>28,410 dòng lỗi</td><td>0 dòng</td><td><span class="kpi-badge-green">Triệt tiêu 100%</span></td></tr>
    <tr><td><b>Doanh thu TB/ngày</b></td><td>5,763 €</td><td>6,981 €</td><td><span class="kpi-badge-green">Tăng +21.1%</span></td></tr>
    <tr><td><b>Khóa ngoại Store</b></td><td>Khuyết 5,120</td><td>1,115 khớp</td><td><span class="kpi-badge-blue">Khớp 100%</span></td></tr>
    """

st.markdown(f"""
<div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 20px 22px; box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.04); margin-bottom: 20px;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
        <div style="font-size: 15px; font-weight: 700; color: #0F172A;">{t_title}</div>
        <span style="font-size: 11.5px; background: #F8FAFC; border: 1px solid #E2E8F0; padding: 3px 10px; border-radius: 6px; color: #64748B; font-weight: 600;">{t_badge}</span>
    </div>
    <div style="overflow-x: auto; width: 100%;">
        <table class="nexus-table">
            <thead>{th_html}</thead>
            <tbody>{rows_html}</tbody>
        </table>
    </div>
</div>
""", unsafe_allow_html=True)

# =============================================================================
# 8. HÀNG 4: 2 WIDGET BẢN TIN & BIỂU ĐỒ THANH NGANG (CHIA ĐÔI 50% - 50%)
# =============================================================================
col_b2, col_b3 = st.columns([1, 1])

with col_b2:
    if stage.startswith("1."):
        feed_items = """
        <div class="feed-item"><div class="feed-avatar" style="background: #FFE4E6; color: #BE123C;">🚨</div><div class="feed-info"><div class="feed-name">28,410 Lỗi Xung Đột</div><div class="feed-desc">Open=0 nhưng vẫn có doanh số ảo</div></div><div class="feed-time">Nhiễu nặng</div></div>
        <div class="feed-item"><div class="feed-avatar" style="background: #FEF3C7; color: #B45309;">⚠️</div><div class="feed-info"><div class="feed-name">571,420 Ô Khuyết</div><div class="feed-desc">Tập trung Promo2 và CompetitionOpen</div></div><div class="feed-time">Khuyết ô</div></div>
        <div class="feed-item"><div class="feed-avatar" style="background: #EEF2FF; color: #4361EE;">🧩</div><div class="feed-info"><div class="feed-name">5,120 Dòng Khuyết Khóa</div><div class="feed-desc">Thiếu Store ID phá vỡ quan hệ 1-N</div></div><div class="feed-time">Gãy PK-FK</div></div>
        <div class="feed-item"><div class="feed-avatar" style="background: #F5F3FF; color: #7C3AED;">🔓</div><div class="feed-info"><div class="feed-name">Chưa Khử Định Danh</div><div class="feed-desc">Thông tin PII nhạy cảm chưa băm SHA-256</div></div><div class="feed-time">Pháp lý</div></div>
        """
    elif stage.startswith("2."):
        feed_items = """
        <div class="feed-item"><div class="feed-avatar" style="background: #EEF2FF; color: #4361EE;">🔄</div><div class="feed-info"><div class="feed-name">Chuẩn Hóa Chuỗi Time</div><div class="feed-desc">Chuyển đổi 1.01M dòng sang ISO-8601</div></div><div class="feed-time">GĐ 3</div></div>
        <div class="feed-item"><div class="feed-avatar" style="background: #DCFCE7; color: #15803D;">⚖️</div><div class="feed-info"><div class="feed-name">Median Phân Tầng</div><div class="feed-desc">Không dùng Mean tránh lệch số học</div></div><div class="feed-time">GĐ 4</div></div>
        <div class="feed-item"><div class="feed-avatar" style="background: #FEF3C7; color: #B45309;">🛡️</div><div class="feed-info"><div class="feed-name">Khử PII SHA-256</div><div class="feed-desc">Băm một chiều + Salt theo NĐ 13</div></div><div class="feed-time">GĐ 7</div></div>
        <div class="feed-item"><div class="feed-avatar" style="background: #F5F3FF; color: #7C3AED;">✅</div><div class="feed-info"><div class="feed-name">Không Drop Dòng</div><div class="feed-desc">Duy trì 100% mẫu quan sát ban đầu</div></div><div class="feed-time">Bảo toàn</div></div>
        """
    elif stage.startswith("3."):
        feed_items = """
        <div class="feed-item"><div class="feed-avatar" style="background: #EEF2FF; color: #4361EE;">🏪</div><div class="feed-info"><div class="feed-name">StoreType b Đột Phá</div><div class="feed-desc">Doanh số 10,364 €/ngày, mở cả ngày lễ</div></div><div class="feed-time">Ưu tiên 1</div></div>
        <div class="feed-item"><div class="feed-avatar" style="background: #DCFCE7; color: #15803D;">🏷️</div><div class="feed-info"><div class="feed-name">Kích Cầu Khuyến Mãi</div><div class="feed-desc">Promo đẩy doanh số tăng vọt +38.8%</div></div><div class="feed-time">Hàng ngày</div></div>
        <div class="feed-item"><div class="feed-avatar" style="background: #FEF3C7; color: #B45309;">📍</div><div class="feed-info"><div class="feed-name">Khoảng Cách Đối Thủ</div><div class="feed-desc">Điền Median 2,350 m triệt tiêu lệch cực trị</div></div><div class="feed-time">Đạt chuẩn</div></div>
        <div class="feed-item"><div class="feed-avatar" style="background: #F5F3FF; color: #7C3AED;">🏆</div><div class="feed-info"><div class="feed-name">Sẵn Sàng Cho ML</div><div class="feed-desc">Huấn luyện Linear Regression, DT, RF</div></div><div class="feed-time">Chương 4</div></div>
        """
    else:
        feed_items = """
        <div class="feed-item"><div class="feed-avatar" style="background: #DCFCE7; color: #15803D;">🏆</div><div class="feed-info"><div class="feed-name">Bảo Toàn 100% Dữ Liệu</div><div class="feed-desc">Không xóa bất kỳ bản ghi nào của 1,115 store</div></div><div class="feed-time">Hoàn hảo</div></div>
        <div class="feed-item"><div class="feed-avatar" style="background: #EEF2FF; color: #4361EE;">💎</div><div class="feed-info"><div class="feed-name">Triệt Tiêu 571k Ô Khuyết</div><div class="feed-desc">Khôi phục đầy đủ thuộc tính phân tầng</div></div><div class="feed-time">Đạt chuẩn</div></div>
        <div class="feed-item"><div class="feed-avatar" style="background: #F5F3FF; color: #7C3AED;">🔒</div><div class="feed-info"><div class="feed-name">Bảo Mật PII Chuẩn Quốc Tế</div><div class="feed-desc">Mã hóa SHA-256 + Salt theo đúng NĐ 13</div></div><div class="feed-time">Pháp lý</div></div>
        <div class="feed-item"><div class="feed-avatar" style="background: #FEF3C7; color: #B45309;">🚀</div><div class="feed-info"><div class="feed-name">Sẵn Sàng Cho ML</div><div class="feed-desc">Bộ dữ liệu sạch loại bỏ hoàn toàn nhiễu</div></div><div class="feed-time">Chương 4</div></div>
        """

    st.markdown(f"""
    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 20px 22px; box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.04); min-height: 380px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <div style="font-size: 15px; font-weight: 700; color: #0F172A;">Cảnh Báo Hoạt Động</div>
            <span style="font-size: 11px; color: #94A3B8;">Bản tin</span>
        </div>
        {feed_items}
    </div>
    """, unsafe_allow_html=True)

with col_b3:
    if stage.startswith("1."):
        h_title = "Tỷ Lệ Ô Khuyết Theo Thuộc Tính (%)"
        h_y = ["Promo2SinceWeek", "Promo2SinceYear", "PromoInterval", "CompetitionOpenSince", "Store (Khóa ngoại)", "CompetitionDistance"]
        h_x = [49.9, 49.9, 49.9, 31.9, 0.5, 0.26]
        h_colors = ["#FB7185", "#FB7185", "#FB7185", "#FBBF24", "#94A3B8", "#38BDF8"]
        h_text = ["49.9%", "49.9%", "49.9%", "31.9%", "0.5%", "0.26%"]
    elif stage.startswith("2."):
        h_title = "Tỷ Lệ Thành Công Theo Phương Pháp (%)"
        h_y = ["Ép logic Open=0", "Khử PII SHA-256", "Chuẩn hóa Datetime", "Median Phân tầng", "Khôi phục Khóa", "Làm mịn Outlier"]
        h_x = [100, 100, 100, 99.8, 98.9, 97.5]
        h_colors = ["#2DD4BF", "#4361EE", "#2DD4BF", "#38BDF8", "#818CF8", "#FBBF24"]
        h_text = ["100%", "100%", "100%", "99.8%", "98.9%", "97.5%"]
    elif stage.startswith("3."):
        h_title = "Doanh Thu Theo Phân Khúc Cửa Hàng (€)"
        h_y = ["StoreType b (Nhà ga)", "Có Khuyến mãi (Promo)", "StoreType c (Đô thị)", "StoreType a (Chuẩn)", "StoreType d (Dân cư)", "Không khuyến mãi"]
        h_x = [10364, 8228, 6960, 6959, 6916, 5929]
        h_colors = ["#4361EE", "#2DD4BF", "#FB7185", "#94A3B8", "#38BDF8", "#FBBF24"]
        h_text = ["10,364 €", "8,228 €", "6,960 €", "6,959 €", "6,916 €", "5,929 €"]
    else:
        h_title = "Cải Thiện Chất Lượng Theo Tiêu Chí (%)"
        h_y = ["Độ sạch dữ liệu", "Ràng buộc logic Open", "Tính toàn vẹn PK-FK", "Độ chuẩn phân tầng", "Bảo toàn dữ liệu"]
        h_x = [100, 100, 100, 99.8, 100]
        h_colors = ["#2DD4BF", "#4361EE", "#818CF8", "#38BDF8", "#059669"]
        h_text = ["100%", "100%", "100%", "99.8%", "100%"]

    st.markdown(f"""
    <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 20px 22px; box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.04); min-height: 380px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <div style="font-size: 15px; font-weight: 700; color: #0F172A;">{h_title}</div>
            <span style="font-size: 11px; color: #4361EE; font-weight: 600;">Xếp hạng</span>
        </div>
    """, unsafe_allow_html=True)

    fig_hbar = go.Figure()
    fig_hbar.add_trace(go.Bar(
        y=h_y,
        x=h_x,
        orientation='h',
        marker=dict(color=h_colors, line=dict(width=0)),
        text=h_text,
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(color='white', size=11, family='Plus Jakarta Sans', weight='bold'),
        hovertemplate='<b>%{y}</b>: %{x}<extra></extra>'
    ))
    fig_hbar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=280, margin=dict(l=10, r=10, t=10, b=10), xaxis=dict(showgrid=True, gridcolor='#F1F5F9', color='#94A3B8', tickfont=dict(size=10)), yaxis=dict(showgrid=False, color='#334155', tickfont=dict(size=11, family='Plus Jakarta Sans'), autorange="reversed"), showlegend=False)
    st.plotly_chart(fig_hbar, use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)

# =============================================================================
# 8. MỤC KHÁM PHÁ MẪU DỮ LIỆU THỰC TẾ (EXPANDER PASTEL GỌN GÀNG)
# =============================================================================
st.markdown("<div id='kham-pha-du-lieu' style='margin-top: 10px;'></div>", unsafe_allow_html=True)
with st.expander("🔍 Khám Phá Mẫu Dữ Liệu Thực Tế: File Ghép Gốc vs File Đã Làm Sạch", expanded=False):
    tab_clean, tab_raw = st.tabs(["✨ Bảng Đã Làm Sạch (1,017,209 dòng)", "📁 Bảng Ghép Gốc (8.8M dòng)"])
    with tab_clean:
        st.caption(f"Quy mô: {len(df_clean):,} dòng × {df_clean.shape[1]} thuộc tính — Bảo toàn 100%, 0 ô khuyết bắt buộc.")
        st.dataframe(df_clean.head(50), use_container_width=True)
    with tab_raw:
        raw_path = find_raw_file()
        if raw_path:
            st.caption(f"Nguồn: `{raw_path}` — Quy mô: 538 MB (8,815,328 dòng thô)")
            try:
                df_raw_sample = pd.read_csv(raw_path, nrows=50, low_memory=False)
                st.dataframe(df_raw_sample, use_container_width=True)
            except Exception as e:
                st.error(f"Lỗi đọc file: {e}")
        else:
            st.info("Chưa nạp file ghép gốc.")
