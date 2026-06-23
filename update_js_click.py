import sys

with open('c:/Users/gabella/Desktop/TZ_for_Kapelnica-med/js/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_click = """        searchResults.querySelectorAll('.js-open-drip-sheet').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                closeSearchDropdown();
                const dripBtn = document.getElementById('open-drip-sheet');
                if(dripBtn) dripBtn.click();
            });
        });"""

new_click = """        searchResults.querySelectorAll('.js-open-drip-sheet').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                closeSearchDropdown();
                // Close mobile menu if open
                const mobileNavClose = document.getElementById('mobileNavClose');
                if (mobileNavClose) mobileNavClose.click();
                
                const dripBtn = document.getElementById('open-drip-sheet');
                if(dripBtn) dripBtn.click();
            });
        });"""

js = js.replace(old_click, new_click)

with open('c:/Users/gabella/Desktop/TZ_for_Kapelnica-med/js/main.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated JS click logic")
