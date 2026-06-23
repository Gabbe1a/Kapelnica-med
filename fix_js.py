import sys

with open('c:/Users/gabella/Desktop/TZ_for_Kapelnica-med/js/main.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_str = 'searchResults.innerHTML = filtered.map(item =>'
end_str = ').join(\\'\\');'

start_idx = content.find(start_str)
end_idx = content.find(end_str, start_idx) + len(end_str)

if start_idx != -1 and end_idx != -1:
    new_code = '''searchResults.innerHTML = filtered.map(item => 
            <a href="#" class="search-result-item js-open-drip-sheet">
                <div>
                    <div class="search-result-title"></div>
                    <div class="search-result-type"></div>
                    <div class="search-result-desc"></div>
                </div>
            </a>
        ).join('');'''
    content = content[:start_idx] + new_code + content[end_idx:]
    with open('c:/Users/gabella/Desktop/TZ_for_Kapelnica-med/js/main.js', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed JS syntax in main.js!")
else:
    print("Could not find the block to replace")
