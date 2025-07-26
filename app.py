
import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# Password logic
MONTHLY_PASSWORD = {
    "july2025": "July2025VIP"
}
user_password = st.text_input("Enter your monthly password:", type="password")
current_key = datetime.now().strftime("%B%Y").lower()
valid_password = MONTHLY_PASSWORD.get(current_key, "invalid")

if user_password != valid_password:
    st.warning("Access Denied. Please enter a valid password.")
    st.stop()
else:
    st.success("Access Granted.")

# Theme switch
mode = st.sidebar.radio("Theme Mode", ["Dark", "Light"])
if mode == "Light":
    st.markdown("""
        <style>
        body, html, .main, .block-container {
            background-color: #ffffff;
            color: #000000;
        }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        body, html, .main, .block-container {
            background-color: #0e1117;
            color: #ffffff;
        }
        </style>
    """, unsafe_allow_html=True)

# Logo and Title
st.markdown("""
<div style='text-align: center;'>
    <img src='https://raw.githubusercontent.com/NavidalTrading/real-crypto-updates-dashboard/main/logo.png' width='180'/>
</div>
<h1 style='text-align: center;'>📈 Real Crypto Updates Dashboard</h1>
<h4 style='text-align: center;'>Master Trading with Real Updates</h4>
""", unsafe_allow_html=True)

# Crypto data table
symbols = ["BTC", "ETH", "XRP", "ADA", "QNT", "CRV", "FIL", "EGLD"]
data = []

for sym in symbols:
    price = "N/A"
    pair_used = ""
    for suffix in ["USDC", "USDT"]:
        pair = f"{sym}{suffix}"
        try:
            r = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={pair}")
            if r.status_code == 200:
                price = float(r.json()["price"])
                pair_used = pair
                break
        except:
            continue
    display_pair = pair_used if pair_used else f"{sym}/N/A"
    data.append([display_pair, "Coming Soon", price, "-5%", "+10%"])

df = pd.DataFrame(data, columns=["Pair", "Signal", "Price", "Stop Loss", "Take Profit"])
st.dataframe(df, use_container_width=True)

# Auto-Trader
st.markdown("""
<hr>
<h2 style='text-align: center;'>🚧 Auto-Trader Bot</h2>
<div style='text-align: center;'>
<p>Launching soon with 100x leverage. Sign up for early access!</p>
<a href='#'><button style='padding: 10px 20px; font-size: 16px; border-radius: 8px; background: #00cc99; color: white;'>Subscribe to get early access!</button></a>
</div>
""", unsafe_allow_html=True)

# Pricing
st.markdown("""
<hr>
<div style='text-align: center;'>
<h3>Plans & Pricing</h3>
<p><strong>Basic:</strong> €19/month — Daily signals + dashboard access</p>
<a href='https://checkout.revolut.com/pay/a1b9167e-f3c2-41b5-85f6-b9db57fd6efc' target='_blank'>
    <button style='background-color:#4CAF50;color:white;padding:10px 20px;font-size:16px;border:none;border-radius:8px;margin:10px;'>Subscribe Basic</button>
</a>
<p><strong>Pro:</strong> €39/month — All altcoin signals + early updates</p>
<a href='https://checkout.revolut.com/pay/b83947eb-463d-46b2-91af-6e1a44115e0a' target='_blank'>
    <button style='background-color:#4CAF50;color:white;padding:10px 20px;font-size:16px;border:none;border-radius:8px;margin:10px;'>Subscribe Pro</button>
</a>
<p><strong>Auto-Trader Bot:</strong> Coming Soon</p>
</div>
""", unsafe_allow_html=True)

# Chatbot Embed
st.markdown("""
<hr>
<iframe src='https://6884df02500f79a19fb33759--cryptodanielwidget.netlify.app/' width='100%' height='500px' style='border:none;'></iframe>
""", unsafe_allow_html=True)
