# Schreibt das Prüfdatum je Anbieter-Domain aus pruefung/anbieter.json als GEPRUEFT in daten.js.
# Aufruf im Repo-Ordner: python3 pruefung/geprueft.py
import json, re, datetime
jahr = datetime.date.today().year
a = json.load(open('pruefung/anbieter.json', encoding='utf-8'))
gp = {}
for r in a:
    m = re.match(r'geprüft (\d\d)\.(\d\d)\.', r[6] or '')
    if not m: continue
    d = '%d-%s-%s' % (jahr, m.group(2), m.group(1))
    if d > datetime.date.today().isoformat(): d = '%d-%s-%s' % (jahr - 1, m.group(2), m.group(1))
    if d > gp.get(r[2], ''): gp[r[2]] = d
p = 'daten.js'; s = open(p, encoding='utf-8').read()
zeile = 'const GEPRUEFT=' + json.dumps(gp, separators=(',', ':')) + ';'
s = re.sub(r'\nconst GEPRUEFT=.*;\n?', '\n', s).rstrip('\n') + '\n' + zeile + '\n'
open(p, 'w', encoding='utf-8').write(s)
print(len(gp), 'Anbieter mit Prüfdatum')
