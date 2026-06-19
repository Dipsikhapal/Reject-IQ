import streamlit as st
from utils import data_manager, ui
import pandas as pd

st.set_page_config(page_title="Admin — RejectIQ", page_icon="🔵", layout="wide")

ui.inject_css()
ui.sidebar_info()
ui.theme_toggle()

ui.page_header(
    "Admin",
    "Manage records, backups and data",
    icon_svg='<svg width="18" height="18" fill="none" stroke="#2563EB" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 11-2.83 2.83l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 11-4 0v-.09a1.65 1.65 0 00-1-1.51 1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 11-2.83-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 110-4h.09a1.65 1.65 0 001.51-1 1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 112.83-2.83l.06.06a1.65 1.65 0 001.82.33h0a1.65 1.65 0 001-1.51V3a2 2 0 114 0v.09a1.65 1.65 0 001 1.51h0a1.65 1.65 0 001.82-.33l.06-.06a2 2 0 112.83 2.83l-.06.06a1.65 1.65 0 00-.33 1.82v0a1.65 1.65 0 001.51 1H21a2 2 0 110 4h-.09a1.65 1.65 0 00-1.51 1z"/></svg>',
)

df = data_manager.load_data()
if df.empty:
    st.info("No records to manage.")

# ── Edit / delete record ──────────────────────────────────────────────────────
ui.section_label("Records")

selected = st.selectbox(
    "Select record ID to edit/delete",
    [None] + (df["ID"].astype(str).tolist() if not df.empty else []),
)

if selected:
    rid = int(selected)
    rec = df[df["ID"] == rid].iloc[0].to_dict()

    st.markdown('<div class="riq-card">', unsafe_allow_html=True)
    with st.form("edit_form"):
        c1, c2 = st.columns(2)
        with c1:
            product = st.text_input("Product", value=rec.get("Product", ""))
            age = st.text_input("Age Group", value=rec.get("Age Group", ""))
            city = st.text_input("City", value=rec.get("City", ""))
        with c2:
            salesperson = st.text_input("Salesperson", value=rec.get("Salesperson", ""))
            reason = st.text_input("Reason", value=rec.get("Reason", ""))
        comments = st.text_area("Comments", value=rec.get("Comments", ""))

        submitted = st.form_submit_button("Save Changes")
        if submitted:
            updates = {
                "Product": product,
                "Age Group": age,
                "City": city,
                "Salesperson": salesperson,
                "Reason": reason,
                "Comments": comments,
            }
            df2, ok = data_manager.edit_record(rid, updates)
            if ok:
                st.success("Record updated.")
            else:
                st.error("Unable to update record.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
    if st.button("Delete Record"):
        _, ok = data_manager.delete_record(rid)
        if ok:
            st.success("Record deleted.")
        else:
            st.error("Delete failed.")
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

# ── Backups ──────────────────────────────────────────────────────────────────
ui.section_label("Backups")

bc1, bc2 = st.columns([1, 2])
with bc1:
    if st.button("Create Backup", use_container_width=True):
        dst = data_manager.backup_csv()
        if dst:
            st.success(f"Backup created: {dst}")
        else:
            st.info("No data to backup.")

backups = data_manager.list_backups()
if backups:
    sel = st.selectbox("Available backups", backups)
    st.markdown('<div class="btn-secondary">', unsafe_allow_html=True)
    if st.button("Restore Selected Backup"):
        ok = data_manager.restore_backup(sel)
        if ok:
            st.success("Backup restored. Reload the app to see changes.")
        else:
            st.error("Restore failed.")
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("No backups found.")

st.divider()

ui.section_label("All Records")
st.dataframe(df.iloc[::-1], use_container_width=True, hide_index=True)