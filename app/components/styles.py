import streamlit as st

def apply_custom_css(theme="dark"):
    """
    Applies premium UI with support for Dark and Light themes, 
    ensuring text visibility in both modes.
    """
    
    # Theme variables
    if theme == "dark":
        bg_color = "radial-gradient(circle at top right, #1a1c29, #0E1117)"
        text_color = "#F0F4F8"
        card_bg = "rgba(30, 35, 47, 0.6)"
        card_border = "rgba(255, 255, 255, 0.05)"
        sidebar_bg = "#0E1117"
        accent_color = "#00C4CC" 
        table_bg = "rgba(255, 255, 255, 0.05)"
        table_border = "rgba(255, 255, 255, 0.1)"
        user_msg_bg = "rgba(255, 255, 255, 0.08)"
    else:
        bg_color = "#F8F9FA"
        text_color = "#1A202C" # Dark text for light mode
        card_bg = "#FFFFFF"
        card_border = "rgba(0, 0, 0, 0.1)"
        sidebar_bg = "#FFFFFF"
        accent_color = "#3182CE" 
        table_bg = "#FFFFFF"
        table_border = "#E2E8F0"
        user_msg_bg = "#EDF2F7" # Light grey for user message

    custom_css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    /* Main Background */
    .stApp {{
        background: {bg_color};
        color: {text_color} !important;
        transition: background 0.3s, color 0.3s;
    }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
        border-right: 1px solid {card_border};
    }}
    
    /* Force all text in sidebar to match theme */
    [data-testid="stSidebar"] * {{
        color: {text_color} !important;
    }}

    /* Typography */
    h1, h2, h3, h4, h5, h6 {{
        color: {text_color} !important;
        font-weight: 700 !important;
    }}

    p, li, span, div {{
        color: {text_color} !important;
    }}

    .app-caption {{
        color: {'#A0AABF' if theme == 'dark' else '#718096'} !important;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-weight: 300;
    }}

    /* Chat Messages */
    [data-testid="stChatMessage"] {{
        background-color: transparent !important;
    }}
    
    /* User message background */
    [data-testid="stChatMessage"]:nth-child(odd) {{
        background-color: {user_msg_bg} !important;
        border-radius: 10px;
        padding: 15px;
    }}

    /* Tables (Fixes the invisible table issue) */
    table {{
        background-color: {table_bg} !important;
        border-collapse: collapse;
        width: 100%;
        border-radius: 8px;
        overflow: hidden;
    }}
    
    th, td {{
        border: 1px solid {table_border} !important;
        padding: 10px;
        color: {text_color} !important;
    }}
    
    th {{
        background-color: {'rgba(255,255,255,0.1)' if theme == 'dark' else '#E2E8F0'} !important;
        font-weight: 600;
    }}

    /* Zomato-Style Source Cards */
    .z-card {{
        background: {card_bg};
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 15px;
        border: 1px solid {card_border};
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }}

    .z-card h4, .z-card p {{
        color: {text_color} !important;
    }}

    /* Badges */
    .badge-high {{
        background-color: rgba(0, 255, 136, 0.15);
        color: {'#00FF88' if theme == 'dark' else '#008A4E'} !important;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }}
    
    .badge-low {{
        background-color: rgba(255, 75, 75, 0.15);
        color: {'#FF4B4B' if theme == 'dark' else '#C53030'} !important;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }}

    /* Chat Input */
    .stChatInput {{
        border-radius: 12px;
        border: 1px solid {accent_color};
        background-color: {card_bg};
    }}
    
    .stChatInput textarea {{
        color: {text_color} !important;
    }}

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 20px;
    }}
    .stTabs [aria-selected="true"] {{
        color: {accent_color} !important;
        border-bottom-color: {accent_color} !important;
    }}
    
    /* Code blocks */
    code {{
        color: {accent_color} !important;
        background-color: {table_bg} !important;
        padding: 2px 6px;
        border-radius: 4px;
    }}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)