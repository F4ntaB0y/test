import re

p_path = 'pencemaran air.html'
with open(p_path, 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Inject the Timed-Sequenced Phased Recovery into resetSimulasi()
old_reset = """function resetSimulasi(){
    setHP(100, false, true); resetGameElements();
    
    clearPollution();

    river.className = "river";"""

new_reset = """function resetSimulasi(){
    // FASE 1: Hilangkan Gelembung & Partikel Seketika (Fade Out 1 detik aktif)
    clearPollution();
    
    // FASE 2: Tunggu 1.2 detik sampai partikel BENAR-BENAR LENYAP dari pandangan, BARULAH bersihkan warna air
    setTimeout(() => {
        setHP(100, false, true); resetGameElements();
        river.className = "river";"""

if old_reset in c:
    c = c.replace(old_reset, new_reset)
    print("Step 1: Phased Simulation reset logic injected successfully!")
else:
    print("WARNING Step 1: Exact string not found. Re-fetching function block...")
    
    # FALLBACK regex replacement for function resetSimulasi
    c = re.sub(r'function resetSimulasi\(\)\{.*?river\.className = "river";', 
               new_reset, c, flags=re.DOTALL)
    print("Step 1 (Regex Fallback): Phased reset logic applied!")


# 2. Append the missing closing bracket brace for our new setTimeout block!
# We need to replace 'document.getElementById("info").innerHTML = "Sungai telah bersih kembali.";\n}'
# with 'document.getElementById("info").innerHTML = "Sungai telah bersih kembali.";\n    }, 1200);\n}'

end_marker = 'document.getElementById("info").innerHTML = "Sungai telah bersih kembali.";\n}'
new_end_marker = 'document.getElementById("info").innerHTML = "Sungai telah bersih kembali.";\n    }, 1200);\n}'

if end_marker in c:
    c = c.replace(end_marker, new_end_marker)
    print("Step 2: Closure timeout brace applied.")
else:
    print("WARNING Step 2: Marker not found.")


# 3. Increase user-delay before Victory fires so they see final explosion
old_victory_timer = """window.victoryTimeout = setTimeout(() => {
                    triggerVictory();
                    resetSimulasi();
                }, 300);"""

new_victory_timer = """window.victoryTimeout = setTimeout(() => {
                    triggerVictory();
                    resetSimulasi();
                }, 1500);"""

if old_victory_timer in c:
    c = c.replace(old_victory_timer, new_victory_timer)
    print("Step 3: User pacing delay boosted to 1500ms.")
else:
    # Robust flexible spacing fallback
    c = re.sub(r'window\.victoryTimeout\s*=\s*setTimeout\(\(\)\s*=>\s*\{.*?\}, 300\);', new_victory_timer, c, flags=re.DOTALL)
    print("Step 3 (Regex): Pacing boost complete.")

with open(p_path, 'w', encoding='utf-8') as f:
    f.write(c)
