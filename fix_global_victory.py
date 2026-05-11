import os

for filename in ['pencemaran tanah.html', 'pencemaran udara.html']:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'triggerVictory();' in content and 'resetSimulasi();' not in content:
        print(f"Fixing {filename}")
        content = content.replace('triggerVictory();\n                }, 300);', 'triggerVictory();\n                    resetSimulasi();\n                }, 300);')
        content = content.replace('triggerVictory();\n                }, 500);', 'triggerVictory();\n                    resetSimulasi();\n                }, 500);')
        content = content.replace('triggerVictory();\n                    resetSimulasi();\n                }, 300);', 'triggerVictory();\n                    resetSimulasi();\n                }, 300);') # Noop to catch duplicate
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filename}")
    else:
        print(f"{filename} does not require update or logic differed.")
