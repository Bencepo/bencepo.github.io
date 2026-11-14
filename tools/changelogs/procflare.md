# Changelog

## 0.3.0

- Own settings window instead of a page in the game's options: drag it anywhere, it stays open while you play and every change applies at once. `/pfl`, the minimap button or the addon menu open it; Options > AddOns > ProcFlare only points to it.
- Sound pack, both sounds and the channel are now picked from lists in the window; picking a sound plays it.
- Warlocks: Shadow Trance (Nightfall) gets the big alert like Clearcasting, in purple. Also found in combat, when the game hides buff details: Shadow Bolt turns instant.
- Reactive abilities: Overpower and Revenge (warrior), Riposte (rogue), Mongoose Bite and Counterattack (hunter) show as a proc for the few seconds after a dodge, parry or block opens them. Only your class's ones; switch off with "Reactive abilities".
- Class procs are now also seen in combat, when the game hides buff details: Flurry and Enrage (warrior), Flurry (shaman), Vengeance and Redoubt (paladin), Remorseless Attacks (rogue), Quick Shots (hunter), Spirit Tap and Focused Casting (priest), Nature's Grace (druid), and the Crusader enchant for everyone.

## 0.2.0

- Two sound packs, both loud and epic: **Melee** (war drums, war horn, axe clash, beast roar, rage spike, thud) and **Caster** (arcane surge, mana burst, frost shatter, fire burst, power chord, spark). ProcFlare picks the pack once from your class and talents; switch it under Options > AddOns > ProcFlare > Sound pack, and change each sound on its own.
- **Volume** slider for ProcFlare's own sounds (25 to 100 %).
- **Sound channel**: ProcFlare plays on the game's Sound Effects channel by default, so the game's volume slider for effects applies too. Master, Ambience or Dialog can be picked instead.
- Sounds you picked by hand stay.

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
