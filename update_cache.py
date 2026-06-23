import sys
with open('c:/Users/gabella/Desktop/TZ_for_Kapelnica-med/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('src="js/main.js?v=3"', 'src="js/main.js?v=4"')

with open('c:/Users/gabella/Desktop/TZ_for_Kapelnica-med/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated cache bust parameter.")
