#!/usr/bin/env python3
"""Generate complete static pages. No client-side translation or storage."""
import html
import hashlib
import json
import posixpath
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://windgeek.github.io/sweepzen-web/'
LOCALES = ['en-US', 'zh-Hans', 'zh-Hant', 'de-DE', 'es-ES', 'fr-FR', 'ja', 'ko', 'pt-BR']
TEXT = {l: json.loads((ROOT / 'content' / f'{l}.json').read_text()) for l in LOCALES}
EMAIL = 'songlaoshi666@gmail.com'
CSS_REVISION = hashlib.sha256((ROOT / 'style.css').read_bytes()).hexdigest()[:12]

def esc(s):
    return html.escape(s, quote=True)

def page_file(locale, privacy=False):
    return ('' if locale == 'en-US' else locale + '/') + ('privacy.html' if privacy else 'index.html')

def public_url(locale, privacy=False):
    return BASE + ('' if locale == 'en-US' else locale + '/') + ('privacy.html' if privacy else '')

def generate(locale, privacy):
    t = TEXT[locale]
    current = page_file(locale, privacy)
    parent = posixpath.dirname(current) or '.'
    def link(path):
        return posixpath.relpath(path, parent)
    def para(s):
        return f'<p>{esc(s)}</p>'
    support, policy, language = t['nav']
    nav = ''.join(f'<a href="{link(page_file(locale, p))}"' + (' aria-current="page"' if p == privacy else '') + f'>{esc(label)}</a>' for p, label in [(False, support), (True, policy)])
    choices = ''.join(f'<li><a href="{link(page_file(l, privacy))}" lang="{l}" hreflang="{l}"' + (' aria-current="page"' if l == locale else '') + f'>{esc(TEXT[l]["language"])}</a></li>' for l in LOCALES)
    alternates = '\n'.join(f'<link rel="alternate" hreflang="{l}" href="{public_url(l, privacy)}">' for l in LOCALES)
    title = t['privacyTitle' if privacy else 'supportTitle']
    desc = t['privacyDescription' if privacy else 'supportDescription']
    main = ''
    if not privacy:
        main = f'<div class="intro"><div><div class="eyebrow">{esc(t["eyebrow"])}</div><h1>{esc(t["hero"])}</h1><div class="rule"></div><p class="lead">{esc(t["lead"])}</p></div><img src="{link("icon.png")}" alt="" width="150" height="150"></div>'
        main += '<div class="quick">' + ''.join(f'<article><span class="number">{esc(n)}</span><h2>{esc(h)}</h2>{para(p)}</article>' for n,h,p in t['cards']) + '</div>'
        main += f'<section class="reading"><h2>{esc(t["startTitle"])}</h2><ol>' + ''.join(f'<li>{esc(s)}</li>' for s in t['steps']) + '</ol></section>'
        main += f'<section class="reading"><h2>{esc(t["faqTitle"])}</h2>' + ''.join(f'<details class="faq"{" open" if i == 0 else ""}><summary>{esc(q)}</summary>{para(a)}</details>' for i,(q,a) in enumerate(t['faq'])) + '</section>'
        main += f'<section class="reading"><h2>{esc(t["contactTitle"])}</h2><div class="contact"><h3>{esc(t["contactHeading"])}</h3><p><a href="mailto:{EMAIL}?subject=SweepZen%20support">{EMAIL}</a></p>{para(t["contactBody"])}<p><a href="https://github.com/windgeek/sweepzen-web/issues">{esc(t["issueLink"])}</a></p>{para(t["issueWarning"])}</div></section>'
    else:
        main = f'<div class="intro privacy-intro"><div><div class="eyebrow">{esc(t["privacyEyebrow"])}</div><h1>{esc(t["privacyHeading"])}</h1><p class="meta">{esc(t["dates"])}</p></div></div><div class="reading">'
        for i,(heading, paragraphs) in enumerate(t['privacySections']):
            main += f'<section><h2>{esc(heading)}</h2>' + ''.join(para(p) for p in paragraphs)
            if i == 3:
                main += f'<p class="policy-links"><a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">{esc(t["policyLinks"][0])}</a><br><a href="https://www.apple.com/legal/privacy/">{esc(t["policyLinks"][1])}</a></p>'
            if i == 4:
                main += f'<p><a href="mailto:{EMAIL}?subject=SweepZen%20privacy">{EMAIL}</a></p>'
            main += '</section>'
        main += '</div>'
    # Preserve the old public #zh anchors without mixing two policies on one page.
    if locale == 'en-US':
        main += f'<aside id="zh" class="legacy-language" lang="zh-Hans"><a href="{link(page_file("zh-Hans", privacy))}">{esc(t["legacyChinese"])}</a></aside>'
    return f'''<!doctype html>
<html lang="{locale}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="dark">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{public_url(locale, privacy)}">
{alternates}
<link rel="alternate" hreflang="x-default" href="{public_url('en-US', privacy)}">
<link rel="icon" href="{link('icon.png')}">
<link rel="stylesheet" href="{link('style.css')}?v={CSS_REVISION}">
</head>
<body>
<header><a class="brand" href="{link(page_file(locale))}"><img src="{link('icon.png')}" alt="" width="44" height="44">SweepZen</a><div class="header-actions"><nav aria-label="{esc(support + ' / ' + policy)}">{nav}</nav><details class="language-picker"><summary><span class="language-label">{esc(language)}</span><span>{esc(t['language'])}</span></summary><ul>{choices}</ul></details></div></header>
<main>{main}</main>
<footer><span>© 2026 Song Li · SweepZen · macOS</span><a href="mailto:{EMAIL}">{esc(t['contactLabel'])}</a><a href="{link(page_file(locale, True))}">{esc(policy)}</a></footer>
</body>
</html>
'''

for locale in LOCALES:
    for privacy in [False, True]:
        output = ROOT / page_file(locale, privacy)
        output.parent.mkdir(exist_ok=True)
        output.write_text(generate(locale, privacy))
urls = [public_url(l,p) for l in LOCALES for p in [False,True]]
(ROOT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{u}</loc></url>\n' for u in urls) + '</urlset>\n')
print(f'Generated {len(urls)} static pages in {len(LOCALES)} languages.')
