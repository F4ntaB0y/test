import re

### FILE 1: pencemaran tanah.html (OIL ENLARGEMENT & HOVER FIX)
t_path = 'pencemaran tanah.html'
with open(t_path, 'r', encoding='utf-8') as f:
    tc = f.read()

# 1. Amplify Oil base dimensions (currently 20x10)
tc = tc.replace('.pd1 { left: 20%; width: 20px; height: 10px; }', '.pd1 { left: 20%; width: 80px; height: 40px; }')
tc = tc.replace('.pd2 { left: 50%; width: 20px; height: 10px; animation-delay: 0.5s; }', '.pd2 { left: 45%; width: 100px; height: 50px; animation-delay: 0.5s; }')
tc = tc.replace('.pd3 { left: 80%; width: 20px; height: 10px; animation-delay: 1s; }', '.pd3 { left: 70%; width: 90px; height: 45px; animation-delay: 1s; }')

# 2. Crank up spreading animation scalar max and add jet-black saturation
tc = tc.replace('@keyframes spread { 0% { transform: scale(1); } 100% { transform: scale(8); } }', 
                '@keyframes spread { 0% { transform: scale(0.5); opacity: 0.5; } 100% { transform: scale(6); opacity: 0.95; } }')

# 3. Excise the hover transform glitch logic
tc = tc.replace('.clickable-pollution:hover { transform: scale(1.2) rotate(5deg) !important; filter: drop-shadow(0 0 25px white) brightness(1.5) !important; z-index: 100; }',
                '.clickable-pollution:hover { filter: drop-shadow(0 0 25px white) brightness(1.5) !important; z-index: 100; }')

# 4. Check for the other element specific hover glitch
tc = tc.replace('.p-item:hover, .trash-item:hover, .barrel-air:hover, .bubble:hover { transform: scale(1.2) rotate(5deg) !important; filter: brightness(1.5) drop-shadow(0 0 25px white) !important; }',
                '.p-item:hover, .trash-item:hover, .barrel-air:hover, .bubble:hover { filter: brightness(1.5) drop-shadow(0 0 25px white) !important; }')

with open(t_path, 'w', encoding='utf-8') as f:
    f.write(tc)
print("Soil File Patched: Oil dimensions quintupled and hover glitches extinguished.")


### FILE 2: pencemaran udara.html (HOVER STABILITY FIX)
u_path = 'pencemaran udara.html'
with open(u_path, 'r', encoding='utf-8') as f:
    uc = f.read()

uc = uc.replace('.clickable-pollution:hover { transform: scale(1.2) rotate(5deg) !important; filter: drop-shadow(0 0 25px white) brightness(1.5) !important; z-index: 100; }',
                '.clickable-pollution:hover { filter: drop-shadow(0 0 25px white) brightness(1.5) !important; z-index: 100; }')

with open(u_path, 'w', encoding='utf-8') as f:
    f.write(uc)
print("Air File Patched: Global hover stability backported.")
