import sys
with open('c:/Users/gabella/Desktop/TZ_for_Kapelnica-med/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('src="js/main.js?v=6"', 'src="js/main.js?v=7"')
content = content.replace('href="css/style.css?v=6"', 'href="css/style.css?v=7"')

with open('c:/Users/gabella/Desktop/TZ_for_Kapelnica-med/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated cache bust parameter to v=7.")
