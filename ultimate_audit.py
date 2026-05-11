import re, os

def patch_file(filepath, selectors, reset_logic_line):
    with open(filepath, 'r', encoding='utf-8') as f:
        c = f.read()
        
    print(f"\nAuditing {filepath}...")
    
    # 1. Check/Incorporate reset function
    reset_func_code = f"""
function resetGameElements() {{
    document.querySelectorAll('{selectors}').forEach(el => {{
        el.style.display = "";
        el.style.opacity = "";
        el.style.pointerEvents = "";
        el.style.transform = "translate(0,0)";
    }});
}}
"""
    if "function resetGameElements" not in c:
        print(" -> Injecting resetGameElements() helper...")
        c = c.replace('</script>', reset_func_code + '\n</script>')
    
    # 2. Inject it into resetSimulasi immediately at the start of implementation
    if 'resetGameElements();' not in c:
        print(" -> Linking helper into resetSimulasi...")
        pattern = r'function resetSimulasi\(\)\s*\{'
        c = re.sub(pattern, r'function resetSimulasi(){\n    resetGameElements();', c)
    
    # 3. HARDCODE FIX: If victory logic doesn't call resetSimulasi(), inject it robustly!
    # Check for triggerVictory without resetSimulasi following it in timeout block
    if 'triggerVictory();' in c and 'resetSimulasi();' not in re.sub(r'\s+', '', c.split('triggerVictory();')[1][:100]):
         print(" -> Injecting resetSimulasi into victory timeout cascade...")
         c = c.replace('triggerVictory();\n                }', 'triggerVictory();\n                    resetSimulasi();\n                }')
         c = c.replace('triggerVictory();\n                    }, 300);', 'triggerVictory();\n                    resetSimulasi();\n                    }, 300);')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f" -> Audit Complete for {filepath}")

# Patch the other files 
patch_file('pencemaran tanah.html', '.trash, .barrel-tanah, .puddle, .gas', 'hideAllPollution();')
patch_file('pencemaran udara.html', '.factory-smoke, .cs', 'clearPollution();')

print("\nALL SYSTEMS FULLY SYNCHRONIZED!")
