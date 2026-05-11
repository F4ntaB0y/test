import re, os

files = ['index.html', 'pencemaran air.html', 'pencemaran udara.html', 'pencemaran tanah.html']

favicon_link = '<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🔬</text></svg>">'

for f_path in files:
    if not os.path.exists(f_path):
        continue
        
    with open(f_path, 'r', encoding='utf-8') as f:
        c = f.read()
        
    if 'rel="icon"' in c or 'favicon.ico' in c:
        print(f"Favicon already handled in {f_path}")
        continue
        
    print(f"Injecting favicon into {f_path}...")
    c = c.replace('<head>', '<head>\n    ' + favicon_link)
    
    with open(f_path, 'w', encoding='utf-8') as f:
        f.write(c)

print("\nFavicon suppression injected site-wide successfully.")
