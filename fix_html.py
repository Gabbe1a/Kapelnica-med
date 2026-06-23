import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = re.sub(r'<img src=\&#34;design-assets/icon_detox.svg\&#34;[^>]+>', '<img src="design-assets/icon_detox.svg" alt="Детокс" class="card-icon detox-icon">', html)
html = re.sub(r'<img src=\&#34;design-assets/icon_energy.svg\&#34;[^>]+>', '<img src="design-assets/icon_energy.svg" alt="Энергия" class="card-icon energy-icon">', html)
html = re.sub(r'<img src=\&#34;design-assets/icon_beauty.svg\&#34;[^>]+>', '<img src="design-assets/icon_beauty.svg" alt="Золушка" class="card-icon beauty-icon">', html)

html = html.replace('\&#34;', '"')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

