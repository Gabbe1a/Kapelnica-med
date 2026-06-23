import sys

with open('c:/Users/gabella/Desktop/TZ_for_Kapelnica-med/js/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_func = """    function openSearchDropdown(isFooter) {
        if (!searchDropdown) return;
        
        if (isFooter) {
            searchDropdown.classList.add('footer-active');
        } else {
            searchDropdown.classList.remove('footer-active');
        }

        searchDropdown.classList.add('active');
        setTimeout(() => { if (globalSearchInput) globalSearchInput.focus(); }, 50);
    }"""

new_func = """    function openSearchDropdown(isFooter) {
        if (!searchDropdown) return;
        
        // Reset dynamic styles
        searchDropdown.style.bottom = '';
        searchDropdown.style.left = '';
        searchDropdown.style.width = '';
        
        if (isFooter && footerSearchInput) {
            searchDropdown.classList.add('footer-active');
            const rect = footerSearchInput.getBoundingClientRect();
            // Position exactly above the footer input
            searchDropdown.style.bottom = (window.innerHeight - rect.top + 10) + 'px';
            searchDropdown.style.left = rect.left + 'px';
            
            // On desktop, limit width to match input approximately, 
            // but searchDropdown has max-width: 400px.
            // Let's ensure it has at least the input width:
            searchDropdown.style.width = Math.max(rect.width, 300) + 'px';
        } else {
            searchDropdown.classList.remove('footer-active');
        }

        searchDropdown.classList.add('active');
        setTimeout(() => { if (globalSearchInput) globalSearchInput.focus(); }, 50);
    }"""

js = js.replace(old_func, new_func)

with open('c:/Users/gabella/Desktop/TZ_for_Kapelnica-med/js/main.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated JS func")
