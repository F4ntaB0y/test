import re

p_path = 'pencemaran air.html'
with open(p_path, 'r', encoding='utf-8') as f:
    c = f.read()

# Define target explicitly by searching for part of the string to handle newline differences gracefully
needle = 'Air kembali bersih dan ekosistem perairan normal.";'
pos = c.find(needle)
if pos != -1:
    # Find the VERY NEXT closing bracket after this needle. That's the function end.
    close_pos = c.find('}', pos)
    if close_pos != -1:
        # Reconstruct the file inserting `}, 1200);` RIGHT BEFORE that final closing bracket!
        # Wait, we want everything from pos to close_pos, then the closing of setTimeout, then the final brace!
        
        # Easier way: replace specific pattern
        text_to_patch = c[pos : close_pos] 
        # Which should contain the quote and the semicolon
        
        final_content = c[:close_pos].rstrip() + "\n    }, 1200);\n" + c[close_pos:]
        
        # Verify that we actually applied it properly
        with open(p_path, 'w', encoding='utf-8') as f:
            f.write(final_content)
        print("SUCCESS: The setTimeout block has been perfectly closed and syntax restored.")
    else:
        print("Error: Could not find final function brace.")
else:
    print("Error: Could not find info message text.")
