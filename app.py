
import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import streamlit.components.v1 as components
import numpy as np
from binance.client import Client

# ⛔️ Replace these with your real Binance API credentials!
binance_api_key = "qyPrbdvwonnPJwKWQFddE5gzsqVHeMN5pReoXheugYJNgyoWEWpOk6jQccx9vxWR"
binance_api_secret = "XXqpVtqzK0H5yULxBo73TdG8Do74SsvxGzzo0VYp7MBrQHNq96MIZOUueL9g2jMR"

client = Client(api_key=binance_api_key, api_secret=binance_api_secret)


def fetch_ohlcv_binance(symbol="BTCUSDT", interval="1h", limit=100):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    data = requests.get(url).json()
    df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
    ])
    df["close"] = df["close"].astype(float)
    df["high"] = df["high"].astype(float)
    df["low"] = df["low"].astype(float)
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df

def ichimoku_signal(df):
    high_9 = df["high"].rolling(window=9).max()
    low_9 = df["low"].rolling(window=9).min()
    tenkan_sen = (high_9 + low_9) / 2

    high_26 = df["high"].rolling(window=26).max()
    low_26 = df["low"].rolling(window=26).min()
    kijun_sen = (high_26 + low_26) / 2

    chikou_span = df["close"].shift(-26)

    if (
        df["close"].iloc[-1] > kijun_sen.iloc[-1]
        and tenkan_sen.iloc[-1] > kijun_sen.iloc[-1]
        and chikou_span.iloc[-27] < df["close"].iloc[-27]
    ):
        return "BUY"
    elif (
        df["close"].iloc[-1] < kijun_sen.iloc[-1]
        and tenkan_sen.iloc[-1] < kijun_sen.iloc[-1]
        and chikou_span.iloc[-27] > df["close"].iloc[-27]
    ):
        return "SELL"
    else:
        return "HOLD"

def pivot_levels(df):
    last_candle = df.iloc[-2]
    high = last_candle["high"]
    low = last_candle["low"]
    close = last_candle["close"]

    pivot = (high + low + close) / 3
    r1 = (2 * pivot) - low
    s1 = (2 * pivot) - high
    r2 = pivot + (high - low)
    s2 = pivot - (high - low)

    return {
        "pivot": round(pivot, 2),
        "r1": round(r1, 2),
        "s1": round(s1, 2),
        "r2": round(r2, 2),
        "s2": round(s2, 2)
    }

def pivot_play_signal(df):
    levels = pivot_levels(df)
    current_close = df["close"].iloc[-1]
    if current_close > levels["r1"]:
        return "BUY"
    elif current_close < levels["s1"]:
        return "SELL"
    return "HOLD"

def fetch_klines(symbol, interval='1h', limit=150):
    url = f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}'
    try:
        response = requests.get(url)
        data = response.json()
        df = pd.DataFrame(data, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base_volume', 'taker_buy_quote_volume', 'ignore'
        ])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        df = df[['open', 'high', 'low', 'close']].astype(float)
        return df
    except:
        return None

def ichimoku_cloud(df):
    high_9 = df['high'].rolling(window=9).max()
    low_9 = df['low'].rolling(window=9).min()
    tenkan_sen = (high_9 + low_9) / 2

    high_26 = df['high'].rolling(window=26).max()
    low_26 = df['low'].rolling(window=26).min()
    kijun_sen = (high_26 + low_26) / 2

    senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(26)

    high_52 = df['high'].rolling(window=52).max()
    low_52 = df['low'].rolling(window=52).min()
    senkou_span_b = ((high_52 + low_52) / 2).shift(26)

    return tenkan_sen, kijun_sen, senkou_span_a, senkou_span_b

def generate_signals(symbols):
   def fetch_klines(symbol, interval='1h', limit=150):
    url = f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}'
    try:
        response = requests.get(url)
        data = response.json()
        df = pd.DataFrame(data, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base_volume', 'taker_buy_quote_volume', 'ignore'
        ])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        df = df[['open', 'high', 'low', 'close']].astype(float)
        return df
    except:
        return None

def ichimoku_cloud(df):
    high_9 = df['high'].rolling(window=9).max()
    low_9 = df['low'].rolling(window=9).min()
    tenkan_sen = (high_9 + low_9) / 2

    high_26 = df['high'].rolling(window=26).max()
    low_26 = df['low'].rolling(window=26).min()
    kijun_sen = (high_26 + low_26) / 2

    senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(26)

    high_52 = df['high'].rolling(window=52).max()
    low_52 = df['low'].rolling(window=52).min()
    senkou_span_b = ((high_52 + low_52) / 2).shift(26)

    return tenkan_sen, kijun_sen, senkou_span_a, senkou_span_b

def generate_signals(symbols):
    results = []
    for symbol in symbols:
        pair = symbol + "USDT"
        try:
            klines = client.get_klines(symbol=pair, interval=KLINE_INTERVAL_1HOUR, limit=52)
            closes = [float(entry[4]) for entry in klines]
            highs = [float(entry[2]) for entry in klines]
            lows = [float(entry[3]) for entry in klines]

            df = pd.DataFrame({
                "Close": closes,
                "High": highs,
                "Low": lows
            })

            signal = get_signal(df)
            entry_price = closes[-1]
            sl = round(entry_price * 0.95, 4)
            tp = round(entry_price * 1.10, 4)
            leverage = "x10"

            results.append([
                symbol.replace("USDT", "/USDT"),
                entry_price,
                f"{tp} / {sl}",
                leverage,
                signal
            ])
        except Exception as e:
            results.append([
                symbol.replace("USDT", "/USDT"),
                "-",
                "-",
                "-",
                f"Error: {str(e)}"
            ])

    return pd.DataFrame(results, columns=["Symbol", "Entry Price", "TP / SL", "Leverage", "Signal"])





# Initialize login state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "auth_expiry" not in st.session_state:
    st.session_state["auth_expiry"] = None

def extract_plan_from_filename(filename):
    fname = filename.lower()
    if "basic" in fname:
        return "Basic"
    elif "pro" in fname:
        return "Pro"
    return None
 
def password_gate():
    st.title("🔒 Enter Password to Access Dashboard")

    # Upload file
    uploaded_file = st.file_uploader("Upload Payment Proof", type=["png", "jpg", "jpeg", "pdf"], key="payment_upload")

    if uploaded_file:
        filename = uploaded_file.name.lower()
        current_month = datetime.now().strftime("%B").lower()

        plan_type = ""

        if "pro" in filename:
            plan_type = "Pro Plan"
            password = f"realcrypto-pro-{current_month}"
        elif "basic" in filename:
            plan_type = "Basic Plan"
            password = f"realcrypto-basic-{current_month}"
        else:
            st.error("❌ Could not determine plan from filename. Use 'basic' or 'pro' in the name.")
            return

        # Store valid password and plan type in session
        st.session_state.valid_password = password
        st.session_state.user_plan = plan_type

        st.success(f"✅ Crypto Daniel verified your **{plan_type}** payment proof.")
        st.info(f"Your password for **{current_month.capitalize()}** is: `{password}` Access valid for 30 days.")

    # Show password input only if access not yet granted
    if "access_granted" not in st.session_state:
        st.session_state.access_granted = False

    if not st.session_state.access_granted:
        password = st.text_input("Password", type="password")
        if st.button("Submit"):
            if password == st.session_state.get("valid_password", ""):
                st.session_state.access_granted = True
                st.success("✅ Access granted.")
                st.rerun()
            else:
                st.error("❌ Incorrect password.")

# Re-check validity
if st.session_state["authenticated"]:
    if st.session_state["auth_expiry"] and datetime.now() > st.session_state["auth_expiry"]:
        st.session_state["authenticated"] = False
        st.warning("⚠️ Your session expired. Please re-authenticate.")
        st.rerun()

# Enforce gate
if not st.session_state.get("access_granted", False):
    password_gate()
    st.stop()# Only stop if password not yet provided


# Theme switch
mode = st.sidebar.radio("Theme Mode", [ "Light"])
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
user_plan = st.session_state.get("user_plan", "Basic")

st.markdown(f"### 👤 You are on the **{user_plan} **")

if user_plan == "Pro":
    st.success("✅ You have access to **Pro** content including early signals, premium coins and full dashboard.")
    symbols = ["BTC", "ETH", "XRP", "ADA", "QNT", "CRV", "FIL", "EGLD"]
else:
    st.info("ℹ️ On the **Basic Plan**, you see standard coins.")
    symbols = ["XRP", "CRV", "FIL", "EGLD"]

# Example: Define your table here
basic_symbols = ["XRPUSDT", "CRVUSDT", "FILUSDT", "EGLDUSDT"]
pro_symbols = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "ADAUSDT", "QNTUSDT", "CRVUSDT", "FILUSDT", "EGLDUSDT"]

# Display signals with new columns
if st.session_state.get("user_plan") == "Basic Plan":
    st.subheader("📊 Real-Time Crypto Signals (Basic Plan)")
    signal_df = generate_signals(basic_symbols)
    signal_df.index = signal_df.index + 1
    st.dataframe(signal_df, use_container_width=True)

elif st.session_state.get("user_plan") == "Pro Plan":
    st.subheader("📊 Real-Time Crypto Signals (Pro Plan)")
    signal_df = generate_signals(pro_symbols)
    signal_df.index = signal_df.index + 1
    st.dataframe(signal_df, use_container_width=True)

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
# FAQ section
st.markdown("---")
st.markdown("### ❓ Frequently Asked Questions")

with st.expander("How do I get access to the dashboard?"):
    st.markdown("After choosing a plan and completing payment via Revolut, upload your **payment proof** directly on Dashboard start page in the upload section.")

with st.expander("How long is the dashboard password valid?"):
    st.markdown("Once your payment is confirmed, you'll receive a password for the current month. The password is **valid for 30 days** and changes monthly.")

with st.expander("When are signals updated?"):
    st.markdown("Signals are updated daily at 20:00 EET (Eastern European Time).")

with st.expander("How do I access the dashboard?"):
    st.markdown("The link can be found on our website at View Live Dashbord button located above the Plans&Pricing Section.")

with st.expander("What coins are included?"):
   st.markdown ("Major altcoins: XRP, ADA, QNT, CRV, FIL, EGLD, and more.")

# Chatbot UI

# Chatbot HTML container
st.markdown("""
<!-- Crypto Daniel AI Chatbot -->
<div class="chat-container" style="position: fixed; bottom: 20px; right: 20px; z-index: 999; background: #fff; border-radius: 12px; padding: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.3); width: 300px;">
  <div class="chat-header" style="font-weight: bold; margin-bottom: 5px;">Crypto Daniel</div>
  <div id="chat-box" style="height: 180px; overflow-y: auto; margin-bottom: 5px;"></div>
  <div id="chat-form">
   <input type="text" id="user-input" placeholder="Ask me anything..." style="width: 100%; padding: 6px;" />
<button id="send-btn" style="width: 100%; margin-top: 5px;">Send</button>

  </div>
</div>

<button onclick="toggleVoice()" style="position: fixed; bottom: 20px; left: 20px; padding: 10px 16px; background: #444; color: #fff; border-radius: 8px; border: none; z-index: 1000;">🔊 Voice</button>
""", unsafe_allow_html=True)

st.markdown("""
<script>
  let voiceEnabled = false;
  let currentLang = navigator.language.startsWith("ro") ? "ro" : "en";

  function getResponse(message) {
    const m = message.toLowerCase();
    if (m.includes("price")) return currentLang === "ro" ? "Basic: 19€/lună, Pro: 39€/lună." : "Basic: €19/month, Pro: €39/month.";
    if (m.includes("signal")) return currentLang === "ro" ? "Semnalele vin la ora 20:00 EET." : "Signals are sent at 20:00 EET.";
    if (m.includes("pay")) return currentLang === "ro"
      ? "<a href='https://checkout.revolut.com/pay/a1b9167e-f3c2-41b5-85f6-b9db57fd6efc' target='_blank'>Plătește Basic</a><br><a href='https://checkout.revolut.com/pay/b83947eb-463d-46b2-91af-6e1a44115e0a' target='_blank'>Plătește Pro</a>"
      : "<a href='https://checkout.revolut.com/pay/a1b9167e-f3c2-41b5-85f6-b9db57fd6efc' target='_blank'>Pay Basic</a><br><a href='https://checkout.revolut.com/pay/b83947eb-463d-46b2-91af-6e1a44115e0a' target='_blank'>Pay Pro</a>";
    return currentLang === "ro" ? "Încă învăț. Poți reformula?" : "I'm still learning. Please rephrase.";
  }

  function speak(text) {
    const utter = new SpeechSynthesisUtterance(text);
    utter.lang = currentLang === "ro" ? "ro-RO" : "en-US";
    const voices = window.speechSynthesis.getVoices();
    utter.voice = voices.find(v => v.name.includes("Male")) || voices[0];
    window.speechSynthesis.speak(utter);
  }

  function toggleVoice() {
    voiceEnabled = !voiceEnabled;
    alert(voiceEnabled ? (currentLang === "ro" ? "Vocea activată" : "Voice enabled") : (currentLang === "ro" ? "Vocea dezactivată" : "Voice disabled"));
  }

  // ✅ Attach event handler after Streamlit loads UI
  const observer = new MutationObserver(() => {
    const input = document.getElementById("user-input");
    const chatbox = document.getElementById("chat-box");
    const sendBtn = document.getElementById("send-btn");

    if (input && chatbox && sendBtn && !sendBtn.dataset.bound) {
      sendBtn.dataset.bound = "true"; // Avoid rebinding
      sendBtn.addEventListener("click", () => {
        const msg = input.value.trim();
        if (!msg) return;
        chatbox.innerHTML += `<div><strong>You:</strong> ${msg}</div>`;
        const reply = getResponse(msg);
        chatbox.innerHTML += `<div><strong>Bot:</strong> ${reply}</div>`;
        input.value = "";
        chatbox.scrollTop = chatbox.scrollHeight;
        if (voiceEnabled) speak(reply);
      });
    }
  });

  observer.observe(document.body, { childList: true, subtree: true });
</script>

""", unsafe_allow_html=True)








