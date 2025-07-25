# Streamlit Dashboard for Real Crypto Updates (With Pricing Footer)
import streamlit as st
import pandas as pd
import requests

# --- Page Config ---
st.set_page_config(page_title="Real Crypto Updates", layout="wide")

# --- Smart Theme Styling ---
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

# --- Sidebar Branding ---
st.sidebar.title("Real Crypto Updates")

# --- Display Centered Logo ---
st.markdown("""
    <div style='text-align: center;'>
        <img src='https://raw.githubusercontent.com/NavidalTrading/real-crypto-updates-dashboard/main/logo.png' width='200'/>
    </div>
""", unsafe_allow_html=True)

# --- Title and Slogan ---
st.markdown("<h1 style='text-align: center;'>📈 Real Crypto Updates Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; font-weight: bold;'>Master Trading with Real Updates.</h4>", unsafe_allow_html=True)

# --- Live Price Data with USDC/USDT Fallback ---
symbols = ["BTC", "ETH", "XRP", "ADA", "QNT", "CRV", "FIL", "EGLD"]
data = []

for coin in symbols:
    symbol_usdc = f"{coin}USDC"
    symbol_usdt = f"{coin}USDT"
    price = "N/A"
    
    for symbol in [symbol_usdc, symbol_usdt]:
        try:
            response = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}")
            if response.status_code == 200:
                price = float(response.json()['price'])
                break
        except:
            continue

    signal = "Coming Soon"
    stop_loss = "-5%"
    take_profit = "+10%"
    pair_display = f"{coin}/USDC" if price != "N/A" else f"{coin}/USDT"
    data.append([pair_display, signal, price, stop_loss, take_profit])

# --- Display Table ---
df = pd.DataFrame(data, columns=["Pair", "Signal", "Price", "Stop Loss", "Take Profit"])
st.dataframe(df, use_container_width=True)

# --- Coming Soon CTA Section ---
st.markdown("---")
st.markdown("<h2 style='text-align: center;'>🚧 Auto-Trader Bot</h2>", unsafe_allow_html=True)

cta_html = '''
    <div style="text-align: center;">
        <p>Our 100x leverage auto-trading bot is launching soon.</p>
        <a href="#" style="text-decoration: none;">
            <button style="padding: 0.75em 1.5em; font-size: 16px; background-color: #00cc99; color: white; border: none; border-radius: 8px; cursor: pointer;">
                Subscribe to get early access!
            </button>
        </a>
    </div>
'''
st.markdown(cta_html, unsafe_allow_html=True)

# --- Pricing Footer ---
st.markdown("---")
st.markdown("### 💼 Plans & Pricing")
st.markdown("""
- **Basic:** €19/month — Daily signals + dashboard access  
- **Pro:** €39/month — All altcoin signals + early updates  
- **Auto-Trader Bot:** Coming Soon  
""")
st.markdown("<div style='text-align: center;'><a href='#'><button style='background-color:#4CAF50; color:white; padding:10px 20px; font-size:16px; border:none; border-radius:8px;'>Upgrade Now</button></a></div>", unsafe_allow_html=True)


