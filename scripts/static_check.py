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
  target=(root/value.split("#",1)[0].split("?",1)[0])
  if value and not target.exists(): errors.append(f"missing local {attr}: {value}")
if "<html" not in text.lower() or "<title>" not in text.lower(): errors.append("basic HTML metadata missing")
if errors:
 print("\n".join(errors)); sys.exit(1)
print("static checks passed")
