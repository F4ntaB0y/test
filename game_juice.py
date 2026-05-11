import re

# NEW CSS FOR JUICE
new_css = """
    /* GAME CSS */
    .health-bar-container { width: 100%; margin-bottom: 20px; text-align: left; }
    .health-bar-text { font-size: 16px; font-weight: 600; color: #f8fafc; margin-bottom: 8px; display: flex; justify-content: space-between; }
    .health-bar-bg { width: 100%; height: 20px; background: rgba(0,0,0,0.5); border-radius: 10px; overflow: hidden; border: 2px solid rgba(255,255,255,0.1); box-shadow: inset 0 0 10px rgba(0,0,0,0.5); }
    .health-bar-fill { width: 100%; height: 100%; background: linear-gradient(90deg, #ef4444 0%, #eab308 50%, #22c55e 100%); transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1); box-shadow: 0 0 15px rgba(34, 197, 94, 0.6); }
    .hp-low { background: linear-gradient(90deg, #7f1d1d 0%, #ef4444 100%); box-shadow: 0 0 15px rgba(239, 68, 68, 0.8); }
    .hp-mid { background: linear-gradient(90deg, #b45309 0%, #f59e0b 100%); box-shadow: 0 0 15px rgba(245, 158, 11, 0.8); }
    .game-hint { text-align: center; font-size: 14px; color: #4ade80; margin-top: 15px; font-weight: 500; animation: pulseHint 2s infinite; display: none; }
    @keyframes pulseHint { 0% { opacity: 0.5; } 50% { opacity: 1; transform: scale(1.05); } 100% { opacity: 0.5; } }
    .clickable-pollution { cursor: crosshair !important; transition: 0.2s cubic-bezier(0.34, 1.56, 0.64, 1); }
    .clickable-pollution:hover { filter: brightness(1.5) drop-shadow(0 0 10px white); }
    .clickable-pollution:active { transform: scale(0.8) !important; }
    
    /* JUICE EFFECTS */
    .particle { position: fixed; width: 8px; height: 8px; border-radius: 50%; pointer-events: none; z-index: 10001; animation: explode 0.6s cubic-bezier(0.1, 0.8, 0.3, 1) forwards; box-shadow: 0 0 5px currentColor; }
    @keyframes explode { 0% { transform: translate(0,0) scale(1); opacity: 1; } 100% { transform: translate(var(--vx), var(--vy)) scale(0); opacity: 0; } }
    .confetti { position: fixed; width: 12px; height: 12px; z-index: 10002; pointer-events: none; animation: fall linear forwards; }
    @keyframes fall { 0% { transform: translateY(-10px) rotate(0deg); opacity: 1; } 100% { transform: translateY(110vh) rotate(720deg); opacity: 0; } }
    .shake { animation: shakeAnim 0.5s cubic-bezier(.36,.07,.19,.97) both; }
    @keyframes shakeAnim { 10%, 90% { transform: translate3d(-2px, 0, 0); } 20%, 80% { transform: translate3d(4px, 0, 0); } 30%, 50%, 70% { transform: translate3d(-6px, 0, 0); } 40%, 60% { transform: translate3d(6px, 0, 0); } }
"""

# NEW JS FOR JUICE
new_js = """
// GAME LOGIC
let currentHP = 100;

function createExplosion(x, y, color) {
    for(let i=0; i<8; i++) {
        let p = document.createElement('div');
        p.className = 'particle';
        p.style.left = x + 'px';
        p.style.top = y + 'px';
        p.style.backgroundColor = color || '#4ade80';
        let angle = Math.random() * Math.PI * 2;
        let speed = Math.random() * 50 + 30;
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
        c.style.animationDuration = (Math.random() * 2 + 1.5) + 's';
        c.style.animationDelay = (Math.random() * 0.5) + 's';
        document.body.appendChild(c);
        setTimeout(()=>c.remove(), 4000);
    }
}

function setHP(val, isDamage = false) {
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
        
        if(isDamage) {
            playDamageSound();
            document.body.classList.add("shake");
            setTimeout(()=>document.body.classList.remove("shake"), 500);
        }

        if(currentHP >= 100) {
            document.getElementById("game-hint").style.display = "none";
            if(window.victoryTimeout) clearTimeout(window.victoryTimeout);
            window.victoryTimeout = setTimeout(() => {
                triggerVictory();
                resetSimulasi();
            }, 300);
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
        
        // Dodging mechanic!
        el.addEventListener('mouseover', function(e) {
            if(Math.random() > 0.5) {
                let dx = (Math.random() - 0.5) * 40;
                let dy = (Math.random() - 0.5) * 40;
                this.style.transform = `translate(${dx}px, ${dy}px) rotate(${Math.random()*45}deg)`;
            }
        });

        el.addEventListener('click', function(e) {
            if(this.style.opacity !== "0" && this.style.display !== "none" && currentHP < 100) {
                this.style.opacity = "0";
                this.style.pointerEvents = "none";
                this.style.transform = "translate(0,0)"; // Reset
                setHP(currentHP + hpGain, false);
                createFloatingText(e, `+${hpGain} HP ✨`, "#4ade80");
                createExplosion(e.clientX, e.clientY);
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
        el.style.transform = "translate(0,0)";
    });
}
"""

files = ['pencemaran air.html', 'pencemaran tanah.html', 'pencemaran udara.html']

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()

    # Replace CSS
    html = re.sub(r'/\*\s*GAME CSS\s*\*/.*?(?=\n\s*/\*\s*INTERACTIVE CSS\s*\*/|\n\s*</style>)', new_css, html, flags=re.DOTALL)
    
    # Replace JS
    html = re.sub(r'// GAME LOGIC.*?(?=\n// Audio Synthesizer)', new_js + "\n", html, flags=re.DOTALL)
    
    # Update setHP calls to include damage (true)
    html = re.sub(r'setHP\((\d+)\);', r'setHP(\1, true);', html)
    # Revert resetSimulasi back to false
    html = html.replace('function resetSimulasi(){\n    setHP(100, true);', 'function resetSimulasi(){\n    setHP(100, false);')

    with open(file, 'w', encoding='utf-8') as f:
        f.write(html)

print("Game Juice injected successfully!")
