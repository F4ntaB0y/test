import re

files = ['pencemaran air.html', 'pencemaran tanah.html', 'pencemaran udara.html']

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        c = f.read()
    
    # 1. Ensure active-pollution makes containers interactive
    c = c.replace('.active-pollution { opacity: 1 !important; }', 
                  '.active-pollution { opacity: 1 !important; pointer-events: auto !important; }')

    # 2. Explicitly ensure .clickable-pollution is interactive regardless of parent pointer-events none
    old_cl = '.clickable-pollution { cursor: crosshair !important;'
    new_cl = '.clickable-pollution { pointer-events: auto !important; cursor: crosshair !important;'
    c = c.replace(old_cl, new_cl)

    # 3. For smoke specifically (udara.html), verify that individual pieces aren't forced invisible via parent's container
    # Ensure .car-smoke-container active state overrides pointer-events
    c = c.replace('.active-pollution { opacity: 1 !important; }', 
                  '.active-pollution { opacity: 1 !important; pointer-events: auto !important; }')
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(c)
    
    print(f"Forced pointer-events auto on {file}")
