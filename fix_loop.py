import re

old_sethp = """function setHP(val, isDamage = false) {
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
}"""

new_sethp = """function setHP(val, isDamage = false, isReset = false) {
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
}"""

files = ['pencemaran air.html', 'pencemaran tanah.html', 'pencemaran udara.html']

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()

    # Replace setHP function
    html = html.replace(old_sethp, new_sethp)
    
    # Replace resetSimulasi
    html = html.replace("function resetSimulasi(){\n    setHP(100, false);", "function resetSimulasi(){\n    setHP(100, false, true);")
    
    # Check pencemaran udara penghijauan
    if 'pencemaran udara.html' in file:
        html = html.replace("function penghijauan(){\n    setHP(100, true);", "function penghijauan(){\n    setHP(100, false, true);")
        # Wait, my previous script didn't modify penghijauan correctly maybe?
        # Let's just safely replace any setHP(100, true); in penghijauan with setHP(100, false, true);
        html = re.sub(r'function penghijauan\(\)\{\n\s*setHP\(100.*?\);', 'function penghijauan(){\n    setHP(100, false, true);', html)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(html)

print("Infinite loop fixed!")
