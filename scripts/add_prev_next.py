#!/usr/bin/env python3
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, 'index.html')
CHAPTERS_DIR = os.path.join(ROOT, 'chapters')

def parse_index_order(index_path):
    html = open(index_path, 'r', encoding='utf-8').read()
    # find all chapter links under chapters/ in the index
    matches = re.findall(r'href\s*=\s*"chapters/([^"]+)"', html)
    # keep unique while preserving order
    seen = set()
    ordered = []
    for m in matches:
        if m not in seen:
            seen.add(m)
            ordered.append(m)
    return ordered

def inject_nav(chapters_order):
    for i, name in enumerate(chapters_order):
        path = os.path.join(CHAPTERS_DIR, name)
        if not os.path.exists(path):
            print('Missing file, skipping:', name)
            continue
        src = open(path, 'r', encoding='utf-8').read()

        # remove existing chapter-nav block if present
        src = re.sub(r'<nav class="chapter-nav">[\s\S]*?</nav>', '', src, flags=re.I)

        prev_link = ''
        next_link = ''
        if i > 0:
            prev_link = f'<a class="btn" href="{chapters_order[i-1]}">← Previous</a>'
        else:
            prev_link = '<span class="btn disabled">← Previous</span>'
        if i < len(chapters_order)-1:
            next_link = f'<a class="btn" href="{chapters_order[i+1]}">Next →</a>'
        else:
            next_link = '<span class="btn disabled">Next →</span>'

        nav_html = f"\n      <nav class=\"chapter-nav\">\n        <div class=\"nav-inner\">{prev_link}<span class=\"sep\"></span>{next_link}</div>\n      </nav>\n"

        # Insert nav_html before the last closing </main>
        if '</main>' in src:
            parts = src.rsplit('</main>', 1)
            new = parts[0] + nav_html + '</main>' + parts[1]
        else:
            # fallback: append before </body>
            new = src.replace('</body>', nav_html + '\n</body>')

        open(path, 'w', encoding='utf-8').write(new)
        print('Injected nav into:', name)

def main():
    order = parse_index_order(INDEX)
    if not order:
        print('No chapters found in index.html')
        return
    inject_nav(order)

if __name__ == '__main__':
    main()
