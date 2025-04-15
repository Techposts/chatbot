# style.py
import streamlit as st

def apply_custom_styling():
    """Apply Anaptyss branding and custom styling to the Streamlit app"""
    
    # Anaptyss brand colors (you can adjust these to match your brand)
    primary_color = "#2563eb"    # Blue
    secondary_color = "#4ade80"  # Green
    bg_color = "#ffffff"         # White
    text_color = "#1e293b"       # Dark slate
    
    # Custom CSS with Anaptyss branding
    st.markdown(f"""
    <style>
        /* General styling */
        .stApp {{
            background-color: {bg_color};
            color: {text_color};
        }}
        
        /* Header styling */
        .stApp header {{
            background-color: {primary_color};
        }}
        
        /* Buttons */
        .stButton > button {{
            background-color: {primary_color};
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 0.25rem;
            transition: background-color 0.3s;
        }}
        .stButton > button:hover {{
            background-color: {secondary_color};
        }}
        
        /* Chat messages */
        .chat-message {{
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
        }}
        .chat-message.user {{
            background-color: #e2e8f0;
            border-bottom-right-radius: 0;
        }}
        .chat-message.assistant {{
            background-color: #eff6ff;
            border: 1px solid #dbeafe;
            border-bottom-left-radius: 0;
        }}
        
        /* Lead form styling */
        .lead-form {{
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 0.5rem;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }}
        
        /* Logo styling */
        .logo-container {{
            padding: 1rem;
            display: flex;
            justify-content: center;
        }}
        .logo-container img {{
            max-height: 50px;
        }}
        
        /* Footer styling */
        footer {{
            border-top: 1px solid #e2e8f0;
            padding-top: 1rem;
            text-align: center;
            font-size: 0.8rem;
            color: #64748b;
        }}
    </style>
    """, unsafe_allow_html=True)
    
    # Add logo to sidebar
    with st.sidebar:
        st.markdown(
            """
            <div class="logo-container">
                <img src="https://yourdomain.com/path/to/your/logo.png" alt="Anaptyss Logo">
            </div>
            """, 
            unsafe_allow_html=True
        )

def create_custom_chat_ui(message, is_user):
    """Create custom chat UI for a message"""
    if is_user:
        return f"""
        <div class="chat-message user">
            <div class="avatar">
                <span style="font-weight: bold;">You</span>
            </div>
            <div class="content">
                {message}
            </div>
        </div>
        """
    else:
        return f"""
        <div class="chat-message assistant">
            <div class="avatar">
                <span style="font-weight: bold;">Anaptyss AI</span>
            </div>
            <div class="content">
                {message}
            </div>
        </div>
        """
