import json,sys
import os;p=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','daten.js')
o=json.loads(sys.argv[1])
L=open(p).read().split('\n')
ids=[json.loads(l.rstrip(','))['id'] for l in L if l.startswith('{"id"')]
assert o['id'] not in ids, 'dup id'
# DATA block: from 'const DATA=[' to first line '];'
s=L.index('const DATA=[')+1
e=s
while not L[e].startswith('];'): e+=1
pos=e
for i in range(s,e):
    d=json.loads(L[i].rstrip(','))
    if (d['von'],d['bis'])>(o['von'],o['bis']): pos=i;break
line=json.dumps(o,ensure_ascii=False,separators=(',',':'))+','
L.insert(pos,line)
# ensure last before ]; no trailing comma issue: keep consistent with file style
open(p,'w').write('\n'.join(L)); print('added',o['id'],'at',pos)
