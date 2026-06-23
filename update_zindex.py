import sys

with open('c:/Users/gabella/Desktop/TZ_for_Kapelnica-med/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Replace z-index: 1000; with z-index: 10000; in .search-dropdown
old_search_dropdown = """.search-dropdown {
    position: fixed;
    top: 80px; /* Below header */
    right: 20px; /* Align to the right like the icons */
    width: 360px;
    background: #ffffff;
    border-radius: 12px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
    z-index: 1000;"""

new_search_dropdown = """.search-dropdown {
    position: fixed;
    top: 80px; /* Below header */
    right: 20px; /* Align to the right like the icons */
    width: 360px;
    background: #ffffff;
    border-radius: 12px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
    z-index: 10000;"""

css = css.replace(old_search_dropdown, new_search_dropdown)

with open('c:/Users/gabella/Desktop/TZ_for_Kapelnica-med/css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Updated style.css z-index")
