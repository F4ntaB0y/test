import re

file_path = 'pencemaran air.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove Health Bar Container HTML
content = re.sub(r'<!-- GAME CSS -->.*?/\* JUICE EFFECTS \*/.*?\.confetti[^}]+}', '', content, flags=re.DOTALL)
content = re.sub(r'<div class="health-bar-container">.*?</div>\s*</div>', '', content, flags=re.DOTALL)

# 2. Remove game-hint HTML
content = re.sub(r'<div class="game-hint".*?</div>', '', content)

# 3. Wipe JS logic section completely
content = re.sub(r'// GAME LOGIC.*?setTimeout\(\(\) => \{.*?\}, 500\);', '', content, flags=re.DOTALL)

# 4. Clean up specific styling classes linked to the game leftover from deletion
content = re.sub(r'\.health-bar-container \{[^}]+\}', '', content)
content = re.sub(r'\.hp-low \{[^}]+\}', '', content)
content = re.sub(r'\.hp-mid \{[^}]+\}', '', content)

# 5. Clean up the JS trigger calls in the button handlers
content = content.replace('setHP(50, true); resetPollutionVisibility(\'.bubble\');', '')
content = content.replace('setHP(40, true); resetPollutionVisibility(\'.barrel-air\');', '')
content = content.replace('setHP(40, true); resetPollutionVisibility(\'.trash-item\');', '')
content = content.replace('setHP(20, true);', '')
content = content.replace('setHP(100, false, true);', '')

# Explicit removals of leftover JS wrappers
content = re.sub(r'function resetPollutionVisibility.*?\}', '', content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Game mode purged completely from pencemaran air.html.")
