import re

files = ['pencemaran air.html', 'pencemaran tanah.html', 'pencemaran udara.html']

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove the shake logic
    content = content.replace('document.body.classList.add("shake");\n            setTimeout(()=>document.body.classList.remove("shake"), 500);', '')
    
    # Optional: also remove the .shake CSS just to be clean
    content = re.sub(r'\.shake \{ animation: shakeAnim.*?\n.*?@keyframes shakeAnim \{.*?\}\n', '', content, flags=re.DOTALL)
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Shake removed!")
