import re

files = ['pencemaran air.html', 'pencemaran tanah.html', 'pencemaran udara.html']

new_css_hint = """    .game-hint { 
        text-align: center; 
        font-size: 15px; 
        color: #ffffff; 
        background: linear-gradient(135deg, #f59e0b, #ea580c); 
        padding: 12px 25px; 
        border-radius: 50px; 
        margin: 20px auto; 
        font-weight: 800; 
        animation: bounceHint 2s infinite; 
        display: none; 
        box-shadow: 0 10px 25px rgba(249, 115, 22, 0.4); 
        border: 3px solid rgba(255,255,255,0.3); 
        max-width: fit-content;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    @keyframes bounceHint { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.05); box-shadow: 0 15px 35px rgba(249, 115, 22, 0.6); } }
    .clickable-pollution { cursor: crosshair !important; transition: 0.3s cubic-bezier(0.34, 1.56, 0.64, 1); animation: dangerPulse 2s infinite ease-in-out; }
    @keyframes dangerPulse { 0%, 100% { filter: drop-shadow(0 0 2px red); } 50% { filter: drop-shadow(0 0 15px red) brightness(1.2); } }
    .clickable-pollution:hover { transform: scale(1.2) rotate(5deg) !important; filter: drop-shadow(0 0 25px white) brightness(1.5) !important; z-index: 100; }"""

old_hint_regex = r'\.game-hint \{.*?display: none; \}.*?\.clickable-pollution:active \{.*?\}'

new_hint_text = "🚨 MISI: KLIK POLUTAN DI LAYAR UNTUK MEMBERSIHKANNYA! 🚀"

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        c = f.read()
    
    # Update the CSS block - being very careful to overwrite existing classes
    c = re.sub(r'\.game-hint\s*\{[^\}]+\}.*?\.clickable-pollution:active\s*\{[^\}]+\}', new_css_hint, c, flags=re.DOTALL)
    
    # Update the HTML text
    c = re.sub(r'id="game-hint">.*?</div>', 'id="game-hint">' + new_hint_text + '</div>', c)

    # Make sure JS displays it as block centrally
    c = c.replace('hint.style.display = "block"', 'hint.style.display = "block"') # Placeholder

    with open(file, 'w', encoding='utf-8') as f:
        f.write(c)
    
    print(f"Revamped Game Mode visual cues in {file}")
