import re

file_path = 'pencemaran air.html'

with open(file_path, 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Upgrade the FOAM background to be a dynamic undulating pattern!
dynamic_foam_css = """
        @keyframes foamRipple {
            0% { background-position: 0% 50%; }
            100% { background-position: 100% 50%; }
        }
        .foam {
            background: linear-gradient(45deg, #e2e8f0 25%, #94a3b8 25%, #94a3b8 50%, #e2e8f0 50%, #e2e8f0 75%, #94a3b8 75%, #94a3b8 100%) !important;
            background-size: 100px 100px !important;
            animation: foamRipple 20s linear infinite !important;
        }
"""
# Replace the old static .foam rule
old_foam_pattern = r'\.foam\s*\{\s*background:\s*linear-gradient\([^)]+\)\s*!important;\s*\}'
c = re.sub(old_foam_pattern, dynamic_foam_css, c)

# 2. Fix the bubble selector hierarchy to ensure RISE works alongside dangerPulse, forcefully!
bubble_fix = """
        /* ULTIMATE BUBBLE FORCE COMPOSITOR */
        .foam-bubbles .bubble.clickable-pollution {
            animation: rise 4s infinite ease-in, dangerPulse 2s infinite ease-in-out !important;
            z-index: 2000 !important;
        }
"""
# Inject right before closing </style> tag
c = c.replace('</style>', bubble_fix + '\n</style>')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(c)

print("Dynamic foam physics and bubble compositor activated.")
