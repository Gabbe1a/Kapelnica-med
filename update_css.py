import sys

with open('c:/Users/gabella/Desktop/TZ_for_Kapelnica-med/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Replace the existing .search-dropdown.footer-active block
old_css_1 = """.search-dropdown.footer-active {
    top: auto;
    bottom: 80px; /* Above the footer */
    right: 50%;
    transform: translateX(50%) translateY(10px);
}
.search-dropdown.footer-active.active {
    transform: translateX(50%) translateY(0);
}"""

new_css_1 = """.search-dropdown.footer-active {
    top: auto;
    bottom: auto; /* Handled by JS */
    left: auto;   /* Handled by JS */
    right: auto;
    transform: translateY(10px);
}
.search-dropdown.footer-active.active {
    transform: translateY(0);
}"""

css = css.replace(old_css_1, new_css_1)

old_css_2 = """@media (max-width: 768px) {
    .search-dropdown.footer-active {
        bottom: 80px;
        left: 5%;
        right: 5%;
        width: 90%;
        transform: translateY(10px);
    }
    .search-dropdown.footer-active.active {
        transform: translateY(0);
    }
}"""

new_css_2 = """@media (max-width: 768px) {
    .search-dropdown.footer-active {
        bottom: auto; /* Handled by JS */
        left: 5% !important; /* Override JS on mobile */
        right: 5% !important;
        width: 90%;
        transform: translateY(10px);
    }
    .search-dropdown.footer-active.active {
        transform: translateY(0);
    }
}"""

css = css.replace(old_css_2, new_css_2)

with open('c:/Users/gabella/Desktop/TZ_for_Kapelnica-med/css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Updated style.css")
