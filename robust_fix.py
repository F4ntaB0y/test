import re

for filename in ['pencemaran tanah.html', 'pencemaran udara.html']:
    with open(filename, 'r', encoding='utf-8') as f:
        c = f.read()
    
    if 'resetSimulasi();' in c:
        # Check if resetSimulasi is already defined inside triggerTimeout
        # Use broader search
        pass

    # Pattern to inject resetSimulasi() immediately after triggerVictory();
    pattern = r'(triggerVictory\(\);)'
    # Check if resetSimulasi is already present directly after triggerVictory
    if re.search(r'triggerVictory\(\);\s*resetSimulasi\(\);', c):
        print(f"{filename} already has the call.")
        continue
        
    new_c = re.sub(pattern, r'\1\n                    resetSimulasi();', c)
    
    if new_c != c:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_c)
        print(f"Fixed {filename} successfully!")
    else:
        print(f"Could not find triggerVictory pattern in {filename}.")
