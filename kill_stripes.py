import re

file_path = 'pencemaran air.html'

with open(file_path, 'r', encoding='utf-8') as f:
    c = f.read()

print(f"Initial length: {len(c)}")

# Targeted, rigid chunk removal of the problematic stripe implementation:
start_marker = "@keyframes foamRipple"
# Find where it ends!
idx_start = c.find(start_marker)
if idx_start == -1:
    print("CRITICAL ERROR: Could not locate starting animation marker!")
    exit(1)

# Scan forward to the first occurrence of the end of the `.foam { ... }` block
# Look for the second closing brace `}` that signifies the end of the .foam class definition itself.
# Let's just scan forward to find the full block up to the dynamic footer!
end_target = "!important;\n        }"
idx_end = c.find(end_target, idx_start)

if idx_end == -1:
    print("CRITICAL ERROR: Could not locate end of definition!")
    exit(1)

# Calculate accurate replacement range!
# We want to span from @keyframes until the complete closing brace of the .foam block.
actual_end = idx_end + len(end_target)

bad_block = c[idx_start:actual_end]
print(f"Found block to annihilate (Length {len(bad_block)}):\n---CONTENT---\n{bad_block}\n---END---")

# Substitute back the pure, clean, static gradient originally intended!
clean_original = """
        .foam {
            background: linear-gradient(180deg, #94a3b8 0%, #475569 100%) !important;
        }
"""

new_c = c[:idx_start] + clean_original + c[actual_end:]

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_c)

print("\nFINAL CONFIRMATION SCRUB COMPLETE. Industrial Stripes Decapitated Successfully!")
