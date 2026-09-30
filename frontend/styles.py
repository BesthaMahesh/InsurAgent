"""
Enterprise CSS Stylesheet for InsurAgent UI.
Provides a clean, professional, minimal, and trustworthy corporate SaaS design.
"""

ENTERPRISE_CSS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">

<style>
    /* ---------- Base Resets & Enterprise Typography ---------- */
    *, *::before, *::after {
        box-sizing: border-box;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    code, pre, .mono-text, [data-testid="stMarkdown"] code {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.9em;
    }

    .stApp {
        background: #f8fafc;
        color: #0f172a;
    }

    .block-container {
        max-width: 1480px;
        padding-top: 1.0rem !important;
        padding-bottom: 2.5rem !important;
        padding-left: 2.0rem !important;
        padding-right: 2.0rem !important;
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
        margin-bottom: 20px;
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
        border-radius: 9px;
        background: linear-gradient(135deg, #091524 0%, #0f2744 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: #38bdf8;
        font-size: 20px;
        font-weight: 800;
        border: 1px solid #1e3a5f;
        box-shadow: 0 2px 6px rgba(15, 39, 68, 0.15);
    }

    .header-title-text {
        font-size: 17px;
        font-weight: 800;
        color: #0f172a;
        letter-spacing: -0.4px;
        line-height: 1.15;
    }

    .header-subtitle-text {
        font-size: 11.5px;
        font-weight: 600;
        color: #0284c7;
        margin-top: 1px;
    }

    .header-right-meta {
        display: flex;
        align-items: center;
        gap: 8px;
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
        padding: 7px 12px !important;
        border-radius: 8px !important;
        margin-bottom: 2px !important;
        transition: all 0.15s ease;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    section[data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(255, 255, 255, 0.08) !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-checked="true"] {
        background: #0284c7 !important;
        font-weight: 700 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.2);
    }

    .sidebar-section-header {
        font-size: 10px;
        font-weight: 800;
        color: #64748b !important;
        letter-spacing: 0.8px;
        text-transform: uppercase;
        margin-top: 14px;
        margin-bottom: 6px;
        padding-left: 4px;
    }

    .sidebar-divider {
        height: 1px;
        background: #1e2e42;
        margin: 12px 0;
    }

    .sidebar-account-box {
        background: #0d1e34;
        border: 1px solid #1e3a5f;
        border-radius: 8px;
        padding: 10px 12px;
        margin-top: 12px;
        margin-bottom: 10px;
    }

    /* ---------- Page Headers ---------- */
    .page-title {
        font-size: 22px;
        font-weight: 800;
        color: #0f172a;
        letter-spacing: -0.4px;
        margin-bottom: 3px;
        line-height: 1.2;
    }

    .page-subtitle {
        font-size: 13px;
        color: #64748b;
        margin-bottom: 18px;
    }

    /* ---------- Executive KPI Cards ---------- */
    .kpi-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 16px 18px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100%;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }

    .kpi-card:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05);
    }

    .kpi-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 4px;
    }

    .kpi-title {
        font-size: 11.5px;
        font-weight: 700;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .kpi-value {
        font-size: 26px;
        font-weight: 800;
        color: #0f172a;
        margin: 6px 0 4px 0;
        letter-spacing: -0.6px;
        line-height: 1.1;
    }

    .kpi-footer {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-top: 6px;
        font-size: 11.5px;
    }

    /* ---------- Status Badges & Pills ---------- */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.1px;
        white-space: nowrap;
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

    /* ---------- Card / Container Styling ---------- */
    .enterprise-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 18px 20px;
        margin-bottom: 16px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03);
    }

    .card-title {
        font-size: 14.5px;
        font-weight: 750;
        color: #0f172a;
        margin-bottom: 2px;
    }

    .card-subtitle {
        font-size: 12px;
        color: #64748b;
        margin-bottom: 12px;
    }

    /* ---------- Document Upload Dropzone & File List ---------- */
    .upload-box-wrapper {
        background: #ffffff;
        border: 2px dashed #cbd5e1;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        transition: border-color 0.2s ease;
    }

    .upload-box-wrapper:hover {
        border-color: #0284c7;
    }

    .file-chip {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 8px 12px;
        margin-top: 6px;
        font-size: 12px;
    }

    /* ---------- Chat Bubbles ---------- */
    .chat-msg-user {
        background: #0f2744;
        color: #ffffff;
        padding: 12px 16px;
        border-radius: 12px 12px 2px 12px;
        font-size: 13.5px;
        margin-bottom: 12px;
        max-width: 80%;
        margin-left: auto;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }

    .chat-msg-ai {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px 12px 12px 2px;
        padding: 14px 18px;
        font-size: 13.5px;
        margin-bottom: 12px;
        max-width: 90%;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        line-height: 1.6;
    }

    .source-citation-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-left: 3px solid #0284c7;
        border-radius: 6px;
        padding: 8px 12px;
        margin-top: 8px;
        font-size: 11.5px;
    }

    /* ---------- Clean Streamlit Overrides ---------- */
    #MainMenu, footer {
        visibility: hidden !important;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    button[data-testid="stSidebarCollapseButton"], 
    div[data-testid="collapsedControl"] {
        visibility: visible !important;
        display: block !important;
        z-index: 999999 !important;
    }

    div.stButton > button {
        border-radius: 8px;
        font-weight: 600;
        font-size: 13px;
        padding: 6px 14px;
        transition: all 0.15s ease;
    }

    div[data-testid="stExpander"] {
        border: 1px solid #e2e8f0 !important;
        border-radius: 10px !important;
        background: #ffffff !important;
        box-shadow: none !important;
        margin-top: 8px !important;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid #e2e8f0;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 6px 6px 0 0;
        padding: 8px 16px;
        font-weight: 600;
        font-size: 13px;
        color: #64748b;
    }

    .stTabs [aria-selected="true"] {
        background-color: transparent !important;
        color: #0284c7 !important;
        border-bottom: 2px solid #0284c7 !important;
    }
</style>
"""
