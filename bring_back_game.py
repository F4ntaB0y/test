import re

file_path = 'pencemaran air.html'

with open(file_path, 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Re-inject HTML Health Bar
html_hp = """    <div class="health-bar-container">
        <div class="health-bar-text">Kesehatan Ekosistem: <span id="hp-text">100%</span></div>
        <div class="health-bar-bg">
            <div class="health-bar-fill" id="hp-fill"></div>
        </div>
    </div>"""
if '<div class="health-bar-container">' not in c:
    c = c.replace('<div class="button-group">', html_hp + '\n\n<div class="button-group">')

# 2. Re-inject HTML Hint Banner
html_hint = '<div class="game-hint" id="game-hint">🚨 MISI: KLIK POLUTAN DI LAYAR UNTUK MEMBERSIHKANNYA! 🚀</div>'
if 'id="game-hint"' not in c:
    c = c.replace('<!-- TABLE -->', html_hint + '\n\n<!-- TABLE -->')

# 3. Re-inject BULLETPROOF CSS at the end of style
css_bulletproof = """
    /* ULTIMATE GAME ENGINE STYLES */
    .health-bar-container { width: 100%; margin-bottom: 20px; text-align: left; }
    .health-bar-text { font-size: 16px; font-weight: 600; color: #f8fafc; margin-bottom: 8px; display: flex; justify-content: space-between; }
    .health-bar-bg { width: 100%; height: 20px; background: rgba(0,0,0,0.5); border-radius: 10px; overflow: hidden; border: 2px solid rgba(255,255,255,0.1); box-shadow: inset 0 0 10px rgba(0,0,0,0.5); }
    .health-bar-fill { width: 100%; height: 100%; background: linear-gradient(90deg, #ef4444 0%, #eab308 50%, #22c55e 100%); transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1); box-shadow: 0 0 15px rgba(34, 197, 94, 0.6); }
    .hp-low { background: linear-gradient(90deg, #7f1d1d 0%, #ef4444 100%); box-shadow: 0 0 15px rgba(239, 68, 68, 0.8); }
    .hp-mid { background: linear-gradient(90deg, #b45309 0%, #f59e0b 100%); box-shadow: 0 0 15px rgba(245, 158, 11, 0.8); }
    .game-hint { 
        text-align: center; font-size: 15px; color: #ffffff; 
        background: linear-gradient(135deg, #f59e0b, #ea580c); 
        padding: 12px 25px; border-radius: 50px; margin: 20px auto; 
        font-weight: 800; animation: bounceHint 2s infinite; 
        display: none; box-shadow: 0 10px 25px rgba(249, 115, 22, 0.4); 
        border: 3px solid rgba(255,255,255,0.3); max-width: fit-content;
        text-transform: uppercase; letter-spacing: 1px;
    }
    @keyframes bounceHint { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.05); box-shadow: 0 15px 35px rgba(249, 115, 22, 0.6); } }
    .clickable-pollution { cursor: crosshair !important; transition: 0.3s cubic-bezier(0.34, 1.56, 0.64, 1); animation: dangerPulse 2s infinite ease-in-out; }
    @keyframes dangerPulse { 0%, 100% { filter: drop-shadow(0 0 5px red); } 50% { filter: drop-shadow(0 0 20px red) brightness(1.2); } }
    
    /* LAYER ISOLATION PROTOCOL */
    .foam-bubbles, .plastic-waste, .toxic-waste, .pestisida-gas { position: absolute; width: 100%; height: 100%; top: 0; left: 0; opacity: 0; transition: 1s ease; pointer-events: none !important; z-index: 10; }
    .active-pollution { opacity: 1 !important; }
    
    /* ABSOLUTE DOMINANCE FOR TARGETS */
    .bubble, .trash-item, .barrel-air, .p-item { position: absolute; pointer-events: auto !important; z-index: 1000 !important; }
    .p-item:hover, .trash-item:hover, .barrel-air:hover, .bubble:hover { transform: scale(1.2) rotate(5deg) !important; filter: brightness(1.5) drop-shadow(0 0 25px white) !important; }

    .particle { position: fixed; width: 8px; height: 8px; border-radius: 50%; pointer-events: none; z-index: 10001; animation: explode 0.6s cubic-bezier(0.1, 0.8, 0.3, 1) forwards; box-shadow: 0 0 5px currentColor; }
    @keyframes explode { 0% { transform: translate(0,0) scale(1); opacity: 1; } 100% { transform: translate(var(--vx), var(--vy)) scale(0); opacity: 0; } }
    .confetti { position: fixed; width: 12px; height: 12px; z-index: 10002; pointer-events: none; animation: fall linear forwards; }
    @keyframes fall { 0% { transform: translateY(-10px) rotate(0deg); opacity: 1; } 100% { transform: translateY(110vh) rotate(720deg); opacity: 0; } }
"""
c = c.replace('</style>', css_bulletproof + '\n</style>')

# 4. Re-inject JS Engine Logic
js_logic = """
// =================== ULTIMATE GAME LOGIC ===================
let currentHP = 100;

function createExplosion(x, y, color) {
    for(let i=0; i<12; i++) {
        let p = document.createElement('div');
        p.className = 'particle';
        p.style.left = x + 'px';
        p.style.top = y + 'px';
        p.style.backgroundColor = color || '#4ade80';
        let angle = Math.random() * Math.PI * 2;
        let speed = Math.random() * 60 + 40;
        p.style.setProperty('--vx', (Math.cos(angle) * speed) + 'px');
        p.style.setProperty('--vy', (Math.sin(angle) * speed) + 'px');
        document.body.appendChild(p);
        setTimeout(() => p.remove(), 600);
    }
}

function playDamageSound() {
    try {
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        let osc = ctx.createOscillator(); let gain = ctx.createGain();
        osc.type = "sawtooth"; osc.frequency.setValueAtTime(150, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(50, ctx.currentTime + 0.3);
        gain.gain.setValueAtTime(0.2, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.3);
        osc.connect(gain); gain.connect(ctx.destination);
        osc.start(); osc.stop(ctx.currentTime + 0.3);
    } catch(e) {}
}

function playPopSound() {
    try {
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = ctx.createOscillator(); const gain = ctx.createGain();
        osc.type = "sine"; osc.frequency.setValueAtTime(800, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(1200, ctx.currentTime + 0.1);
        gain.gain.setValueAtTime(0.2, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.1);
        osc.connect(gain); gain.connect(ctx.destination);
        osc.start(); osc.stop(ctx.currentTime + 0.1);
    } catch(e) {}
}

function triggerVictory() {
    try {
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        [400, 500, 600, 800].forEach((freq, i) => {
            let osc = ctx.createOscillator(); let gain = ctx.createGain();
            osc.frequency.value = freq; osc.connect(gain); gain.connect(ctx.destination);
            gain.gain.setValueAtTime(0, ctx.currentTime + i*0.1);
            gain.gain.linearRampToValueAtTime(0.1, ctx.currentTime + i*0.1 + 0.05);
            gain.gain.linearRampToValueAtTime(0, ctx.currentTime + i*0.1 + 0.15);
            osc.start(ctx.currentTime + i*0.1); osc.stop(ctx.currentTime + i*0.1 + 0.15);
        });
    } catch(e) {}
    for(let i=0; i<50; i++) {
        let c = document.createElement('div');
        c.className = 'confetti';
        c.style.left = (Math.random() * window.innerWidth) + 'px';
        c.style.top = '-20px';
        c.style.backgroundColor = ['#facc15', '#ef4444', '#3b82f6', '#22c55e', '#a855f7'][Math.floor(Math.random()*5)];
        document.body.appendChild(c);
        setTimeout(()=>c.remove(), 4000);
    }
}

function setHP(val, isDamage = false, isReset = false) {
    let previousHP = currentHP;
    currentHP = val;
    if(currentHP > 100) currentHP = 100;
    if(window.victoryTimeout) clearTimeout(window.victoryTimeout);
    const hpText = document.getElementById("hp-text");
    const hpFill = document.getElementById("hp-fill");
    if(hpText && hpFill) {
        hpText.innerText = currentHP + "%";
        hpFill.style.width = currentHP + "%";
        hpFill.className = "health-bar-fill";
        if(currentHP <= 30) hpFill.classList.add("hp-low");
        else if(currentHP <= 60) hpFill.classList.add("hp-mid");
        if(isDamage) playDamageSound();
        
        const hint = document.getElementById("game-hint");
        if(currentHP >= 100) {
            if(hint) hint.style.display = "none";
            if(previousHP < 100 && !isDamage && !isReset) {
                window.victoryTimeout = setTimeout(() => {
                    triggerVictory();
                    resetSimulasi();
                }, 300);
            }
        } else {
            if(hint) hint.style.display = "block";
        }
    }
}

function bindCleanAction(selector, hpGain) {
    document.querySelectorAll(selector).forEach(el => {
        el.classList.add('clickable-pollution');
        el.addEventListener('click', function(e) {
            if(currentHP < 100) {
                this.style.display = "none"; 
                setHP(currentHP + hpGain, false, false);
                createFloatingText(e, `+${hpGain} HP ✨`, "#4ade80");
                createExplosion(e.clientX, e.clientY);
                playPopSound();
                e.stopPropagation();
            }
        });
    });
}

function resetGameElements() {
    document.querySelectorAll('.bubble, .trash-item, .barrel-air, .p-item').forEach(el => {
        el.style.display = "";
    });
}

setTimeout(() => {
    bindCleanAction('.bubble', 10);
    bindCleanAction('.trash-item', 20);
    bindCleanAction('.barrel-air', 20);
    bindCleanAction('.p-item', 25);
}, 500);
// ===========================================================
"""
c = c.replace('</script>', js_logic + '\n</script>')

# 5. Reinject function calls to trigger game
c = c.replace('function deterjen(){', 'function deterjen(){\n    setHP(50, true); resetGameElements();')
c = c.replace('function pabrik(){', 'function pabrik(){\n    setHP(40, true); resetGameElements();')
c = c.replace('function plastik(){', 'function plastik(){\n    setHP(40, true); resetGameElements();')
c = c.replace('function pestisida(){', 'function pestisida(){\n    setHP(20, true); resetGameElements();')
c = c.replace('function resetSimulasi(){', 'function resetSimulasi(){\n    setHP(100, false, true); resetGameElements();')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(c)

print("ULTIMATE GAME ENGINE HAS RETURNED SUCCESSFULLY!")
