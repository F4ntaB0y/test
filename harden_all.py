import re

files = ['pencemaran air.html', 'pencemaran tanah.html']
hint_html = '    <div class="game-hint" id="game-hint">🎮 GAME MODE: Klik polutan (sampah/asap/limbah) di simulasi untuk membersihkannya!</div>\n'

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        c = f.read()
    
    # 1. Ensure HTML div exists
    if 'id="game-hint"' not in c:
        if '<!-- TABLE -->' in c:
            c = c.replace('<!-- TABLE -->', hint_html + '    <!-- TABLE -->')
            print(f"Injected hint div to {file}")
        elif '<div class="table-box">' in c:
            c = c.replace('<div class="table-box">', hint_html + '<div class="table-box">')
            print(f"Injected hint div fallback to {file}")

    # 2. Wrap game-hint access with safety check
    old_hint_none = 'document.getElementById("game-hint").style.display = "none";'
    new_hint_none = 'const hintN = document.getElementById("game-hint"); if(hintN) hintN.style.display = "none";'
    c = c.replace(old_hint_none, new_hint_none)

    old_hint_block = 'document.getElementById("game-hint").style.display = "block";'
    new_hint_block = 'const hintB = document.getElementById("game-hint"); if(hintB) hintB.style.display = "block";'
    c = c.replace(old_hint_block, new_hint_block)
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"Hardened setHP in {file}")
