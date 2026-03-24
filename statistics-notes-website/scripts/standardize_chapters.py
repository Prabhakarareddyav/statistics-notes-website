#!/usr/bin/env python3
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAPTERS = os.path.join(ROOT, 'chapters')

TEMPLATE = '''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{title}</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../style.css">
</head>
<body>
  <header class="site-header">
    <div class="wrap">
      <a class="brand" href="../index.html">Statistics Notes</a>
      <nav class="top-nav">
        <a href="../index.html">Home</a>
        <a href="../index.html#about">About</a>
      </nav>
      <div class="header-actions">
        <input class="search" placeholder="Search topics" aria-label="Search topics">
      </div>
    </div>
  </header>

  <main class="wrap main-grid chapter-page">
    {content}
  </main>

  <footer class="site-footer">
    <div class="wrap">
      <div>© {year} Statistics Notes</div>
      <nav>
        <a href="../index.html#about">About</a>
      </nav>
    </div>
  </footer>
</body>
</html>
'''

def clean_html(src):
    # remove <style> blocks
    src = re.sub(r'<style[\s\S]*?</style>', '', src, flags=re.I)
    # remove existing header and footer
    src = re.sub(r'<header[\s\S]*?</header>', '', src, flags=re.I)
    src = re.sub(r'<footer[\s\S]*?</footer>', '', src, flags=re.I)
    # remove meta and head remnants if present
    src = re.sub(r'<head[\s\S]*?</head>', '', src, flags=re.I)
    # trim
    return src.strip()

def extract_title(src, default):
    m = re.search(r'<title>(.*?)</title>', src, flags=re.I|re.S)
    if m:
        return m.group(1).strip()
    return default

def extract_body(src):
    m = re.search(r'<body[^>]*>([\s\S]*?)</body>', src, flags=re.I)
    if m:
        return m.group(1).strip()
    # fallback: entire file
    return src

def main():
    files = [f for f in os.listdir(CHAPTERS) if f.lower().endswith('.html')]
    for fn in files:
        path = os.path.join(CHAPTERS, fn)
        with open(path, 'r', encoding='utf-8') as fh:
            src = fh.read()

        title = extract_title(src, fn)
        body = extract_body(src)
        body = clean_html(body)

        new = TEMPLATE.format(title=title, content=body, year=str(__import__('datetime').datetime.now().year))

        bak = path + '.bak'
        if not os.path.exists(bak):
            open(bak, 'w', encoding='utf-8').write(src)

        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(new)

        print('Standardized:', fn)

if __name__ == '__main__':
    main()
