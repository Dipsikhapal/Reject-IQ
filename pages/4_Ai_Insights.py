import streamlit as st
from utils import data_manager, insights, ui
import pandas as pd

st.set_page_config(page_title="AI Insights — RejectIQ", page_icon="🔵", layout="wide")

ui.inject_css()
ui.sidebar_info()
ui.theme_toggle()

ui.page_header(
    "AI Insights",
    "Data-driven recommendations for your business",
    icon_svg='<svg width="18" height="18" fill="none" stroke="#2563EB" stroke-width="2" viewBox="0 0 24 24"><path d="M12 2a7 7 0 00-4 12.74V17a2 2 0 002 2h4a2 2 0 002-2v-2.26A7 7 0 0012 2z"/><line x1="9" y1="21" x2="15" y2="21"/></svg>',
)

df = data_manager.load_data()
if df.empty:
    ui.empty_state("No data found. Add rejections to generate insights.")
    st.stop()

# ── Overall summary ──────────────────────────────────────────────────────────
ui.section_label("Overall Summary")
total = len(df)
top_product = df["Product"].mode()[0] if total > 0 else "—"
top_reason = df["Reason"].mode()[0] if total > 0 else "—"
top_city = df["City"].mode()[0] if total > 0 else "—"
top_salesperson = df["Salesperson"].mode()[0] if total > 0 else "—"

c1, c2, c3, c4 = st.columns(4)
c1.metric("Records", total)
c2.metric("Top Product", top_product)
c3.metric("Top Reason", top_reason)
c4.metric("Top City", top_city)

st.divider()

# ── Product insights ──────────────────────────────────────────────────────────
ui.section_label("Product Insights & Opportunity Score")
product_counts = df["Product"].value_counts()

SUGGESTION_MAP = {
    "Too Expensive": "Consider discounts or budget variants.",
    "Already Using Competitor": "Highlight unique features and benefits.",
    "Need Discount": "Launch promotional offers.",
    "Need More Information": "Improve product demonstrations.",
    "Not Interested": "Improve targeting and marketing.",
}

for product in product_counts.index:
    temp = df[df["Product"] == product]
    reason = temp["Reason"].mode()[0]
    city = temp["City"].mode()[0]
    opportunity = max(0, 100 - int((len(temp) / len(df)) * 100))
    suggestion = SUGGESTION_MAP.get(reason, "Collect additional customer feedback.")

    st.markdown(f"""
    <div class="riq-card">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:0.75rem">
        <div>
          <div style="font-size:1rem;font-weight:700;color:#F8FAFC">{product}</div>
          <div style="font-size:0.78rem;color:#64748B;margin-top:2px">{len(temp)} rejections recorded</div>
        </div>
        {ui.badge(f"{opportunity}/100 Opportunity", "green" if opportunity >= 60 else "yellow" if opportunity >= 35 else "red")}
      </div>
      <div style="display:flex;gap:1.5rem;margin-bottom:0.75rem">
        <div>
          <div style="font-size:0.7rem;color:#475569;text-transform:uppercase;letter-spacing:0.06em">Most Common Reason</div>
          <div style="font-size:0.85rem;color:#CBD5E1;font-weight:500">{reason}</div>
        </div>
        <div>
          <div style="font-size:0.7rem;color:#475569;text-transform:uppercase;letter-spacing:0.06em">Most Affected City</div>
          <div style="font-size:0.85rem;color:#CBD5E1;font-weight:500">{city}</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    ui.insight_card("Suggestion", suggestion, variant="success")

st.divider()

# ── City insights ──────────────────────────────────────────────────────────────
ui.section_label("City Insights")
city_counts = df["City"].value_counts()
for city in city_counts.index:
    temp = df[df["City"] == city]
    reason = temp["Reason"].mode()[0]
    ui.insight_card(city, f"Main rejection reason: <strong>{reason}</strong> &nbsp;·&nbsp; Total rejections: <strong>{len(temp)}</strong>", variant="warning")

st.divider()

# ── Salesperson activity ────────────────────────────────────────────────────────
ui.section_label("Salesperson Activity")
sales = df["Salesperson"].value_counts().reset_index()
sales.columns = ["Salesperson", "Entries"]
st.dataframe(sales, use_container_width=True, hide_index=True)

st.divider()

# ── Quick recommendations ────────────────────────────────────────────────────────
ui.section_label("Quick Recommendations")
for item in insights.get_all_insights(df):
    ui.insight_card("Recommendation", item, variant="success")

st.divider()

# ── Business health score ────────────────────────────────────────────────────────
ui.section_label("Business Health Score")
score = 100
if total > 50:
    score -= 10
if top_reason == "Too Expensive":
    score -= 15
if top_reason == "Already Using Competitor":
    score -= 10
if top_reason == "Need Discount":
    score -= 8

score_color = "#10B981" if score >= 80 else "#F59E0B" if score >= 60 else "#EF4444"
st.markdown(f"""
<div class="riq-card" style="text-align:center;padding:1.75rem">
  <div class="riq-health-number" style="color:{score_color}">{score}</div>
  <div style="font-size:0.8rem;color:#64748B;margin-top:0.25rem">out of 100</div>
</div>
""", unsafe_allow_html=True)
ui.score_bar(score, "Overall Health")

st.divider()

# ── Customer segmentation ────────────────────────────────────────────────────────
ui.section_label("Customer Segmentation")
seg = [
    ("At-risk", df[df["Reason"].isin(["Too Expensive", "Need Discount"])].shape[0], "red"),
    ("Needs Info", df[df["Reason"] == "Need More Information"].shape[0], "cyan"),
    ("Competitor", df[df["Reason"] == "Already Using Competitor"].shape[0], "yellow"),
]
seg_cols = st.columns(3)
for col, (name, count, color) in zip(seg_cols, seg):
    with col:
        st.markdown(f"""
        <div class="riq-card" style="text-align:center">
          <div style="font-size:1.6rem;font-weight:700;color:#F8FAFC">{count}</div>
          <div style="margin-top:0.4rem">{ui.badge(name, color)}</div>
        </div>
        """, unsafe_allow_html=True)