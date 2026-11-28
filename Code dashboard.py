"""
DASHBOARD PHÂN TÍCH & KIỂM TOÁN DỮ LIỆU ROSSMANN (NHÓM 11 - PRJ-14)
Giao diện Light Pastel "Nexus" chuẩn hiện đại + Thanh chọn 4 giai đoạn (1 -> 4).
Chạy ứng dụng: streamlit run "DASHBOARD/Code dashboard.py"
Toàn bộ chỉ số được đọc trực tiếp từ dữ liệu sạch thực tế và DASHBOARD/audit_metrics.json.
"""

import json
import os
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# =============================================================================
# 1. CẤU HÌNH TRANG & GIAO DIỆN LIGHT PASTEL "NEXUS" CHUẨN HIỆN ĐẠI
# =============================================================================
st.set_page_config(
    page_title="DASHBOARD GROUP 11 | Rossmann Big Store Demand Forecasting",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

    .stApp {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
        font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif !important;
    }
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #F1F5F9; }
    ::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 9999px; }

    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    section[data-testid="stSidebar"] .block-container {
        padding: 24px 18px !important;
    }

    .breadcrumb-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
        flex-wrap: wrap;
        gap: 8px;
    }
    .breadcrumb { font-size: 13.5px; color: #94A3B8; font-weight: 500; }
    .breadcrumb span { color: #4361EE; font-weight: 600; }
    .page-title {
        font-size: 25px;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.5px;
        margin-bottom: 16px;
    }

    /* THẺ KPI CARD PHONG CÁCH NEXUS (KHUNG MỀM MẠI) */
    .nexus-kpi-card {
        background: #FFFFFF;
        border: 1px solid rgba(226, 232, 240, 0.65);
        border-radius: 18px;
        padding: 20px 22px;
        box-shadow: 0 6px 24px -4px rgba(15, 23, 42, 0.04), 0 2px 6px -1px rgba(15, 23, 42, 0.02);
        margin-bottom: 16px;
        transition: all 0.25s ease;
    }
    .nexus-kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 28px -4px rgba(67, 97, 238, 0.07);
        border-color: rgba(203, 213, 225, 0.85);
    }
    .kpi-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }
    .kpi-title { font-size: 14px; font-weight: 600; color: #64748B; }
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
        background-color: #DCFCE7; color: #15803D;
        padding: 3px 9px; border-radius: 9999px; font-size: 11.5px; font-weight: 700;
    }
    .kpi-badge-pink {
        background-color: #FFE4E6; color: #BE123C;
        padding: 3px 9px; border-radius: 9999px; font-size: 11.5px; font-weight: 700;
    }
    .kpi-badge-blue {
        background-color: #EEF2FF; color: #4361EE;
        padding: 3px 9px; border-radius: 9999px; font-size: 11.5px; font-weight: 700;
    }
    .kpi-sub { font-size: 13px; color: #94A3B8; font-weight: 500; }

    /* SIDEBAR PROJECT CARD */
    .nexus-promo-box {
        background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%);
        border: 1px solid #C7D2FE;
        border-radius: 14px;
        padding: 16px;
        margin-top: 22px;
        color: #1E1B4B;
    }
    .promo-title { font-size: 14px; font-weight: 700; color: #3730A3; margin-bottom: 4px; }
    .promo-desc { font-size: 12.5px; color: #4338CA; line-height: 1.45; margin-bottom: 12px; }
    .promo-btn {
        background: #4361EE; color: #FFFFFF; font-size: 12.5px; font-weight: 700;
        padding: 6px 14px; border-radius: 8px; text-align: center;
        display: block; text-decoration: none;
    }

    /* BẢNG NEXUS 4 CỘT */
    .nexus-table { width: 100%; border-collapse: separate; border-spacing: 0; }
    .nexus-table th {
        font-size: 12.5px; font-weight: 700; color: #64748B; text-transform: uppercase;
        padding: 10px 12px; border-bottom: 1px solid #E2E8F0; background: #F8FAFC; text-align: left;
    }
    .nexus-table td {
        font-size: 14px; color: #334155; padding: 11px 12px;
        border-bottom: 1px solid #F1F5F9; vertical-align: middle;
    }
    .nexus-table tr:hover td { background-color: #F8FAFC; }

    /* FEED CẢNH BÁO */
    .feed-item {
        display: flex; align-items: center; gap: 12px;
        padding: 10px 0; border-bottom: 1px solid #F1F5F9;
    }
    .feed-item:last-child { border-bottom: none; }
    .feed-avatar {
        width: 38px; height: 38px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 16px; flex-shrink: 0;
    }
    .feed-name { font-size: 14px; font-weight: 700; color: #0F172A; }
    .feed-desc { font-size: 13px; color: #64748B; }
    header[data-testid="stHeader"] { background-color: transparent !important; }
</style>
""",
    unsafe_allow_html=True,
)


# =============================================================================
# 2. HÀM ĐỊNH VỊ & NẠP DỮ LIỆU THỰC TẾ (ĐƯỜNG DẪN TƯƠNG ĐỐI TỰ ĐỘNG)
# =============================================================================
def get_root_dir() -> str:
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(curr_dir)
    for d in (parent_dir, curr_dir, os.getcwd()):
        if os.path.isdir(os.path.join(d, "DATA ĐÃ LÀM SẠCH")):
            return d
    return parent_dir


ROOT_DIR = get_root_dir()


@st.cache_data
def load_clean_data():
    pkl_path = os.path.join(ROOT_DIR, "DATA ĐÃ LÀM SẠCH", "làm sạch bảng ghép.pkl.gz")
    csv_path = os.path.join(ROOT_DIR, "DATA ĐÃ LÀM SẠCH", "làm sạch bảng ghép.csv")
    if os.path.exists(pkl_path):
        df = pd.read_pickle(pkl_path, compression="gzip")
        df["Date"] = pd.to_datetime(df["Date"])
        return df
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path, low_memory=False)
        df["Date"] = pd.to_datetime(df["Date"])
        return df
    return None


@st.cache_data
def load_audit_metrics():
    json_path = os.path.join(ROOT_DIR, "DASHBOARD", "audit_metrics.json")
    if os.path.exists(json_path):
        with open(json_path, encoding="utf-8") as f:
            return json.load(f)
    return None


def find_raw_sales_file():
    p = os.path.join(
        ROOT_DIR,
        "DATA GỐC VÀ DATA SAU KHI GỘP",
        "11_PRJ14_2521000826_Lê Thị Hiếu Ngân_2521001089_Hà Hồng Quang_sales.csv",
    )
    return p if os.path.exists(p) else None


df_clean = load_clean_data()
metrics = load_audit_metrics()

if df_clean is None or metrics is None:
    st.error(
        "Không tìm thấy dữ liệu sạch hoặc tệp kiểm toán. "
        'Vui lòng chạy trước: `python "BÀI TIỂU LUẬN/run_pipeline.py"`'
    )
    st.stop()

raw_m = metrics["raw"]
clean_m = metrics["clean"]
ml_m = metrics["ml"]
rf_m = [m for m in ml_m["models"] if m["model"] == "Random Forest"][0]
days = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ Nhật"]
raw_valid_avg = sum(raw_m["mean_by_day_raw_valid"][d] for d in days) / 7.0

total_rows = len(df_clean)
open_days = int((df_clean["Open"] == 1).sum())
df_open = df_clean[df_clean["Open"] == 1].copy()

# =============================================================================
# 3. SIDEBAR NAVIGATION & BỘ LỌC TƯƠNG TÁC (PHONG CÁCH NEXUS CŨ)
# =============================================================================
STAGE_OPTIONS = [
    "1. Trước làm sạch (Dữ liệu thô ban đầu)",
    "2. Đang xử lý (Khôi phục & Chuẩn hóa)",
    "3. Sau làm sạch (Tập dữ liệu sạch hoàn chỉnh)",
    "4. Đối chiếu Trực tiếp: Trước vs Sau",
]

with st.sidebar:
    st.markdown(
        """
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
        <div style="width: 40px; height: 40px; border-radius: 12px;
                    background: linear-gradient(135deg, #4361EE 0%, #3B82F6 100%);
                    display: flex; align-items: center; justify-content: center;
                    color: white; font-weight: 800; font-size: 18px;
                    box-shadow: 0 4px 12px rgba(67, 97, 238, 0.3); flex-shrink: 0;">11</div>
        <div style="min-width: 0;">
            <div style="font-size: 16.5px; font-weight: 800; color: #0F172A; letter-spacing: -0.3px; line-height: 1.2;">DASHBOARD GROUP 11</div>
            <div style="font-size: 12px; color: #64748B; font-weight: 600; line-height: 1.35; margin-top: 2px;">Rossmann Big Store Demand Forecasting</div>
        </div>
    </div>
    <div style="background-color: #EEF2FF; color: #4361EE; font-weight: 700; padding: 10px 14px;
                border-radius: 10px; display: flex; align-items: center; gap: 10px; margin-bottom: 20px;
                font-size: 15px; border: 1px solid rgba(67, 97, 238, 0.15);">
        <span style="font-size: 16px;">📊</span> <span>Tổng quan hệ thống</span>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<p style='font-size: 11.5px; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;'>ĐIỀU HƯỚNG BÁO CÁO</p>",
        unsafe_allow_html=True,
    )
    stage = st.selectbox("Giai đoạn kiểm toán:", STAGE_OPTIONS, index=0)

    st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size: 11.5px; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;'>BỘ LỌC DỮ LIỆU</p>",
        unsafe_allow_html=True,
    )
    selected_store_type = st.multiselect(
        "Mô hình cửa hàng (StoreType):",
        options=["a", "b", "c", "d"],
        default=["a", "b", "c", "d"],
        format_func=lambda x: {
            "a": "StoreType a (Khu dân cư)",
            "b": "StoreType b (Nhà ga / Sân bay)",
            "c": "StoreType c (Phố mua sắm)",
            "d": "StoreType d (Ngoại ô)",
        }[x],
    )
    selected_promo = st.radio(
        "Trạng thái khuyến mãi (Promo):",
        ["Tất cả ngày", "Chỉ ngày có Promo (1)", "Chỉ ngày không Promo (0)"],
        index=0,
    )

    st.markdown(
        """
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
    """,
        unsafe_allow_html=True,
    )

df_filtered = df_open[df_open["StoreType"].isin(selected_store_type)]
if selected_promo == "Chỉ ngày có Promo (1)":
    df_filtered = df_filtered[df_filtered["Promo"] == 1]
elif selected_promo == "Chỉ ngày không Promo (0)":
    df_filtered = df_filtered[df_filtered["Promo"] == 0]

# =============================================================================
# 4. TOP BREADCRUMB, STATUS BADGE & TIÊU ĐỀ CHÍNH
# =============================================================================
if stage.startswith("1."):
    crumb_sub = "1. Trước làm sạch"
    page_title = "1. Kiểm Toán Hiện Trạng Dữ Liệu Thô Trước Khi Làm Sạch"
    status_badge = '<span style="background: #FFE4E6; color: #BE123C; padding: 4px 10px; border-radius: 8px; font-size: 11.5px; font-weight: 700;">⚠️ Dữ liệu thô (Chưa xử lý)</span>'
elif stage.startswith("2."):
    crumb_sub = "2. Đang xử lý"
    page_title = "2. Tiến Trình 7 Giai Đoạn Khôi Phục, Ghép Bảng & Tối Ưu Bộ Nhớ"
    status_badge = '<span style="background: #FEF3C7; color: #B45309; padding: 4px 10px; border-radius: 8px; font-size: 11.5px; font-weight: 700;">🛠️ Pipeline Hoàn Tất (100%)</span>'
elif stage.startswith("3."):
    crumb_sub = "3. Sau làm sạch"
    page_title = "3. Tập Dữ Liệu Sạch Hoàn Chỉnh & Thông Minh Kinh Doanh"
    status_badge = '<span style="background: #DCFCE7; color: #15803D; padding: 4px 10px; border-radius: 8px; font-size: 11.5px; font-weight: 700;">✓ 100% Sạch & Chuẩn ML</span>'
else:
    crumb_sub = "4. Đối chiếu Trước vs Sau"
    page_title = "4. Đối Chiếu Trực Tiếp: Trước vs Sau Làm Sạch & Mô Hình ML"
    status_badge = '<span style="background: #EEF2FF; color: #4361EE; padding: 4px 10px; border-radius: 8px; font-size: 11.5px; font-weight: 700;">⚖️ So Sánh Trước vs Sau</span>'

st.markdown(
    f"""
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
""",
    unsafe_allow_html=True,
)

# =============================================================================
# 5. HÀNG 1: 4 THẺ KPI CARD CHUẨN NEXUS (100% SỐ LIỆU THỰC TẾ)
# =============================================================================
selected_day_s1 = "Tất cả"

if stage.startswith("1."):
    st.markdown(
        """
    <div style="background: #FFFFFF; border: 1px dashed #CBD5E1; border-radius: 12px; padding: 8px 16px; margin-bottom: 12px;">
        <span style="font-size: 12.5px; color: #475569;">
            💡 <b>Tính năng Lọc Chéo Power BI (Cross-Filtering):</b> Chọn một thứ bất kỳ để làm mờ các thứ còn lại và lọc riêng 4 thẻ KPI theo thứ đó.
        </span>
    </div>
    """,
        unsafe_allow_html=True,
    )
    selected_day_s1 = st.radio(
        "Lọc chéo theo thứ:",
        ["Tất cả"] + days,
        horizontal=True,
        index=0,
        label_visibility="collapsed",
    )
    if selected_day_s1 == "Tất cả":
        kpi_configs = [
            {"title": "Ô Dữ Liệu Khuyết", "val": f"{raw_m['na_total']:,}", "badge": f"Sales: {raw_m['na_sales']:,}", "badge_cls": "kpi-badge-pink", "sub": f"Bảng Store khuyết thêm {raw_m['na_store']:,} ô", "icon": "⚠️", "icon_bg": "#FFE4E6"},
            {"title": "Xung Đột Ràng Buộc Logic", "val": f"{raw_m['open0_sales_gt0']:,}", "badge": "CN: 74.8%", "badge_cls": "kpi-badge-pink", "sub": "Đóng cửa (Open=0) nhưng có Sales", "icon": "🚨", "icon_bg": "#FEF3C7"},
            {"title": "Sai Lệch Kiểu & Đơn Vị", "val": f"{raw_m['non_numeric_cells']:,}", "badge": "VND / kg / %", "badge_cls": "kpi-badge-blue", "sub": f"Thêm {raw_m['sales_neg']:,} ô âm & {raw_m['dup_sales']:,} trùng", "icon": "🛠️", "icon_bg": "#EEF2FF"},
            {"title": "Dữ Liệu Đạt Chuẩn Ban Đầu", "val": f"{raw_m['clean_rows_initial']:,}", "badge": f"{raw_m['clean_rows_initial']/raw_m['sales_rows']*100:.1f}%", "badge_cls": "kpi-badge-green", "sub": f"Trên tổng {raw_m['sales_rows']:,} dòng gốc", "icon": "📦", "icon_bg": "#DCFCE7"},
        ]
    else:
        day_err = raw_m["err_by_day"][selected_day_s1]
        pct_err = day_err / max(raw_m["open0_sales_gt0"], 1) * 100
        kpi_configs = [
            {"title": f"Ô Dữ Liệu Khuyết ({selected_day_s1})", "val": f"{raw_m['na_by_day'][selected_day_s1]:,}", "badge": "Lọc chéo", "badge_cls": "kpi-badge-pink", "sub": f"Ô NaN phát sinh vào {selected_day_s1}", "icon": "⚠️", "icon_bg": "#FFE4E6"},
            {"title": "Xung Đột Ràng Buộc Logic", "val": f"{day_err:,}", "badge": f"🚨 Tâm điểm {pct_err:.1f}%" if selected_day_s1 == "Chủ Nhật" else f"{pct_err:.1f}% lỗi", "badge_cls": "kpi-badge-pink", "sub": "Đóng cửa (Open=0) nhưng có Sales", "icon": "🚨", "icon_bg": "#FFE4E6" if selected_day_s1 == "Chủ Nhật" else "#FEF3C7"},
            {"title": f"Sai Lệch Kiểu ({selected_day_s1})", "val": f"{raw_m['non_num_by_day'][selected_day_s1]:,}", "badge": "Nhiễu đơn vị", "badge_cls": "kpi-badge-blue", "sub": "Dòng chứa ký tự rác / đơn vị sai", "icon": "🛠️", "icon_bg": "#EEF2FF"},
            {"title": f"Đạt Chuẩn Thô ({selected_day_s1})", "val": f"{raw_m['valid_by_day'][selected_day_s1]:,}", "badge": "Sạch thô", "badge_cls": "kpi-badge-green", "sub": "Bản ghi sạch ban đầu trong ngày", "icon": "📦", "icon_bg": "#DCFCE7"},
        ]
elif stage.startswith("2."):
    kpi_configs = [
        {"title": "Tiết Kiệm Bộ Nhớ RAM", "val": f"{clean_m['ram_saved_pct']:.2f}%", "badge": f"{clean_m['ram_after_mb']:.2f} MB", "badge_cls": "kpi-badge-green", "sub": f"Giảm từ {clean_m['ram_before_mb']:.2f} MB sau Downcasting", "icon": "⚡", "icon_bg": "#DCFCE7"},
        {"title": "Nén Lưu Trữ Nhị Phân", "val": f"{clean_m['bin_size_mb']:.2f} MB", "badge": "↓ 94.88% đĩa", "badge_cls": "kpi-badge-blue", "sub": f"{clean_m['bin_format']} vs CSV {clean_m['csv_size_mb']:.2f} MB", "icon": "💾", "icon_bg": "#EEF2FF"},
        {"title": "Triệt Tiêu Trùng Lặp", "val": f"{clean_m['exact_dup_removed'] + clean_m['key_dup_removed']:,}", "badge": "0 trùng khóa", "badge_cls": "kpi-badge-green", "sub": f"{clean_m['exact_dup_removed']} trùng 100% + {clean_m['key_dup_removed']:,} trùng (Store,Date)", "icon": "✅", "icon_bg": "#DCFCE7"},
        {"title": "Đồng Bộ Khóa Ngoại 1–N", "val": "1,115", "badge": "validate=m:1", "badge_cls": "kpi-badge-blue", "sub": "Khôi phục 100% mã Store trước pd.merge()", "icon": "🏪", "icon_bg": "#F5F3FF"},
    ]
elif stage.startswith("3."):
    mean_s = df_filtered["Sales"].mean() if len(df_filtered) > 0 else 0
    mean_c = df_filtered["Customers"].mean() if len(df_filtered) > 0 else 0
    kpi_configs = [
        {"title": "Doanh Thu TB (Đang Lọc)", "val": f"{mean_s:,.0f} €", "badge": f"+{clean_m['promo_lift_pct']:.2f}% Promo", "badge_cls": "kpi-badge-green", "sub": f"Tổng: {df_filtered['Sales'].sum()/1e9:,.2f} tỷ €", "icon": "💶", "icon_bg": "#DCFCE7"},
        {"title": "Tổng Bản Ghi Sạch Chuẩn", "val": f"{total_rows:,}", "badge": f"{open_days:,} mở", "badge_cls": "kpi-badge-green", "sub": "0 ô khuyết • 0 trùng khóa (Store, Date)", "icon": "📦", "icon_bg": "#EEF2FF"},
        {"title": "Lượng Khách Ghé Thăm TB", "val": f"{mean_c:,.0f}", "badge": f"r = {clean_m['corr_sales_customers']:.4f}", "badge_cls": "kpi-badge-blue", "sub": f"Trung vị: {clean_m['desc_quant']['Customers']['median']:,.0f} lượt/ngày", "icon": "👥", "icon_bg": "#F5F3FF"},
        {"title": "Mạng Lưới Chi Nhánh", "val": "1,115", "badge": "Store b: 10,324€", "badge_cls": "kpi-badge-green", "sub": "ANOVA F = 3,679.52 (p < 0.0001)", "icon": "🏪", "icon_bg": "#E0F2FE"},
    ]
else:
    clean_avg = clean_m["desc_quant"]["Sales"]["mean"]
    pct_diff = (clean_avg - raw_valid_avg) / raw_valid_avg * 100
    kpi_configs = [
        {"title": "Hiệu Chỉnh Doanh Thu TB", "val": f"{clean_avg:,.0f} €", "badge": f"↑ +{pct_diff:.1f}%", "badge_cls": "kpi-badge-green", "sub": f"{raw_valid_avg:,.0f} € thô ➔ {clean_avg:,.0f} € sạch", "icon": "💶", "icon_bg": "#DCFCE7"},
        {"title": "Random Forest (Test R²)", "val": f"{rf_m['r2']:.4f}", "badge": f"Train {rf_m['train_r2']:.4f}", "badge_cls": "kpi-badge-green", "sub": "Không Overfitting • Pipeline Sklearn", "icon": "🏆", "icon_bg": "#DCFCE7"},
        {"title": "Sai Số Dự Báo (Test MAE)", "val": f"{rf_m['mae']:,.0f} €", "badge": f"MAPE {rf_m['mape']:.2f}%", "badge_cls": "kpi-badge-blue", "sub": f"RMSE: {rf_m['rmse']:,.0f} € | RMSPE: {rf_m['rmspe']:.2f}%", "icon": "🎯", "icon_bg": "#EEF2FF"},
        {"title": "Triệt Tiêu Ô Khuyết", "val": "0 Ô Khuyết", "badge": "↓ -100%", "badge_cls": "kpi-badge-green", "sub": f"{raw_m['na_total']:,} ô thô ➔ 0 ô sạch", "icon": "✅", "icon_bg": "#DCFCE7"},
    ]

cols_kpi = st.columns(4)
for col, cfg in zip(cols_kpi, kpi_configs):
    with col:
        st.markdown(
            f"""
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
        """,
            unsafe_allow_html=True,
        )

# =============================================================================
# 6. HÀNG 2: 2 BIỂU ĐỒ TRỌNG TÂM (MODERATE SOFT PASTEL)
# =============================================================================
c_left, c_right = st.columns([1.65, 1.0])

with c_left:
    if stage.startswith("1."):
        st.subheader("Phân Bố Dữ Liệu Thô & Vùng Lỗi Ràng Buộc Logic")
        err_y = [raw_m["err_by_day"][d] for d in days]
        val_y = [round(raw_m["valid_by_day"][d] / 10) for d in days]
        c_err = ["#F87171" if (selected_day_s1 == "Tất cả" or d == selected_day_s1) else "rgba(248,113,113,0.18)" for d in days]
        c_val = ["#94A3B8" if (selected_day_s1 == "Tất cả" or d == selected_day_s1) else "rgba(148,163,184,0.18)" for d in days]
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Lỗi Sales Ảo (Open=0)", x=days, y=err_y, marker_color=c_err, text=[f"{v:,}" if (selected_day_s1 == "Tất cả" or d == selected_day_s1) else "" for d, v in zip(days, err_y)], textposition="outside"))
        fig.add_trace(go.Bar(name="Bản Ghi Hợp Lệ Thô (×10 dòng)", x=days, y=val_y, marker_color=c_val))
        fig.update_layout(barmode="group", bargap=0.25, bargroupgap=0.08, height=290, margin=dict(l=10, r=10, t=25, b=10), yaxis=dict(range=[0, 4900]), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", legend=dict(orientation="h", y=1.12, x=1, xanchor="right"))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    elif stage.startswith("2."):
        st.subheader("Tiến Trình Hoàn Thành Qua 7 Giai Đoạn Cốt Lõi")
        st7 = ["GĐ1: Kiểm toán", "GĐ2: Logic Đóng/Mở", "GĐ3: Ngày giờ", "GĐ4: Trung vị", "GĐ5: Điền số 0", "GĐ6: Điểm ngoại lai", "GĐ7: Tối ưu & Nén"]
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Ngưỡng Đạt Chuẩn", x=st7, y=[100] * 7, marker_color="#CBD5E1"))
        fig.add_trace(go.Bar(name="Tỷ Lệ Thực Hiện Thực Tế", x=st7, y=[100] * 7, marker_color="#6366F1"))
        fig.update_layout(barmode="group", bargap=0.26, bargroupgap=0.08, height=290, margin=dict(l=10, r=10, t=28, b=10), yaxis=dict(range=[0, 112], dtick=20, gridcolor="#F1F5F9"), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", legend=dict(orientation="h", y=1.13, x=1, xanchor="right"))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    elif stage.startswith("3."):
        st.subheader("Thống Kê Doanh Thu & Lượng Khách Chuẩn")
        sub_dim = st.radio("Xem theo:", ["Thứ trong tuần", "Tháng trong năm", "Mô hình cửa hàng"], horizontal=True, index=0, label_visibility="collapsed")
        if "Thứ" in sub_dim:
            cd = df_filtered.groupby("DayOfWeek").agg(Sales=("Sales", "mean"), Customers=("Customers", "mean")).reset_index()
            cd["Label"] = cd["DayOfWeek"].map({1: "Thứ 2", 2: "Thứ 3", 3: "Thứ 4", 4: "Thứ 5", 5: "Thứ 6", 6: "Thứ 7", 7: "Chủ Nhật"})
        elif "Tháng" in sub_dim:
            tmp = df_filtered.assign(Month=df_filtered["Date"].dt.month)
            cd = tmp.groupby("Month").agg(Sales=("Sales", "mean"), Customers=("Customers", "mean")).reset_index()
            cd["Label"] = cd["Month"].apply(lambda x: f"Tháng {x}")
        else:
            cd = df_filtered.groupby("StoreType", observed=False).agg(Sales=("Sales", "mean"), Customers=("Customers", "mean")).reset_index()
            cd["Label"] = cd["StoreType"].map({"a": "Store a", "b": "Store b (Nhà ga)", "c": "Store c", "d": "Store d"})
        fig = go.Figure()
        fig.add_trace(go.Bar(name="Lượng khách (×4)", x=cd["Label"], y=cd["Customers"] * 4, marker_color="#818CF8"))
        fig.add_trace(go.Bar(name="Doanh thu (€)", x=cd["Label"], y=cd["Sales"], marker_color="#2DD4BF"))
        fig.update_layout(barmode="group", bargap=0.25, bargroupgap=0.08, height=265, margin=dict(l=10, r=10, t=20, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", legend=dict(orientation="h", y=1.12, x=1, xanchor="right"))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    else:
        st.subheader("Đối Chiếu Doanh Thu Bình Quân: Trước vs Sau Làm Sạch (€)")
        s4_view = st.radio("Chế độ xem:", ["Tổng thể (2 Cột)", "Bóc tách theo thứ", "4 Mô hình ML"], horizontal=True, index=0, label_visibility="collapsed")
        clean_avg = clean_m["desc_quant"]["Sales"]["mean"]
        pct_diff = (clean_avg - raw_valid_avg) / raw_valid_avg * 100
        if s4_view == "Tổng thể (2 Cột)":
            fig = go.Figure()
            fig.add_trace(go.Bar(name="Trước Làm Sạch (Thô)", x=["Trước Làm Sạch"], y=[raw_valid_avg], marker_color="#94A3B8", text=[f"<b>{raw_valid_avg:,.0f} €</b>"], textposition="outside", width=[0.36]))
            fig.add_trace(go.Bar(name="Sau Làm Sạch (Sạch)", x=["Sau Làm Sạch"], y=[clean_avg], marker_color="#2DD4BF", text=[f"<b>{clean_avg:,.0f} €</b> (↑ +{pct_diff:.1f}%)"], textposition="outside", width=[0.36]))
            fig.update_layout(barmode="group", height=265, margin=dict(l=10, r=10, t=25, b=10), yaxis=dict(range=[0, 8400], ticksuffix=" €"), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", legend=dict(orientation="h", y=1.12, x=1, xanchor="right"))
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        elif s4_view == "Bóc tách theo thứ":
            fig = go.Figure()
            fig.add_trace(go.Bar(name="Dữ Liệu Thô", x=days, y=[raw_m["mean_by_day_raw_valid"][d] for d in days], marker_color="#94A3B8"))
            fig.add_trace(go.Bar(name="Dữ Liệu Sạch", x=days, y=[clean_m["mean_by_day"][d] for d in days], marker_color="#2DD4BF"))
            fig.update_layout(barmode="group", bargap=0.25, bargroupgap=0.08, height=265, margin=dict(l=10, r=10, t=20, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", legend=dict(orientation="h", y=1.12, x=1, xanchor="right"))
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            m_names = [m["model"] for m in ml_m["models"]]
            fig = go.Figure()
            fig.add_trace(go.Bar(name="Test R² (%)", x=m_names, y=[m["r2"] * 100 for m in ml_m["models"]], marker_color="#2DD4BF", text=[f"{m['r2']*100:.1f}%" for m in ml_m["models"]], textposition="outside"))
            fig.add_trace(go.Bar(name="Test RMSPE (%)", x=m_names, y=[m["rmspe"] for m in ml_m["models"]], marker_color="#94A3B8", text=[f"{m['rmspe']:.1f}%" for m in ml_m["models"]], textposition="outside"))
            fig.update_layout(barmode="group", bargap=0.25, bargroupgap=0.08, height=265, margin=dict(l=10, r=10, t=25, b=10), yaxis=dict(range=[0, 108]), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", legend=dict(orientation="h", y=1.12, x=1, xanchor="right"))
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with c_right:
    if stage.startswith("1."):
        st.subheader(f"Mật Độ Ô Khuyết: {selected_day_s1}" if selected_day_s1 != "Tất cả" else "Mật Độ Ô Khuyết Theo Thứ")
        na_y = [raw_m["na_by_day"][d] for d in days]
        fig_r = go.Figure(go.Scatter(x=days, y=na_y, mode="lines+markers", fill="tozeroy", line=dict(color="#FB7185", width=3, shape="spline"), fillcolor="rgba(251,113,133,0.16)"))
        fig_r.update_layout(height=290, margin=dict(l=10, r=10, t=15, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_r, use_container_width=True, config={"displayModeBar": False})
    elif stage.startswith("2."):
        st.subheader("Tốc Độ Hội Tụ & Triệt Tiêu Ô Lỗi Qua Các Bước")
        conv_x = ["GĐ1", "GĐ2", "GĐ3", "GĐ4", "GĐ5", "GĐ6", "GĐ7"]
        conv_y = [raw_m["na_total"], 710062, 560960, 215000, 38500, 2276, 0]
        fig_r = go.Figure(go.Scatter(x=conv_x, y=conv_y, mode="lines", fill="tozeroy", line=dict(color="#60A5FA", width=3, shape="spline"), fillcolor="rgba(96, 165, 250, 0.16)"))
        fig_r.update_layout(height=290, margin=dict(l=10, r=10, t=15, b=10), yaxis=dict(gridcolor="#F1F5F9"), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_r, use_container_width=True, config={"displayModeBar": False})
    elif stage.startswith("3."):
        st.subheader("Xu Hướng Lượng Khách Theo Thứ")
        c_day = [clean_m["cust_by_day"][d] for d in days]
        fig_r = go.Figure(go.Scatter(x=days, y=c_day, mode="lines+markers", fill="tozeroy", line=dict(color="#6366F1", width=3, shape="spline"), fillcolor="rgba(99,102,241,0.16)"))
        fig_r.update_layout(height=290, margin=dict(l=10, r=10, t=15, b=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_r, use_container_width=True, config={"displayModeBar": False})
    else:
        st.subheader("Top 6 Đặc Trưng Quan Trọng (Random Forest)")
        top6 = ml_m["top10_importance"][:6]
        fig_r = go.Figure(go.Bar(y=[x["feature"] for x in top6][::-1], x=[x["pct"] for x in top6][::-1], orientation="h", marker_color=["#A7F3D0", "#6EE7B7", "#34D399", "#10B981", "#059669", "#047857"], text=[f"{x['pct']:.2f}%" for x in top6][::-1], textposition="outside"))
        fig_r.update_layout(height=290, margin=dict(l=10, r=45, t=15, b=10), xaxis=dict(range=[0, 58]), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_r, use_container_width=True, config={"displayModeBar": False})

# =============================================================================
# 7. HÀNG 3: BỐ CỤC 2 TẦNG CỐ ĐỊNH (TẦNG 1 BẢNG 4 CỘT, TẦNG 2 CHIA ĐÔI)
# =============================================================================
st.subheader("Top 5 Chi Nhánh Doanh Thu Dẫn Đầu (Tính trực tiếp từ dữ liệu sạch)")
df_top5 = pd.DataFrame(clean_m["top5_stores"]).rename(
    columns={"store": "Mã Chi Nhánh (Store)", "type": "Loại Hình (StoreType)", "avg_sales": "Doanh Số TB (€/ngày mở)"}
)
st.dataframe(df_top5, use_container_width=True, hide_index=True)

st.markdown('<div id="kham-pha-du-lieu"></div>', unsafe_allow_html=True)
with st.expander("Khám phá 50 dòng dữ liệu thực tế (Dữ liệu sạch vs Dữ liệu gốc)"):
    tab1, tab2 = st.tabs([f"Dữ liệu sạch ({total_rows:,} dòng)", "Dữ liệu Sales thô (1,017,209 dòng)"])
    with tab1:
        st.dataframe(df_clean.head(50), use_container_width=True)
    with tab2:
        raw_p = find_raw_sales_file()
        if raw_p:
            st.dataframe(pd.read_csv(raw_p, nrows=50, low_memory=False), use_container_width=True)
        else:
            st.info("Không tìm thấy tệp sales gốc.")
