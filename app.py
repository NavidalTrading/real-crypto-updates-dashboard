
import streamlit as st
from datetime import datetime
import base64

# --- Config ---
st.set_page_config(page_title="Real Crypto Updates", layout="centered")

# --- Password Authentication ---
def get_current_password():
    # Password changes monthly based on current month
    now = datetime.now()
    return f"RCU-{now.strftime('%B').upper()}-2025"

def password_gate():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        password = st.text_input("Enter Password to Access Dashboard", type="password")
        if st.button("Submit"):
            if password == get_current_password():
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password.")

    return st.session_state.authenticated

# --- Main Dashboard Content ---
def render_dashboard():
    st.title("📊 Real Crypto Updates Dashboard")
    st.markdown("Welcome to your live signal board. All data is updated in real-time.")

    st.markdown("### Sample Signal Table")
    st.table({
        "Pair": ["BTC/USDT", "ETH/USDT", "ADA/USDT"],
        "Entry Price": ["29,800", "1,850", "0.60"],
        "Stop Loss": ["-5%", "-5%", "-5%"],
        "Take Profit": ["+10%", "+10%", "+10%"],
        "Leverage": ["10x", "10x", "20x"]
    })

    st.markdown("---")
    st.markdown("For questions, payments, or access issues, talk to **Crypto Daniel** below!")

# --- Inject Chatbot Widget ---
def inject_chatbot():
    chatbot_code = '''
    <iframe src="https://6884df02500f79a19fb33759--cryptodanielwidget.netlify.app" width="100%" height="500px" style="border:none;"></iframe>
    '''
    st.components.v1.html(chatbot_code, height=520)

# --- Run App ---
if password_gate():
    render_dashboard()
    inject_chatbot()
