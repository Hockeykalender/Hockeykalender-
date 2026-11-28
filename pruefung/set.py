import json,sys,re
# usage: set.py id field value
import os;p=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','daten.js')
s=open(p).read().split('\n')
i,f,v=sys.argv[1:4]
for n,l in enumerate(s):
    if l.startswith('{"id":"%s",'%i):
        o=json.loads(l.rstrip(','));old=o.get(f);o[f]=v
        s[n]=json.dumps(o,ensure_ascii=False,separators=(',',':'))+(',' if l.endswith(',') else '')
        print(i,f,':',old,'->',v);break
else: print('NOT FOUND',i)
open(p,'w').write('\n'.join(s))
