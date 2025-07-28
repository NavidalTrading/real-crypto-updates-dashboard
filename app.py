
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
    st.title("🔒 Enter Password to Access Dashboard")

    # Upload file
    uploaded_file = st.file_uploader("Upload Payment Proof", type=["png", "jpg", "jpeg", "pdf"], key="payment_upload")

    if uploaded_file:
        filename = uploaded_file.name.lower()
        current_month = datetime.datetime.now().strftime("%B").lower()
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
        st.info(f"Your password for **{current_month.capitalize()}** is: `{password}`\n\nAccess valid for 30 days.")

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
user_plan = st.session_state.get("user_plan", "Basic")

st.markdown(f"### 👤 You are on the **{user_plan} Plan**")

if user_plan == "Pro":
    st.success("✅ You have access to **Pro** content including early signals, premium coins and full dashboard.")
else:
    st.info("ℹ️ On the **Basic Plan**, you see standard coins.")
    symbols = ["XRP", "CRV", "FIL", "EGLD"] if user_plan == "Basic" else ["BTC", "ETH", "XRP", "ADA", "QNT", "CRV", "FIL", "EGLD"]


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








