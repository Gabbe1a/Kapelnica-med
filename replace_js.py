import sys
import re

with open('c:/Users/gabella/Desktop/TZ_for_Kapelnica-med/js/main.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_idx = content.find('const searchModal =')

new_js = '''
    // Global Search Dropdown Logic
    const searchDropdown = document.getElementById('searchDropdown');
    const globalSearchInput = document.getElementById('globalSearchInput');
    const searchDropdownClose = document.getElementById('searchDropdownClose');
    const searchHints = document.getElementById('searchHints');
    const searchResults = document.getElementById('searchResults');
    const searchNoResults = document.getElementById('searchNoResults');
    const hintTags = document.querySelectorAll('.search-hint-tag');

    const headerSearchOpeners = document.querySelectorAll('.js-open-search-modal');
    const footerSearchInput = document.querySelector('.footer-search-input');
    const mobileSearchInput = document.querySelector('.mobile-search-input');

    function openSearchDropdown() {
        if (!searchDropdown) return;
        searchDropdown.classList.add('active');
        setTimeout(() => { if (globalSearchInput) globalSearchInput.focus(); }, 50);
    }

    function closeSearchDropdown() {
        if (!searchDropdown) return;
        searchDropdown.classList.remove('active');
        if (globalSearchInput) globalSearchInput.value = '';
        if (footerSearchInput) footerSearchInput.value = '';
        if (mobileSearchInput) mobileSearchInput.value = '';
        renderResults('');
    }

    headerSearchOpeners.forEach(opener => {
        opener.addEventListener('click', (e) => {
            e.preventDefault();
            openSearchDropdown();
        });
    });

    if (footerSearchInput) {
        footerSearchInput.addEventListener('focus', () => {
            openSearchDropdown();
            if (globalSearchInput) globalSearchInput.value = footerSearchInput.value;
            renderResults(footerSearchInput.value);
        });
        footerSearchInput.addEventListener('input', (e) => {
            if (globalSearchInput) globalSearchInput.value = e.target.value;
            openSearchDropdown();
            renderResults(e.target.value);
        });
    }

    if (mobileSearchInput) {
        mobileSearchInput.addEventListener('focus', () => {
            openSearchDropdown();
            if (globalSearchInput) globalSearchInput.value = mobileSearchInput.value;
            renderResults(mobileSearchInput.value);
        });
        mobileSearchInput.addEventListener('input', (e) => {
            if (globalSearchInput) globalSearchInput.value = e.target.value;
            openSearchDropdown();
            renderResults(e.target.value);
        });
    }

    if (searchDropdownClose) {
        searchDropdownClose.addEventListener('click', closeSearchDropdown);
    }

    document.addEventListener('click', (e) => {
        if (searchDropdown && searchDropdown.classList.contains('active')) {
            const isClickInside = searchDropdown.contains(e.target);
            const isOpener = Array.from(headerSearchOpeners).some(opener => opener.contains(e.target));
            const isFooterInput = footerSearchInput && footerSearchInput.contains(e.target);
            const isMobileInput = mobileSearchInput && mobileSearchInput.contains(e.target);
            
            if (!isClickInside && !isOpener && !isFooterInput && !isMobileInput) {
                closeSearchDropdown();
            }
        }
    });

    function renderResults(query) {
        if (!searchHints || !searchResults || !searchNoResults) return;
        if (!query) {
            searchHints.style.display = "block";
            searchResults.style.display = "none";
            searchNoResults.style.display = "none";
            return;
        }

        searchHints.style.display = "none";
        
        const filtered = searchCatalog.filter(item => {
            return item.title.toLowerCase().includes(query.toLowerCase()) || item.keywords.toLowerCase().includes(query.toLowerCase());
        });

        if (filtered.length === 0) {
            searchResults.style.display = "none";
            searchNoResults.style.display = "block";
            return;
        }

        searchNoResults.style.display = "none";
        searchResults.style.display = "flex";

        searchResults.innerHTML = filtered.map(item => 
            <a href="#" class="search-result-item js-open-drip-sheet">
                <div>
                    <div class="search-result-title"> + item.title + </div>
                    <div class="search-result-type"> + (item.type === 'drip' ? 'Капельница на дому' : 'Услуга') + </div>
                    <div class="search-result-desc"> + item.desc + </div>
                </div>
            </a>
        ).join('');

        searchResults.querySelectorAll('.js-open-drip-sheet').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                closeSearchDropdown();
                const dripBtn = document.getElementById('open-drip-sheet');
                if(dripBtn) dripBtn.click();
            });
        });
    }

    if (globalSearchInput) {
        globalSearchInput.addEventListener('input', (e) => {
            const val = e.target.value;
            if (footerSearchInput) footerSearchInput.value = val;
            if (mobileSearchInput) mobileSearchInput.value = val;
            renderResults(val);
        });
    }

    hintTags.forEach(tag => {
        tag.addEventListener('click', () => {
            if (globalSearchInput) globalSearchInput.value = tag.textContent;
            renderResults(tag.textContent);
        });
    });
});
'''

new_content = content[:start_idx] + new_js

with open('c:/Users/gabella/Desktop/TZ_for_Kapelnica-med/js/main.js', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Replaced!")
