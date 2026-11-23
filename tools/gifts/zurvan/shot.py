from playwright.sync_api import sync_playwright
import sys
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1000,'height':1300})
    errs=[]; pg.on('console',lambda m: errs.append(m.text) if m.type=='error' else None); pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.goto('file://'+sys.argv[1]); pg.select_option('#ex','P1_natural'); pg.wait_for_timeout(300)
    print('D1',pg.inner_text('#d1'),'D2',pg.inner_text('#d2'),'rpv',pg.inner_text('#rpv').replace('\n',' | '))
    pg.screenshot(path='zurvan_shot.png',full_page=True); print('errors',errs); b.close()
