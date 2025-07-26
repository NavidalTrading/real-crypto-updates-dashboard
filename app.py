
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

<!-- Custom AI Assistant Widget -->
    <script>
      window.chatbotConfig = {
        welcome: "Hi! I'm your Crypto Assistant 👋 Ask me about pricing, signals, or how to get started.",
        voiceEnabled: true
      };
    </script>
    <script src="https://realcryptobot-widget-host.com/widget.js" async></script>
    
    <!-- Temporary Mock AI Chat Widget -->
  
  <!-- Crypto Daniel AI Chatbot -->
 <!-- Crypto Daniel Chatbox -->
 <!-- Chat UI -->
  <div class="chat-container" style="position: fixed; bottom: 20px; right: 20px; z-index: 999; background: #fff; border-radius: 12px; padding: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.3); width: 300px;">
    <div class="chat-header" style="font-weight: bold; margin-bottom: 5px;">🤖 Crypto Daniel</div>
    <div id="chat-box" style="height: 180px; overflow-y: auto; margin-bottom: 5px;"></div>
    <form id="chat-form">
      <input type="text" id="user-input" placeholder="Ask me anything..." style="width: 100%; padding: 8px;" required />
      <button type="submit" style="margin-top: 5px; width: 100%;">Send</button>
    </form>
  </div>

  <!-- Voice and Logic Integration for Crypto Daniel Chatbot -->
<script>
  // Language Detection
  const userLang = navigator.language || navigator.userLanguage;
  const isRomanian = userLang.startsWith("ro");
  let currentLang = isRomanian ? "ro" : "en";

  // Simple Assistant Logic
  function getResponse(message) {
    const lower = message.toLowerCase();
    if (lower.includes("price")) {
      return currentLang === "ro" ? "Planul Basic este 19€/lună, iar Pro este 39€/lună." : "The Basic Plan is €19/month and the Pro Plan is €39/month.";
    } else if (lower.includes("signal")) {
      return currentLang === "ro" ? "Actualizările zilnice cu semnale vin la ora 20:00 EET." : "Daily signal updates are sent at 20:00 EET.";
    } else if (lower.includes("dashboard")) {
      return currentLang === "ro" ? "Puteți accesa dashboard-ul folosind butonul de mai sus." : "You can access the dashboard using the button above.";
    } else if (lower.includes("pay") || lower.includes("buy")) {
      return currentLang === "ro" ? "Puteți plăti folosind linkul Revolut de la planul ales." : "You can pay using the Revolut link from your selected plan.";
    } else {
      return currentLang === "ro" ? "Încă lucrez la răspunsul ăsta. Vrei să reformulezi?" : "I'm still learning this one. Want to rephrase it?";
    }
  }

  // Handle chat form
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

  // Voice functionality
  let voiceEnabled = false;
  const synth = window.speechSynthesis;

  function speak(text) {
    const utter = new SpeechSynthesisUtterance(text);
    utter.lang = currentLang === "ro" ? "ro-RO" : "en-US";
    utter.pitch = 1;
    utter.rate = 1;
    utter.voice = synth.getVoices().find(v => v.name.includes("Male") || v.name.includes("Bărbat")) || synth.getVoices()[0];
    synth.speak(utter);
  }

  function toggleVoice() {
    voiceEnabled = !voiceEnabled;
    const status = voiceEnabled ? (currentLang === "ro" ? "Vocea este activă" : "Voice is active") : (currentLang === "ro" ? "Vocea este dezactivată" : "Voice is off");
    alert(status);
  }
</script>

<!-- Voice Toggle Button -->
<button onclick="toggleVoice()" style="position: fixed; bottom: 20px; left: 20px; padding: 10px 16px; background: #444; color: #fff; border-radius: 8px; border: none; z-index: 1000;">🔊 Voice</button>

</body>
