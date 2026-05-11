import re

files = ['index.html', 'pencemaran air.html', 'pencemaran tanah.html', 'pencemaran udara.html']

for file in files:
    try:
        with open(file, 'r', encoding='utf-8') as f:
            c = f.read()
        
        # Ensure background-clip: text follows -webkit-background-clip: text;
        if '-webkit-background-clip: text;' in c and 'background-clip: text;' not in c:
            c = c.replace('-webkit-background-clip: text;', '-webkit-background-clip: text; background-clip: text;')
            with open(file, 'w', encoding='utf-8') as f:
                f.write(c)
            print(f"Fixed file: {file}")
    except Exception as e:
        print(f"Failed processing {file}: {e}")

print("Done cleaning compatibility warnings.")
