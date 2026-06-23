import sys
import re

with open('c:/Users/gabella/Desktop/TZ_for_Kapelnica-med/js/main.js', 'r', encoding='utf-8') as f:
    content = f.read()

# I want to find the start of "const searchModal =" or "// Search Functionality"
start_idx = content.find('const searchModal =')
if start_idx == -1:
    start_idx = content.find('// Умный поиск по сайту')

print("Found search section at index:", start_idx)
if start_idx != -1:
    print(content[start_idx:start_idx+500])
