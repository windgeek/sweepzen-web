# Localization review — 2026-10-05

Support and privacy pages now cover the app/storefront's nine locales:
`en-US`, `de-DE`, `es-ES`, `fr-FR`, `ja`, `ko`, `pt-BR`, `zh-Hans`, `zh-Hant`.
English defines meaning; localized wording is not runtime machine translation.

## Content review

Each translation was compared with the English source for the following points:

- Scan, storage map, uninstall, background/extensions and toolbox are separate
  paths. No automatic administrator deletion or system menu removal is promised.
- Shared data and data used by another app copy remain protected. Folder grants
  and macOS restrictions are explicit. Only in-app removals use Trash; restoration
  ends when the user empties it. No automatic Trash emptying or Time Machine
  snapshot deletion is promised.
- File processing and stored bookmarks, preferences and listed-app identifiers
  remain on the Mac. This description was checked against SweepZen 1.2's
  Preferences.swift, entitlements and navigation. Opening help links uses the
  system browser; the app has no network requests.
- Email and public GitHub issues are user-initiated, separate from app data.
  Support deletion requests retain the qualification for applicable retention
  obligations. GitHub hosting requests and Apple services have their own policies.
- Developer, public support email and policy links stay identical across languages.
  The original effective date is retained; October 5 is the clarification and
  translation update date, not a new data-collection practice.

The app's localized feature titles were used for the getting-started instructions.
Original `/` and `/privacy.html` URLs still work; old `#zh` anchors retain a link
into Simplified Chinese. Other locales have complete independent pages.

## Verification

- Regeneration and static checks pass for all 18 pages: matching section coverage,
  one H1, correct lang/hreflang, all nine language links, page-type preservation,
  valid relative links/assets, and no browser scripts.
- Browser layout checks pass for every page at 320, 390 and 1280 px: 54 layouts
  without horizontal overflow. Desktop and mobile contact sheets were inspected.
- German narrow-screen heading overflow was fixed. Japanese privacy title sizing
  avoids a lone final character. Mobile help text uses the full available width.
- Mobile language menu shows all nine languages within the viewport. Actual
  navigation Portuguese privacy → Japanese privacy → Japanese support → Chinese
  support preserves the correct language/page type.
- The site adds no cookies, analytics, fonts, or third-party translation service.
  GitHub Pages continues to publish checked-in HTML directly from main.

Browser screenshots and DOM layout records are kept in the separate SweepZen
workspace under Store/QA/2026-10-05/Website; they are not part of the public site.

## Support and privacy clarification — 2026-10-06

The nine locales now explain folder access versus administrator authorization,
remaining or restarted background helpers, and optional post-removal login-item
checks. Search-name copying and rechecking match the revised 1.2 interface. All
added translations were reviewed against the English source and back-checked for
these preserved meanings: no administrator privilege from a folder grant; no
automatic removal when a helper stops; no guarantee that emptying Trash clears a
macOS settings record. German retains the site's established informal address.

Privacy text now explicitly describes local process-name/executable-path checks
and user-triggered clipboard writes. Existing clipboard contents are not read.
The original effective date remains unchanged; the clarification date is October
6. No new collection, upload, tracking or external transmission is introduced.
This was checked against the app's ProcessProbe, UninstallModel, clipboard writes,
entitlements and privacy manifest.

Regeneration and 18-page checks passed. All 54 support/privacy layouts (9 locales
at 320, 390 and 1280 px), including opened FAQ text and language menus, were
checked for horizontal overflow. The French menu at 320 px needed right alignment
when navigation wraps; this is fixed for every locale. Full screenshots and
review contact sheets are stored separately in SweepZen/Store/QA/2026-10-06/Website.


## Restarting helpers — 2026-10-06

The helper FAQ in all nine locales now explains the optional Login Items & Extensions background-activity route. Reviewed and back-checked each translation against the app copy: only clearly associated entries should be changed; publisher entries can affect other apps; unidentified entries should stay unchanged. Returning triggers a check, not removal, and stopping every helper is not guaranteed. No privacy practice changed.
