"""
RejectIQ — UI helpers & design system components.
All rendering helpers live here; no business logic.
"""

import pathlib
import streamlit as st


# ── CSS injection ──────────────────────────────────────────────────────────────

def inject_css():
    """Load the central stylesheet and inject shared component CSS."""
    css_path = pathlib.Path("assets/style.css")
    try:
        if css_path.exists():
            with open(css_path, "r", encoding="utf-8") as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception:
        pass

    # Inline component tokens not easily expressible in static CSS
    st.markdown("""
    <style>
    /* Glass card */
    .riq-card {
      background: #1E293B;
      border: 1px solid #334155;
      border-radius: 12px;
      padding: 1.25rem 1.5rem;
      margin-bottom: 1rem;
      transition: border-color 0.2s ease, transform 0.2s ease;
    }
    .riq-card:hover { border-color: #2563EB; transform: translateY(-1px); }

    /* Page header */
    .riq-page-header {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      margin-bottom: 1.75rem;
    }
    .riq-page-header-icon {
      width: 36px; height: 36px;
      background: rgba(37,99,235,0.15);
      border-radius: 8px;
      display: flex; align-items: center; justify-content: center;
    }
    .riq-page-title {
      font-size: 1.5rem !important;
      font-weight: 700 !important;
      color: #F8FAFC !important;
      margin: 0 !important;
      letter-spacing: -0.02em;
    }
    .riq-page-subtitle {
      font-size: 0.85rem !important;
      color: #94A3B8 !important;
      margin: 0 !important;
    }

    /* Section label */
    .riq-section-label {
      font-size: 0.7rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: #475569;
      margin-bottom: 0.75rem;
    }

    /* Status badge */
    .riq-badge {
      display: inline-block;
      padding: 0.2rem 0.65rem;
      border-radius: 9999px;
      font-size: 0.72rem;
      font-weight: 600;
      letter-spacing: 0.04em;
    }
    .riq-badge-blue   { background: rgba(37,99,235,0.15); color: #60A5FA; border: 1px solid rgba(37,99,235,0.3); }
    .riq-badge-green  { background: rgba(16,185,129,0.12); color: #34D399; border: 1px solid rgba(16,185,129,0.25); }
    .riq-badge-yellow { background: rgba(245,158,11,0.12); color: #FCD34D; border: 1px solid rgba(245,158,11,0.25); }
    .riq-badge-red    { background: rgba(239,68,68,0.12); color: #F87171; border: 1px solid rgba(239,68,68,0.25); }
    .riq-badge-cyan   { background: rgba(6,182,212,0.12); color: #22D3EE; border: 1px solid rgba(6,182,212,0.25); }

    /* Insight card */
    .riq-insight {
      background: #1E293B;
      border: 1px solid #334155;
      border-left: 3px solid #2563EB;
      border-radius: 0 10px 10px 0;
      padding: 1rem 1.25rem;
      margin-bottom: 0.75rem;
    }
    .riq-insight-title {
      font-size: 0.9rem;
      font-weight: 600;
      color: #F8FAFC;
      margin-bottom: 0.3rem;
    }
    .riq-insight-body {
      font-size: 0.82rem;
      color: #94A3B8;
    }
    .riq-insight-warning { border-left-color: #F59E0B; }
    .riq-insight-success { border-left-color: #10B981; }
    .riq-insight-danger  { border-left-color: #EF4444; }

    /* Score bar */
    .riq-score-wrap { margin: 0.5rem 0 1rem; }
    .riq-score-bar-bg {
      height: 6px;
      background: #334155;
      border-radius: 999px;
      overflow: hidden;
    }
    .riq-score-bar-fill {
      height: 100%;
      border-radius: 999px;
      transition: width 0.6s ease;
    }

    /* Sidebar logo */
    .riq-sidebar-logo {
      display: flex;
      align-items: center;
      gap: 0.6rem;
      padding: 0.25rem 0 1.25rem;
      border-bottom: 1px solid #1E293B;
      margin-bottom: 1.25rem;
    }
    .riq-sidebar-logo-mark {
      width: 30px; height: 30px;
      background: #2563EB;
      border-radius: 7px;
      display: flex; align-items: center; justify-content: center;
      font-size: 0.8rem;
      font-weight: 700;
      color: white;
      letter-spacing: -0.05em;
    }
    .riq-sidebar-logo-text {
      font-size: 1rem;
      font-weight: 700;
      color: #F8FAFC;
      letter-spacing: -0.02em;
    }
    .riq-sidebar-logo-tag {
      font-size: 0.65rem;
      color: #475569;
      margin-top: -2px;
    }

    /* Sidebar nav section label */
    .riq-nav-label {
      font-size: 0.65rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: #475569;
      margin: 1rem 0 0.4rem;
    }

    /* User row in sidebar */
    .riq-user-row {
      display: flex;
      align-items: center;
      gap: 0.6rem;
      padding: 0.75rem;
      background: #111827;
      border: 1px solid #1E293B;
      border-radius: 10px;
      margin-top: 1.5rem;
    }
    .riq-avatar {
      width: 28px; height: 28px;
      background: linear-gradient(135deg, #2563EB, #06B6D4);
      border-radius: 50%;
      display: flex; align-items: center; justify-content: center;
      font-size: 0.7rem;
      font-weight: 700;
      color: white;
      flex-shrink: 0;
    }
    .riq-user-name { font-size: 0.82rem; font-weight: 600; color: #E2E8F0; }
    .riq-user-status { font-size: 0.7rem; color: #10B981; }

    /* Quick stat row */
    .riq-stat-row {
      display: flex;
      gap: 0.5rem;
      margin-bottom: 0.5rem;
    }
    .riq-stat-pill {
      flex: 1;
      background: #1E293B;
      border: 1px solid #334155;
      border-radius: 8px;
      padding: 0.6rem 0.75rem;
      text-align: center;
    }
    .riq-stat-pill-val {
      font-size: 1.1rem;
      font-weight: 700;
      color: #F8FAFC;
      display: block;
    }
    .riq-stat-pill-lbl {
      font-size: 0.65rem;
      color: #64748B;
      text-transform: uppercase;
      letter-spacing: 0.06em;
    }

    /* Empty state */
    .riq-empty {
      text-align: center;
      padding: 3rem 1rem;
      color: #475569;
    }
    .riq-empty-icon { font-size: 2rem; margin-bottom: 0.75rem; }
    .riq-empty-msg { font-size: 0.9rem; }

    /* Chart wrapper */
    .riq-chart-wrap {
      background: #1E293B;
      border: 1px solid #334155;
      border-radius: 12px;
      padding: 1rem 1rem 0.5rem;
      margin-bottom: 1rem;
    }

    /* Table header label */
    .riq-table-header {
      font-size: 0.72rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: #64748B;
      margin-bottom: 0.5rem;
    }

    /* Health score display */
    .riq-health-number {
      font-size: 3rem;
      font-weight: 800;
      letter-spacing: -0.04em;
      line-height: 1;
    }
    </style>
    """, unsafe_allow_html=True)


# ── Page header ────────────────────────────────────────────────────────────────

def page_header(title: str, subtitle: str = "", icon_svg: str = ""):
    """Render a consistent page title with optional subtitle."""
    icon_html = ""
    if icon_svg:
        icon_html = f"""
        <div class="riq-page-header-icon">
          {icon_svg}
        </div>"""
    st.markdown(f"""
    <div class="riq-page-header">
      {icon_html}
      <div>
        <div class="riq-page-title">{title}</div>
        {"<div class='riq-page-subtitle'>" + subtitle + "</div>" if subtitle else ""}
      </div>
    </div>
    """, unsafe_allow_html=True)


# ── Sidebar ────────────────────────────────────────────────────────────────────

def sidebar_info():
    """Render the branded sidebar header and user info."""
    username = st.session_state.get("username", "User")
    initials = username[:2].upper() if username else "U"

    st.sidebar.markdown(f"""
    <div class="riq-sidebar-logo">
      <div class="riq-sidebar-logo-mark">RQ</div>
      <div>
        <div class="riq-sidebar-logo-text">RejectIQ</div>
        <div class="riq-sidebar-logo-tag">Business Intelligence</div>
      </div>
    </div>

    <div class="riq-nav-label">Navigation</div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown(f"""
    <div class="riq-user-row">
      <div class="riq-avatar">{initials}</div>
      <div>
        <div class="riq-user-name">{username}</div>
        <div class="riq-user-status">&#x25CF; Online</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("<div style='margin-top:1rem'></div>", unsafe_allow_html=True)

    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()


# ── Theme toggle (preserved for compatibility) ─────────────────────────────────

def theme_toggle():
    """Kept for API compatibility — dark-only in this design."""
    if "theme" not in st.session_state:
        st.session_state["theme"] = "dark"


# ── Card helpers ───────────────────────────────────────────────────────────────

def card(content_html: str, hover: bool = True):
    """Render content inside a riq-card container."""
    hover_class = "riq-card" if hover else "riq-card" 
    st.markdown(f"<div class='{hover_class}'>{content_html}</div>", unsafe_allow_html=True)


def section_label(text: str):
    st.markdown(f"<div class='riq-section-label'>{text}</div>", unsafe_allow_html=True)


# ── Status badge ───────────────────────────────────────────────────────────────

def badge(text: str, color: str = "blue") -> str:
    """Return HTML for an inline badge. color: blue|green|yellow|red|cyan"""
    return f"<span class='riq-badge riq-badge-{color}'>{text}</span>"


# ── Insight card ───────────────────────────────────────────────────────────────

def insight_card(title: str, body: str, variant: str = ""):
    """Render a left-bordered insight card. variant: warning|success|danger|''"""
    cls = f"riq-insight riq-insight-{variant}" if variant else "riq-insight"
    st.markdown(f"""
    <div class="{cls}">
      <div class="riq-insight-title">{title}</div>
      <div class="riq-insight-body">{body}</div>
    </div>
    """, unsafe_allow_html=True)


# ── Score bar ──────────────────────────────────────────────────────────────────

def score_bar(score: int, label: str = "Score"):
    """Render a labeled progress bar for scores 0-100."""
    if score >= 80:
        color = "#10B981"
    elif score >= 55:
        color = "#F59E0B"
    else:
        color = "#EF4444"

    st.markdown(f"""
    <div class="riq-score-wrap">
      <div style="display:flex;justify-content:space-between;margin-bottom:6px">
        <span style="font-size:0.8rem;color:#94A3B8">{label}</span>
        <span style="font-size:0.875rem;font-weight:700;color:{color}">{score}/100</span>
      </div>
      <div class="riq-score-bar-bg">
        <div class="riq-score-bar-fill" style="width:{score}%;background:{color}"></div>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ── Quick stat pills (2-up) ────────────────────────────────────────────────────

def stat_pills(stats: list):
    """
    stats: list of (value, label) tuples.
    Renders them in grouped pill rows of 2.
    """
    html = '<div class="riq-stat-row">'
    for i, (val, lbl) in enumerate(stats):
        html += f"""
        <div class="riq-stat-pill">
          <span class="riq-stat-pill-val">{val}</span>
          <span class="riq-stat-pill-lbl">{lbl}</span>
        </div>"""
        if (i + 1) % 2 == 0 and i < len(stats) - 1:
            html += '</div><div class="riq-stat-row">'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


# ── Empty state ────────────────────────────────────────────────────────────────

def empty_state(message: str = "No data available yet."):
    st.markdown(f"""
    <div class="riq-empty">
      <div class="riq-empty-icon">
        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#334155" stroke-width="1.5">
          <rect x="3" y="3" width="18" height="18" rx="2"/><path d="M9 9h6M9 13h4"/>
        </svg>
      </div>
      <div class="riq-empty-msg">{message}</div>
    </div>
    """, unsafe_allow_html=True)


# ── Chart download ─────────────────────────────────────────────────────────────

def download_button_for_plotly(fig, filename: str = "chart.png"):
    """Offer a PNG download for a Plotly figure."""
    try:
        img_bytes = fig.to_image(format="png")
        st.download_button(
            label="Download chart",
            data=img_bytes,
            file_name=filename,
            mime="image/png",
        )
    except Exception:
        pass  # kaleido not installed — silently skip


# ── Plotly theme ───────────────────────────────────────────────────────────────

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#94A3B8", size=12),
    title_font=dict(family="Inter, sans-serif", color="#F8FAFC", size=14, weight=600),
    margin=dict(l=16, r=16, t=40, b=16),
    xaxis=dict(
        gridcolor="#1E293B",
        linecolor="#334155",
        tickfont=dict(size=11, color="#64748B"),
        showgrid=True,
    ),
    yaxis=dict(
        gridcolor="#1E293B",
        linecolor="#334155",
        tickfont=dict(size=11, color="#64748B"),
        showgrid=True,
    ),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        bordercolor="#334155",
        font=dict(color="#94A3B8", size=11),
    ),
    colorway=["#2563EB", "#06B6D4", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6", "#EC4899"],
)


def apply_plotly_theme(fig):
    """Apply the RejectIQ dark theme to any Plotly figure."""
    fig.update_layout(**PLOTLY_LAYOUT)
    return fig