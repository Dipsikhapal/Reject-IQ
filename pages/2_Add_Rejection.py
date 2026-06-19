import streamlit as st
from datetime import datetime
from utils import data_manager
from utils import ui

st.set_page_config(page_title="Add Rejection — RejectIQ", page_icon="🔵", layout="wide")

ui.inject_css()
ui.sidebar_info()
ui.theme_toggle()

ui.page_header(
    "Add Customer Rejection",
    "Record a new rejection event for analysis",
    icon_svg='<svg width="18" height="18" fill="none" stroke="#2563EB" stroke-width="2" viewBox="0 0 24 24"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>',
)

df = data_manager.load_data()

st.markdown('<div class="riq-card">', unsafe_allow_html=True)

left, right = st.columns(2)

with left:
    product = st.text_input("Product Name", placeholder="e.g. Enterprise Plan")

    age = st.selectbox(
        "Age Group",
        ["18-25", "26-35", "36-45", "46-60", "60+"],
    )

    city = st.text_input("City", placeholder="e.g. Nagpur")

with right:
    salesperson = st.text_input("Salesperson", placeholder="e.g. Riya Sharma")

    reason = st.selectbox(
        "Rejection Reason",
        [
            "Too Expensive",
            "Need Discount",
            "Need More Information",
            "Already Using Competitor",
            "Not Interested",
            "Bad Timing",
            "Poor Quality",
            "Other",
        ],
    )

    comments = st.text_area("Comments", placeholder="Add any additional context...", height=100)

st.markdown("</div>", unsafe_allow_html=True)

st.write("")

col1, col2 = st.columns([2, 1], gap="large")

with col1:
    ui.section_label("Save Record")

    if st.button("Save Rejection", use_container_width=True):
        if not product.strip() or not city.strip() or not salesperson.strip():
            st.error("Please fill Product, City and Salesperson.")
        else:
            record = {
                "Product": product.strip(),
                "Age Group": age,
                "City": city.strip(),
                "Salesperson": salesperson.strip(),
                "Reason": reason,
                "Comments": comments.strip(),
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

            df, added, dups = data_manager.add_record(record, force=False)
            if not added and dups is not None and len(dups) > 0:
                st.warning("Possible duplicate(s) found:")
                st.dataframe(dups, use_container_width=True, hide_index=True)
                if st.button("Force Save Duplicate", use_container_width=True):
                    df, added2, _ = data_manager.add_record(record, force=True)
                    if added2:
                        st.success("Rejection added (duplicate forced).")
            else:
                st.success("Rejection added successfully.")

with col2:
    ui.section_label("Bulk Import & Backup")

    uploaded = st.file_uploader("Upload CSV", help="Columns: Product, Age Group, City, Salesperson, Reason, Comments")
    if uploaded is not None:
        merged, err = data_manager.upload_csv_file(uploaded, merge=True)
        if err:
            st.error(f"Upload failed: {err}")
        else:
            st.success("CSV uploaded and merged.")

    if st.button("Backup CSV", use_container_width=True):
        dst = data_manager.backup_csv()
        if dst:
            st.success(f"Backup created: {dst}")
        else:
            st.info("No data to backup.")

st.divider()

ui.section_label("Latest Records")

df = data_manager.load_data()
if df.empty:
    ui.empty_state("No records found yet.")
else:
    st.dataframe(df.tail(10).iloc[::-1], use_container_width=True, hide_index=True)