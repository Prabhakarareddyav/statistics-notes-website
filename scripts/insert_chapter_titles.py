#!/usr/bin/env python3
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAPTERS = os.path.join(ROOT, 'chapters')

def get_title(src):
    m = re.search(r'<title>(.*?)</title>', src, flags=re.I|re.S)
    return m.group(1).strip() if m else None

def has_chapter_title(src):
    return bool(re.search(r'class\s*=\s*"chapter-title"', src))

def insert_title(path):
    with open(path, 'r', encoding='utf-8') as fh:
        src = fh.read()

    if has_chapter_title(src):
        return False

    title = get_title(src) or os.path.basename(path)

    insert_html = f'\n    <h1 class="chapter-title">{title}</h1>\n'

    # prefer inserting right after <div class="content"> or after main grid start
    if '<div class="content">' in src:
        new = src.replace('<div class="content">', '<div class="content">' + insert_html, 1)
    else:
        # fallback: insert after opening <main ...>
        new = re.sub(r'(<main[^>]*>)', r"\1\n    " + insert_html, src, count=1, flags=re.I)

    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(new)
    return True

def main():
    files = [f for f in os.listdir(CHAPTERS) if f.lower().endswith('.html')]
    changed = []
    for f in files:
        p = os.path.join(CHAPTERS, f)
        try:
            if insert_title(p):
                changed.append(f)
        except Exception as e:
            print('Error processing', f, e)
    for c in changed:
        print('Inserted title into', c)

if __name__ == '__main__':
    main()
