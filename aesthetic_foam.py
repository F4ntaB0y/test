import re

file_path = 'pencemaran air.html'

with open(file_path, 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Craft the Soft Organic Foam Texture replacements
soft_foam_css = """
        @keyframes foamBoil {
            0% { background-position: 0% 20%; filter: blur(0.5px); }
            50% { background-position: 100% 80%; filter: blur(2px); }
            100% { background-position: 0% 20%; filter: blur(0.5px); }
        }
        .foam {
            background: 
                radial-gradient(circle at 20% 20%, rgba(255,255,255,0.9) 0%, transparent 60%),
                radial-gradient(circle at 80% 30%, rgba(255,255,255,0.8) 0%, transparent 50%),
                radial-gradient(circle at 40% 80%, rgba(255,255,255,0.7) 0%, transparent 70%),
                radial-gradient(circle at 90% 90%, rgba(255,255,255,0.8) 0%, transparent 50%),
                linear-gradient(180deg, #e2e8f0 0%, #94a3b8 100%) !important;
            background-size: 200% 200% !important;
            animation: foamBoil 8s ease-in-out infinite alternate !important;
        }
"""

# Regular expression to find the old stripey foam block:
old_stripe_pattern = r'@keyframes foamRipple\s*\{[^}]+\}\s*\.foam\s*\{[^}]+\}'
# Let's perform a fuzzy match check to be certain
if 'foamRipple' in c:
    c = re.sub(old_stripe_pattern, soft_foam_css, c)
    print("Successfully swapped industrial stripes for organic cloud foam.")
else:
    print("Could not find foamRipple in the current file contents.")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(c)
