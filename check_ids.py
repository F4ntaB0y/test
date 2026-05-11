import re
with open('pencemaran udara.html', 'r', encoding='utf-8') as f:
    c = f.read()
matches = re.findall(r'id=["\'](.*?)["\']', c)
for m in matches:
    if m in ['air','langit','manusia','lingkungan']:
        print(f"Found ID: {m}")
