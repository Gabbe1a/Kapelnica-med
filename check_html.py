import sys
import re

with open('c:/Users/gabella/Desktop/TZ_for_Kapelnica-med/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("Header:")
print(re.search(r'<div class="social-icons-group">.*?</div>', content, re.DOTALL).group(0))

print("\nFooter:")
print(re.search(r'<div class="footer-search">.*?</div>', content, re.DOTALL).group(0))

print("\nMobile:")
print(re.search(r'<div class="mobile-search-box">.*?</div>', content, re.DOTALL).group(0))
