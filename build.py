#!/usr/bin/env python3
"""Builds data.js from content/*.txt. Run: python3 build.py"""
import json, glob, re, html, os
here = os.path.dirname(os.path.abspath(__file__))

AX = '<line x1="10" y1="80" x2="150" y2="80" class="ax"/><line x1="80" y1="150" x2="80" y2="10" class="ax"/><text x="152" y="84" class="lb">x</text><text x="76" y="8" class="lb">y</text>'
def svg(body, cap):
    return f'<figure class="fig"><svg viewBox="0 0 165 160" width="220" role="img" aria-label="{cap}">{body}</svg><figcaption>{cap}</figcaption></figure>'
FIGS = {
 'punctured': svg('<rect x="10" y="10" width="140" height="140" class="in"/>'+AX+'<circle cx="80" cy="80" r="4" class="hole"/>', 'Shaded = domain. Open dot = origin removed.'),
 'twolines': svg('<rect x="10" y="10" width="140" height="140" class="in"/>'+AX+'<line x1="60" y1="10" x2="60" y2="150" class="out"/><line x1="10" y1="100" x2="150" y2="100" class="out"/><text x="34" y="22" class="lb">x = −1</text><text x="112" y="114" class="lb">y = −1</text>', 'Shaded = domain. Dashed lines removed.'),
 'noxaxis': svg('<rect x="10" y="10" width="140" height="140" class="in"/><line x1="80" y1="150" x2="80" y2="10" class="ax"/><text x="76" y="8" class="lb">y</text><line x1="10" y1="80" x2="150" y2="80" class="out"/><text x="152" y="84" class="lb">x</text>', 'Shaded = domain. x-axis (dashed) removed.'),
 'noyaxis': svg('<rect x="10" y="10" width="140" height="140" class="in"/><line x1="10" y1="80" x2="150" y2="80" class="ax"/><text x="152" y="84" class="lb">x</text><line x1="80" y1="150" x2="80" y2="10" class="out"/><text x="76" y="8" class="lb">y</text>', 'Shaded = domain. y-axis (dashed) removed.'),
 'halfplane': svg('<polygon points="10,150 10,10 150,10" class="in"/>'+AX+'<line x1="10" y1="150" x2="150" y2="10" class="edge"/><text x="118" y="56" class="lb">y = x</text>', 'Shaded = domain: on and above the line y = x.'),
 'opendisk': svg(AX+'<circle cx="80" cy="80" r="50" class="in"/><circle cx="80" cy="80" r="50" class="out"/><text x="132" y="94" class="lb">4</text>', 'Open disk, radius 4. Dashed circle NOT included.'),
 'closeddisk': svg(AX+'<circle cx="80" cy="80" r="45" class="in"/><circle cx="80" cy="80" r="45" class="edge"/><text x="127" y="94" class="lb">3</text>', 'Closed disk, radius 3. Solid circle included.'),
 'house': svg('<polygon points="40,140 40,75 80,45 120,75 120,140" class="in"/><polyline points="40,140 40,75 80,45 120,75 120,140" class="edge"/><line x1="40" y1="140" x2="120" y2="140" class="out"/><line x1="40" y1="75" x2="120" y2="75" class="out"/><text x="76" y="155" class="lb">w</text><text x="28" y="112" class="lb">h</text><text x="126" y="112" class="lb">h</text><text x="50" y="56" class="lb">s</text><text x="104" y="56" class="lb">s</text>', 'The wire (solid) makes 5 sides: h, s, s, h and the base w.'),
}

def fmt(text):
    """escape, bold, paragraphs, figures"""
    out = []
    for para in re.split(r'\n\s*\n', text.strip()):
        para = para.strip()
        if not para: continue
        m = re.fullmatch(r'\{\{fig:(\w+)\}\}', para)
        if m: out.append(FIGS[m.group(1)]); continue
        p = html.escape(para, quote=False)
        p = re.sub(r'\{\{fig:(\w+)\}\}', lambda m: FIGS[m.group(1)], p)
        p = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', p)
        p = re.sub(r'\n(?=\$\$)|(?<=\$\$)\n', '', p).replace('\n', '<br>')
        if p.startswith('$$') and p.endswith('$$') and p.count('$$') == 2:
            out.append(f'<div class="dm">{p}</div>')
        else:
            out.append(f'<p>{p}</p>')
    return '\n'.join(out)

parts = []; topic = None; q = None; mode = None; buf = []
def flush():
    global buf, mode
    text = '\n'.join(buf); buf = []
    if mode is None: return
    kind, arg = mode
    if kind == 'method': topic['method'] = fmt(text)
    elif kind == 'q': q['q'] = fmt(text)
    elif kind == 's': q['steps'].append({'t': html.escape(arg, quote=False), 'b': fmt(text)})
    elif kind == 'a': q['a'] = fmt(arg + ('\n' + text if text.strip() else ''))
    mode = None

for f in sorted(glob.glob(os.path.join(here, 'content', '*.txt'))):
    for line in open(f, encoding='utf-8').read().split('\n'):
        if line.startswith('@@part '):
            flush(); parts.append({'title': line[7:].strip(), 'topics': []})
        elif line.startswith('@@topic '):
            flush(); i, t, src = [s.strip() for s in line[8:].split('|')]
            topic = {'id': i, 'title': t, 'src': src, 'method': '', 'qs': []}; parts[-1]['topics'].append(topic)
        elif line.startswith('@method'):
            flush(); mode = ('method', None)
        elif line.startswith('@q '):
            flush(); q = {'ref': line[3:].strip(), 'q': '', 'steps': [], 'a': ''}; topic['qs'].append(q); mode = ('q', None)
        elif line.startswith('@s '):
            flush(); mode = ('s', line[3:].strip())
        elif line.startswith('@a '):
            flush(); mode = ('a', line[3:].strip())
        else:
            buf.append(line)
    flush()

# numbered lists inside method boxes: lines "1. ..." are kept as paragraphs (simple and readable)
n = sum(len(t['qs']) for p in parts for t in p['topics'])
for p in parts:
    for t in p['topics']:
        for k, qq in enumerate(t['qs']):
            qq['id'] = f"{t['id']}-{k}"
            assert qq['q'] and qq['steps'] and qq['a'], qq['ref']
open(os.path.join(here, 'data.js'), 'w', encoding='utf-8').write('window.DATA=' + json.dumps(parts, ensure_ascii=False) + ';\n')
print('topics', sum(len(p['topics']) for p in parts), 'questions', n)
