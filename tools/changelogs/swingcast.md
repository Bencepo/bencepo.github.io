# Changelog

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
