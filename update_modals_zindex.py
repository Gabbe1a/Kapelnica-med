import sys

with open('c:/Users/gabella/Desktop/TZ_for_Kapelnica-med/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Replace z-index: 1000; in .sheet-overlay
old_sheet = """.sheet-overlay {
  position: fixed;
  inset: 0;
  z-index: 1000;"""

new_sheet = """.sheet-overlay {
  position: fixed;
  inset: 0;
  z-index: 10001;"""

css = css.replace(old_sheet, new_sheet)

# Replace z-index: 1000; in .consultation-overlay
old_consult = """.consultation-overlay {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1000;"""

new_consult = """.consultation-overlay {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 10001;"""

css = css.replace(old_consult, new_consult)

with open('c:/Users/gabella/Desktop/TZ_for_Kapelnica-med/css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Updated modals z-index")
