# Changelog

## 0.1.7

- Existing installs switch from the old default sounds (Raid warning, Map ping) to ProcFlare's own sounds once. A sound you picked yourself stays.

## 0.1.6

- ProcFlare's own sounds: "ProcFlare chime" for Clearcasting and "ProcFlare ping" for other procs, the same tones as on the web page. They are the new defaults; the game's sounds (Raid warning, Map ping and others) can still be picked in the options.

## 0.1.5

- Brighter icon that stays readable on the round minimap button.

## 0.1.4

- Icon reworked: bigger die with clear pips and less glare, easy to read even at minimap size.

## 0.1.3

- New icon: a die mid-roll with a glowing face, for the minimap button and the addon list.

## 0.1.2

- Fixed: while your target's debuffs were hidden (in combat), a proc on the target could stop the scan halfway, so procs on you were announced again and again.
- Classes without Clearcasting no longer rescan their buffs on every change of mana, rage or energy; with Clearcasting at most five times a second.

## 0.1.1

- Clearcasting is now also found in combat, where Forever hides buff details from addons: by spell, by the game's own proc glow, or by your abilities becoming free.
- No more "Auras cannot be accessed when secret" errors in combat.
- Spells you cast yourself (e.g. Regrowth) no longer count as procs.

## 0.1.0

- Clearcasting: big pulsing icon above your character as long as the buff is up, with remaining seconds, a sound and a short blue flash at the screen edges. Also alerts again when a new proc refreshes it.
- Other procs (weapon enchants such as Crusader, trinkets, talents): small icons with countdown and a softer sound. Found on their own, no list to maintain.
- Procs on your target: debuffs your weapon or talents put on the target (e.g. Icy Chill, Spell Vulnerability).
- Move mode: drag the icons where you want them; your recent procs are shown and a right-click mutes or unmutes one.
- Options under Options > AddOns > ProcFlare: alerts, sounds, screen flash, only own procs, longest proc duration, size, preview.
- Minimap button and addon menu entry: left-click options, shift-click move mode, right-click preview.
