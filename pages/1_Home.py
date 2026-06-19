import streamlit as st
from utils import data_manager, ui

st.set_page_config(page_title="Home — RejectIQ", page_icon="🔵", layout="wide")

ui.inject_css()
ui.sidebar_info()
ui.theme_toggle()

ui.page_header(
    "Home",
    "Welcome to the Customer Rejection Intelligence Platform",
    icon_svg='<svg width="18" height="18" fill="none" stroke="#2563EB" stroke-width="2" viewBox="0 0 24 24"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><path d="M9 22V12h6v10"/></svg>',
)

df = data_manager.load_data()
total = len(df)

top_product = df["Product"].mode()[0] if total > 0 and not df["Product"].isna().all() else "—"
top_reason = df["Reason"].mode()[0] if total > 0 and not df["Reason"].isna().all() else "—"
top_city = df["City"].mode()[0] if total > 0 and not df["City"].isna().all() else "—"

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Rejections", total)
c2.metric("Top Product", top_product)
c3.metric("Top Reason", top_reason)
c4.metric("Top City", top_city)

st.divider()

left, right = st.columns([2, 1], gap="large")

with left:
    ui.section_label("Recent Entries")
    if total > 0:
        st.dataframe(df.tail(10).iloc[::-1], use_container_width=True, hide_index=True)
    else:
        ui.empty_state("No data available. Add a rejection to get started.")

with right:
    ui.section_label("Quick Summary")
    st.markdown(f"""
    <div class="riq-card">
      <div style="display:flex;justify-content:space-between;padding:0.4rem 0;border-bottom:1px solid #334155">
        <span style="font-size:0.82rem;color:#94A3B8">Products</span>
        <span style="font-size:0.82rem;font-weight:600;color:#F8FAFC">{df['Product'].nunique() if total > 0 else 0}</span>
      </div>
      <div style="display:flex;justify-content:space-between;padding:0.4rem 0;border-bottom:1px solid #334155">
        <span style="font-size:0.82rem;color:#94A3B8">Cities</span>
        <span style="font-size:0.82rem;font-weight:600;color:#F8FAFC">{df['City'].nunique() if total > 0 else 0}</span>
      </div>
      <div style="display:flex;justify-content:space-between;padding:0.4rem 0;border-bottom:1px solid #334155">
        <span style="font-size:0.82rem;color:#94A3B8">Salespersons</span>
        <span style="font-size:0.82rem;font-weight:600;color:#F8FAFC">{df['Salesperson'].nunique() if total > 0 else 0}</span>
      </div>
      <div style="display:flex;justify-content:space-between;padding:0.4rem 0">
        <span style="font-size:0.82rem;color:#94A3B8">Rejection Reasons</span>
        <span style="font-size:0.82rem;font-weight:600;color:#F8FAFC">{df['Reason'].nunique() if total > 0 else 0}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

ui.section_label("Platform Features")
a, b, c = st.columns(3)
with a:
    ui.insight_card(
        "Add Rejections",
        "Store customer feedback and rejection reasons as they happen.",
    )
with b:
    ui.insight_card(
        "Dashboard",
        "View rejection trends across products, cities and salespeople.",
        variant="success",
    )
with c:
    ui.insight_card(
        "AI Insights",
        "Get smart, data-driven recommendations for your business.",
        variant="warning",
    )

st.divider()
st.caption("Customer Rejection Intelligence Platform")