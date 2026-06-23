import sys
import re

with open('c:/Users/gabella/Desktop/TZ_for_Kapelnica-med/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

dropdown_html = '''
    <!-- Search Dropdown -->
    <div class="search-dropdown" id="searchDropdown">
        <div class="search-dropdown-header">
            <input type="text" id="globalSearchInput" class="search-dropdown-input" placeholder="Поиск по услугам..." autocomplete="off">
            <button class="search-dropdown-close" id="searchDropdownClose" aria-label="Закрыть">
                <img src="design-assets/x.svg" alt="" width="20" height="20">
            </button>
        </div>
        <div class="search-dropdown-body">
            <div class="search-hints" id="searchHints">
                <p class="search-hints-title">Например, вы искали:</p>
                <div class="search-hints-tags">
                    <span class="search-hint-tag">Мигрень</span>
                    <span class="search-hint-tag">Слабость</span>
                    <span class="search-hint-tag">Детокс</span>
                    <span class="search-hint-tag">Витамины</span>
                </div>
            </div>
            <div class="search-results-list" id="searchResults"></div>
            <div class="search-no-results" id="searchNoResults" style="display: none;">
                По вашему запросу ничего не найдено.
            </div>
        </div>
    </div>
'''

content = content.replace('</body>', dropdown_html + '\n</body>')

with open('c:/Users/gabella/Desktop/TZ_for_Kapelnica-med/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
