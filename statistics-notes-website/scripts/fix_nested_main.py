#!/usr/bin/env python3
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAPTERS = os.path.join(ROOT, 'chapters')

def fix_file(path):
    with open(path, 'r', encoding='utf-8') as fh:
        s = fh.read()
    idx = s.find('<main')
    if idx == -1:
        return False
    # find end of opening main tag
    start_tag_end = s.find('>', idx)
    if start_tag_end == -1:
        return False
    prefix = s[:start_tag_end+1]
    rest = s[start_tag_end+1:]
    new_rest = rest.replace('<main', '<div').replace('</main>', '</div>')
    new = prefix + new_rest
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(new)
    return True

def main():
    files = [f for f in os.listdir(CHAPTERS) if f.lower().endswith('.html')]
    for fn in files:
        path = os.path.join(CHAPTERS, fn)
        ok = fix_file(path)
        print('Fixed nested main:' if ok else 'Skipped:', fn)

if __name__ == '__main__':
    main()
