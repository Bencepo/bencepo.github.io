# bencepo.github.io

Web pages for Bencepo's World of Warcraft: Forever addons.

- [Home and import hub](https://bencepo.github.io/): all addons, paste any export and the right page opens.
- [LevelTrail](https://bencepo.github.io/leveltrail/): paste the `/trail` export and see your leveling run, records, achievements and a share image.
- [VendorFloor](https://bencepo.github.io/vendorfloor/): paste the VendorFloor export and see profit per day, cumulative profit, best weekdays, all items and a share image.
- [ProcFlare](https://bencepo.github.io/procflare/), [SwingCast](https://bencepo.github.io/swingcast/), [StatTrim](https://bencepo.github.io/stattrim/): addon pages with a live demo, features and changelog.

All pages run entirely in the browser; nothing is uploaded.

## Structure

- `assets/site.css`, `assets/site.js`: shared design and helpers (import hand-off between pages, toasts, section tabs).
- `assets/icons/`: addon icons (64, 128, 256 px). `assets/fonts/`: Cinzel (SIL Open Font License).
- `tools/build.py`: generates `index.html`, `procflare/`, `swingcast/`, `stattrim/`, and refreshes header, footer, versions and changelogs inside `leveltrail/` and `vendorfloor/` (between the `<!--@...-->` markers).
- `tools/changelogs/<addon>.md`: copy of each addon's `CHANGELOG.md`.

After an addon release: copy its `CHANGELOG.md` to `tools/changelogs/`, run `python3 tools/build.py`, commit and push.

The LevelTrail and VendorFloor pages are edited here directly; the addon repos keep a copy in `web/index.html`.

Copyright (c) 2026 Bencepo. All rights reserved. Source is visible for hosting only; no licence to copy, modify or redistribute is granted.
