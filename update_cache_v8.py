import sys
with open('c:/Users/gabella/Desktop/TZ_for_Kapelnica-med/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('href="css/style.css?v=7"', 'href="css/style.css?v=8"')

with open('c:/Users/gabella/Desktop/TZ_for_Kapelnica-med/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated cache bust parameter to v=8.")
