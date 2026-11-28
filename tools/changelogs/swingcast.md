# Changelog

## 1.1.4

- Fix: the swing strip did not show in combat. It no longer depends on Forever's built-in swing timer: it now runs on the game's own swing event, so the "Swing Timer" game option is no longer needed.
- The swing time follows your attack speed: Cat Form, Bear Form, haste buffs and slows are counted in, and a change mid-swing rescales the rest of the running swing.
- The off-hand strip only shows with a weapon in the off hand.
- Settings window: "More from Bencepo" button in the footer links to all Bencepo addons (BencepoUI 6).
- Code cleanup, no change in behaviour.

## 1.1.3

- Zero idle frame work: the swing driver sleeps whenever no swing bar or preview is active, and queued-ability tinting updates on `CURRENT_SPELL_CAST_CHANGED` instead of polling `IsCurrentSpell` 20 times per second.
- Fixed: `applySelection` no longer wipes the cast bar's Edit Mode selection box if anchors were not ready yet, and respects combat lockdown; queued-ability tinting now colours only the Main-Hand bar (not Off-Hand or Ranged); visible strips stack without empty gaps; toggling the latency zone updates an active cast immediately.
- Shared settings window updated to BencepoUI 5.

## 1.1.2

- The shared settings window (BencepoUI 4): the hint in its title row ("drag to move …") no longer runs into the title and version; it is shortened or left out when there is no room.

## 1.1.1

- The swing strip preview from the minimap button no longer ends the preview of the open settings window after 8 seconds.
- English only: the German description in the addon list is removed.
- The shared settings window (BencepoUI) is now one version for all Bencepo addons: every settings window looks and works the same, whichever addon loads first.

## 1.1.0

- The settings window now uses the same look as the other Bencepo addons. The font is picked from a list.

## 1.0.0

- New icon in the addon list and on the minimap button, part of the new Bencepo logo family.
- SwingCast is now 1.0: stable after the 0.x releases, nothing else changes.

## 0.5.4

- Fix: Lua error at login ("attempt to call a nil value", line 585) with other addons' frames loaded, for example the damage meter. The swing strip then stayed without its position. The search for swing bars under other names from 0.5.3 is removed again.

## 0.5.3

- Fix: the built-in swing timer showed up again next to SwingCast's strip. The game sets its bars visible again on its own (on a swing, after Edit Mode or a loading screen); SwingCast now keeps them hidden on every frame while "Hide built-in swing bars" is on.
- Swing bars the game adds under another name are picked up as well.

## 0.5.2

- "Report a bug" button in the window: shows the link to the bug reports, ready to copy with Ctrl+C.
- Fix: the spell icon disappears with the cast instead of staying while the cast bar fades out.
- Fix: `/swc reset` also puts the window back in its default place.
- Fix: `/swc lock` says so when the strip is already locked.
- Fix: extra spaces in commands (`/swc color  swing`) no longer break them.

## 0.5.1

- Spell icon inside the cast bar, at its left end and as high as the bar (new default), so it needs no room next to the bar. "Icon inside the bar" off puts it left of the bar as before.
- With the icon left of the bar, Edit Mode's box around the cast bar includes the icon's room, and Edit Mode shows a placeholder icon, so you see where it lands while placing the bar.

## 0.5.0

- Own options window instead of a page in the game's options: drag it anywhere, it stays open while you play and every change shows live. `/swc`, the minimap button or the addon menu open it; the game's options only point to it. While it is open the swing strip shows a preview.
- Move the swing strip: in the game's Edit Mode it shows up as a blue frame you can drag, like the game's own frames. Or "Move strip" in the window (`/swc unlock`), right-click to lock. Width for the free position, "Default position" puts it back under the cast bar.
- Fix: when another addon hides or replaces the standard cast bar, the swing strip no longer ends up in the top left corner. It switches to its own position and tells you once in chat.
- New commands: `/swc unlock`, `/swc lock`, `/swc width <60-600>`, `/swc attach`, `/swc position reset`. `/swc help` lists all.

## 0.4.4

- Brighter icon that stays readable on the round minimap button.

## 0.4.3

- New icon: a blazing weapon swing above a cast bar, for the minimap button and the addon list.

## 0.4.2

- With the swing strip switched off, SwingCast no longer does any work each frame.

## 0.4.1

- The cast time label is only redrawn when the shown value changes, not every frame.
- Code check with LuaLS and the WoW API annotations runs with every change; removed fallbacks for old clients.

## 0.4.0

- First stable release. No functional changes since 0.3.2.
- README and project description now lead with the options window; chat commands moved to an advanced section.

## 0.3.2-alpha

- Own minimap and addon list icon.

## 0.3.1-alpha

- Now also released on Wago.

## 0.3.0-alpha

- Font: choose the font of the cast time and the swing seconds (the fonts every client has) and its size, in the options window or with `/swc font <7-20>`.
- Colours: swing strip, queued swing, Cleave and latency zone each get a "Choose" button in the options window that opens the game's colour picker, plus a reset button. Also `/swc color swing|queued|cleave|latency|reset`.

## 0.2.0-alpha

- Minimap button: left-click opens the options, right-click shows the swing strip preview. `/swc minimap` hides or shows it.
- Entry in the game's addon menu next to the minimap, with the same clicks.
- Options window under Options > AddOns > SwingCast with every setting, including the strip height.
- `/swc options` opens the options window.
- Fixed: `/swc swingText` and `/swc hideNative` did nothing because the command is read in lower case.

## 0.1.1-alpha

- Swing strip copies the built-in timer's values and seconds label as they are. Forever hands the attack speed to addons as a secret value that cannot be calculated with.
- If the strip fails, it switches itself off and the built-in swing timer is shown again.

## 0.1.0-alpha

- Spell icon, remaining cast time and latency zone on the standard player cast bar.
- Swing strip under the cast bar, mirrored from Forever's built-in swing timer (main hand, off hand and ranged where present).
- Strip turns orange while Maul, Heroic Strike or Raptor Strike is queued, blue for Cleave.
- `/swc` settings, `/swc test` preview.
- Released on CurseForge (project 1800255).
