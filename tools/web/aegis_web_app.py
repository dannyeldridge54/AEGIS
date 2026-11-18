"""AEGIS Web desktop app: opens the AEGIS Web display (aegis_web.html) in a native window (pywebview → Windows Edge WebView2).
Build (Windows): python -m PyInstaller --onefile --windowed --name AEGIS_Web --add-data "aegis_web.html;." aegis_web_app.py"""
import os, sys, webview
base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
page = os.path.join(base, 'aegis_web.html')
html = open(page, encoding='utf-8').read()
if not html.lstrip().lower().startswith('<!doctype'):
    html = ('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<style>body{margin:0;font:14px system-ui}[hidden]{display:none!important}</style></head><body>' + html + '</body></html>')
webview.create_window('AEGIS Web', html=html, width=1600, height=1000, min_size=(900, 600), background_color='#05020D')
webview.start()
