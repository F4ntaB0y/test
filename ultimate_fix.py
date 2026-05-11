import re

new_js = """// GAME LOGIC
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
        
        if(isDamage) {
            playDamageSound();
            document.body.classList.add("shake");
            setTimeout(()=>document.body.classList.remove("shake"), 500);
        }

        if(currentHP >= 100) {
            document.getElementById("game-hint").style.display = "none";
            if(previousHP < 100 && !isDamage && !isReset) {
                window.victoryTimeout = setTimeout(() => {
                    triggerVictory();
                    resetSimulasi();
                }, 300);
            }
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
                this.style.transform = "translate(0,0)"; 
                setHP(currentHP + hpGain, false, false);
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

    # Replace GAME LOGIC block exactly
    html = re.sub(r'// GAME LOGIC.*?(?=setTimeout\(\(\) => \{)', new_js, html, flags=re.DOTALL)
    
    # Fix the missing damage true argument in pollution calls
    html = re.sub(r'setHP\(40\);', r'setHP(40, true);', html)
    html = re.sub(r'setHP\(30\);', r'setHP(30, true);', html)
    html = re.sub(r'setHP\(50\);', r'setHP(50, true);', html)
    
    # Ensure resetSimulasi has false, true
    html = html.replace('setHP(100);', 'setHP(100, false, true);')
    html = html.replace('setHP(100, false);', 'setHP(100, false, true);')
    html = html.replace('setHP(100, false, true, true);', 'setHP(100, false, true);')
    
    # Penghijauan in udara also resets
    html = re.sub(r'function penghijauan\(\)\{\n\s*setHP\(.*?\);', 'function penghijauan(){\n    setHP(100, false, true);', html)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(html)

print("Ultimate fix applied!")
