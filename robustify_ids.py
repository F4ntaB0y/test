import re

with open('pencemaran udara.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Fix the background-clip warning the user requested
c = c.replace('-webkit-background-clip: text;', '-webkit-background-clip: text; background-clip: text;')

# Rename conflicting element IDs to unique names
c = c.replace('id="air"', 'id="status-air"')
c = c.replace('id="langit"', 'id="status-langit"')
c = c.replace('id="manusia"', 'id="status-manusia"')
c = c.replace('id="lingkungan"', 'id="status-lingkungan"')

# Update JavaScript calls to the new IDs
c = c.replace('document.getElementById("air").innerHTML', 'document.getElementById("status-air").innerHTML')
c = c.replace('document.getElementById("langit").innerHTML', 'document.getElementById("status-langit").innerHTML')
c = c.replace('document.getElementById("manusia").innerHTML', 'document.getElementById("status-manusia").innerHTML')
c = c.replace('document.getElementById("lingkungan").innerHTML', 'document.getElementById("status-lingkungan").innerHTML')

with open('pencemaran udara.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("IDs updated to ensure total robustness!")
