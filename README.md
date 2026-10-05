# SweepZen support website

Public support and privacy pages for SweepZen, a macOS app by Song Li.

- Support: https://windgeek.github.io/sweepzen-web/
- Privacy: https://windgeek.github.io/sweepzen-web/privacy.html

Both pages are available in English (U.S.), Simplified Chinese, Traditional Chinese,
German, Spanish (Spain), French, Japanese, Korean, and Portuguese (Brazil).
The language menu preserves the page type, and Support/Privacy navigation preserves
language. English keeps the original root URLs; the eight other languages use
`/<locale>/` and `/<locale>/privacy.html`. Existing `#zh` anchors still lead to a
Simplified Chinese link.

Static HTML and CSS, with no browser scripts, translation API, analytics, cookies,
third-party fonts, or client-side language storage. GitHub Pages publishes the
root of `main`. Application source is maintained separately.

## Updating content

`content/en-US.json` defines the meaning and structure. The eight other JSON files
contain reviewed translations. After editing, regenerate all 18 checked-in pages:

```sh
python3 scripts/generate.py
python3 scripts/check_site.py
python3 -m http.server 8765
```

There is no deployment build step. Review the generated diff and preview desktop
and narrow layouts before pushing to `main`. Keep translated privacy promises
consistent: local app processing, no network requests, on-device stored state,
user-initiated support mail, public GitHub issues, hosting requests and Apple
services remain separate. Update every language when these facts change.
