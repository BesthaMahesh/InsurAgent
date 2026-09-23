"""
Enterprise CSS Stylesheet for InsurAgent UI.
Provides a clean, professional, minimal, and trustworthy corporate SaaS design.
"""

ENTERPRISE_CSS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">

<style>
    /* ---------- Base Resets & Typography ---------- */
    * {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    code, pre, .mono-text {
        font-family: 'JetBrains Mono', monospace !important;
    }

    .stApp {
        background: #f8fafc;
        color: #0f172a;
    }

    .block-container {
        max-width: 1440px;
        padding-top: 1.0rem !important;
        padding-bottom: 2.5rem;
    }

    /* ---------- Top Header Bar ---------- */
    .top-header-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 12px 20px;
        margin-bottom: 16px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03);
    }

    .header-brand {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .header-logo-icon {
        width: 38px;
        height: 38px;
        border-radius: 10px;
        background: #0f2744;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #38bdf8;
        font-size: 20px;
        font-weight: 800;
        box-shadow: 0 2px 6px rgba(15, 39, 68, 0.2);
    }

    .header-title-text {
        font-size: 18px;
        font-weight: 800;
        color: #0f172a;
        letter-spacing: -0.4px;
        line-height: 1.1;
    }

    .header-subtitle-text {
        font-size: 11px;
        font-weight: 600;
        color: #0369a1;
        margin-top: 1px;
    }

    .header-right-meta {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* ---------- Sidebar Enterprise Styling ---------- */
    section[data-testid="stSidebar"] {
        background: #091524 !important;
        border-right: 1px solid #1e2e42;
    }

    section[data-testid="stSidebar"] * {
        color: #f1f5f9 !important;
    }

    section[data-testid="stSidebar"] .stRadio label {
        font-size: 13px !important;
        font-weight: 500 !important;
        padding: 6px 10px !important;
        border-radius: 6px !important;
        margin-bottom: 2px !important;
        transition: all 0.15s ease;
    }

    section[data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(255, 255, 255, 0.07);
    }

    section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-checked="true"] {
        background: #0284c7 !important;
        font-weight: 700 !important;
    }

    /* ---------- Page Headers ---------- */
    .page-title {
        font-size: 20px;
        font-weight: 800;
        color: #0f172a;
        letter-spacing: -0.3px;
        margin-bottom: 2px;
    }

    .page-subtitle {
        font-size: 12.5px;
        color: #64748b;
        margin-bottom: 16px;
    }

    /* ---------- Executive KPI Cards ---------- */
    .kpi-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 14px 16px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.02);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100%;
    }

    .kpi-title {
        font-size: 11px;
        font-weight: 700;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .kpi-value {
        font-size: 24px;
        font-weight: 800;
        color: #0f172a;
        margin: 6px 0 3px 0;
        letter-spacing: -0.5px;
    }

    .kpi-footer {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-top: 4px;
        font-size: 11px;
    }

    /* ---------- Status Pills & Badges ---------- */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 2.5px 8px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.1px;
    }

    .badge-green {
        background: #ecfdf5;
        color: #047857;
        border: 1px solid #a7f3d0;
    }

    .badge-blue {
        background: #eff6ff;
        color: #1d4ed8;
        border: 1px solid #bfdbfe;
    }

    .badge-navy {
        background: #f1f5f9;
        color: #0f2744;
        border: 1px solid #cbd5e1;
    }

    .badge-amber {
        background: #fffbeb;
        color: #b45309;
        border: 1px solid #fde68a;
    }

    .badge-red {
        background: #fef2f2;
        color: #b91c1c;
        border: 1px solid #fecaca;
    }

    .badge-purple {
        background: #faf5ff;
        color: #7e22ce;
        border: 1px solid #e9d5ff;
    }

    /* ---------- Search Box Container ---------- */
    .search-box-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 16px;
        box-shadow: 0 1px 4px rgba(15, 23, 42, 0.02);
    }

    /* ---------- Enterprise Reasoning Box ---------- */
    .reasoning-box {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #0284c7;
        border-radius: 8px;
        padding: 14px 16px;
        margin-top: 10px;
        color: #1e293b;
        font-size: 13px;
        line-height: 1.6;
    }

    /* ---------- Timeline Items ---------- */
    .timeline-node {
        display: flex;
        gap: 12px;
        padding: 10px 0;
        border-bottom: 1px solid #f1f5f9;
    }

    .timeline-step-badge {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        background: #0284c7;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 11px;
        font-weight: 800;
        flex-shrink: 0;
    }

    .timeline-content {
        flex: 1;
    }

    .timeline-title {
        font-size: 12.5px;
        font-weight: 700;
        color: #0f172a;
    }

    .timeline-desc {
        font-size: 11.5px;
        color: #64748b;
        margin-top: 1px;
    }

    /* ---------- Agent Execution Card ---------- */
    .agent-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 14px;
        margin-bottom: 10px;
    }

    .agent-card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 6px;
    }

    .agent-card-title {
        font-size: 13.5px;
        font-weight: 750;
        color: #0f172a;
    }

    /* ---------- Clean Streamlit Overrides ---------- */
    #MainMenu, footer, header {
        visibility: hidden !important;
    }

    div.stButton > button {
        border-radius: 8px;
        font-weight: 600;
        font-size: 13px;
        padding: 6px 14px;
    }

    div[data-testid="stExpander"] {
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
        background: #ffffff !important;
        box-shadow: none !important;
    }
</style>
"""
