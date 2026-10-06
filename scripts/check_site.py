#!/usr/bin/env python3
"""Check locale coverage, generated content, navigation and local assets."""
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote

ROOT = Path(__file__).resolve().parents[1]
LOCALES = ['en-US','zh-Hans','zh-Hant','de-DE','es-ES','fr-FR','ja','ko','pt-BR']

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links=[];self.assets=[];self.ids=set();self.lang=None
        self.h1=0;self.alternates=[];self.scripts=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='html':self.lang=a.get('lang')
        if tag=='h1':self.h1+=1
        if tag=='script':self.scripts+=1
        if 'id' in a:self.ids.add(a['id'])
        if tag=='a':self.links.append(a)
        if tag=='img':self.assets.append(a['src'])
        if tag=='link' and a.get('rel') in ['stylesheet','icon']:self.assets.append(a['href'])
        if tag=='link' and a.get('rel')=='alternate':self.alternates.append(a)

source=json.loads((ROOT/'content/en-US.json').read_text())
checked=0
for locale in LOCALES:
    data=json.loads((ROOT/'content'/f'{locale}.json').read_text())
    assert set(data)==set(source),locale
    assert len(data['cards'])==3 and len(data['steps'])==5 and len(data['faq'])==10,locale
    assert [len(p) for h,p in data['privacySections']]==[2,4,2,2,1],locale
    assert '2026' in data['dates'] and 'Song Li' in data['dates']
    def nonempty(value):
        if isinstance(value,str):assert value.strip(),locale
        elif isinstance(value,list):
            for v in value:nonempty(v)
        elif isinstance(value,dict):
            for v in value.values():nonempty(v)
    nonempty(data)
    for privacy in [False,True]:
        path=ROOT/('' if locale=='en-US' else locale)/('privacy.html' if privacy else 'index.html')
        markup=path.read_text();page=Page();page.feed(markup)
        assert page.lang==locale and page.h1==1 and not page.scripts,path
        assert {a['hreflang'] for a in page.alternates}==set(LOCALES)|{'x-default'},path
        choices=[a for a in page.links if 'hreflang' in a]
        assert len(choices)==9 and sum(a.get('aria-current')=='page' for a in choices)==1,path
        assert all(a['href'].endswith('privacy.html' if privacy else 'index.html') for a in choices),path
        for a in page.links+[{'href':s} for s in page.assets]:
            url=urlparse(a['href'])
            if url.scheme or url.netloc:continue
            target=(path.parent/unquote(url.path)).resolve() if url.path else path
            assert target.is_relative_to(ROOT) and target.is_file(),(path,a['href'])
            if url.fragment:
                linked=Page();linked.feed(target.read_text())
                assert url.fragment in linked.ids,(path,a['href'])
        assert 'songlaoshi666@gmail.com' in markup
        if locale=='en-US':assert 'zh' in page.ids
        checked+=1
print(f'Checked {checked} pages: 9 complete locales, matching section coverage, language-preserving navigation, all local links/assets present, no runtime scripts.')
