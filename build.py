#!/usr/bin/env python3
"""Builds data.js from content/*.txt. Run: python3 build.py"""
import json, glob, re, html, os
here = os.path.dirname(os.path.abspath(__file__))

AX = '<line x1="10" y1="80" x2="150" y2="80" class="ax"/><line x1="80" y1="150" x2="80" y2="10" class="ax"/><text x="152" y="84" class="lb">x</text><text x="76" y="8" class="lb">y</text>'
def svg(body, cap, vb="0 0 165 160", w=220):
    return f'<figure class="fig"><svg viewBox="{vb}" width="{w}" role="img" aria-label="{cap}">{body}</svg><figcaption>{cap}</figcaption></figure>'
FIGS = {

 'halfdisk': svg('<path d="M80,30 A50,50 0 0,1 80,130 Z" class="in"/>'+AX+'<path d="M80,30 A50,50 0 0,1 80,130" class="out"/><line x1="80" y1="30" x2="80" y2="130" class="out"/><text x="133" y="94" class="lb">2</text><text x="85" y="142" class="lb">−2</text>', 'Shaded = domain: right half of the disk. Dashed edges NOT included.'),
 'tree': svg('<text x="104" y="16" class="lb b">w</text>'
   '<line x1="106" y1="20" x2="40" y2="58" class="edge"/><line x1="108" y1="20" x2="108" y2="58" class="edge"/><line x1="110" y1="20" x2="176" y2="58" class="edge"/>'
   '<text x="56" y="36" class="lb">w<tspan dy="2" font-size="7">x</tspan></text><text x="112" y="42" class="lb">w<tspan dy="2" font-size="7">y</tspan></text><text x="150" y="36" class="lb">w<tspan dy="2" font-size="7">z</tspan></text>'
   '<text x="36" y="70" class="lb b">x</text><text x="104" y="70" class="lb b">y</text><text x="174" y="70" class="lb b">z</text>'
   '<line x1="40" y1="74" x2="106" y2="112" class="edge"/><line x1="108" y1="74" x2="108" y2="112" class="edge"/><line x1="176" y1="74" x2="110" y2="112" class="edge"/>'
   '<text x="52" y="98" class="lb">dx/dt</text><text x="112" y="96" class="lb">dy/dt</text><text x="146" y="98" class="lb">dz/dt</text>'
   '<text x="105" y="124" class="lb b">t</text>', 'Three branches from w down to t. Multiply along each branch, then add.', '0 0 216 130', 280),
 'gradient': svg('<ellipse cx="90" cy="76" rx="70" ry="50" class="ct"/><ellipse cx="90" cy="76" rx="45" ry="32" class="ct"/><ellipse cx="90" cy="76" rx="20" ry="14" class="ct"/>'
   '<text x="160" y="80" class="lb">1</text><text x="137" y="80" class="lb">2</text><text x="112" y="80" class="lb">3</text><text x="150" y="20" class="lb">heights</text>'
   '<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 z" class="ahd"/></marker></defs>'
   '<line x1="90" y1="146" x2="90" y2="112" class="arr" marker-end="url(#ah)"/><circle cx="90" cy="126" r="2.5" class="dot"/>'
   '<text x="96" y="146" class="lb">∇f</text>', 'Contour map of a hill (top view). ∇f points straight uphill, at right angles to the contour lines.', '0 0 190 155', 260),
 'critical': svg('<path d="M10,15 Q45,95 80,15" class="edge"/><circle cx="45" cy="55" r="3" class="dot"/>'
   '<path d="M100,85 Q135,5 170,85" class="edge"/><circle cx="135" cy="45" r="3" class="dot"/>'
   '<path d="M190,20 Q225,90 260,20" class="edge"/><path d="M190,80 Q225,10 260,80" class="out"/><circle cx="225" cy="55" r="3" class="dot"/>'
   '<text x="45" y="106" text-anchor="middle" class="lb b">minimum</text><text x="135" y="106" text-anchor="middle" class="lb b">maximum</text><text x="225" y="106" text-anchor="middle" class="lb b">saddle</text>'
   '<text x="45" y="119" text-anchor="middle" class="lb">bowl, D &gt; 0</text><text x="135" y="119" text-anchor="middle" class="lb">hill top, D &gt; 0</text><text x="225" y="119" text-anchor="middle" class="lb">D &lt; 0</text>'
   '<text x="225" y="131" text-anchor="middle" class="lb">up one way, down other</text>',
   'The three kinds of flat spot (side views).', '-5 0 290 136', 360),
 'lagrange': svg('<circle cx="80" cy="80" r="45" class="edge"/><text x="20" y="140" class="lb">constraint g = c</text>'
   '<line x1="40" y1="20" x2="160" y2="140" class="ct"/><line x1="20" y1="40" x2="140" y2="160" class="ct"/>'
   '<line x1="96" y1="0" x2="176" y2="80" class="out"/><circle cx="111.8" cy="48.2" r="3.5" class="dot"/>'
   '<text x="60" y="44" class="lb b">best point →</text><text x="128" y="96" class="lb">level lines of f</text>',
   'Walk round the circle. The best point is where a level line of f just touches it.', '0 0 180 160', 250),
 'punctured': svg('<rect x="10" y="10" width="140" height="140" class="in"/>'+AX+'<circle cx="80" cy="80" r="4" class="hole"/>', 'Shaded = domain. Open dot = origin removed.'),
 'twolines': svg('<rect x="10" y="10" width="140" height="140" class="in"/>'+AX+'<line x1="60" y1="10" x2="60" y2="150" class="out"/><line x1="10" y1="100" x2="150" y2="100" class="out"/><text x="34" y="22" class="lb">x = −1</text><text x="112" y="114" class="lb">y = −1</text>', 'Shaded = domain. Dashed lines removed.'),
 'noxaxis': svg('<rect x="10" y="10" width="140" height="140" class="in"/><line x1="80" y1="150" x2="80" y2="10" class="ax"/><text x="76" y="8" class="lb">y</text><line x1="10" y1="80" x2="150" y2="80" class="out"/><text x="152" y="84" class="lb">x</text>', 'Shaded = domain. x-axis (dashed) removed.'),
 'noyaxis': svg('<rect x="10" y="10" width="140" height="140" class="in"/><line x1="10" y1="80" x2="150" y2="80" class="ax"/><text x="152" y="84" class="lb">x</text><line x1="80" y1="150" x2="80" y2="10" class="out"/><text x="76" y="8" class="lb">y</text>', 'Shaded = domain. y-axis (dashed) removed.'),
 'halfplane': svg('<polygon points="10,150 10,10 150,10" class="in"/>'+AX+'<line x1="10" y1="150" x2="150" y2="10" class="edge"/><text x="118" y="56" class="lb">y = x</text>', 'Shaded = domain: on and above the line y = x.'),
 'opendisk': svg(AX+'<circle cx="80" cy="80" r="50" class="in"/><circle cx="80" cy="80" r="50" class="out"/><text x="132" y="94" class="lb">4</text>', 'Open disk, radius 4. Dashed circle NOT included.'),
 'closeddisk': svg(AX+'<circle cx="80" cy="80" r="45" class="in"/><circle cx="80" cy="80" r="45" class="edge"/><text x="127" y="94" class="lb">3</text>', 'Closed disk, radius 3. Solid circle included.'),
 'house': svg('<polygon points="40,140 40,75 80,45 120,75 120,140" class="in"/><polyline points="40,140 40,75 80,45 120,75 120,140" class="edge"/><line x1="40" y1="140" x2="120" y2="140" class="out"/><line x1="40" y1="75" x2="120" y2="75" class="out"/><text x="76" y="155" class="lb">w</text><text x="28" y="112" class="lb">h</text><text x="126" y="112" class="lb">h</text><text x="50" y="56" class="lb">s</text><text x="104" y="56" class="lb">s</text>', 'The wire (solid) makes 5 sides: h, s, s, h and the base w.'),
 'punct10': svg('<rect x="10" y="10" width="140" height="140" class="in"/>'+AX+'<circle cx="105" cy="80" r="4" class="hole"/><text x="102" y="96" class="lb">1</text>', 'Shaded = domain. Open dot = the point (1, 0) removed.'),
 'halfplaneneg': svg('<polygon points="10,10 150,10 150,150" class="in"/>'+AX+'<line x1="10" y1="10" x2="150" y2="150" class="edge"/><text x="92" y="134" class="lb">y = −x</text>', 'Shaded = domain: on and above the line y = −x.'),
 'opendisk3': svg(AX+'<circle cx="80" cy="80" r="50" class="in"/><circle cx="80" cy="80" r="50" class="out"/><text x="132" y="94" class="lb">3</text>', 'Open disk, radius 3. Dashed circle NOT included.'),
 'halfdiskup': svg('<path d="M30,80 A50,50 0 0,1 130,80 Z" class="in"/>'+AX+'<path d="M30,80 A50,50 0 0,1 130,80" class="out"/><line x1="30" y1="80" x2="130" y2="80" class="out"/><text x="133" y="94" class="lb">3</text><text x="14" y="94" class="lb">−3</text>', 'Shaded = domain: top half of the disk. Dashed edges NOT included.'),
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


def parse(folder):
    parts = []; st = {'topic': None, 'q': None, 'mode': None, 'buf': []}
    def flush():
        text = '\n'.join(st['buf']); st['buf'] = []
        m = st['mode']; st['mode'] = None
        if m is None: return
        kind, arg = m; t = st['topic']; q = st['q']
        if kind == 'method': t['method'] = fmt(text)
        elif kind == 'learn': t['learn'] = fmt(text)
        elif kind == 'stem': t['stem'] = fmt(text)
        elif kind == 'check': t['check'] = {'q': fmt(arg + ('\n' + text if text.strip() else '')), 'a': ''}
        elif kind == 'checka': t['check']['a'] = fmt(arg + ('\n' + text if text.strip() else ''))
        elif kind == 'q': q['q'] = fmt(text)
        elif kind == 's': q['steps'].append({'t': html.escape(arg, quote=False), 'b': fmt(text)})
        elif kind == 'a': q['a'] = fmt(arg + ('\n' + text if text.strip() else ''))
    for f in sorted(glob.glob(os.path.join(here, 'content', folder, '*.txt'))):
        for line in open(f, encoding='utf-8').read().split('\n'):
            if line.startswith('@@part '):
                flush(); parts.append({'title': line[7:].strip(), 'topics': []})
            elif line.startswith('@@topic '):
                flush(); i, t, src = [x.strip() for x in line[8:].split('|')]
                st['topic'] = {'id': i, 'title': t, 'src': src, 'method': '', 'learn': '', 'stem': '', 'check': None, 'qs': []}
                parts[-1]['topics'].append(st['topic'])
            elif line.startswith('@method'): flush(); st['mode'] = ('method', None)
            elif line.startswith('@learn'): flush(); st['mode'] = ('learn', None)
            elif line.startswith('@stem'): flush(); st['mode'] = ('stem', None)
            elif line.startswith('@checka '): flush(); st['mode'] = ('checka', line[8:].strip())
            elif line.startswith('@check '): flush(); st['mode'] = ('check', line[7:].strip())
            elif line.startswith('@q '):
                flush(); st['q'] = {'ref': line[3:].strip(), 'q': '', 'steps': [], 'a': ''}
                st['topic']['qs'].append(st['q']); st['mode'] = ('q', None)
            elif line.startswith('@s '): flush(); st['mode'] = ('s', line[3:].strip())
            elif line.startswith('@a '): flush(); st['mode'] = ('a', line[3:].strip())
            else: st['buf'].append(line)
        flush()
    for p in parts:
        for t in p['topics']:
            for k, qq in enumerate(t['qs']):
                qq['id'] = f"{t['id']}-{k}"
                assert qq['q'] and qq['steps'] and qq['a'], qq['ref']
    return parts

def parse_sim():
    """content/sim/*.txt: one similar question (new numbers) per exam-path question, keyed by question id"""
    sims = {}; stems = {}; cur = None; mode = None; buf = []
    def flush():
        nonlocal mode, buf
        text = '\n'.join(buf); buf = []
        if mode is None: return
        kind, arg = mode; mode = None
        if kind == 'stem': stems[arg] = fmt(text)
        elif kind == 'q': cur['q'] = fmt(text)
        elif kind == 's': cur['steps'].append({'t': html.escape(arg, quote=False), 'b': fmt(text)})
        elif kind == 'a': cur['a'] = fmt(arg + ('\n' + text if text.strip() else ''))
    for f in sorted(glob.glob(os.path.join(here, 'content', 'sim', '*.txt'))):
        for line in open(f, encoding='utf-8').read().split('\n'):
            if line.startswith('@simstem '):
                flush(); mode = ('stem', line[9:].strip())
            elif line.startswith('@sim '):
                flush(); cur = {'q': '', 'steps': [], 'a': ''}; sims[line[5:].strip()] = cur; mode = ('q', None)
            elif line.startswith('@s '): flush(); mode = ('s', line[3:].strip())
            elif line.startswith('@a '): flush(); mode = ('a', line[3:].strip())
            else: buf.append(line)
        flush()
    return sims, stems

data = {'core': parse('core'), 'full': parse('full')}

# "Off the exam path": every homework question that is NOT on the exam path.
# New topics first (most likely to come up first), then extra practice by chapter.
NEW_TOPICS = ['levelcurves', 'continuity', 'variation', 'directions', 'region', 'higher']
core_refs = {q['ref'] for p in data['core'] for t in p['topics'] for q in t['qs']}
full_topics = {t['id']: t for p in data['full'] for t in p['topics']}
def rest(t):
    qs = [q for q in t['qs'] if q['ref'] not in core_refs]
    return dict(t, qs=qs) if qs else None
off = [{'title': 'New topics (most likely first)', 'topics': [rest(full_topics[i]) for i in NEW_TOPICS]}]
for p in data['full']:
    ts = [r for r in (rest(t) for t in p['topics'] if t['id'] not in NEW_TOPICS) if r]
    if ts: off.append({'title': 'More practice: ' + p['title'], 'topics': ts})
n_off = sum(len(t['qs']) for p in off for t in p['topics'])
n_full = sum(len(t['qs']) for p in data['full'] for t in p['topics'])
n_core_hw = sum(1 for r in core_refs if not r.startswith('Sample exam'))
assert n_off + n_core_hw == n_full, (n_off, n_core_hw, n_full)
print('off the exam path', n_off)
sims, sim_stems = parse_sim(); used = set()
for p in data['core']:
    for t in p['topics']:
        for qq in t['qs']:
            sm = sims.get(qq['id'])
            assert sm and sm['q'] and sm['steps'] and sm['a'], 'no similar question for ' + qq['id']
            qq['sim'] = sm; used.add(qq['id'])
assert used == set(sims), set(sims) - used
print('similar questions', len(used))
# Multi-part questions that share a stem ("Let T = ... and P = ..."): every part shows the
# whole question, stem plus all parts, with the current part highlighted.
def whole(stem, qs):
    def lbl(ref):
        m = re.search(r'Q\d+(\(\w\))$', ref)
        return f'<span class="pl">{m.group(1)}</span> ' if m else ''
    texts = [(lbl(q['ref']), re.sub(r'^<p>|</p>$', '', q['q'].strip())) for q in qs]
    # a merged part like "(d) ... (e) ..." carries its own labels in the text: bold those too
    texts = [(l, t if l else re.sub(r'(^|(?<=[.?] ))(\([a-e]\))', r'\1<span class="pl">\2</span>', t)) for l, t in texts]
    out = []
    for i in range(len(qs)):
        parts = ''.join(f'<div class="qpart{" on" if j == i else ""}">{l}{t}</div>' for j, (l, t) in enumerate(texts))
        out.append(stem + f'<div class="qparts">{parts}</div>')
    return out
stemmed = set()
for p in data['core']:
    for t in p['topics']:
        stem = t.pop('stem')
        if not stem: continue
        assert t['id'] in sim_stems, 'no @simstem for ' + t['id']
        qs = t['qs']
        main = whole(stem, qs)
        alt = whole(sim_stems[t['id']], [{'ref': q['ref'], 'q': q['sim']['q']} for q in qs])
        for q, w, ws in zip(qs, main, alt):
            q['q'] = w; q['sim'] = dict(q['sim'], q=ws)
        stemmed.add(t['id'])
for p in data['full'] + off:
    for t in p['topics']: t.pop('stem', None)
assert stemmed == set(sim_stems), set(sim_stems) ^ stemmed
print('shared-stem questions', sorted(stemmed))
# Show each past-exam part inside its topic too (last in the topic), so you see what the exam asks.
EXAM_IN_TOPIC = {'x-q1-0': 'c-domains', 'x-q1-1': 'c-domains', 'x-q1-2': 'c-limits',
    'x-q2-0': 'c-partials', 'x-q2-1': 'c-chain', 'x-q2-2': 'c-chain',
    'x-q3-0': 'c-implicit', 'x-q3-1': 'c-jacobian', 'x-q3-2': 'c-approx',
    'x-q4-0': 'c-gradient', 'x-q4-1': 'c-gradient', 'x-q4-2': 'c-gradient', 'x-q4-3': 'c-gradient',
    'x-q5-0': 'c-tangent', 'x-q5-1': 'c-critical3', 'x-q6-0': 'c-lagrange', 'x-q6-1': 'c-undet'}
core_topics = {t['id']: t for p in data['core'] for t in p['topics']}
exam_qs = {q['id']: q for p in data['core'] for t in p['topics'] for q in t['qs'] if q['id'].startswith('x-')}
assert set(exam_qs) == set(EXAM_IN_TOPIC), set(exam_qs) ^ set(EXAM_IN_TOPIC)
for qid, tid in EXAM_IN_TOPIC.items():
    core_topics[tid]['qs'].append(exam_qs[qid])
data = {'core': data['core'], 'off': off}
open(os.path.join(here, 'data.js'), 'w', encoding='utf-8').write('window.DATA=' + json.dumps(data, ensure_ascii=False) + ';\n')
for k, v in data.items():
    print(k, 'topics', sum(len(p['topics']) for p in v), 'questions', sum(len(t['qs']) for p in v for t in p['topics']))

# cache-bust: stamp index.html's data.js reference with a hash of the data
import hashlib
ver = hashlib.md5(open(os.path.join(here, 'data.js'), 'rb').read()).hexdigest()[:8]
ip = os.path.join(here, 'index.html'); h = open(ip, encoding='utf-8').read()
h = re.sub(r'<script src="data\.js(\?v=\w+)?"></script>', f'<script src="data.js?v={ver}"></script>', h)
open(ip, 'w', encoding='utf-8').write(h)
