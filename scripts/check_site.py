import pathlib
import re
import sys

SITE = pathlib.Path("_site")
MARKERS = ["<!--START_SECTION:activity-->", "<!--END_SECTION:activity-->"]
SKIP = ("http://", "https://", "//", "#", "mailto:", "/", "javascript:", "data:")
errors = []

# 1. 首頁存在，而且有 activity 區塊
index = SITE / "index.html"
if not index.exists():
    errors.append("找不到 _site/index.html")
elif "Recent activity" not in index.read_text(encoding="utf-8"):
    errors.append("首頁沒有 Recent activity 區塊")

# 2. README 的兩個標記都還在
readme = pathlib.Path("README.md").read_text(encoding="utf-8")
for marker in MARKERS:
    if marker not in readme:
        errors.append(f"README.md 缺少標記 {marker}")

# 3. 站內連結都指向存在的檔案
for page in SITE.rglob("*.html"):
    html = page.read_text(encoding="utf-8")
    for link in re.findall(r'href="([^"]+)"', html):
        if link.startswith(SKIP):
            continue
        path = link.split("#")[0].split("?")[0]
        target = page.parent / path
        if target.is_dir():
            target = target / "index.html"
        if not target.exists() and not target.with_suffix(".html").exists():
            errors.append(f"{page.relative_to(SITE)} 有壞掉的連結：{link}")

if errors:
    print("❌ Gate 未通過，這個版本不會部署：")
    for e in errors:
        print("  -", e)
    sys.exit(1)
print("✅ Gate 通過：首頁、標記、站內連結都正常")
