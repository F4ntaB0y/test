import re

files = ['index.html', 'pencemaran air.html', 'pencemaran tanah.html', 'pencemaran udara.html']

for file in files:
    try:
        with open(file, 'r', encoding='utf-8') as f:
            c = f.read()
        
        # Robust substitution using regex to insert background-clip directly after webkit-background-clip
        if re.search(r'-webkit-background-clip:\s*text;', c):
            if not re.search(r'[^-]background-clip:\s*text;', c):
                # Insert right after it, preserving whatever indentation/newlines were present
                c = re.sub(r'(-webkit-background-clip:\s*text;)', r'\1 background-clip: text;', c)
                with open(file, 'w', encoding='utf-8') as f:
                    f.write(c)
                print(f"Successfully robust-patched {file}")
            else:
                 print(f"{file} already has background-clip.")
        else:
            print(f"Skipped {file} - no match.")
    except Exception as e:
        print(f"Error in {file}: {e}")
