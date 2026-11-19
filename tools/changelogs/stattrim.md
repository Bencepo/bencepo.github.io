# Changelog

## 1.0.4

- "Report a bug" button in the list window (`/stt list`): shows the link to the bug reports, ready to copy with Ctrl+C.
- Fix: stats with the same name in merged categories can each be moved with the arrows.
- Fix: when StatTrim gets switched off during combat, the stats panel is put back right after combat.
- Fix: shifted stat labels are set again when the game resets them while scrolling.
- Fix: saved positions anchored to the screen are restored completely.
- Fewer allocations while scrolling in edit mode; commands no longer error before the addon has loaded; `/stt dump` skips protected rows.
- README lists `/stattrim` and `/stt dump`.

## 1.0.3

- Brighter icon that stays readable on the round minimap button.

## 1.0.2

- New icon: gilded stat bars, one cut away, for the minimap button and the addon list.

## 1.0.1

- The stats panel is only laid out again when the game changed it, not ten times a second while the character window is open. Without any hidden or moved stats StatTrim does nothing at all.
- An error during the layout no longer stops StatTrim until a /reload.

## 1.0.0

- Hide whole categories or single stats in the character window's stats panel.
- Hide only a category's name: its stats join the category above.
- Reorder categories and stats with arrows.
- Edit mode right in the window: gear icon above the stats panel (or /stt) shows a checkbox and arrows on every row.
- Works in combat without errors: StatTrim never touches Blizzard's stat list, it only moves and fades the finished rows.
- /stt list: all categories and stats in one window. /stt reset shows everything again, /stt order restores the original order.
