import re

u_path = 'pencemaran udara.html'
with open(u_path, 'r', encoding='utf-8') as f:
    c = f.read()

old_fire_css = '.fire { position: absolute; bottom: 100px; left: 50%; transform: translateX(-50%); font-size: 110px; display: none; animation: fireAnim 0.5s infinite alternate; filter: drop-shadow(0 -10px 20px #ef4444); }'

new_fire_css = """
        .fire { 
            position: absolute; 
            bottom: 115px; 
            right: 10px; 
            font-size: 95px; 
            display: none; 
            animation: fireAnim 0.5s infinite alternate, sway 4s infinite alternate ease-in-out; 
            transform-origin: bottom; 
            filter: drop-shadow(0 -10px 30px #ef4444) brightness(1.3); 
            z-index: 1001 !important; 
            pointer-events: auto !important;
        }"""

if old_fire_css in c:
    c = c.replace(old_fire_css, new_fire_css)
    print("Successfully anchored fire to the tree structure.")
else:
    print("Warning: Target CSS not matched exactly.")
    print(f"Snippet in file: {c[c.find('.fire {'):c.find('.fire {')+100]}")

with open(u_path, 'w', encoding='utf-8') as f:
    f.write(c)
