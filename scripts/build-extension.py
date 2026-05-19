#!/usr/bin/env python3
"""
Build the Narrow Write Chrome Extension from source.

Usage:
    python scripts/build-extension.py --version 1.0.0

Output:
    dist/narrow-write-extension-v1.0.0.zip   <- load this in Chrome

Requires: pillow  (pip install pillow)
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

# ── Args ──────────────────────────────────────────────────────────────────────

parser = argparse.ArgumentParser(description='Build Narrow Write Chrome Extension')
parser.add_argument('--version', required=True, help='Extension version (e.g. 1.0.0 or v1.0.0)')
parser.add_argument('--out', default='dist', help='Output directory (default: dist)')
args = parser.parse_args()

version = args.version.lstrip('v')
root    = Path(__file__).parent.parent
out_dir = root / args.out
build   = out_dir / 'extension'

print(f'Building Narrow Write v{version} → {build}')

# ── Clean ─────────────────────────────────────────────────────────────────────

shutil.rmtree(build, ignore_errors=True)
build.mkdir(parents=True)

# ── Extract scripts from index.html ───────────────────────────────────────────

html = (root / 'index.html').read_text(encoding='utf-8')

# 1. Head script: theme flash prevention (first <script> block)
head_re = re.compile(r'(<script>)([\s\S]*?)(</script>)', re.MULTILINE)
head_m  = head_re.search(html)
if not head_m:
    sys.exit('ERROR: could not find head <script> block')

theme_init_js = head_m.group(2).strip()
(build / 'theme-init.js').write_text(theme_init_js, encoding='utf-8')
print('  extracted theme-init.js')

html = html[:head_m.start()] + '<script src="theme-init.js"></script>' + html[head_m.end():]

# 2. Body script: main app (now the only remaining <script> block)
body_m = head_re.search(html)
if not body_m:
    sys.exit('ERROR: could not find body <script> block')

app_js = body_m.group(2).strip()
(build / 'app.js').write_text(app_js, encoding='utf-8')
print('  extracted app.js')

html = html[:body_m.start()] + '<script src="app.js"></script>' + html[body_m.end():]

# ── Pico.css ──────────────────────────────────────────────────────────────────

PICO_URL = 'https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.classless.min.css'
PICO_CDN = 'href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.classless.min.css"'
PICO_LOCAL = 'href="pico.classless.min.css"'

print('  downloading pico.classless.min.css …')
with urllib.request.urlopen(PICO_URL) as r:
    data = r.read()
(build / 'pico.classless.min.css').write_bytes(data)
print('  downloaded pico.classless.min.css')

html = html.replace(PICO_CDN, PICO_LOCAL)

# ── Write patched index.html ──────────────────────────────────────────────────

(build / 'index.html').write_text(html, encoding='utf-8')
print('  wrote index.html')

# ── Icons from nw.png ─────────────────────────────────────────────────────────
# Add dark background (#1a1a1a) so the icon is visible on light toolbars.

src_icon = root / 'assets' / 'nw.png'
sizes    = [16, 48, 128]

try:
    from PIL import Image

    src = Image.open(src_icon).convert('RGBA')
    for size in sizes:
        bg = Image.new('RGBA', (size, size), (26, 26, 26, 255))
        fg = src.resize((size, size), Image.LANCZOS)
        bg.paste(fg, mask=fg.split()[3])
        bg.convert('RGB').save(build / f'icon{size}.png')
        print(f'  icon{size}.png')

except ImportError:
    # Fall back to ImageMagick (available in CI ubuntu runners)
    for size in sizes:
        subprocess.run([
            'magick', str(src_icon),
            '-background', '#1a1a1a',
            '-alpha', 'remove',
            '-resize', f'{size}x{size}!',
            str(build / f'icon{size}.png'),
        ], check=True)
        print(f'  icon{size}.png (ImageMagick)')

# ── manifest.json ─────────────────────────────────────────────────────────────

manifest = {
    "manifest_version": 3,
    "name": "Narrow Write",
    "version": version,
    "description": "Write without looking back — a distraction-free, forward-only writing tool.",
    "chrome_url_overrides": {
        "newtab": "index.html"
    },
    "content_security_policy": {
        "extension_pages": (
            "script-src 'self'; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src https://fonts.gstatic.com;"
        )
    },
    "icons": {
        "16":  "icon16.png",
        "48":  "icon48.png",
        "128": "icon128.png"
    }
}

(build / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
print('  manifest.json')

# ── Zip ───────────────────────────────────────────────────────────────────────

zip_name = f'narrow-write-extension-v{version}.zip'
zip_path = out_dir / zip_name

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    for f in sorted(build.rglob('*')):
        if f.is_file():
            zf.write(f, f.relative_to(build))

print(f'\nDone: {zip_path}')
print('Contents:')
for f in sorted(build.iterdir()):
    print(f'  {f.name}')
