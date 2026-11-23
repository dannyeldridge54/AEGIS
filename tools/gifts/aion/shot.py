from playwright.sync_api import sync_playwright
import sys
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1000,'height':1100}); errs=[]
    pg.on('pageerror',lambda e: errs.append(str(e))); pg.goto('file://'+sys.argv[1]); pg.wait_for_timeout(300)
    if len(sys.argv)>2: pg.click('#bIO'); pg.wait_for_timeout(200)
    print(pg.inner_text('#bars').replace('\n',' | '), pg.inner_text('#mbb'), pg.inner_text('#sum')); pg.screenshot(path='aion_shot.png',full_page=True); print('errs',errs); b.close()
