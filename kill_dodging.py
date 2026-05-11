import re

files = ['pencemaran air.html', 'pencemaran tanah.html', 'pencemaran udara.html']

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        c = f.read()
    
    # Target pattern for annoying mouseover dodging code block
    pattern = r"el\.addEventListener\('mouseover', function\(e\) \{.*?\}\);\s*\n\s*"
    
    # Replace logic using re.DOTALL so it spans across lines
    cleaned_c = re.sub(r"el\.addEventListener\('mouseover', function\(e\) \{.*?\}\);", r"", c, flags=re.DOTALL)

    if cleaned_c != c:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(cleaned_c)
        print(f"Disabled dodging mechanic in {file} - stable target tracking achieved!")
    else:
        print(f"No dodging code detected in {file}")
