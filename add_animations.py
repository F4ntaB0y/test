import re

# 1. PENCEMARAN AIR
with open('pencemaran air.html', 'r', encoding='utf-8') as f:
    html = f.read()

css_air = """
        /* NEW POLLUTION CSS */
        .foam-bubbles, .plastic-waste, .toxic-waste, .pestisida-gas { position: absolute; width: 100%; height: 100%; top: 0; left: 0; pointer-events: none; opacity: 0; transition: opacity 1s ease; }
        .active-pollution { opacity: 1 !important; }
        .bubble { position: absolute; background: rgba(255,255,255,0.7); border-radius: 50%; animation: rise 4s infinite ease-in; box-shadow: inset 0 0 10px rgba(255,255,255,0.9); }
        .b1 { width: 40px; height: 40px; left: 20%; bottom: -40px; animation-delay: 0s; }
        .b2 { width: 60px; height: 60px; left: 40%; bottom: -60px; animation-delay: 1s; }
        .b3 { width: 30px; height: 30px; left: 60%; bottom: -30px; animation-delay: 2s; }
        .b4 { width: 50px; height: 50px; left: 80%; bottom: -50px; animation-delay: 0.5s; }
        .b5 { width: 35px; height: 35px; left: 50%; bottom: -35px; animation-delay: 1.5s; }
        @keyframes rise { 0% { transform: translateY(0) scale(1); opacity: 0; } 50% { opacity: 1; } 100% { transform: translateY(-300px) scale(1.5); opacity: 0; } }
        .trash-item, .barrel-air { position: absolute; font-size: 40px; filter: drop-shadow(0 5px 5px rgba(0,0,0,0.4)); animation: float-trash 6s infinite alternate ease-in-out; }
        .t1 { top: 30px; left: 20%; animation-delay: 0s; }
        .t2 { top: 60px; left: 50%; animation-delay: 1s; }
        .t3 { top: 40px; left: 80%; animation-delay: 2s; }
        .br1 { bottom: 20px; left: 25%; font-size: 60px; animation: sink 3s forwards; }
        .br2 { bottom: 30px; left: 55%; font-size: 50px; animation: sink 3s forwards 0.5s; }
        .br3 { bottom: 10px; left: 85%; font-size: 70px; animation: sink 3s forwards 1s; }
        @keyframes float-trash { 0% { transform: translateY(0) rotate(-10deg); } 100% { transform: translateY(20px) rotate(10deg); } }
        @keyframes sink { 0% { transform: translateY(-200px) rotate(0deg); opacity: 0; } 50% { opacity: 1; } 100% { transform: translateY(0) rotate(15deg); opacity: 1; } }
        .pestisida-gas { background: radial-gradient(circle at center, rgba(74, 222, 128, 0.4) 0%, transparent 70%); filter: blur(20px); animation: pulse-gas 3s infinite alternate; }
        @keyframes pulse-gas { from { transform: scale(1); opacity: 0.5; } to { transform: scale(1.2); opacity: 1; } }
    </style>
"""
html = html.replace("    </style>", css_air)

html_air = """
        <!-- POLLUTION ELEMENTS -->
        <div class="foam-bubbles" id="foam-bubbles">
            <div class="bubble b1"></div><div class="bubble b2"></div><div class="bubble b3"></div><div class="bubble b4"></div><div class="bubble b5"></div>
        </div>
        <div class="plastic-waste" id="plastic-waste">
            <div class="trash-item t1">🛍️</div><div class="trash-item t2">🥤</div><div class="trash-item t3">🧴</div>
        </div>
        <div class="toxic-waste" id="toxic-waste">
            <div class="barrel-air br1">🛢️</div><div class="barrel-air br2">🛢️</div><div class="barrel-air br3">🛢️</div>
        </div>
        <div class="pestisida-gas" id="pestisida-gas"></div>
    </div>
"""
html = re.sub(r'</div>\s*<!-- INFO -->', html_air + '\n    <!-- INFO -->', html)

js_air = """
function clearPollution() {
    document.getElementById("foam-bubbles").classList.remove("active-pollution");
    document.getElementById("plastic-waste").classList.remove("active-pollution");
    document.getElementById("toxic-waste").classList.remove("active-pollution");
    document.getElementById("pestisida-gas").classList.remove("active-pollution");
}
"""
html = html.replace("function deterjen(){", js_air + "\nfunction deterjen(){\n    clearPollution();\n    document.getElementById('foam-bubbles').classList.add('active-pollution');")
html = html.replace("function pabrik(){", "function pabrik(){\n    clearPollution();\n    document.getElementById('toxic-waste').classList.add('active-pollution');")
html = html.replace("function plastik(){", "function plastik(){\n    clearPollution();\n    document.getElementById('plastic-waste').classList.add('active-pollution');")
html = html.replace("function pestisida(){", "function pestisida(){\n    clearPollution();\n    document.getElementById('pestisida-gas').classList.add('active-pollution');")
html = html.replace("function resetSimulasi(){", "function resetSimulasi(){\n    clearPollution();")

with open('pencemaran air.html', 'w', encoding='utf-8') as f:
    f.write(html)

# 2. PENCEMARAN TANAH
with open('pencemaran tanah.html', 'r', encoding='utf-8') as f:
    html = f.read()

css_tanah = """
        /* NEW POLLUTION TANAH */
        .oil-spill, .toxic-gas { position: absolute; width: 100%; height: 100%; top: 0; left: 0; pointer-events: none; opacity: 0; transition: 1s; }
        .active-pollution { opacity: 1 !important; }
        .puddle { position: absolute; background: #111827; border-radius: 50%; filter: drop-shadow(0 0 10px #000); animation: spread 4s forwards; bottom: 20px; opacity: 0.9; }
        .pd1 { left: 20%; width: 20px; height: 10px; }
        .pd2 { left: 50%; width: 20px; height: 10px; animation-delay: 0.5s; }
        .pd3 { left: 80%; width: 20px; height: 10px; animation-delay: 1s; }
        @keyframes spread { 0% { transform: scale(1); } 100% { transform: scale(8); } }
        .gas { position: absolute; background: rgba(74, 222, 128, 0.4); filter: blur(20px); border-radius: 50%; animation: gas-rise 5s infinite alternate; }
        .g1 { width: 150px; height: 100px; bottom: 50px; left: 30%; }
        .g2 { width: 200px; height: 120px; bottom: 30px; left: 60%; animation-delay: 1s; }
        @keyframes gas-rise { 0% { transform: translateY(0) scale(1); opacity: 0.5; } 100% { transform: translateY(-50px) scale(1.5); opacity: 0.8; } }
        .barrel-tanah { position: absolute; font-size: 50px; opacity: 0; transition: 1s; filter: drop-shadow(0 5px 5px rgba(0,0,0,0.5)); }
        .bt1 { bottom: 30px; left: 30%; transform: rotate(-20deg); }
        .bt2 { bottom: 20px; left: 60%; transform: rotate(10deg); }
        .show-barrel { opacity: 1; }
    </style>
"""
html = html.replace("    </style>", css_tanah)

html_tanah = """
        <div class="oil-spill" id="oil-spill">
            <div class="puddle pd1"></div><div class="puddle pd2"></div><div class="puddle pd3"></div>
        </div>
        <div class="toxic-gas" id="toxic-gas">
            <div class="gas g1"></div><div class="gas g2"></div>
        </div>
        <div class="barrel-tanah bt1">🛢️</div><div class="barrel-tanah bt2">☣️</div>
    </div>
"""
html = re.sub(r'</div>\s*<div class="info-box"', html_tanah + '\n    <div class="info-box"', html)

js_tanah = """
const barrels = document.querySelectorAll(".barrel-tanah");
function hideAllPollution() {
    trash.forEach(i=>i.classList.remove("show-trash"));
    barrels.forEach(i=>i.classList.remove("show-barrel"));
    document.getElementById("oil-spill").classList.remove("active-pollution");
    document.getElementById("toxic-gas").classList.remove("active-pollution");
}
"""
html = html.replace("function showTrash(){trash.forEach(i=>i.classList.add(\"show-trash\"));}", js_tanah + "\nfunction showTrash(){trash.forEach(i=>i.classList.add(\"show-trash\"));}")

html = html.replace("function sampah(){", "function sampah(){\n    hideAllPollution();\n    ")
html = html.replace("function pestisida(){", "function pestisida(){\n    hideAllPollution();\n    document.getElementById('toxic-gas').classList.add('active-pollution');\n    ")
# Make sure pestisida doesn't show trash if it was called via showTrash()
html = html.replace("showTrash();damagePlants();document.getElementById(\"soil\").innerHTML=\"Tercemar\";", "damagePlants();document.getElementById(\"soil\").innerHTML=\"Tercemar\";")

html = html.replace("function limbah(){", "function limbah(){\n    hideAllPollution();\n    barrels.forEach(i=>i.classList.add('show-barrel'));\n    ")
html = html.replace("showTrash();damagePlants();document.getElementById(\"soil\").innerHTML=\"Rusak\";", "damagePlants();document.getElementById(\"soil\").innerHTML=\"Rusak\";")

html = html.replace("function oli(){", "function oli(){\n    hideAllPollution();\n    document.getElementById('oil-spill').classList.add('active-pollution');\n    ")
html = html.replace("showTrash();damagePlants();document.getElementById(\"soil\").innerHTML=\"Tercemar Oli\";", "damagePlants();document.getElementById(\"soil\").innerHTML=\"Tercemar Oli\";")

html = html.replace("function resetSimulasi(){", "function resetSimulasi(){\n    hideAllPollution();\n    ")

with open('pencemaran tanah.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Animations added successfully!")
