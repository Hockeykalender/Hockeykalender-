import sys, threading, http.server, functools
from playwright.sync_api import sync_playwright
root=sys.argv[1]
H=functools.partial(http.server.SimpleHTTPRequestHandler,directory=root)
srv=http.server.ThreadingHTTPServer(("127.0.0.1",8765),H); threading.Thread(target=srv.serve_forever,daemon=True).start()
with sync_playwright() as p:
  b=p.chromium.launch()
  for name,kw in [("desktop",dict(viewport={"width":1280,"height":900})),("handy",dict(**p.devices["iPhone 13"]) if False else dict(viewport={"width":390,"height":844},is_mobile=True,has_touch=True,device_scale_factor=3))]:
    ctx=b.new_context(**kw); pg=ctx.new_page(); errs=[]; ext=[]
    pg.on("pageerror",lambda e:errs.append(str(e))); pg.on("console",lambda m:m.type=="error" and errs.append(m.text))
    pg.on("request",lambda r:(not r.url.startswith("http://127.0.0.1")) and ext.append(r.url))
    pg.goto("http://127.0.0.1:8765/index.html"); pg.wait_for_timeout(1500)
    cards=pg.locator(".card").count(); bells=pg.locator("[data-watch]").count()
    pg.locator("[data-watch]").first.click(); pg.wait_for_timeout(300)
    ls=pg.evaluate("localStorage.getItem('hk-watch')")
    pg.reload(); pg.wait_for_timeout(1200)
    after=pg.locator(".card.watched").count(); n=pg.inner_text("#watchN")
    pg.check("#fWatch"); pg.wait_for_timeout(300); only=pg.locator(".card").count()
    sw=pg.evaluate("document.documentElement.scrollWidth"); vw=pg.evaluate("innerWidth")
    pg.uncheck("#fWatch"); pg.screenshot(path=f"/tmp/{name}.png")
    print(name,"karten",cards,"glocken",bells,"gespeichert",bool(ls),"nach_reload_markiert",after,n,"nur_beob",only,"scrollW/vw",sw,vw,"fehler",errs,"extern",ext)
    ctx.close()
  # Speicher gesperrt
  ctx=b.new_context(); pg=ctx.new_page(); errs=[]
  pg.add_init_script("Object.defineProperty(window,'localStorage',{get(){throw new Error('blocked')}})")
  pg.on("pageerror",lambda e:errs.append(str(e)))
  pg.goto("http://127.0.0.1:8765/index.html"); pg.wait_for_timeout(1200)
  pg.locator("[data-watch]").first.click(); pg.wait_for_timeout(300)
  print("gesperrt karten",pg.locator(".card").count(),"markiert",pg.locator(".card.watched").count(),"msg",pg.inner_text("#watchMsg"),"fehler",errs)
  b.close()
srv.shutdown()
