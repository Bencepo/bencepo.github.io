# Changelog

## 1.4.0-beta

- New "Report a bug" button in the export window (and `/trail bug`): shows the link to the bug report page, ready to copy with Ctrl+C.
- XP: the first XP after a break or a fresh install is no longer lost, and a jump over several levels counts the full XP of the levels in between.
- Play sessions: online time keeps a session going even without XP (crafting, auction house, travel); a session that ended is saved with its last numbers; kills, quests and loot after a break go to the new session; sessions are recorded at the level cap too. `/trail session` says when no session is running.
- Logging out after XP-only play now saves the latest XP, level and session.
- Dungeon visits: kills and deaths count even before the first session of a login; a visit ends when you come back to life outside, and time outside the instance no longer counts.
- Zone times: the minute before a loading screen goes to the zone you left.
- Loot value: items the game had not loaded yet are valued as soon as their data arrives.
- Bank: the first bank bag is read again, and a scan right after closing the bank no longer wipes the saved bank contents.
- Reputation: factions under collapsed headers and headers with their own standing are listed; your collapsed headers stay collapsed.
- Spell ranks are read on non-English clients; recipes "in range" are the ones that still give skill; recipes of linked or other players' professions are no longer saved as yours.
- Deaths are counted per level for the web viewer, so the deathless streak and its badge use every death.
- Esc closes the export window even without clicking into the text; a clear message when the character is not loaded yet; `/trail minimap` says so when there is no minimap button.
- Minimap settings moved to their own saved variable (`LevelTrailSettings`).
- Web viewer: safer import (only numbers where numbers belong), times no longer show "60 min", the level cap comes from the export, "Hide character name" stays on, a notice when the browser does not keep the import, and better screen reader support.

## 1.3.6-beta

- Brighter icon that stays readable on the round minimap button.

## 1.3.5-beta

- New icon: glowing footsteps climbing to a star, for the minimap button and the addon list.

## 1.3.4-beta

- /trail hud, /trail minimap, /trail session and /trail help no longer rebuild the whole character snapshot first.
- Bank and recipe scans wait a second after the last change instead of running on every single item move or craft.

## 1.3.3-beta

- Less work while farming: the character snapshot (bags, quests, talents, reputation, spells) is rebuilt at most once a minute instead of after every loot or money change; right away on level-up, zone change, export and logout.
- Removed fallbacks for old clients and the spare minimap button that was only used without LibDBIcon.
- Code check with LuaLS and the WoW API annotations runs with every change.

## 1.3.2-beta

- Now also on Wago Addons.
- Automated tests (busted) for chat parsing, pace and formatting run with every change.

## 1.3.1-beta

- Own minimap and addon list icon.
- Removed everything left from the former name BencepoExport: the data takeover, the `/bx` command, the optional dependency and the `legacy/` and `migration/` folders. Use `/trail` or `/lt`.
- Exports no longer carry the `bencepoExport` marker; the web viewer only reads LevelTrail exports.

## 1.3.0-beta

- Best zone per level: online time and XP per zone and level (`char.zoneLevels`).
- Session recap: kills, quests, deaths and vendor value of the loot per play session; `/trail session` shows the running session in chat.
- Dungeon runs: every visit to a dungeon or raid with time, XP, gold, kills, deaths and loot (`char.dungeons`, last 50).
- Travel time: time on flights and corpse runs, in total and per level (`char.travel`).
- Quest numbers (`char.questStats`: completed, quest log, quests per level) and talent trees with points (`char.talentTrees`).
- Web viewer: level times compared with your other characters, best zone for your level, rested XP, travel time, quests, talents (unspent points), gear (weakest slots), professions (at the cap), reputation, death analysis, last session recap, dungeons.

## 1.2.0-beta

- Minimap button (LibDBIcon, so minimap button collectors can take it): left-click opens the export for the web page, right-click turns the tracker window on or off, drag to move. `/trail minimap` hides or shows it. LevelTrail also appears in the game's addon menu next to the minimap.

## 1.1.0-beta

- Tracker window (`/trail hud`): level progress, time on the level, session and average XP per hour, time to the next level and to 60. Movable, remembers position and visibility per character.
- Pace: XP per hour from the last five full levels (or the session), time to the next level and the level cap, in the export (`char.pace`) and in `/trail chat`.
- Zones: online time, XP and deaths per zone (`char.zones`).
- `/trail help` lists the commands.
- Web viewer: XP per hour, time to 60 from the addon, zones table.
- VendorFloor: if Bencepo's auction house addon VendorFloor is installed, its profit is part of the export (account-wide totals, profit per day, and per play session). The web viewer shows it next to the gold curve. Without VendorFloor nothing changes.
- Play sessions in the web viewer show gold per hour.

## 1.0.0-beta

- First public version: level splits, XP sources, deaths, gold per day, repairs, play sessions, library books (WoW Forever) and a copyable export (`/trail`) for the LevelTrail web viewer at https://bencepo.github.io/leveltrail/
