
import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import streamlit.components.v1 as components

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
    st.title("🔐 Enter Password to Access Dashboard")
    uploaded_file = st.file_uploader("Upload Payment Proof", type=["png", "jpg", "jpeg", "pdf"])

    if uploaded_file:
        plan = extract_plan_from_filename(uploaded_file.name)
        current_month = datetime.now().strftime("%B").lower()
        expected_password = f"realcrypto-{current_month}"
        if plan:
            st.success(f"✅ Crypto Daniel verified your **{plan} Plan** payment proof.")
            st.session_state["authenticated"] = True
            st.session_state["auth_expiry"] = datetime.now() + timedelta(days=30)
            st.info(f"Your password for **{current_month.capitalize()}** is: `{expected_password}`\\n\\nAccess valid for 30 days.")
        else:
            st.warning("❌ Unable to verify payment.")

    password = st.text_input("Password", type="password")
    if st.button("Submit"):
        expected_password = f"realcrypto-{datetime.now().strftime('%B').lower()}"
        if password == expected_password:
            st.session_state["authenticated"] = True
            st.session_state["auth_expiry"] = datetime.now() + timedelta(days=30)
            st.success("✅ Access granted. Welcome!")
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
if not st.session_state.get("authenticated", False):
    password_gate()
    st.stop()  # Only stop if password not yet provided


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
# FAQ section
st.markdown("---")
st.markdown("### ❓ Frequently Asked Questions")

with st.expander("How do I get access to the dashboard?"):
    st.markdown("After choosing a plan and completing payment via Revolut, upload your **payment proof** directly in the chat to Crypto Daniel.")

with st.expander("How long is the dashboard password valid?"):
    st.markdown("Once your payment is confirmed, you'll receive a password for the current month. The password is **valid for 30 days** and changes monthly.")
# Chatbot UI
st.markdown("""
<!-- Chat Container -->
<div class="chat-container" style="position: fixed; bottom: 20px; right: 20px; z-index: 999; background: white; border-radius: 10px; padding: 10px; width: 300px; box-shadow: 0 0 10px rgba(0,0,0,0.3);">
  <div style="font-weight: bold; margin-bottom: 5px;">Crypto Daniel</div>
  <div id="chat-box" style="height: 180px; overflow-y: auto; background: #f9f9f9; padding: 5px; margin-bottom: 5px;"></div>
  <input type="text" id="user-input" placeholder="Ask me..." style="width: 100%; padding: 6px;"/>
  <button id="send-btn" style="width: 100%; margin-top: 5px;">Send</button>
</div>

<script>
const userLang = navigator.language || navigator.userLanguage;
const isRomanian = userLang.startsWith("ro");
let currentLang = isRomanian ? "ro" : "en";
let voiceEnabled = false;
const synth = window.speechSynthesis;

function getResponse(message) {
  const lower = message.toLowerCase();
  if (lower.includes("price")) {
    return currentLang === "ro" ? "Planul Basic este 19€/lună, iar Pro este 39€/lună." : "The Basic Plan is €19/month and the Pro Plan is €39/month.";
  } else if (lower.includes("signal")) {
    return currentLang === "ro" ? "Semnalele sunt publicate la 20:00 EET." : "Signals are posted at 20:00 EET.";
  } else if (lower.includes("dashboard")) {
    return currentLang === "ro" ? "Poți accesa dashboard-ul după ce introduci parola lunii." : "You can access the dashboard after entering the current month's password.";
  } else if (lower.includes("pay") || lower.includes("buy")) {
    return currentLang === "ro"
      ? "<a href='https://checkout.revolut.com/pay/a1b9167e-f3c2-41b5-85f6-b9db57fd6efc' target='_blank'>Plătește Basic</a><br><a href='https://checkout.revolut.com/pay/b83947eb-463d-46b2-91af-6e1a44115e0a' target='_blank'>Plătește Pro</a>"
      : "<a href='https://checkout.revolut.com/pay/a1b9167e-f3c2-41b5-85f6-b9db57fd6efc' target='_blank'>Pay Basic</a><br><a href='https://checkout.revolut.com/pay/b83947eb-463d-46b2-91af-6e1a44115e0a' target='_blank'>Pay Pro</a>";
  } else {
    return currentLang === "ro" ? "Încă învăț. Reformulează?" : "Still learning. Can you rephrase?";
  }
}

function speak(text) {
  const utter = new SpeechSynthesisUtterance(text);
  utter.lang = currentLang === "ro" ? "ro-RO" : "en-US";
  utter.voice = synth.getVoices().find(v => v.name.includes("Male") || v.name.includes("Bărbat")) || synth.getVoices()[0];
  synth.speak(utter);
}

document.addEventListener("DOMContentLoaded", () => {
  const sendBtn = document.getElementById("send-btn");
  const input = document.getElementById("user-input");
  const chatbox = document.getElementById("chat-box");

  sendBtn.addEventListener("click", () => {
    const message = input.value.trim();
    if (message) {
      chatbox.innerHTML += "<div class='user'><b>You:</b> " + message + "</div>";
      const reply = getResponse(message);
      chatbox.innerHTML += "<div class='bot'><b>Bot:</b> " + reply + "</div>";
      input.value = "";
      chatbox.scrollTop = chatbox.scrollHeight;
      if (voiceEnabled) speak(reply);
    }
  });
});
</script>
""", unsafe_allow_html=True)




