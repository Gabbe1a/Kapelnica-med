import sys
import re

with open('c:/Users/gabella/Desktop/TZ_for_Kapelnica-med/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

svg_close = """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#888" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>"""

content = content.replace('<img src="design-assets/x.svg" alt="" width="20" height="20">', svg_close)

with open('c:/Users/gabella/Desktop/TZ_for_Kapelnica-med/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Replaced close icon!")
