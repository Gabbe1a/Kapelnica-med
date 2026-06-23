import sys
import re

with open('c:/Users/gabella/Desktop/TZ_for_Kapelnica-med/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the search modal
content = re.sub(r'<!-- Search Modal -->.*?<div class="modal-overlay" id="searchModal" aria-hidden="true" role="dialog">.*?</body>', '</body>', content, flags=re.DOTALL)

with open('c:/Users/gabella/Desktop/TZ_for_Kapelnica-med/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
