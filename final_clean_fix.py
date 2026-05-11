import re

files = ['pencemaran air.html', 'pencemaran tanah.html', 'pencemaran udara.html']

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        c = f.read()
    
    # FIX: Revert the container back to pointer-events: none so it doesn't swallow mouse events!
    # Only children (clickable-pollution) will catch them!
    c = c.replace('.active-pollution { opacity: 1 !important; pointer-events: auto !important; }', 
                  '.active-pollution { opacity: 1 !important; }')
    
    # Extra safe: double ensure containers are none, children are auto
    # Look for container definitions and make sure they have pointer-events: none;
    c = re.sub(r'(\.foam-bubbles.*?) {', r'\1 { pointer-events: none !important;', c)
    c = re.sub(r'(\.plastic-waste.*?) {', r'\1 { pointer-events: none !important;', c)
    c = re.sub(r'(\.toxic-waste.*?) {', r'\1 { pointer-events: none !important;', c)
    c = re.sub(r'(\.pestisida-gas.*?) {', r'\1 { pointer-events: none !important;', c)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"Container shield deactivated for {file} - only target objects will catch clicks!")
