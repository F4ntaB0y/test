import re

css_game = """
    /* GAME CSS */
    .health-bar-container { width: 100%; margin-bottom: 20px; text-align: left; }
    .health-bar-text { font-size: 16px; font-weight: 600; color: #f8fafc; margin-bottom: 8px; display: flex; justify-content: space-between; }
    .health-bar-bg { width: 100%; height: 20px; background: rgba(0,0,0,0.5); border-radius: 10px; overflow: hidden; border: 2px solid rgba(255,255,255,0.1); box-shadow: inset 0 0 10px rgba(0,0,0,0.5); }
    .health-bar-fill { width: 100%; height: 100%; background: linear-gradient(90deg, #ef4444 0%, #eab308 50%, #22c55e 100%); transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1); box-shadow: 0 0 15px rgba(34, 197, 94, 0.6); }
    .hp-low { background: linear-gradient(90deg, #7f1d1d 0%, #ef4444 100%); box-shadow: 0 0 15px rgba(239, 68, 68, 0.8); }
    .hp-mid { background: linear-gradient(90deg, #b45309 0%, #f59e0b 100%); box-shadow: 0 0 15px rgba(245, 158, 11, 0.8); }
    .game-hint { text-align: center; font-size: 14px; color: #4ade80; margin-top: 15px; font-weight: 500; animation: pulseHint 2s infinite; display: none; }
    @keyframes pulseHint { 0% { opacity: 0.5; } 50% { opacity: 1; transform: scale(1.05); } 100% { opacity: 0.5; } }
    .clickable-pollution { cursor: crosshair !important; transition: 0.2s; }
    .clickable-pollution:hover { transform: scale(1.2) rotate(10deg); filter: brightness(1.5) drop-shadow(0 0 10px white); }
    .clickable-pollution:active { transform: scale(0.8); }
"""

js_game_base = """
// GAME LOGIC
let currentHP = 100;
function setHP(val) {
    currentHP = val;
    if(currentHP > 100) currentHP = 100;
    const hpText = document.getElementById("hp-text");
    const hpFill = document.getElementById("hp-fill");
    if(hpText && hpFill) {
        hpText.innerText = currentHP + "%";
        hpFill.style.width = currentHP + "%";
        hpFill.className = "health-bar-fill";
        if(currentHP <= 30) hpFill.classList.add("hp-low");
        else if(currentHP <= 60) hpFill.classList.add("hp-mid");
        
        if(currentHP >= 100) {
            document.getElementById("game-hint").style.display = "none";
            setTimeout(resetSimulasi, 500);
        } else {
            document.getElementById("game-hint").style.display = "block";
        }
    }
}

function playPopSound() {
    try {
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        const ctx = new AudioContext();
        const osc = ctx.createOscillator();
        const gainNode = ctx.createGain();
        osc.type = "sine";
        osc.frequency.setValueAtTime(800, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(1200, ctx.currentTime + 0.1);
        gainNode.gain.setValueAtTime(0.2, ctx.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.1);
        osc.connect(gainNode);
        gainNode.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + 0.1);
    } catch(e) {}
}

function bindCleanAction(selector, hpGain) {
    document.querySelectorAll(selector).forEach(el => {
        el.classList.add('clickable-pollution');
        el.addEventListener('click', function(e) {
            if(this.style.opacity !== "0" && this.style.display !== "none" && currentHP < 100) {
                this.style.opacity = "0";
                this.style.pointerEvents = "none";
                setHP(currentHP + hpGain);
                createFloatingText(e, "Bersih! ✨", "#4ade80");
                playPopSound();
                e.stopPropagation();
            }
        });
    });
}

function resetPollutionVisibility(selector) {
    document.querySelectorAll(selector).forEach(el => {
        el.style.opacity = "";
        el.style.pointerEvents = "";
    });
}
"""

html_hp_bar = """
    <div class="health-bar-container">
        <div class="health-bar-text">Kesehatan Ekosistem: <span id="hp-text">100%</span></div>
        <div class="health-bar-bg">
            <div class="health-bar-fill" id="hp-fill"></div>
        </div>
    </div>
"""
html_hint = '<div class="game-hint" id="game-hint">🎮 GAME MODE: Klik polutan (sampah/asap/limbah) di simulasi untuk membersihkannya!</div>'


# APPLY TO PENCEMARAN AIR
with open('pencemaran air.html', 'r', encoding='utf-8') as f:
    air = f.read()

if "/* GAME CSS */" not in air:
    air = air.replace("</style>", css_game + "\n</style>")
    air = re.sub(r'<div class="button-group">', html_hp_bar + '\n<div class="button-group">', air)
    air = re.sub(r'</div>\s*<!-- TABLE -->', html_hint + '\n</div>\n<!-- TABLE -->', air)
    
    # Update JS
    air = air.replace("</script>", js_game_base + "\n" + """
setTimeout(() => {
    bindCleanAction('.bubble', 10);
    bindCleanAction('.trash-item', 20);
    bindCleanAction('.barrel-air', 20);
    bindCleanAction('#pestisida-gas', 60);
}, 500);
""" + "\n</script>")

    # Modify functions
    air = air.replace("function deterjen(){", "function deterjen(){\n    setHP(50); resetPollutionVisibility('.bubble');")
    air = air.replace("function pabrik(){", "function pabrik(){\n    setHP(40); resetPollutionVisibility('.barrel-air');")
    air = air.replace("function plastik(){", "function plastik(){\n    setHP(40); resetPollutionVisibility('.trash-item');")
    air = air.replace("function pestisida(){", "function pestisida(){\n    setHP(40); resetPollutionVisibility('#pestisida-gas');")
    air = air.replace("function resetSimulasi(){", "function resetSimulasi(){\n    setHP(100);")
    
    with open('pencemaran air.html', 'w', encoding='utf-8') as f:
        f.write(air)

# APPLY TO PENCEMARAN TANAH
with open('pencemaran tanah.html', 'r', encoding='utf-8') as f:
    tanah = f.read()

if "/* GAME CSS */" not in tanah:
    tanah = tanah.replace("</style>", css_game + "\n</style>")
    tanah = re.sub(r'<div class="button-group">', html_hp_bar + '\n<div class="button-group">', tanah)
    tanah = re.sub(r'</div>\s*<div class="table-box">', html_hint + '\n</div>\n<div class="table-box">', tanah)
    
    tanah = tanah.replace("</script>", js_game_base + "\n" + """
setTimeout(() => {
    bindCleanAction('.trash', 20);
    bindCleanAction('.barrel-tanah', 30);
    bindCleanAction('.puddle', 20);
    bindCleanAction('.gas', 30);
}, 500);
""" + "\n</script>")

    tanah = tanah.replace("function sampah(){", "function sampah(){\n    setHP(40); resetPollutionVisibility('.trash');")
    tanah = tanah.replace("function pestisida(){", "function pestisida(){\n    setHP(40); resetPollutionVisibility('.gas');")
    tanah = tanah.replace("function limbah(){", "function limbah(){\n    setHP(40); resetPollutionVisibility('.barrel-tanah');")
    tanah = tanah.replace("function oli(){", "function oli(){\n    setHP(40); resetPollutionVisibility('.puddle');")
    tanah = tanah.replace("function resetSimulasi(){", "function resetSimulasi(){\n    setHP(100);")
    
    with open('pencemaran tanah.html', 'w', encoding='utf-8') as f:
        f.write(tanah)

# APPLY TO PENCEMARAN UDARA
with open('pencemaran udara.html', 'r', encoding='utf-8') as f:
    udara = f.read()

if "/* GAME CSS */" not in udara:
    udara = udara.replace("</style>", css_game + "\n</style>")
    udara = re.sub(r'<div class="buttons">', html_hp_bar + '\n<div class="buttons">', udara)
    udara = re.sub(r'</div>\s*<div class="table-box">', html_hint + '\n</div>\n<div class="table-box">', udara)
    
    udara = udara.replace("</script>", js_game_base + "\n" + """
setTimeout(() => {
    bindCleanAction('.factory-smoke', 20);
    bindCleanAction('.cs', 20);
    
    // Add click to fire
    let fire = document.getElementById('fire');
    if(fire) {
        fire.classList.add('clickable-pollution');
        fire.addEventListener('click', function(e) {
            if(this.style.display !== "none" && currentHP < 100) {
                this.style.display = "none";
                setHP(100);
                createFloatingText(e, "Api padam! 💦", "#4ade80");
                playPopSound();
                e.stopPropagation();
            }
        });
    }
}, 500);
""" + "\n</script>")

    udara = udara.replace("function kendaraan(){", "function kendaraan(){\n    setHP(40); resetPollutionVisibility('.cs');")
    udara = udara.replace("function pabrik(){", "function pabrik(){\n    setHP(40); resetPollutionVisibility('.factory-smoke');")
    udara = udara.replace("function kebakaran(){", "function kebakaran(){\n    setHP(30);")
    udara = udara.replace("function penghijauan(){", "function penghijauan(){\n    setHP(100);")
    udara = udara.replace("function resetSimulasi(){", "function resetSimulasi(){\n    setHP(100);")
    
    with open('pencemaran udara.html', 'w', encoding='utf-8') as f:
        f.write(udara)

print("Game Mode integrated!")
