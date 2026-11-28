# SwingCast

**Cast bar plus swing timer.** Adds spell icon, cast time, latency zone and a swing timer to the standard cast bar instead of replacing it. The strip lights up while Maul, Heroic Strike or Cleave is queued.

**Website and live demo:** https://bencepo.github.io/swingcast/

## What it does

- **Spell icon and cast time.** On the standard cast bar, inside it or left of it.
- **Latency zone.** At the end of the bar: once the bar reaches it, press the next spell.
- **Swing timer.** A thin strip under the cast bar with the seconds to the next swing. It follows your attack speed: forms, haste buffs and slows count, also mid-swing. The off-hand strip shows only with a weapon in the off hand.
- **Queued swing.** Orange while Maul, Heroic Strike or Raptor Strike is queued, blue for Cleave.
- **Your look.** Height, width, position, font, font size and colours.

## How to use

- Works without Forever's own swing timer option. If you have it switched on, "Hide built-in swing bars" in the window keeps only the strip visible.
- `/swc` or the minimap button opens the window; right-click the button for a preview.
- Move the strip in Edit Mode or with "Move strip" in the window.

## Good to know

- SwingCast times each swing from the game's own swing event (main hand, off hand, ranged), so Cat Form, Bear Form, haste buffs and slows are counted in. A speed change mid-swing rescales the rest of the swing.
- If the strip ever fails, it switches itself off and the built-in bar comes back.

## Feedback and bug reports

Found a bug or have an idea? [Open an issue on GitHub](https://github.com/Bencepo/SwingCast/issues/new/choose) or leave a comment. Every report gets read.

## More from Bencepo

All addons, live demos and guides: **https://bencepo.github.io**

Like the addons? Support them on Ko-fi: **https://ko-fi.com/bencepo**

## AI disclosure

The code was written with the help of an AI assistant (Claude). Bencepo designed the features, tests everything in game and maintains the addon.
