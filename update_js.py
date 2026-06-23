import sys

with open('c:/Users/gabella/Desktop/TZ_for_Kapelnica-med/js/main.js', 'r', encoding='utf-8') as f:
    content = f.read()

start_str = '// Global Search Dropdown Logic'
# Find where the DOMContentLoaded ends. We can replace from start_str up to the end of file (assuming search logic is at the end)

start_idx = content.find(start_str)

new_js = """// Global Search Dropdown Logic
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

    function openSearchDropdown(isFooter) {
        if (!searchDropdown) return;
        
        if (isFooter) {
            searchDropdown.classList.add('footer-active');
        } else {
            searchDropdown.classList.remove('footer-active');
        }

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

    // Hide on scroll
    window.addEventListener('scroll', () => {
        if (searchDropdown && searchDropdown.classList.contains('active')) {
            closeSearchDropdown();
        }
    }, { passive: true });

    headerSearchOpeners.forEach(opener => {
        opener.addEventListener('click', (e) => {
            e.preventDefault();
            openSearchDropdown(false);
        });
    });

    if (footerSearchInput) {
        footerSearchInput.addEventListener('focus', () => {
            openSearchDropdown(true);
            if (globalSearchInput) globalSearchInput.value = footerSearchInput.value;
            renderResults(footerSearchInput.value);
        });
        footerSearchInput.addEventListener('input', (e) => {
            if (globalSearchInput) globalSearchInput.value = e.target.value;
            openSearchDropdown(true);
            renderResults(e.target.value);
        });
    }

    if (mobileSearchInput) {
        mobileSearchInput.addEventListener('focus', () => {
            openSearchDropdown(false);
            if (globalSearchInput) globalSearchInput.value = mobileSearchInput.value;
            renderResults(mobileSearchInput.value);
        });
        mobileSearchInput.addEventListener('input', (e) => {
            if (globalSearchInput) globalSearchInput.value = e.target.value;
            openSearchDropdown(false);
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

        searchResults.innerHTML = filtered.map(item => `
            <a href="#" class="search-result-item js-open-drip-sheet">
                <div>
                    <div class="search-result-title">${item.title}</div>
                    <div class="search-result-type">${item.type === 'drip' ? 'Капельница на дому' : 'Услуга'}</div>
                </div>
            </a>
        `).join('');

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
});"""

content = content[:start_idx] + new_js

with open('c:/Users/gabella/Desktop/TZ_for_Kapelnica-med/js/main.js', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated JS logic!")
