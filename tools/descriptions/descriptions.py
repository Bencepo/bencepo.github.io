"""One source for every addon description: README.md, CurseForge and Wago.
Style: clear, direct, honest. Same sections in the same order for every addon."""

A = {}

A["leveltrail"] = dict(
    name="LevelTrail", repo="LevelTrail", tag="Your leveling run, analysed",
    lead="Records your leveling run in WoW Forever: time per level, XP sources, deaths, gold and dungeon runs. Paste the export on the website and see your run split by split, with records and a share image.",
    what=[
        ("Level splits", "When each level was reached and how much online time it took."),
        ("XP sources", "Quests, kills and exploration, in total and per level."),
        ("Pace", "XP per hour and the time to the next level and to level 60, in a small tracker window."),
        ("Deaths, gold, repairs", "Per level and per zone; gold per day."),
        ("Zones and dungeons", "Online time, XP and deaths per zone; time, XP and loot per dungeon visit."),
        ("Library books", "Which of the 40 Forever books are handed in, read from your completed quests."),
        ("Several characters", "Each one is kept separately, and the viewer lists your alts."),
    ],
    use=[
        "`/trail` opens the export, already selected: Ctrl+C, then paste it at the website.",
        "`/trail hud` turns the tracker window on or off, `/trail options` sets it up.",
        "Minimap button: left-click settings, right-click export, shift-click tracker on/off.",
        "Place the tracker in the game's Edit Mode; lines, text size, alignment and opacity are set in the settings.",
    ],
    good=[
        "Online time counts from the install on. A level the addon did not see from the start is marked as partial.",
        "Nothing is sent anywhere. The website reads the export in your browser and uploads nothing.",
        "With VendorFloor installed, its auction profit shows up in the export too.",
    ],
    dev="""## Development

- Web viewer: `web/index.html`, published from `Bencepo/bencepo.github.io` (folder `leveltrail/`). Copy it there after changes.
- Tests: `busted` (`tests/`). Roadmap: [ROADMAP.md](ROADMAP.md).
- Release: new version heading at the top of `CHANGELOG.md`, push to `main`; the workflow checks the code and uploads to CurseForge and Wago.""",
)

A["vendorfloor"] = dict(
    name="VendorFloor", repo="VendorFloor", tag="Buy for less than a merchant pays, sell to the merchant, keep the difference",
    lead="VendorFloor is an auction house sniper for WoW Forever. It finds auctions that are worth more than they cost: below vendor price, below disenchant value, or the reagents for a profitable craft. A tab of its own in the auction house window; every purchase is your own click.",
    image="![VendorFloor in the auction house](https://bencepo.github.io/media/vendorfloor/finds.jpg)",
    what=[
        ("Vendor finds", "Auctions below what a merchant pays. Buy, collect from the mail and sell, each with one button."),
        ("Disenchant finds", "Green and blue gear below its disenchant value, from Forever's tables and your own results."),
        ("Disenchant basket", "Enchanters disenchant the bought items one click or one key at a time."),
        ("Crafting profits", "Which of your recipes make a profit right now, reagents from the cheapest source."),
        ("Realistic values", "Materials count at the cheapest listings and at what your auctions really sold for."),
        ("Ledger", "Spent, sold and real profit per session, day and item."),
        ("Continuous mode", "Rescans on its own and announces new finds with an optional sound."),
        ("Ready sound", "A short sound the moment the Check or Buy button can be clicked, so you are faster than the others."),
        ("Share", "Today's and all-time profit as a short text for Discord or chat; the website makes a share image from the export."),
    ],
    use=[
        "Open the auction house and click the VendorFloor tab. The first time, three short callouts show the way: Scan, Check, Buy.",
        "Pick a list and press Scan.",
        "Click a find to check it against the live auctions, then Buy. At the mailbox: Collect purchases; at a merchant: Sell purchases.",
        "Menu (top right): statistics, watchlist, ignore list, export and settings.",
    ],
    good=[
        "The full scan reads every auction at once. The auction house allows it every 15 minutes, and only after your click.",
        "All auction addons share one search channel: stop the scan before searching elsewhere.",
        "Export the ledger and paste it on the website for profit per day and per item.",
    ],
    dev="""## Development

- Ledger page: `web/index.html`, published from `Bencepo/bencepo.github.io` (folder `vendorfloor/`).
- Tests: `busted`. Release: new version heading at the top of `CHANGELOG.md`, push to `main`; the workflow checks the code and uploads to CurseForge and Wago. Changes wait under `## Unreleased` for the weekly release.""",
)

A["procflare"] = dict(
    name="ProcFlare", repo="ProcFlare", tag="Never miss a proc",
    lead="A big pulsing Clearcasting alert with sound and screen flash, and small icons with a countdown for weapon, trinket and talent procs. Nothing to set up.",
    what=[
        ("Clearcasting", "Big icon above your character while the buff is up, with a sound and a short flash. Druid, mage, shaman, and Shadow Trance for warlocks."),
        ("Other procs", "Crusader, trinkets and talent procs as small icons with a countdown. New weapons and trinkets are picked up on their own."),
        ("Reactive abilities", "Overpower, Revenge, Riposte, Mongoose Bite and Counterattack for the seconds they are open."),
        ("Procs on your target", "Debuffs from your weapon or talents, such as Icy Chill."),
        ("Own sound packs", "Melee and caster, with volume and sound channel."),
        ("Proc counter", "Optional: how often each proc fired in this fight and the last one."),
    ],
    use=[
        "`/pfl` or the minimap button opens the window. Drag it anywhere, changes apply live.",
        "Move mode (shift-click the button): drag the alerts, right-click a proc to mute it.",
    ],
    good=[
        "Procs that only deal damage (Fiery Weapon) or grant an extra attack (Hand of Justice, Windfury) cannot be shown: Forever keeps the combat log from addons.",
        "In restricted content (some boss fights, battlegrounds) Forever hides buff data. ProcFlare still tries Clearcasting there.",
    ],
)

A["swingcast"] = dict(
    name="SwingCast", repo="SwingCast", tag="Cast bar plus swing timer",
    lead="Adds spell icon, cast time, latency zone and a swing timer to the standard cast bar instead of replacing it. The strip lights up while Maul, Heroic Strike or Cleave is queued.",
    what=[
        ("Spell icon and cast time", "On the standard cast bar, inside it or left of it."),
        ("Latency zone", "At the end of the bar: once the bar reaches it, press the next spell."),
        ("Swing timer", "A thin strip under the cast bar with the seconds to the next swing."),
        ("Queued swing", "Orange while Maul, Heroic Strike or Raptor Strike is queued, blue for Cleave."),
        ("Your look", "Height, width, position, font, font size and colours."),
    ],
    use=[
        "Switch on Forever's swing timer first: Options > Advanced Options > Swing Timer. \"Hide built-in swing bars\" in the window keeps only the strip visible.",
        "`/swc` or the minimap button opens the window; right-click the button for a preview.",
        "Move the strip in Edit Mode or with \"Move strip\" in the window.",
    ],
    good=[
        "SwingCast mirrors Forever's built-in swing timer. It is the only accurate source, because Forever keeps the combat log from addons.",
        "If the strip ever fails, it switches itself off and the built-in bar comes back.",
    ],
)

A["stattrim"] = dict(
    name="StatTrim", repo="StatTrim", tag="A tidy character window",
    lead="Trim the stats panel of the character window down to what you actually look at: hide, merge and reorder categories and stats right in the window.",
    image="![StatTrim demo](https://bencepo.github.io/media/stattrim/demo.gif)",
    what=[
        ("Hide categories or stats", "A checkbox on every row."),
        ("Merge categories", "Hide just a category name: its stats join the category above."),
        ("Reorder", "Move categories and stats up and down with arrows."),
        ("Edit in the window", "The gear icon above the stats panel switches edit mode on and off."),
    ],
    use=[
        "Open the character window and click the gear icon above the stats.",
        "Right-click the gear icon, or use the addon menu at the minimap, for the list window: every stat with a checkbox and \"Default order\".",
        "`/stt reset` shows everything again, `/stt order` restores the original order.",
    ],
    good=[
        "StatTrim never changes Blizzard's stat list, it only moves and fades the rows. So it keeps working in combat without errors.",
    ],
)

A["transmogsweep"] = dict(
    name="TransmogSweep", repo="TransmogSweep", tag="Collect transmogs from the auction house",
    lead="Every transmog appearance on the auction house you have not collected yet, cheapest first, as a tab in the auction house window. Also finds the recipes your character has not learned yet. Buy them top to bottom with one button.",
    image="![TransmogSweep in the auction house](https://bencepo.github.io/media/transmogsweep/demo.gif)",
    what=[
        ("Its own tab", "Next to the tabs of other auction addons, which stay where they are."),
        ("Fast scan", "Weapons and armor only, a few seconds, repeat it any time."),
        ("What the game says", "Account-wide, exactly as the item tooltip shows \"You haven't collected this appearance\"."),
        ("Unique appearances", "One row per look, the cheapest item. Off: every source you lack."),
        ("Filters", "Usable by my class, slot, search, maximum price, hide items above your level."),
        ("Recipes", "A second list: unlearned recipes for your character's professions, cheapest first. \"Learnable now\" keeps it to what your skill allows today."),
        ("Buy top to bottom", "\"Start buying\" checks the first item, the next click buys it, then the next row is checked by itself."),
    ],
    use=[
        "Open the auction house, click the TransmogSweep tab, pick Appearances or Recipes, press Scan.",
        "Ctrl+click previews an item, right-click hides a look, Alt+click shows a diagnosis for bug reports.",
    ],
    good=[
        "Nothing is ever bought without your click.",
        "Bought looks arrive in the mail and stay hidden until you learn them: wear the item or sell it to a vendor.",
        "Recipes count per character and only for the professions it has.",
    ],
)

A["trinketdock"] = dict(
    name="TrinketDock", repo="TrinketDock", tag="A light trinket menu",
    lead="Two buttons for your trinkets and a flyout to swap them. In combat the swap is queued and done the moment combat ends. Nothing runs in the background.",
    what=[
        ("Two use buttons", "Top and bottom trinket with cooldowns. Click or bind a key."),
        ("Flyout to swap", "Hover a button: left-click a trinket for the top slot, right-click for the bottom slot."),
        ("Queue in combat", "Trinkets cannot be swapped in combat, so the swap waits and happens when combat ends."),
        ("Light", "Bags are read only when the flyout opens. Made as a slim replacement for ItemRack's trinket menu."),
        ("Your layout", "Side by side or stacked, flyout up or down, any scale, lock. Frame and background in colours of your choice, opacity from 0 to 100 %."),
    ],
    use=[
        "`/tdock` or the addon menu at the minimap opens the settings.",
        "Move the dock in the game's Edit Mode or shift-drag a button. Keybindings: Options > Keybindings > TrinketDock.",
    ],
    good=[
        "No work when you loot, none when combat starts or ends.",
    ],
)

A["spikespotter"] = dict(
    name="SpikeSpotter", repo="SpikeSpotter", tag="Find the addon behind the stutter",
    lead="Short FPS drops when you kill, loot or pull? SpikeSpotter asks the game's own addon profiler which addons used those frames and ranks them, with a copyable report.",
    what=[
        ("Catches the stutter", "A frame that takes much longer than usual counts as a spike; loading screens are left out."),
        ("Ranking of the culprits", "Every addon in a spike, with total time, count and its worst frame."),
        ("Game or addon?", "Spikes without a notable addon share count as the game's own: then disabling addons will not help."),
        ("Context", "The game events just before each spike, so you see when an addon gets expensive."),
        ("Copy report", "Ranking and the last 100 spikes as text for a bug report or forum post."),
        ("Off when you are done", "One switch stops all measuring; then it costs nothing."),
    ],
    use=[
        "`/spike` or the addon menu at the minimap opens the window.",
        "Click Reset, play a few minutes the way the stutter happens, read the ranking. Disable the top addon and test again.",
    ],
    good=[
        "SpikeSpotter only names addons that used the spike frames. Whether that addon is broken or just busy, its author has to judge.",
    ],
)

A["profcd"] = dict(
    name="ProfCD", repo="ProfCD", tag="Profession cooldowns at a glance",
    lead="Hover the minimap button for the transmute, Mooncloth and Salt Shaker timers of all your characters. Click it to see which crafts you have the mats for.",
    what=[
        ("Timers on hover", "Every tracked cooldown of every character, with the time left or \"Ready\"."),
        ("Mats check", "Each craft shows \"Mats in bags\", \"Mats in bank\" or what is missing, and for how many crafts."),
        ("Forever cooldowns", "Every transmute on its own cooldown (Arcanite, Truesilver, Gold, the elemental ones), plus Mooncloth and the Salt Shaker."),
        ("Recipes from the game", "Reagents are read from the profession window, so recipe changes show up on their own."),
        ("Alts included", "Other characters show as of their last login."),
        ("Macro instead of a button", "Turn the minimap button off and ProfCD creates a macro: one click opens the window, the next closes it."),
    ],
    use=[
        "Hover or click the minimap button, or type `/pcd`.",
        "The x on a character's line removes it (deleted or renamed characters). `/pcd minimap` toggles the button.",
    ],
    good=[
        "Log in once with each crafter so ProfCD knows its cooldowns.",
        "Cooldown durations come from the game, so changes in Forever are picked up without an update.",
    ],
)


def body(a, readme):
    k = [x for x in A if A[x] is a][0]
    out = [f"# {a['name']}", "", f"**{a['tag']}.** {a['lead']}", "",
           f"**Website and live demo:** https://bencepo.github.io/{k}/", ""]
    if a.get("image"):
        out += [a["image"], ""]
    out += ["## What it does", ""] + [f"- **{t}{'' if t[-1] in '?!' else '.'}** {d}" for t, d in a["what"]] + [""]
    out += ["## How to use", ""] + [f"- {u}" for u in a["use"]] + [""]
    out += ["## Good to know", ""] + [f"- {g}" for g in a["good"]] + [""]
    issues = f"https://github.com/Bencepo/{a['repo']}/issues/new/choose"
    if readme:
        fb = f"Found a bug or have an idea? [Open an issue]({issues}), it takes a minute. No GitHub account? Comment on [CurseForge](https://www.curseforge.com/wow/addons/{k}#comments). Every report gets read."
    else:
        fb = f"Found a bug or have an idea? [Open an issue on GitHub]({issues}) or leave a comment. Every report gets read."
    out += ["## Feedback and bug reports", "", fb, ""]
    out += ["## More from Bencepo", "",
            "All addons, live demos and guides: **https://bencepo.github.io**", "",
            "Like the addons? Support them on Ko-fi: **https://ko-fi.com/bencepo**", ""]
    out += ["## AI disclosure", "",
            "The code was written with the help of an AI assistant (Claude). Bencepo designed the features, tests everything in game and maintains the addon.", ""]
    if readme:
        if a.get("dev"):
            out += [a["dev"], ""]
        out += ["## License", "", "All rights reserved, see [LICENSE](LICENSE).", ""]
    return "\n".join(out)


if __name__ == "__main__":
    import os
    os.makedirs("/home/claude/desc/out", exist_ok=True)
    for k, a in A.items():
        open(f"/home/claude/desc/out/{k}.README.md", "w").write(body(a, True))
        open(f"/home/claude/desc/out/{k}.store.md", "w").write(body(a, False))
    print("ok")
