import sys
import re

with open('c:/Users/gabella/Desktop/TZ_for_Kapelnica-med/js/main.js', 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(
    r'searchResults\.innerHTML = filtered\.map\(item =>\s*<a href="#" class="search-result-item js-open-drip-sheet">.*?</a>\s*\)\.join\(\'\'\);',
    '''searchResults.innerHTML = filtered.map(item => \
            <a href="#" class="search-result-item js-open-drip-sheet">
                <div>
                    <div class="search-result-title">\</div>
                    <div class="search-result-desc">\</div>
                </div>
                <div class="search-result-arrow">→</div>
            </a>
        \).join('');''',
    content,
    flags=re.DOTALL
)

with open('c:/Users/gabella/Desktop/TZ_for_Kapelnica-med/js/main.js', 'w', encoding='utf-8') as f:
    f.write(content)
