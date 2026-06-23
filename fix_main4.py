import sys

with open('c:/Users/gabella/Desktop/TZ_for_Kapelnica-med/js/main.js', 'r', encoding='utf-8') as f:
    content = f.read()

idx1 = content.find('function renderResults(query) {')
idx2 = content.find('searchInput.addEventListener(\'input\'', idx1)

new_fn = '''function renderResults(query) {
        if (!query) {
            searchHints.style.display = 'block';
            searchResults.style.display = 'none';
            return;
        }

        searchHints.style.display = 'none';
        searchResults.style.display = 'block';

        const filtered = searchCatalog.filter(item => {
            return item.title.toLowerCase().includes(query.toLowerCase()) || item.keywords.toLowerCase().includes(query.toLowerCase());
        });

        if (filtered.length === 0) {
            searchResults.innerHTML = '<div class="search-empty">Ничего не найдено. Попробуйте другой запрос.</div>';
            return;
        }

        searchResults.innerHTML = filtered.map(item => \
            <a href="#" class="search-result-item js-open-drip-sheet">
                <div>
                    <div class="search-result-title">\</div>
                    <div class="search-result-desc">\</div>
                </div>
                <div class="search-result-arrow">&rarr;</div>
            </a>
        \).join('');

        searchResults.querySelectorAll('.js-open-drip-sheet').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                closeSearchModal();
                const dripBtn = document.getElementById('open-drip-sheet');
                if(dripBtn) dripBtn.click();
            });
        });
    }

    '''

content = content[:idx1] + new_fn + content[idx2:]

with open('c:/Users/gabella/Desktop/TZ_for_Kapelnica-med/js/main.js', 'w', encoding='utf-8') as f:
    f.write(content)
