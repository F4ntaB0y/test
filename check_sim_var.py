import re
with open('pencemaran udara.html', 'r', encoding='utf-8') as f:
    c = f.read()
matches = re.findall(r'(const|let|var)\s+simulation\s*=', c)
print(f"Simulation declarations count: {len(matches)}")
for m in matches:
    print(m)
