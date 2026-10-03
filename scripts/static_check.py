from pathlib import Path
import re, sys
root=Path(__file__).resolve().parents[1]
html=root/"index.html"
if not html.is_file(): raise SystemExit("index.html missing")
text=html.read_text(encoding="utf-8")
errors=[]
for attr in ("href","src"):
 for value in re.findall(rf'{attr}=["\']([^"\']+)["\']',text):
  if value.startswith(("http://","https://","mailto:","tel:","#","data:","javascript:")) or not value: continue
  target=root/value.split("#",1)[0].split("?",1)[0]
  if not target.exists(): errors.append(f"missing local {attr}: {value}")
low=text.lower()
for token,label in [("<html","html element"),("<title>","title"),('name="description"',"meta description"),('name="viewport"',"viewport"),("skip-link","skip link"),("prefers-reduced-motion","reduced-motion support")]:
 if token not in low: errors.append(f"missing {label}")
if 'target="_blank"' in text:
 for tag in re.findall(r'<a\b[^>]*target="_blank"[^>]*>',text,re.I):
  if 'rel="noopener noreferrer"' not in tag: errors.append("external blank link missing noopener/noreferrer")
if errors:
 print("\n".join(errors)); sys.exit(1)
print("static accessibility and link checks passed")
