# Changelog

## 1.3.0

- Trinket swaps while casting (a mount, for example) are queued like in combat and done as soon as the cast ends, so the cast is not cancelled.
- Empty trinket slots are now hidden automatically: with one trinket equipped only that slot is shown, and with none equipped the dock hides (still visible in Edit Mode).
- Tooltips on the dock and in the flyout now show only the hovered trinket, without equipped comparison tooltips.
- Settings window: "More from Bencepo" button in the footer links to all Bencepo addons (BencepoUI 6).
- Code cleanup, no change in behaviour.

## 1.2.1

- Fixed: clicking a trinket in combat with slight mouse movement no longer triggers `ADDON_ACTION_BLOCKED` in `OnDragStop`; exiting Edit Mode as combat begins no longer leaves the Edit Mode mover blocking the trinket buttons; queued post-combat swaps now wait if you are dead or casting instead of being lost, and out-of-combat swaps verify the bag slot first.
- Lower memory and event overhead: bag scans read item IDs and links directly without allocating `ContainerItemInfo` tables for every slot, `BAG_UPDATE_COOLDOWN` only refreshes cooldowns, and `PLAYER_EQUIPMENT_CHANGED` updates only the changed slot.
- Shared settings window updated to BencepoUI 5.

## 1.2.0

- The dock can be placed in the game's Edit Mode: it shows there (blue, with its name) even when hidden or locked. With Edit Mode's "Snap" on it snaps flush to the other Edit Mode frames, the screen edges and the screen centre; without it, it stays where you drop it. Shift-drag still works as before.

## 1.1.1

- The shared settings window (BencepoUI) is now one version for all Bencepo addons: "Report a bug" sits in a footer of its own, and the hint in the title row no longer runs into the title.

## 1.1.0

- Frame and background for the dock, each on or off, with a colour of your choice (window: Look). The background also has its own opacity.
- Opacity of the whole dock from 0 to 100 %. At 0 % the buttons are invisible but still clickable, and keybindings keep working.

## 1.0.1

- New icon in the addon list and in the addon menu at the minimap, part of the new Bencepo logo family.

## 1.0.0

- Two use buttons for the top and bottom trinket, with cooldowns. Keybindings for both.
- Flyout with the trinkets in your bags: left-click equips to the top slot, right-click to the bottom slot.
- In combat the flyout queues the swap: it happens as soon as combat ends, shown as a small icon on the button.
- No background work: bags are read only when the flyout opens.
- Side by side or stacked, flyout up or down, scale, lock, Shift-drag to move.
- Settings window of its own with a "Report a bug" button.
