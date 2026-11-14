# Changelog

## 0.9.0

- Settings in a window of their own instead of a page in the game's options: drag it anywhere, it stays open while you play and every change applies at once. Open it from the menu (Settings) or with `/vfloor options`; Options > AddOns > VendorFloor only points to it.

## 0.8.6

- Brighter icon that stays readable on the round minimap button.

## 0.8.5

- New icon: a gold coin in a sniper reticle, for the minimap button and the addon list.

## 0.8.4

- Less work outside the auction house: casting spells no longer reads the bags (only Disenchant does, and not in combat); looting no longer rescans the bags for the purchase tracker or an empty disenchant basket. Sales at a merchant are still counted.
- The window redraws at most ten times a second while item data loads during a scan, and its buttons no longer rebuild their frame on every hover.
- Closing the auction house now also ends a running scan, check or quote and frees the full scan's auction list.

## 0.8.3

- Full scans on a client with an empty item cache (a fresh install, or a client language you play for the first time: the cache is kept per language) found almost nothing, because most items had not loaded within 30 seconds. The scan now asks for each item once and keeps waiting as long as items keep arriving, up to 3 minutes.
- Normal scans also pick up items whose data arrives later.

## 0.8.2

- The disenchant basket is its own small window now, not a button on the mail window. It only appears for characters that can disenchant, and only when new disenchant purchases arrive in your bags, or when you open it by hand (Menu > Disenchant basket). It closes when it is empty or with its x, and you can drag it anywhere.

## 0.8.1

- Removed fallbacks for old clients (bags, addon info) and the spare minimap button that was only used without LibDBIcon.
- Code check with LuaLS and the WoW API annotations runs with every change.

## 0.8.0

- Disenchant basket: items bought on the disenchant tab go into a basket. At the mailbox a "Disenchant basket" button appears below "Collect purchases": each click disenchants the next item, no cursor, no searching the bags. It also works on a key (Key Bindings > AddOns > VendorFloor), anywhere, not only at the mailbox. Every disenchant is still one click or key press. In combat the button does nothing.
- Vendor purchases that land in the reagent bag (profession bag) when collected from the mail are now sold at the merchant like the rest.
- An auction the auction house refuses to sell ("Internal auction error") is no longer offered again and again: each auction is bid on once, then the next one is checked.

## 0.7.0

- First release out of beta.
- While a full scan runs, the window says what is happening and that the first finds appear in about a minute, instead of an empty list.
- The progress bar shows "loading item data" in the second half of a full scan instead of "waiting for the auction house".
- "1 find" and "1 craft with profit" instead of "1 finds" and "1 crafts"; no stray comma before the profession list.
- The disenchant tab explains where its values come from (WoW Forever tables and your own results).
- New addon description in the addon list and in addon managers.

## 0.6.4-beta

- Now also on Wago Addons.
- Own minimap and addon list icon.
- Own auctions: a buyer or an expiry is counted for the oldest auction without a buyer yet, so expired auctions are no longer missed after a sale.
- Automated tests (busted) for prices, minimum profit, disenchant values and own auctions run with every change.

## 0.6.3-beta

- Minimum profit in percent right in the window: click for more, right-click for less. It also hides finds that are already listed.
- New Menu button: statistics, your disenchants, your auctions, export and settings, without chat commands.
- Wands made by enchanters are no longer offered as disenchant finds; an item the game refuses to disenchant is remembered and hidden too.
- The saved finds follow every quick scan, check and purchase, not only the full scan: the next visit no longer starts with finds that are long gone, and new finds from quick scans are kept.
- Every checked item updates its stored price (median and cheapest listings), so prices stay fresh between full scans.
- The tooltip of a disenchant find says whether its value comes from your own disenchants or from the general table.

## 0.6.2-beta

- VendorFloor learns from your own disenchants: it records what each item gave you, and after 3 disenchants of an item (or 5 of the same kind and item level) it values finds by your real results instead of the general table.
- New command /vfloor de shows your recorded disenchant results.
- VendorFloor records your own auctions (also when posted with Auctionator): how long until a buyer is found, the price that sold and how many expire. Disenchant materials and crafted items are valued at the price that really sold and by the share that sells. /vfloor sales shows it.

## 0.6.1-beta

- Much faster buying of gear finds (disenchant tab, gear in the vendor tab): a purchase check that gets no answer gives up after 5 instead of 15 seconds, tries the plain item key right away, and remembers per item which key works.
- Each tab scans for itself: "Scan" on the disenchant tab reads only green and blue weapons and armor, the vendor tab only looks for vendor finds (lighter on the frame rate). The crafting tab gets a "Prices" button: one search per reagent and product of your recipes, the current price goes into the price history. Continuous mode follows the tab shown; full scans still fill every tab.
- Realistic material prices: disenchant values and crafting use the price of the cheapest listings (the price a sale has to beat, or the price you buy at) instead of the median, which was too optimistic (a shard valued at 25s that sells for 22s).
- Disenchant values now follow the WoW Forever table: rows by the level required to equip the item (not its item level), the same row for green and blue items, a shard chance of about 4% for greens. Before, the Classic table by item level gave values one band too high or too low.
- Disenchant finds are grouped by item: all levels and suffixes of an item are one row (they disenchant the same). Buying tries the cheapest variant first, then the next.
- Disenchant finds show their disenchant value ("DE ~13s 19c") instead of a vendor price in the list, the status line and chat.
- Items bought on the disenchant tab can be taken out of the mail with "Collect purchases" as well.
- Removed the market tab and posting: too many questionable finds and checks. Price history stays (disenchant materials, crafting).
- Disenchant tab between full scans: normal scans and quick rounds also find gear below its disenchant value (with the prices stored by earlier full scans).
- The finds of the last full scan (up to an hour old) are back when you open the auction house again, so the tabs are not empty until the next full scan is allowed. They are checked when you click them.
- At most 150 checks per round, the most promising first; the rest follow in the next round.
- Sound and taskbar flash once per round (at most once a minute) instead of per find; the check counter counts up correctly.
- Quieter chat: no line per find any more, one line per round with the new finds per tab (sound and taskbar flash stay).

## 0.6.0-beta

- New tab **Crafting**: which of your learned recipes make a profit right now. Product value: auction house after the 5% cut or a merchant, whichever is more; reagents: auction house or merchant, whichever is cheaper. Recipes are read when a profession window is open (a "Craft profits" button there opens the tab), merchant prices of reagents when a merchant window is open, auction prices come from full scans. `/vfloor craft` lists the best ten in chat.

## 0.5.0-beta

- Three tabs, never mixed: **Vendor** (below what a merchant pays), **Market** (far below the usual price, to sell again on the auction house) and **Disenchant** (green and blue weapons and armor below what disenchanting them brings).
- Price history: every full scan stores the usual price of each item (median, last 14 days). The market tab uses it; it gets better with every day of full scans.
- Disenchant values after the Classic disenchant tables, with the materials at their usual price (an estimate: WoW Forever may differ).
- Posting: in the market tab a "Post" button puts the next item bought there on the auction house for 24 hours, just under its usual price and never below cost plus the minimum profit. One auction per click. Sales come from the seller mails and go into the ledger.
- Minimum profit in percent and per bag slot (whole auction), for all tabs: `/vfloor percent 20`, `/vfloor slot 10s`, also in the settings.
- Quick rounds: items found below vendor price before are kept on a watch list; continuous mode checks the most frequent of them one by one (two quick rounds, then one full item list), and runs a full scan whenever one is allowed. `/vfloor quick` starts one by hand.
- Taskbar flash on new finds while the game is in the background (`/vfloor flash`, settings).
- New look: flat dark window in the colours of the web page, gold accents, flat buttons (also at the mailbox and merchant), a "Continuous" switch, zebra rows and a clearer progress bar. Larger text throughout; the buy button shows its amounts in dark text so they stay readable on gold.
- Fix: single items (e.g. bags) could show hundreds of units for one auction, with a unit price below 1 copper and a huge fake profit. Units per auction are now capped at the stack size, and prices below 1 copper per unit are ignored.
- Fixed: the "Sell purchases" button at a merchant (and "Collect purchases" at the mailbox) could appear as an empty red bar without its text until the bags changed.
- Minimap button (LibDBIcon, so minimap button collectors can take it): left-click opens the ledger export (at the auction house: the window), right-click prints the totals, the tooltip shows today's and the total profit. Drag to move, `/vfloor minimap` hides or shows it. VendorFloor also appears in the game's addon menu next to the minimap.
- Continuous mode: between two rounds the scan button shows "Stop (12)" with the seconds to the next round, so it is clear the loop is running. While a round, the checks or the loop run, the button stays pressed in. A click stops it.
- Fixed: the arrow between auction and vendor price showed as an empty box.
- Progress bar shows its text: percent of the full scan, "checking 12 of 40 (30 %)", or the auctions read so far.
- Fixed: after a purchase the round could stop with "Bought." and a half-full bar, because the auction house kept reporting that it was not ready for the next query. Such a query is now sent anyway after 10 seconds. `/vfloor debug` prints the internal state if it still happens.
- Sales by other addons count: bought items sold at a merchant in any way (for example by an addon that sells grey items automatically) now go into the ledger. VendorFloor counts them from the bags.
- Faster checks: a check waits 3 instead of 6 seconds for an answer, and a find that stays silent twice (sold out meanwhile) is skipped for 30 minutes instead of being checked every round.
- Fewer useless checks: an item checked without a buyout below the vendor price (for example one with bid-only auctions) is skipped for 30 minutes, unless a cheaper listing appears.

## 0.4.0-beta

- Ledger per day and per item: spending, sales and real profit per calendar day (last 120 days), and per item how many were bought and sold and how long they waited until the sale.
- `/vfloor export`: the ledger as text to copy into the new web page https://bencepo.github.io/vendorfloor/ (profit per day, best items, holding time). Nothing is uploaded; the page runs in your browser.
- LevelTrail, if installed, shows your VendorFloor profit next to your gold curve and per play session.

## 0.3.0-beta

- Full scan: reads every auction of the auction house at once (allowed every 15 minutes). Each auction comes with its buyout, so finds appear complete and without checking each item. Between full scans the normal rounds keep running.
- Collect purchases: a button at the mailbox takes the items VendorFloor bought out of the auction house mail.
- Sell purchases: a button at a merchant sells them, at most as many as VendorFloor bought, so items of your own stay.
- Ledger counts sales and the profit they really made, profit per hour and what is still to sell. `/vfloor stats` shows the totals, `/vfloor forget` clears the purchases still to sell.
- Progress bar for full scans and checks, and a summary line with the cost and profit of the whole list.

## 0.2.2-beta

- Faster checking: results the auction house already holds are read at once instead of after a 15 second wait.
- Fewer lost finds: a check without an answer is tried again later instead of dropping the find, and several variants of one item (e.g. "of the Bear", "of the Monkey") whose data is still loading are all kept.
- Stackable goods appear in the list right after the scan; the check then counts the units below vendor price ("?×" until then).
- Single items are checked first, best potential profit first.

## 0.2.1-beta

- Fixed: the window failed to open with "attempt to index upvalue 'L'" when the texts file had not been loaded. VendorFloor now falls back to English texts.

## 0.2.0-beta.2

- English interface; German when the game client is German.
- Key binding "Buy next find" (Options > Keybindings > AddOns) and `/vfloor buy`: each press checks or buys the best find.
- Stackable goods are checked before they are listed, so the list shows how many units are really below vendor price.
- Each row shows the total profit and the number of units.
- Right-click a find to hide that item for good. `/vfloor ignore list` and `/vfloor ignore clear`.
- Settings under Options > AddOns > VendorFloor: alert sound, continuous mode, pause between rounds, minimum profit.
- Session ledger in the window (buys, spent, vendor value, profit) and `/vfloor stats` for totals since install.
- The version is shown in the window title and in `/vfloor help`.
- The list is cleared when the auction house closes, since prices change in the meantime.

## 0.1.0-beta

- First release. Finds auction house listings priced below vendor value and buys them on click.
- Only auctions with a buyout price are listed; bid-only auctions are ignored.
- Adjustable minimum profit per unit (`/vfloor profit`).
- Interface currently in German.
