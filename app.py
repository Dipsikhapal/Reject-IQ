import streamlit as st
from utils import ui, data_manager
from utils.auth import login, signup

# ── Session defaults ───────────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RejectIQ — Customer Rejection Intelligence",
    page_icon="assets/favicon.ico" if __import__("pathlib").Path("assets/favicon.ico").exists() else "🔵",
    layout="wide",
    initial_sidebar_state="collapsed",
)

ui.inject_css()

# ── Auth wall ──────────────────────────────────────────────────────────────────
if not st.session_state.logged_in:

    # Extra auth-screen styles
    st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none !important; }
    .block-container { max-width: 460px !important; margin: 0 auto; padding-top: 5rem !important; }

    .auth-logo {
      display: flex; align-items: center; gap: 0.6rem;
      margin-bottom: 2rem;
    }
    .auth-logo-mark {
      width: 38px; height: 38px;
      background: #2563EB;
      border-radius: 9px;
      display: flex; align-items: center; justify-content: center;
      font-size: 1rem; font-weight: 800; color: white;
    }
    .auth-logo-text { font-size: 1.25rem; font-weight: 700; color: #F8FAFC; letter-spacing: -0.02em; }
    .auth-logo-tag  { font-size: 0.7rem; color: #475569; }

    .auth-card {
      background: #1E293B;
      border: 1px solid #334155;
      border-radius: 14px;
      padding: 2rem;
    }
    .auth-heading { font-size: 1.35rem; font-weight: 700; color: #F8FAFC; margin-bottom: 0.25rem; }
    .auth-sub     { font-size: 0.85rem; color: #94A3B8; margin-bottom: 1.5rem; }
    .auth-switch  { font-size: 0.8rem; color: #64748B; margin-top: 1rem; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

    # Logo
    st.markdown("""
    <div class="auth-logo">
      <div class="auth-logo-mark">RQ</div>
      <div>
        <div class="auth-logo-text">RejectIQ</div>
        <div class="auth-logo-tag">Customer Rejection Intelligence</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Card
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)

    tab_login, tab_signup = st.tabs(["Sign in", "Create account"])

    with tab_login:
        st.markdown('<div class="auth-heading">Welcome back</div>', unsafe_allow_html=True)
        st.markdown('<div class="auth-sub">Sign in to your RejectIQ workspace</div>', unsafe_allow_html=True)

        username_l = st.text_input("Username", key="login_user", placeholder="your username")
        password_l = st.text_input("Password", type="password", key="login_pass", placeholder="••••••••")

        if st.button("Sign in", use_container_width=True, key="btn_login"):
            if not username_l.strip() or not password_l.strip():
                st.error("Please enter username and password.")
            elif login(username_l.strip(), password_l.strip()):
                st.session_state.logged_in = True
                st.session_state.username = username_l.strip()
                st.rerun()
            else:
                st.error("Incorrect username or password.")

    with tab_signup:
        st.markdown('<div class="auth-heading">Create account</div>', unsafe_allow_html=True)
        st.markdown('<div class="auth-sub">Start capturing customer intelligence today</div>', unsafe_allow_html=True)

        username_s = st.text_input("Username", key="signup_user", placeholder="choose a username")
        password_s = st.text_input("Password", type="password", key="signup_pass", placeholder="min. 6 characters")

        if st.button("Create account", use_container_width=True, key="btn_signup"):
            if not username_s.strip() or not password_s.strip():
                st.error("Username and password are required.")
            elif len(password_s) < 6:
                st.error("Password must be at least 6 characters.")
            elif signup(username_s.strip(), password_s.strip()):
                st.success("Account created — you can now sign in.")
            else:
                st.error("That username is already taken.")

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ── Authenticated: Home ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RejectIQ — Home",
    page_icon="🔵",
    layout="wide",
    initial_sidebar_state="expanded",
)

ui.inject_css()
ui.sidebar_info()
ui.theme_toggle()

df = data_manager.load_data()
total = len(df)

# Hero header
st.markdown(f"""
<div style="margin-bottom:2rem">
  <div style="font-size:0.75rem;font-weight:600;text-transform:uppercase;letter-spacing:0.1em;color:#2563EB;margin-bottom:0.4rem">
    Welcome back, {st.session_state.username}
  </div>
  <div style="font-size:1.75rem;font-weight:800;color:#F8FAFC;letter-spacing:-0.03em;line-height:1.2">
    Customer Rejection Intelligence
  </div>
  <div style="font-size:0.9rem;color:#64748B;margin-top:0.4rem">
    Turn every "no" into actionable business intelligence.
  </div>
</div>
""", unsafe_allow_html=True)

# ── KPI row ────────────────────────────────────────────────────────────────────
top_product    = df["Product"].mode()[0]    if total > 0 and not df["Product"].isna().all()    else "—"
top_reason     = df["Reason"].mode()[0]     if total > 0 and not df["Reason"].isna().all()     else "—"
top_city       = df["City"].mode()[0]       if total > 0 and not df["City"].isna().all()       else "—"
top_salesperson = df["Salesperson"].mode()[0] if total > 0 and not df["Salesperson"].isna().all() else "—"

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Rejections", total)
c2.metric("Top Product", top_product)
c3.metric("Top Reason", top_reason)
c4.metric("Top City", top_city)

st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

# ── Summary pills ──────────────────────────────────────────────────────────────
products_n    = df["Product"].nunique()    if total > 0 else 0
cities_n      = df["City"].nunique()       if total > 0 else 0
salespeople_n = df["Salesperson"].nunique() if total > 0 else 0
reasons_n     = df["Reason"].nunique()     if total > 0 else 0

st.markdown(f"""
<div style="display:flex;gap:0.75rem;flex-wrap:wrap;margin-bottom:1.75rem">
  <div style="background:#1E293B;border:1px solid #334155;border-radius:8px;padding:0.6rem 1rem;display:flex;align-items:center;gap:0.5rem">
    <svg width="14" height="14" fill="none" stroke="#2563EB" stroke-width="2" viewBox="0 0 24 24"><path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z"/></svg>
    <span style="font-size:0.8rem;color:#94A3B8"><strong style="color:#F8FAFC">{products_n}</strong> Products</span>
  </div>
  <div style="background:#1E293B;border:1px solid #334155;border-radius:8px;padding:0.6rem 1rem;display:flex;align-items:center;gap:0.5rem">
    <svg width="14" height="14" fill="none" stroke="#06B6D4" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 010 20M12 2a15.3 15.3 0 000 20"/></svg>
    <span style="font-size:0.8rem;color:#94A3B8"><strong style="color:#F8FAFC">{cities_n}</strong> Cities</span>
  </div>
  <div style="background:#1E293B;border:1px solid #334155;border-radius:8px;padding:0.6rem 1rem;display:flex;align-items:center;gap:0.5rem">
    <svg width="14" height="14" fill="none" stroke="#10B981" stroke-width="2" viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>
    <span style="font-size:0.8rem;color:#94A3B8"><strong style="color:#F8FAFC">{salespeople_n}</strong> Salespersons</span>
  </div>
  <div style="background:#1E293B;border:1px solid #334155;border-radius:8px;padding:0.6rem 1rem;display:flex;align-items:center;gap:0.5rem">
    <svg width="14" height="14" fill="none" stroke="#F59E0B" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
    <span style="font-size:0.8rem;color:#94A3B8"><strong style="color:#F8FAFC">{reasons_n}</strong> Rejection Reasons</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Main content ───────────────────────────────────────────────────────────────
left, right = st.columns([3, 2], gap="large")

with left:
    ui.section_label("Recent Entries")
    if total > 0:
        st.dataframe(
            df.tail(10).iloc[::-1],
            use_container_width=True,
            hide_index=True,
        )
    else:
        ui.empty_state("No rejections recorded yet. Add your first entry to get started.")

with right:
    ui.section_label("Quick Actions")
    st.markdown("""
    <div style="display:flex;flex-direction:column;gap:0.6rem">
      <div class="riq-card" style="padding:0.9rem 1rem">
        <div style="font-size:0.85rem;font-weight:600;color:#F8FAFC;margin-bottom:0.2rem">Add Rejection</div>
        <div style="font-size:0.75rem;color:#64748B">Record a new customer rejection event</div>
      </div>
      <div class="riq-card" style="padding:0.9rem 1rem">
        <div style="font-size:0.85rem;font-weight:600;color:#F8FAFC;margin-bottom:0.2rem">View Dashboard</div>
        <div style="font-size:0.75rem;color:#64748B">Explore charts and trend analysis</div>
      </div>
      <div class="riq-card" style="padding:0.9rem 1rem">
        <div style="font-size:0.85rem;font-weight:600;color:#F8FAFC;margin-bottom:0.2rem">AI Insights</div>
        <div style="font-size:0.75rem;color:#64748B">Get intelligent business recommendations</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    ui.section_label("Platform")
    st.markdown("""
    <div style="display:flex;flex-direction:column;gap:0.4rem">
      <div style="display:flex;align-items:center;gap:0.5rem;padding:0.5rem 0;border-bottom:1px solid #1E293B">
        <svg width="14" height="14" fill="none" stroke="#10B981" stroke-width="2" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>
        <span style="font-size:0.82rem;color:#94A3B8">Record customer rejections</span>
      </div>
      <div style="display:flex;align-items:center;gap:0.5rem;padding:0.5rem 0;border-bottom:1px solid #1E293B">
        <svg width="14" height="14" fill="none" stroke="#10B981" stroke-width="2" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>
        <span style="font-size:0.82rem;color:#94A3B8">Analyze trends and patterns</span>
      </div>
      <div style="display:flex;align-items:center;gap:0.5rem;padding:0.5rem 0;border-bottom:1px solid #1E293B">
        <svg width="14" height="14" fill="none" stroke="#10B981" stroke-width="2" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>
        <span style="font-size:0.82rem;color:#94A3B8">AI-powered recommendations</span>
      </div>
      <div style="display:flex;align-items:center;gap:0.5rem;padding:0.5rem 0">
        <svg width="14" height="14" fill="none" stroke="#10B981" stroke-width="2" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>
        <span style="font-size:0.82rem;color:#94A3B8">Export and report data</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("<div style='text-align:center;font-size:0.72rem;color:#1E293B'>RejectIQ &mdash; Customer Rejection Intelligence Platform</div>", unsafe_allow_html=True)