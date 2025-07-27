
import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import streamlit.components.v1 as components

# Utility to get the current valid monthly password
def get_current_password():
    return f"RCU-{datetime.now().strftime('%B').upper()}-2025"

# Initialize login state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Display password field if not authenticated
if not st.session_state.authenticated:
    st.title("🔐 Enter Password to Access Dashboard")
    password = st.text_input("Password", type="password")
    if st.button("Submit"):
        if password == get_current_password():
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password.")
    st.stop()  # Stop here if not logged in

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
"""
# Chatbot and Voice Assistant (injected safely)
chatbot_widget = """
st.markdown("""
<!-- Crypto Daniel AI Chatbot -->
<div class="chat-container" style="position: fixed; bottom: 20px; right: 20px; z-index: 999; background: #fff; border-radius: 12px; padding: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.3); width: 300px;">
  <div class="chat-header" style="font-weight: bold; margin-bottom: 5px;"> Crypto Daniel</div>
  <div id="chat-box" style="height: 180px; overflow-y: auto; margin-bottom: 5px;"></div>
  <form id="chat-form">
    <input type="text" id="user-input" placeholder="Ask me anything..." style="width: 100%; padding: 8px;" required />
    <button type="submit" style="margin-top: 5px; width: 100%;">Send</button>
  </form>
</div>
""", unsafe_allow_html=True)
st.markdown("""
<button onclick="toggleVoice()" style="position: fixed; bottom: 20px; left: 20px; padding: 10px 16px; background: #444; color: #fff; border-radius: 8px; border: none; z-index: 1000;">Voice</button>
""", unsafe_allow_html=True)
st.markdown("""
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
      return currentLang === "ro" ? "Semnalele zilnice sunt disponibile în dashboard la ora 20:00 EET." : "Daily signals are available in the dashboard at 20:00 EET.";
    } else if (lower.includes("dashboard")) {
      return currentLang === "ro" ? "Accesează dashboard-ul după autentificare cu parola lunii curente." : "Access the dashboard after logging in with this month's password.";
    } else if (lower.includes("pay") || lower.includes("buy")) {
      return currentLang === "ro" ? "<a href='https://checkout.revolut.com/pay/a1b9167e-f3c2-41b5-85f6-b9db57fd6efc' target='_blank'>Click aici pentru a plăti Planul Basic</a><br><a href='https://checkout.revolut.com/pay/b83947eb-463d-46b2-91af-6e1a44115e0a' target='_blank'>Click aici pentru a plăti Planul Pro</a>" : "<a href='https://checkout.revolut.com/pay/a1b9167e-f3c2-41b5-85f6-b9db57fd6efc' target='_blank'>Click here to pay for Basic Plan</a><br><a href='https://checkout.revolut.com/pay/b83947eb-463d-46b2-91af-6e1a44115e0a' target='_blank'>Click here to pay for Pro Plan</a>";
    } else {
      return currentLang === "ro" ? "Încă învăț. Poți reformula întrebarea?" : "I'm still learning. Can you rephrase?";
    }
  }

  function speak(text) {
    const utter = new SpeechSynthesisUtterance(text);
    utter.lang = currentLang === "ro" ? "ro-RO" : "en-US";
    utter.voice = synth.getVoices().find(v => v.name.includes("Male") || v.name.includes("Bărbat")) || synth.getVoices()[0];
    synth.speak(utter);
  }

  function toggleVoice() {
    voiceEnabled = !voiceEnabled;
    const status = voiceEnabled ? (currentLang === "ro" ? "Vocea activată" : "Voice enabled") : (currentLang === "ro" ? "Vocea dezactivată" : "Voice disabled");
    alert(status);
  }

  document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("#chat-form");
    const input = document.querySelector("#user-input");
    const chatbox = document.querySelector("#chat-box");

    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const message = input.value.trim();
      if (message) {
        chatbox.innerHTML += `<div class='user'>${message}</div>`;
        const reply = getResponse(message);
        chatbox.innerHTML += `<div class='bot'>${reply}</div>`;
        input.value = "";
        chatbox.scrollTop = chatbox.scrollHeight;
        if (voiceEnabled) speak(reply);
      }
    });
  });
</script>
""", unsafe_allow_html=True)
