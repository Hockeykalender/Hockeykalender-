# Erzeugt pruefung/links-1.html ... mit allen Anbieter-Links (je 100), damit die tägliche Prüfung sie abrufen kann.
import json,os,re,subprocess,glob
d=os.path.dirname(os.path.abspath(__file__));root=os.path.join(d,'..')
js=subprocess.run(['node','-e','const vm=require("vm"),fs=require("fs");const c={};vm.createContext(c);vm.runInContext(fs.readFileSync(process.argv[1],"utf8")+";this.A=DATA.concat(LAUFEND,OHNE)",c);console.log(JSON.stringify(c.A.map(x=>x.url||"")))',os.path.join(root,'daten.js')],capture_output=True,text=True,check=True).stdout
u=[];seen=set()
for x in json.loads(js)+[r[7] for r in json.load(open(os.path.join(d,'anbieter.json')))]:
    if x and x not in seen: seen.add(x);u.append(x)
for f in glob.glob(os.path.join(d,'links-*.html')): os.remove(f)
n=(len(u)+99)//100
for i in range(n):
    part=u[i*100:(i+1)*100]
    h='<!DOCTYPE html><html lang="de"><head><meta charset="utf-8"><meta name="robots" content="noindex"><title>Prüfliste %d/%d</title></head><body><h1>Prüfliste %d von %d</h1><ol>'%(i+1,n,i+1,n)
    h+=''.join('<li><a href="%s">%s</a></li>'%(x.replace('"','%22'),x.replace('&','&amp;').replace('<','&lt;')) for x in part)+'</ol></body></html>\n'
    open(os.path.join(d,'links-%d.html'%(i+1)),'w').write(h)
print(len(u),'Links auf',n,'Seiten')
