# Account-level / player-level skill, talent and research trees (mobile, card battlers, roguelites)

Notes compiled 2026-11-24. Reliability tags:
- **[fetched]**: the page itself was read.
- **[snippet]**: the fact came from a search-result summary and the page was not opened. The URL is the most likely origin among the results, but tie it to that exact page only with care.

Fandom wikis (archero, hades, summonerswar, raid, kingdomrush, clashofclans) returned HTTP 402 to the fetcher, so most numbers come from guide sites, wiki.gg, cookierun.wiki and official publisher pages.

---

## Q1. Mobile account/commander/base trees: structure, gating, currency, cost curves, respec

### Takeaway
On mobile, "account trees" come in five recurring shapes:
1. **Random-draw talent pool** (Archero).
2. **Research lab with timers**, one queue, and a paid extra queue (Clash of Clans, Cookie Run: Kingdom).
3. **Point-allocation branches with a hard point cap and paid respec** (Rise of Kingdoms commanders).
4. **Faction-wide stat buildings** bought with a PvP or side currency (Raid Great Hall, Summoners War sanctuaries).
5. **Level-sharing devices** that make the roster cheap to use (AFK Arena Resonating Crystal / AFK Journey Resonating Hall).

Almost all are pure-stat and steeply back-loaded. The quality-of-life and rule changes usually sit in the economy branch (production, storage, research speed) rather than in combat.

### Cited Findings

**Archero (original, 2019 to now) and Archero 2**
- Talents are permanent stat upgrades bought with gold, and each purchase gives a *random* talent (examples: max HP, damage, attack speed). The deconstruction's author criticises the randomness: in harder chapters "it gets frustrating and pushes players away". [fetched] — [Game Developer, "Finding the fun: Archero part 2 – progression" (2019)](https://www.gamedeveloper.com/design/finding-the-fun-archero-part-2---progression)
- Same article on the other layers:
  - Equipment has 6 slots (1 weapon, 1 armor, 2 rings, 2 spirits) and 6 rarity tiers. It levels with gold plus type-specific scrolls, and 3 identical items fuse into the next rarity.
  - Gacha boxes: 1 free, 1 per day for an ad, a better one weekly, more for gems.
  - A gold spinner at run start pays more in later chapters, which the author calls a catch-up mechanic.
  - Core loop: "fight, get rewards, improve", and each new chapter resets the player to "too weak".
  - [fetched] — [Game Developer](https://www.gamedeveloper.com/design/finding-the-fun-archero-part-2---progression)
- Cost and order rules [snippet]:
  - "You purchase a random talent and each time you do so the cost of the next random talent goes up."
  - Talents unlock in a fixed order.
  - Glory maxes at level 1, other talents at 10 (one guide lists Strength at 20).
  - "Once you hit 15 Talents, you'll only be able to upgrade once per account level after that."
  - Sources: [Gamezebo talents list](https://www.gamezebo.com/walkthroughs/archero-talents-list-a-list-of-all-talents-and-how-to-get-them/); [ProGameGuides talents list](https://progameguides.com/archero/archero-talents-list/)
- Archero talent gold cost table: 200 gold at level 1, 800 by level 10, 2,600 by level 20. The wiki table is garbled, so treat these as approximate. [snippet] — [Archero Fandom "Talent"](https://archero.fandom.com/wiki/Talent)
- One guide: upgrading 22 times in total unlocks the final talent, "Time Reward". [snippet] — [ProGameGuides](https://progameguides.com/archero/archero-talents-list/)
- Archero 2: "Talent Cards" come from a gold draw. Each card acquired raises the cost of the next, each chapter opens new Talent Cards, and cards come in tiers. This is a single low-confidence source. [snippet] — [TheriaGames](https://theriagames.com/?p=86962)

**Survivor.io**
- The Evolve tab (main menu, far right) lets players "invest gold and other materials in order to unlock a variety of passive upgrades that permanently enhance the stats of your characters". It is separate from in-run weapon evolutions, which need weapon at 5 stars plus a paired passive. [snippet] — [BlueStacks Survivor.io beginner guide](https://www.bluestacks.com/blog/game-guides/survivor-io/sio-beginner-guide-en.html); [BlueStacks skills & evolution guide](https://www.bluestacks.com:443/blog/game-guides/survivor-io/sio-skills-evolution-guide-en.html)

**Clash of Clans Laboratory (per-unit research, account-owned building)**
- Single-queue research with multi-day timers. One guide lists Barbarian level 7 at 10 days, Archer level 7 at 14 days and Dragon level 8 at 12 days, and the Lab's own level-10 upgrade at 6 days. [snippet] — [Pocket Gamer, Laboratory breakdown](https://www.pocketgamer.com/clash-of-clans/laboratory-clash-of-clans-building-breakdown)
- One article claims "over 1,500 days" of total Lab upgrades. This is unverified. [snippet] — [TheGlobalGaming, longest upgrades](https://theglobalgaming.com/clash-of-clans/what-is-the-longest-upgrade)
- Supercell repeatedly cuts research and build time and cost ("a TON of upgrade cost and upgrade time reductions", Dec 2023). [snippet] — [Supercell, Cost and time reductions Dec 2023](https://supercell.com/en/games/clashofclans/blog/news/cost-and-time-reductions-december-2023/)

**Rise of Kingdoms: commander talent trees**
- Max commander level is 60 and max talent points is 74. Each commander has 3 specialties mapped to 3 talent trees, and only the *primary* commander's talents apply in a march. [snippet] — [RiseOfKingdomsGuides, talent tree](https://riseofkingdomsguides.com/talent-tree/)
- "Talent Tree 2.0" (2018) reset every commander's talents and refunded all points. Points come back on reset. No source found for today's paid reset item price. [snippet] — [AppGamer, Talent Tree 2.0 update](https://www.appgamer.com/talent-tree-2-0-update); [AppGamer answer on reset](https://www.appgamer.com/rise-of-kingdoms/answers/25448-what-happens-when-you-reset-the-tal)

**Cookie Run: Kingdom: Sugar Gnome Laboratory (account research, two branches)**
- Unlock and building cost: unlocks at Cookie Castle Lv.5, and building it costs 5 Tempered Pickaxe + 2 Diggy Shovel. [fetched] — [cookierun.wiki Sugar Gnome Laboratory](https://cookierun.wiki/w/Sugar_Gnome_Laboratory)
- Research slots and sub-trees:
  - One research at a time; the page says a Kingdom Pass allows up to 6 at once.
  - Two sub-trees: **Kingdom Technologies** (economy, production, storage, QoL) and **Cookie Technologies** (Cookie stats, adventure helpers such as Topping Upgrade Cost Reduction and Arena Ticket Recharge Rate).
  - [fetched] — same source
- Roster-wide nodes:
  - All-Cookie stat nodes unlock by lab level: HP (Lab Lv.6 row), DEF (Lv.8), ATK I (Lv.9), CRIT DMG (Lv.12).
  - Class-wide nodes also exist (e.g. "Charge Cookies: HP Bonus I").
  - [fetched] — same source
- Lab upgrade coin cost by Cookie Castle level is roughly geometric:

  | Cookie Castle level | Coins |
  |---|---|
  | 5 | 100k |
  | 6 | 200k |
  | 7 | 400k |
  | 8 | 600k |
  | 9 | 900k |
  | 10 | 1.2M |
  | 11 | 1.5M |
  | 12 | 1.8M |
  | 13 | 2.0M |

  Each level also needs a growing count of building materials. [fetched] — same source
- Speed-ups: maxed research-efficiency technologies cut research time by 45%, and collecting all Silence Yeast Ore cuts another 30%. [fetched] — same source
- Example node cost: "Toppings: Cheaper Upgrades I" costs 70,000 coins, takes 2 h and needs Lab Lv.4. [snippet] — [cookierun.wiki Cookie Technologies](https://cookierun.wiki/w/Cookie_Technologies)
- Guide advice is to prioritise Kingdom (economy) research over Cookie (stat) research. [snippet] — [CharlieIntel CRK lab guide](https://charlieintel.com/cookie-run-kingdom-sugar-gnome-laboratory-guide-best-upgrades-tips/212761)

**AFK Arena Resonating Crystal / AFK Journey Resonating Hall (roster level-sharing)**
- Pentagram rules:
  - The 5 highest-level heroes sit on a 5-slot "Crystal Pentagram", and any other slotted hero is raised to the level of the lowest of those 5, within its ascension cap.
  - Once 5 heroes reach level 240 the cap can be broken; the crystal's own level then drives the slotted heroes.
  - Removing a hero puts that slot on a 24 h cooldown, skippable with diamonds.
  - [fetched] — [afk.guide Resonating Crystal](https://afk.guide/resonating-crystal)
- AFK Journey's Resonating Hall works the same way: level 5 heroes and the rest follow the lowest of them, the top 5 can be repositioned at any time, and the cap breaks at 240. [snippet] — [LootBar AFK Journey Resonating Hall guide](https://lootbar.gg/blog/en/afk-journey-resonating-hall-guide-optimal-resonance-setup.html)

**Raid: Shadow Legends Great Hall (affinity-wide account buffs)** — see Q6 for numbers.

**Summoners War buildings (element-wide account buffs)** — see Q6.

### Inferences
- The sources split cleanly into **stat trees** (Archero talents, Survivor.io Evolve, the CRK Cookie branch, Raid, Summoners War) and **economy/QoL trees** (the CRK Kingdom branch, the CoC lab queue). Guides tend to tell players to buy economy nodes first (CRK), so economy nodes work like compounding interest and stat nodes like a tax.
- Timer-plus-queue labs (CoC, CRK) make money through extra queues (CRK: Kingdom Pass gives up to 6 slots) and speed-ups. Point-cap trees (RoK) make money through respec items and commander duplicates. Random-draw trees (Archero) make money only indirectly, through gold.
- Level-sharing devices (AFK Resonating) are an "anti-tax" layer: they remove the per-unit grind so a large roster stays usable. This matters for a 78-hero roster like PokiClash's.

### Gaps
- **Lords Mobile research, Hero Wars, Legend of Mushroom, PvZ2 plant mastery, Rush Royale, Clash Mini, Squad Busters, Monopoly Go-likes, Pokémon Café/Puzzle meta:** not researched in this pass (tool-call budget). No cited data.
  - Unverified background: Lords Mobile has an Academy research tree with several categories (Economy, Defense, Military, Monster Hunting…).
  - Unverified background: Clash Mini was shut down by Supercell (historical).
  - All of this needs checking before use.
- **Archero 2 Talent Cards:** exact numbers (costs, tiers, chapter gates) not found.
- **Survivor.io Evolve:** node layout (base nodes vs special nodes, player-level gates) not found.
- **Rise of Kingdoms:** current paid talent-reset cost and the "expertise" rules not found.
- **CoC Lab:** current total time to max at TH17/TH18 not confirmed by a primary source.
- **AFK Crystal:** cost to level the crystal after the 240 cap break not found.
- **Raid masteries:** per-champion mastery trees (Offense/Defense/Support, scroll costs) not researched.

---

## Q2. Roguelite meta trees (Hades, Rogue Legacy, Dead Cells, Vampire Survivors, Darkest Dungeon, etc.)

### Takeaway
Roguelite meta systems fall into four types:
1. **Slot-based talents with A/B alternates and swaps** (Hades Mirror of Night).
2. **Flat shops whose prices inflate globally** (Vampire Survivors: +10% per purchase; Rogue Legacy 2: every purchase raises *all* costs).
3. **Unlock shops that widen the item pool** (Dead Cells blueprints and the Collector).
4. **Base-building with multi-currency heirlooms** (Darkest Dungeon Hamlet).

The best-liked designs make respec cheap or free and mix rule changes (extra lives, starting kits, new classes, custom mode) with modest stat bumps.

### Cited Findings

**Hades: Mirror of Night**
- Structure and currency:
  - Talents are bought with Darkness; each slot has two mutually exclusive versions (e.g. Death Defiance vs Stubborn Defiance).
  - "Only one version of each ability can be active at a time, and they can be switched between freely while reflecting at the Mirror."
  - [snippet] — [Gamepressure: what carries over](https://www.gamepressure.com/hades/progress-what-gets-carried-forward/z9ebaa); [Prima Games Mirror guide](https://primagames.com/gaming/hades-guide-mirror-of-night-upgrades-fated-list-of-prophecies)
- Slot unlocks: the first 4 talents are free, and later ones unlock in pairs for Chthonic Keys. One guide gives 5, then 10, then 20, then 30 keys (12 slots in total). Some guides date from Early Access, so check these numbers. [snippet] — [SegmentNext Mirror guide (2020)](https://segmentnext.com/2020/09/23/hades-mirror-of-night-upgrades-guide/); [Prima Games](https://primagames.com/gaming/hades-guide-mirror-of-night-upgrades-fated-list-of-prophecies)
- Respec: "Refunding Darkness costs one Chthonic Key and refunds all Darkness spent." The refund option unlocks after several escape attempts. [snippet] — [GameSkinny, how to reset the Mirror](https://www.gameskinny.com/tips/how-to-reset-the-mirror-of-night-in-hades/)
- Example costs [snippet] — [Fextralife Mirror of the Night](https://hades.wiki.fextralife.com/Mirror+of+the+Night); [Hades wiki (Gamepedia) Fated Authority](https://hades.gamepedia.com/Fated_Authority):
  - **Fiery Presence:** 5 ranks at 10/15/20/25/30 Darkness (100 total), available from the start, bonus damage vs undamaged foes. Per-rank % conflicts: 15% per Fextralife, 10% per PC Invasion.
  - **Stubborn Defiance:** 1 rank, 600 Darkness, revive at 30% HP once per chamber. It is the alternate to Death Defiance.
  - **Ruthless Reflex:** 1 rank, 75 Darkness, +50% damage and dodge for 2 s after a last-moment dash.
- Rule-changing vs stat: the Defiance pair (extra lives) and Ruthless Reflex (a new dash mechanic) change rules, while Fiery Presence is pure %. [snippet] — same sources

**Rogue Legacy 2: Castle (manor) upgrades**
- "For upgrades with multiple levels, each further level costs more gold investment, but more than that, every upgrade you buy also increases the cost of all other upgrades." [snippet] — [Digital Trends RL2 beginner's guide](https://digitaltrends.com/gaming/rogue-legacy-2-beginners-guide)
- Classes unlock through the castle tree with prerequisites (e.g. Archery Range → Ranger). There are 15 classes in 1.0, against 4 in an early-access-era guide. Gold-gain upgrades exist to speed up later purchases. [snippet] — [Prima Games, how to unlock classes in RL2](https://primagames.com/tips/how-to-unlock-new-classes-in-rogue-legacy-2)

**Dead Cells**
- Between biomes the Collector trades Cells for permanent upgrades and weapon (blueprint) unlocks. Guides rank extra Health Flasks as "by far the most important permanent improvement". [snippet] — [GameSpot Dead Cells guide](https://www.gamespot.com/gallery/dead-cells-guide-10-tips-we-wish-we-knew-before-st/2900-2201/); [Gamepressure: what to unlock first](https://www.gamepressure.com/dead-cells/what-uprgrades-should-be-unlocked-first/z0b356)
- Recycling, starting kits and runes:
  - Recycling I/II convert found items into gold (Recycling II costs 120 cells).
  - Recycling Tubes let the player choose among starting equipment sets.
  - Runes are permanent traversal abilities.
  - [snippet] — [Dead Cells wiki.gg Runes](https://deadcells.wiki.gg/wiki/Runes)
- Custom Mode lets players unlock or relock items and change rules. Its unlock moved in patch 1.2.10 (now: a mini-boss on Prison Roofs). [snippet] — [GOGDB Dead Cells release notes](https://www.gogdb.org/product/1237807960/releasenotes)

**Vampire Survivors: PowerUp shop (flat, non-tree)**
- Price inflation: each PowerUp bought raises the price of later ones by 10%. Guides disagree on whether this is 10% of the current price or of the base price, so purchase order changes the total spent. [snippet] — [GamerJournalist PowerUps prices](https://gamerjournalist.com/vampire-survivors-powerups/); [KosGames optimal order](https://kosgames.com/vampire-survivors-optimal-powerup-selection-order-15884/)
- Totals: one guide gives 97,140 gold to buy everything (order: Amount > Growth > Cooldown > …). An older guide says 202,000, so totals vary by version. [snippet] — same
- Refund returns 100% of coins with no penalty and also resets the price inflation. [snippet] — [Prima Games PowerUp order](https://primagames.com/tips/best-purchase-order-for-powerup-shop-in-vampire-survivors)

**Darkest Dungeon: Hamlet (multi-currency base tree)**
- Currencies: four heirloom currencies (Bust, Portrait, Deed, Crest), plus Blueprints in the Crimson Court DLC for Districts. Crests are used by every building; Busts by Abbey, Sanitarium and Stage Coach recruits; Portraits by Guild and Tavern; Deeds by Blacksmith and Stage Coach. [fetched] — [Darkest Dungeon wiki.gg Heirlooms](https://darkestdungeon.wiki.gg/wiki/Heirlooms)
- Total to max every building:

  | Scope | Bust | Portrait | Deed | Crest | Blueprint |
  |---|---|---|---|---|---|
  | Base game | 534 | 241 | 421 | 2,042 | – |
  | With Districts (DLC) | 674 | 396 | 731 | 3,967 | 12 |

  [fetched] — same
- In-dungeon carry caps: 12 Crests, 6 Busts/Deeds, 3 Portraits. Trading heirlooms always loses value (e.g. 3 Crests → 1 Bust; Portrait → Crest at 1:3). [fetched] — same

### Inferences
- Global price inflation (VS, RL2) turns a flat shop into a soft "choose your order" puzzle without a visible tree. A free full refund (VS) removes the fear of a wrong pick. Hades charges a small, rare currency (1 key) for a full refund.
- The A/B alternate per slot (Hades) is the cleanest way to make an account tree "horizontal": the player invests once and then picks a playstyle. The swap is free and the power level stays the same.
- Multi-currency gating (Darkest Dungeon heirlooms with carry caps) ties the meta tree to *where* players go. This works like PokiClash's per-island progression: each island could drop its own tree currency.

### Gaps
- **Rogue Legacy 1 manor, Loop Hero camp, Brotato, Risk of Rain, Inscryption:** no sources gathered this pass.
  - Unverified background: Brotato, Risk of Rain and Inscryption have *no* stat meta tree; progression is unlock-only, which makes them useful as counterexamples.
- **Hades:** exact total Darkness to max the Mirror not found (unverified recollection: about 6–7k).
- **Hades II:** Arcana cards (its meta system) not researched.
- **Rogue Legacy 2:** exact gold cost formula not found.

---

## Q3. Card battlers with account progression (LoR Path of Champions, Marvel Snap, Clash Royale, Slay the Spire 2, Monster Train 2, Balatro, Hearthstone, TCG Pocket)

### Takeaway
Card games keep account progression mostly **horizontal or cosmetic** and move power into collection breadth:
- **Clash Royale (May 2026)** replaced XP with a Collection Level (sum of card levels) and a King Tower Level gated by card thresholds.
- **Marvel Snap's** Collection Level is a reward track that unlocks card pools.
- **LoR Path of Champions'** Legend Level is the closest true account tree that "powers up your whole roster". Its rewards are rule and economy perks (rerolls, starting gold, shop and healer upgrades), not raw stats.
- **Roguelike deckbuilders** (StS2 Epochs, Monster Train 2 clan levels, Balatro) unlock content only and give no power.

### Cited Findings

**Legends of Runeterra: Path of Champions (PvE roguelite)**
- Legend Level (account):
  - Max 30. It "powers up your whole champion roster" and rewards carry over between champions.
  - Points come from first clears of adventures and from quests.
  - Rewards by level:
    - Rerolls: +1 at L1, 2 at L8, 3 at L18, +1 at L26.
    - Starting gold: +100 at L11, +200 at L28.
    - Gold gain: +10% at L9, +20% at L16, +10% gold earned at L24.
    - Shop upgrades at L6 and L13; healer upgrades at L10, 15 and 20.
    - Relics at L5 and L12.
    - At L22, champions can appear in reward picks and shops.
    - Wild Fragments (42 in total) at L21–29.
  - [fetched] — [Riot Support: Legend Level](https://support.riotgames.com/en-us/legends-of-runeterra/gameplay/legend-level-the-path-of-champions)
- Champion Level (per champion): max 30, earned from champion XP (failed runs still give XP). Levels grant deck upgrades, items and Relic slots. [fetched] — [Riot Support: Champion levels and stars](https://support.riotgames.com/en-us/legends-of-runeterra/gameplay/champion-levels-and-stars-the-path-of-champions)
- Stars (per champion): 0–3, costing 10/20/40 champion fragments. Each star adds or upgrades a "game-changing" Star Power, e.g. Jinx: 1 Nexus damage when you play or discard a card, upgraded at 3★ to also hit a random enemy. [fetched] — same
- Patch 3.8 reset PoC progression into three power layers: Champion levels, Star Powers and Legend Levels. Common and Rare relics became shared across the roster. [snippet] — [Dot Esports on Patch 3.8](https://dotesports.com/?p=593671)

**Clash Royale: progression overhaul (announced 13 May 2026, live 26 May 2026)**
- Collection Level:
  - It equals the sum of all owned card levels, plus 5 per Evolution or Hero form (125 cards at the time).
  - Unlocking higher rarities gives more levels (e.g. unlocking Valkyrie gives +3), and each upgrade gives +1.
  - Milestones start at CL 20 and come every 10 levels, every 5 after CL 1500.
  - Milestone rewards: Gems, Wild Cards, Lucky Chests, Evolution Boxes, banners and a tower skin.
  - [fetched] — [Supercell: New Collection Levels & Mastery changes](https://supercell.com/en/games/clashroyale/blog/news/new-collection-levels-and-mastery-changes/)
- King Tower Level:
  - It now comes from card thresholds (KT2 needs 9 cards at L1+; KT16 needs 14 cards at L15+) and can never go down.
  - Tower Troops are capped at KT level and don't count toward it.
  - Each KT level-up grants a full upgrade's worth of Tower Princess cards and Gold.
  - [fetched] — same
- Removals and feature gates: XP and King's Journey are removed ("No more complicated XP systems"; players should "always know how close you are"). Feature unlocks moved from King Level to Arenas (e.g. Card Mastery from King Level 14 to Arena 4). [fetched] — same
- Card Mastery: tasks made easier (Hog Rider's first task cut from 85,000 to 37,000 damage) and now pay a flat 4,000/6,000/15,000 Gold. Gems and Wild Cards moved from Mastery to Collection Level milestones. [fetched] — same
- Earlier, in June 2025, 2,525 Gems were moved from Card Mastery rewards to Trophy Road. [snippet] — [Sportskeeda, Card Mastery reward changes (17 Jun 2025)](https://www.sportskeeda.com/mobile-games/clash-royale-card-mastery-reward-changes-explained-june-17-2025)
- Max Collection Level at launch: 2,265. [snippet] — [Sportskeeda May 2026 update](https://www.sportsdunia.com/gaming/clash-royale-may-update-2026) (aggregator; may be imprecise)

**Marvel Snap: Collection Level as a reward track**
- Pool brackets by Collection Level: Pool 1 runs CL 18–214 (46 cards), Pool 2 runs CL 222–474 (25 cards), Pool 3 starts at CL 486. Mystery cards drop every 8–12 CL in Pool 2. Pool 3's size conflicts across sites (76 vs 104 cards). [snippet] — [MarvelSnapZone progression guide](https://marvelsnapzone.com/marvel-snap-progression-guide/); [PCGamesN pool series](https://www.pcgamesn.com/marvel-snap/pool-cards-series)
- After CL 500 the track feeds Spotlight Caches, later Tokens: 3,000 tokens every 120 CL. [snippet] — same

**Slay the Spire 2 (Early Access from 5 March 2026)**
- "Epochs" on a Timeline are the meta system. They unlock cards, relics, potions, characters and Ancients, mostly by beating the game with each character; some are score-based. [snippet] — [Destructoid: how to unlock all Epochs](https://www.destructoid.com/how-to-unlock-all-epochs-in-slay-the-spire-2/); [PC Gamer EA features](https://www.pcgamer.com/games/roguelike/slay-the-spire-2-early-access-features)

**Monster Train 2**
- Old clans unlock after 6 Pyre Hearts plus a clan-specific task. Clan levels unlock new cards and champions, and clan level 5 unlocks alternative clan leaders. [snippet] — [bo3.gg, unlocking old clans](https://bo3.gg/games/articles/how-to-unlock-old-clans-in-monster-train-2)
- The "Destiny of the Railforged" DLC adds the Soul Savior mode, which permanently unlocks "souls" as a new meta-progression. [snippet] — [PC Gamer DLC details](https://pcgamer.com/games/card-games/monster-train-2-destiny-of-the-railforged-details)

**Balatro**
- Unlock-only: unlocks come from in-game actions, milestones and deck wins. There are 15 decks and 8 stakes, and Challenges open after 5 wins. No permanent power. [snippet] — [games.gg unlock guide](https://games.gg/balatro/guides/how-to-unlock-everything-balatro/); [Dot Esports stakes order](https://dotesports.com/indies/news/all-balatro-stakes-in-unlock-order)

### Inferences
- In LoR PoC, the account layer (Legend Level) gives **run-economy and rule perks** (rerolls, gold, shop and healer quality, champions in the reward pool). Per-unit power sits on the champion (levels, stars, Star Powers). This split maps directly onto a "tamer tree + per-creature evolution" model.
- Clash Royale's 2026 overhaul shows the 2026 trend toward a **transparent, derived account level** (computed from collection rather than an XP grind) with milestone rewards and no separate tree.
- Clash Royale and Marvel Snap keep account progression from buying PvP power directly; tower-troop power is capped at King Tower level.

### Gaps
- **LoR PoC:** the Riot pages describe 3 stars and Legend Level 30. Unverified background: later patches (2023–2024) raised stars to 6 and added Constellations per champion, so check the live version.
- **Hearthstone Mercenaries:** historical, shut down 2023 (background, unverified here).
- **Hearthstone Battlegrounds:** progression not researched.
- **Pokémon TCG Pocket:** progression not researched.
- **Marvel Snap:** card upgrades being cosmetic only (they raise Collection Level but not power) is widely known but was not confirmed in a fetched source this pass.

---

## Q4. How trees avoid being mandatory stat taxes; rule-changers vs pure %

### Takeaway
The evidence points to four techniques:
1. **Cheap or free respec and A/B swaps** (Hades, Vampire Survivors, Kingdom Rush free star reset).
2. **Rule, QoL and economy nodes instead of stats** (LoR Legend Level rerolls and shop; CRK Kingdom tech; Dead Cells flasks, starting kits and Custom Mode; RL2 class unlocks).
3. **Visible caps and derived levels** (Clash Royale King Tower can't go down; tower troops capped).
4. **Content-unlock-only meta** (Slay the Spire 2, Balatro, Monster Train 2 clan levels).

Pure-% trees with no reset (Raid Great Hall: "cannot revert") are the clearest examples of stat taxes.

### Cited Findings
- Design framing: meta-progression is "a persistent layer above run-level systems". Calibration is the central problem: too weak feels meaningless, too strong trivialises the challenge. Some games slow meta-progression on purpose to keep runs tense. [snippet] — [GameBrief glossary: meta progression](https://www.gamebrief.net/glossary/meta-progression)
- Vertical vs horizontal: Slay the Spire's meta adds options and variety, while Dead Cells' raises starting power. A Moonlighter 2 analysis places Hades as "variety-plus-power" and StS as "variety-only". [snippet] — [GameBrief](https://www.gamebrief.net/glossary/meta-progression); [Moonlighter 2 progression analysis](https://saschb2b.github.io/game-mechanics/games/moonlighter-2/progression)
- Kingdom Rush (original): stars buy upgrades in 6 trees (4 towers, 2 spells) with 5 upgrades each, 65 stars for everything. A Reset button refunds all stars at any time, so the tree works as a free-respec loadout. [snippet] — [wikily.gg Kingdom Rush upgrades](https://wikily.gg/kingdom-rush/upgrades); [Kingdom Rush Fandom Upgrades](https://kingdomrushtd.fandom.com/wiki/Upgrades)
- Later Kingdom Rush games:
  - Vengeance and KR5 Alliance use upgrade points earned only in Campaign; in Alliance, stars are only a cosmetic progress marker.
  - Heroes earn hero points by levelling and spend them on abilities (Frontiers, Origins, Vengeance).
  - KR6 Genesis has 4 tower trees with 7 upgrades each; a full path costs 14 points, 56 for all.
  - [snippet] — [wikily.gg KR6 tower upgrades](https://wikily.gg/kingdom-rush-6-genesis/tower-upgrades); [GrindNStrat KR6 tower upgrades guide](https://grindnstrat.com/kingdom-rush-6-genesis-tower-upgrades-guide/)
- Raid Great Hall: "once you've upgraded a stat boost in the Great Hall, you cannot revert your decision". [fetched] — [GamerEmpire Great Hall guide](https://gamerempire.net/raid-shadow-legends-great-hall-guide/)
- Archero talents are random draws with no player choice, which the 2019 deconstruction says frustrates players in harder chapters. [fetched] — [Game Developer](https://www.gamedeveloper.com/design/finding-the-fun-archero-part-2---progression)
- Rule-changing node examples:
  - Hades Death Defiance / Stubborn Defiance (extra lives) [snippet] — [Fextralife](https://hades.wiki.fextralife.com/Mirror+of+the+Night)
  - LoR rerolls, starting gold, shop and healer upgrades, champions in the reward pool [fetched] — [Riot Support](https://support.riotgames.com/en-us/legends-of-runeterra/gameplay/legend-level-the-path-of-champions)
  - Dead Cells Recycling Tubes (choice of starting kit) and Custom Mode (lock or unlock items, change rules) [snippet] — [Dead Cells wiki.gg](https://deadcells.wiki.gg/wiki/Runes); [GOGDB release notes](https://www.gogdb.org/product/1237807960/releasenotes)
  - RL2 class unlocks [snippet] — [Prima Games](https://primagames.com/tips/how-to-unlock-new-classes-in-rogue-legacy-2)
  - CRK research queue and storage QoL [fetched] — [cookierun.wiki](https://cookierun.wiki/w/Sugar_Gnome_Laboratory)
  - AFK level sharing [fetched] — [afk.guide](https://afk.guide/resonating-crystal)

### Inferences
- A practical rule from these examples: **stats as the filler between rule-changing keystones**. Hades mixes 1-rank keystones costing hundreds of Darkness with 5-rank % nodes costing tens; LoR places rerolls and shop upgrades every few levels with gold % in between.
- A free or cheap respec turns a tree from a tax into a **loadout**. That fits a game where island, element and boss matchups vary (as in PokiClash's 5 parallel islands).
- Derived levels (Clash Royale Collection Level, Marvel Snap CL) avoid a separate "spend points" decision entirely. That is an option if the goal is pacing rewards rather than choice.

### Gaps
- No quantitative player-sentiment or retention data compares respec-able vs locked trees; none was found.
- No GDC talk or developer post on account-tree tax avoidance was retrieved this pass. Deconstructor of Fun, Naavik and GameRefinery searches were not run because of the call budget.

---

## Q5. Cost curves and pacing (time to fill, soft caps, chapter/biome gating)

### Takeaway
Cost curves are almost always convex.
- **Back-loaded:** Raid's per-slot medal cost grows about 20× from level 1 to 10, and changes currency tier along the way.
- **Roughly geometric:** CRK lab coin costs double, then grow linearly into the millions.
- **Global inflation:** Vampire Survivors (+10% per buy) and RL2 (every buy raises all prices).

Gating is by account or castle level (Raid L6, CRK Castle 5–13), by chapter (Archero 2 Talent Cards per chapter; Archero 15 talents then one per account level), by key currency (Hades), or by stage and star progress (Kingdom Rush). Full-completion times range from hours (VS, Kingdom Rush) to many months (CoC lab, Darkest Dungeon districts).

### Cited Findings

**Raid Great Hall cost and bonus table (per slot)** [fetched] — [GamerEmpire](https://gamerempire.net/raid-shadow-legends-great-hall-guide/)

| Upgrade | Cost |
|---|---|
| 0→1 | 50 Bronze |
| 1→2 | 150 Bronze |
| 2→3 | 300 Bronze |
| 3→4 | 400 Silver |
| 4→5 | 500 Silver |
| 5→6 | 600 Silver |
| 6→7 | 700 Gold |
| 7→8 | 800 Gold |
| 8→9 | 900 Gold |
| 9→10 | 1,000 Gold |

- Exchange rates: 1 Silver = 2 Bronze, 1 Gold = 4 Bronze.
- One slot costs 500 Bronze + 1,500 Silver + 3,400 Gold, about 17,100 Bronze-equivalent. All 24 slots cost about 410,400 Bronze-equivalent. These totals are the fetch tool's arithmetic from the page table, not stated by the page.
- Bonus curve: HP/ATK/DEF give +2, 3, 4, 6, 8, 10, 12, 14, 17, 20%. C.DMG gives +2…+25%. RES/ACC give +5…+80 flat.

**Other games**
- CRK lab level coin cost runs 100k, 200k, 400k, 600k, 900k, 1.2M, 1.5M, 1.8M, 2.0M (Castle 5→13). Research-speed nodes cut timers by up to 45%. [fetched] — [cookierun.wiki](https://cookierun.wiki/w/Sugar_Gnome_Laboratory)
- Archero talents: gold cost about 200 (L1), 800 (L10), 2,600 (L20) (garbled table). After 15 talents, one upgrade per account level. [snippet] — [Archero Fandom](https://archero.fandom.com/wiki/Talent); [Gamezebo](https://www.gamezebo.com/walkthroughs/archero-talents-list-a-list-of-all-talents-and-how-to-get-them/)
- Vampire Survivors: +10% per purchase, about 97k gold for everything (version-dependent), free refund. [snippet] — [KosGames](https://kosgames.com/vampire-survivors-optimal-powerup-selection-order-15884/); [Prima Games](https://primagames.com/tips/best-purchase-order-for-powerup-shop-in-vampire-survivors)
- Hades: the Chthonic Key unlock cost per slot pair escalates (5 → 10 → 20 → 30, per one guide). Per-rank Darkness escalates (Fiery Presence 10 → 30). [snippet] — [SegmentNext](https://segmentnext.com/2020/09/23/hades-mirror-of-night-upgrades-guide/); [Fextralife](https://hades.wiki.fextralife.com/Mirror+of+the+Night)
- Kingdom Rush: 65 stars for the whole original upgrade tree. Stars come from stage clears (up to 3 per stage), so the tree fills with campaign completion. [snippet] — [wikily.gg](https://wikily.gg/kingdom-rush/upgrades)
- Darkest Dungeon: about 3,967 Crests and 12 Blueprints to max everything with DLC, gated by small carry caps per expedition (12 Crests). [fetched] — [DD wiki.gg](https://darkestdungeon.wiki.gg/wiki/Heirlooms)
- Clash of Clans: per-level research of 10–14 days at mid tiers, possibly more than 1,500 days in total (unverified). Supercell periodically cuts timers. [snippet] — [Pocket Gamer](https://www.pocketgamer.com/clash-of-clans/laboratory-clash-of-clans-building-breakdown); [Supercell Dec 2023](https://supercell.com/en/games/clashofclans/blog/news/cost-and-time-reductions-december-2023/)
- LoR PoC Legend Level: 30 levels from first clears and quests. Perks are spread evenly with big ones at about L8, 16, 18, 22 and 28. [fetched] — [Riot Support](https://support.riotgames.com/en-us/legends-of-runeterra/gameplay/legend-level-the-path-of-champions)
- Clash Royale: Collection Level milestones every 10 levels (every 5 after CL 1500), reportedly up to CL 2,265. [fetched] — [Supercell](https://supercell.com/en/games/clashroyale/blog/news/new-collection-levels-and-mastery-changes/)

### Inferences
- Raid's design ("climb currency tiers": Bronze → Silver → Gold medals by level band) is a reusable pattern. Early levels are cheap and spread wide; late levels need a currency only available in higher brackets (arena tier). That is a natural soft cap.
- Per-unit timers (CoC, CRK) pace in real days; star-based trees (Kingdom Rush) pace by content cleared. For a stage-based game with 5×70 stages (PokiClash), star or clear gating is easy to read and needs no timers.
- Global price inflation is a lightweight soft cap that discourages maxing one node, the same effect Raid gets through steep per-level cost ("don't max a stat before upgrading another").

### Gaps
- No source gave "days to complete" for Raid's Great Hall, Archero talents, Hades Mirror or RL2 castle. Medal or gold income rates would be needed.
- Survivor.io and Archero 2 cost curves not found.

---

## Q6. Double layer: collectible creatures + account tree (element-, class- or affinity-wide buffs)

### Takeaway
Collection RPGs layer **faction-wide account buffs** over per-unit growth:
- Summoners War: per-element sanctuaries giving +3%→+21% ATK, plus all-monster ATK, HP, SPD and CRIT DMG buildings.
- Raid: per-affinity × per-stat Great Hall, 24 slots at up to +20%.
- CRK: All-Cookie and per-class research nodes.
- AFK: level sharing via the Crystal.

These buffs push players to concentrate on one faction (team identity) while keeping the whole roster relevant. They are usually bought with a mode-specific currency (arena medals, glory points) and are often non-refundable.

### Cited Findings
- **Summoners War sanctuaries:**
  - Fire Sanctuary: a 5×5 Glory building costing 120 Glory Points that raises Fire monsters' ATK from +3% up to +21% at max. [snippet] — [Summoners War Fandom Buildings](https://summonerswar.fandom.com/wiki/Buildings)
  - Glory Shop buildings:
    - one ATK sanctuary per element: Fire, Water, Wind, Light, Dark;
    - Ancient Sword (+ATK all), Crystal Altar (+HP all), Guardstone (+DEF all);
    - Sky Tribe Totem (+SPD all), Fallen Ancient Guardian (+CRIT DMG all);
    - Crystal Rock and Arcane Booster Tower (Arcane Tower attack and speed).
    - [fetched] — [SummonersWarSkyArena.info buildings guide](https://summonerswarskyarena.info/buildings-guide/)
- **Summoners War v8.1.4 (Nov 2023):** glory building effects were revamped into **Summoner skills** upgraded with skill points earned from Summoner level 21 to 100, and existing building effects stayed the same. This came from a search summary of an official notice; the news-list URL now shows newer items. [snippet] — [summonerswar.com news](https://summonerswar.com/en/skyarena/news/list/4673)
- **Summoners War v9.4.0 (dated 2026-11-20):** adds "Summoner Mastery" with 10 categories (Summoner's Tower > Profile > Mastery). Details not retrieved. [fetched, list page] — [summonerswar.com news list](https://summonerswar.com/en/skyarena/news/list/4673)
- **Raid Great Hall:**
  - Unlocks at account level 6.
  - Each affinity gets 6 stat slots (HP, ATK, DEF, C.DMG, RES, ACC): 4 affinities × 6 stats = 24 slots, 10 levels each, maxing at +20% HP/ATK/DEF, +25% C.DMG and +80 RES/ACC.
  - Paid with Arena Medals; no revert.
  - [fetched] — [GamerEmpire](https://gamerempire.net/raid-shadow-legends-great-hall-guide/)
  - Its effect is "global Stat boosts to all Champions belonging to that Affinity". [snippet] — [Plarium forum Great Hall guide](https://forum.plarium.com/raid-shadow-legends/673_guides-and-tutorials/594610_basic-guide-great-hall)
- **Raid Area Bonuses:** a second Great Hall tab, unlocking at level 50 with Live Arena, bought with Live Arena Crests. These bonuses apply only in specific locations (dungeons or modes), i.e. a **mode-scoped** account buff. [snippet] — [HellHades: Area Bonuses](https://hellhades.com/how-to-use-area-bonuses-in-raid-shadow-legends/)
- **Cookie Run: Kingdom:** "All Cookies: HP/DEF/ATK/CRIT DMG" nodes plus class-wide nodes ("Charge Cookies: HP Bonus I"), gated by lab level. [fetched] — [cookierun.wiki](https://cookierun.wiki/w/Sugar_Gnome_Laboratory)
- **AFK Arena / AFK Journey:** roster-wide level sharing (5 core heroes set the level for all others) rather than % buffs. [fetched] — [afk.guide](https://afk.guide/resonating-crystal); [snippet] — [LootBar](https://lootbar.gg/blog/en/afk-journey-resonating-hall-guide-optimal-resonance-setup.html)
- **LoR PoC:** the account Legend Level "powers up your whole champion roster" through run perks. Per-champion stars and Star Powers hold unit identity. [fetched] — [Riot Support](https://support.riotgames.com/en-us/legends-of-runeterra/gameplay/legend-level-the-path-of-champions)

### Inferences
- For a 5-element creature game (PokiClash: Thủy/Hỏa/Kim/Mộc/Thổ, 78 heroes, 5 parallel islands), the observed patterns map to these options:
  - **(a) Per-element "sanctuary" nodes** (Summoners War: +3→+21% ATK per element).
  - **(b) Element × stat grid** (Raid: 5 elements × N stats).
  - **(c) Class or role nodes** (CRK class buffs).
  - **(d) Level sharing** (AFK Crystal).
  - **(e) Mode-scoped bonuses** (Raid Area Bonuses), e.g. a buff valid only on its own island.
- Funding: Raid and Summoners War pay for faction buffs with a *side-mode* currency (arena medals, glory points). An island-specific currency (one drop per island) would tie each element branch to its island and naturally pace the 5 parallel islands.
- Risk: element-wide % buffs with no refund (Raid) lock players into their first element and make later-element heroes feel weak. Summoners War moving these effects into Summoner skills from levels 21–100 suggests a shift toward one account-level skill-point pool. The v9.4.0 "Summoner Mastery" (Nov 2026) may extend this; details unknown.

### Gaps
- Summoners War: exact Glory Point cost per level, the full max-level table, and the v8.1.4 and v9.4.0 skill-point details were not retrieved. The fandom page was blocked (402) and the official news list page has rotated.
- Whether Raid Great Hall bonuses apply in all PvE: Plarium describes them as global for the affinity, but no fetched source states PvE/PvP scope explicitly.
- Pokémon-like games with account-wide type buffs (e.g. Pokémon Masters EX, Pokémon Unite) were not researched.
