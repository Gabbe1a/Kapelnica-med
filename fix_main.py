import sys

with open('c:/Users/gabella/Desktop/TZ_for_Kapelnica-med/js/main.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix backticks missing in searchResults.innerHTML
old_code = '''searchResults.innerHTML = filtered.map(item => 
            <a href="#" class="search-result-item js-open-drip-sheet">
                <div>
                    <div class="search-result-title"> + item.title + </div>
                    <div class="search-result-desc"> + (item.type === 'drip' ? 'Капельница на дому' : 'Сдача анализов') + </div>
                </div>
                <div class="search-result-arrow">→</div>
            </a>
        ).join('');'''

new_code = '''searchResults.innerHTML = filtered.map(item => \
            <a href="#" class="search-result-item js-open-drip-sheet">
                <div>
                    <div class="search-result-title">\</div>
                    <div class="search-result-desc">\</div>
                </div>
                <div class="search-result-arrow">→</div>
            </a>
        \).join('');'''

content = content.replace(old_code, new_code)

with open('c:/Users/gabella/Desktop/TZ_for_Kapelnica-med/js/main.js', 'w', encoding='utf-8') as f:
    f.write(content)
