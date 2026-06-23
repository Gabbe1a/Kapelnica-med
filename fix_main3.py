import sys

with open('c:/Users/gabella/Desktop/TZ_for_Kapelnica-med/js/main.js', 'r', encoding='utf-8') as f:
    content = f.read()

idx1 = content.find('searchResults.innerHTML = filtered.map(')
idx2 = content.find('.join(\\'\\');', idx1) + len('.join(\\'\\');')

new_code = '''searchResults.innerHTML = filtered.map(item => \
            <a href="#" class="search-result-item js-open-drip-sheet">
                <div>
                    <div class="search-result-title">\</div>
                    <div class="search-result-desc">\</div>
                </div>
                <div class="search-result-arrow">→</div>
            </a>
        \).join('');'''

content = content[:idx1] + new_code + content[idx2:]

with open('c:/Users/gabella/Desktop/TZ_for_Kapelnica-med/js/main.js', 'w', encoding='utf-8') as f:
    f.write(content)
