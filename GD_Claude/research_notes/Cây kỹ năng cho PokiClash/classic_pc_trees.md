# Classic PC/console skill trees and talent systems: design history and lessons

Scope: structure (shape, node count, node types), point economy, choice model, respec, build-diversity outcomes, readability, and what developers have said publicly. Researched 2026-11-24. Some wikis (poewiki, Bulbapedia, UESP, megatenwiki, Fandom) blocked automated fetches. Where a fact comes only from a search-result summary or a secondary site, the bullet says so.

---

## 1. World of Warcraft talents: vanilla trees → Cataclysm → Mists "1 of 3" rows → Dragonflight class/spec trees (and after)

### Takeaway
Each WoW revamp went after the same problem. Large free-allocation trees filled with small passive "+x%" ranks produced filler points, "no-brainer" talents and one solved build per spec. Cataclysm shrank the trees. Mists replaced them with 1-of-3 rows to remove filler and make every pick a sidegrade. Dragonflight brought trees back because the rows felt thin (7 picks in total) and gave little sense of growth while levelling. It kept the lessons: separate utility points from main-role power, add choice nodes and gates, and allow free respec in rested areas.

### Cited Findings
**Vanilla to Wrath (free-allocation 3-tree model)**
- Each class had three talent trees and could put points into any of them. Most talents had up to 5 ranks, so a typical talent took 5 points for its full effect. Deeper tiers unlocked as points were spent in that tree. — [warcraft.wiki.gg: Talent](https://warcraft.wiki.gg/wiki/Talent)
- Respec required a class trainer and a gold fee that rose with each reset. Dual Talent Specialization came in patch 3.1.0 at 1000 gold and was later cut to 100 gold, with the level requirement lowered from 40 to 30. — [warcraft.wiki.gg: Talent](https://warcraft.wiki.gg/wiki/Talent)
- The wiki notes that before Cataclysm, the old design would have reached 76 talent points at the level cap, with more than 230 places to spend them. — [warcraft.wiki.gg: Talent](https://warcraft.wiki.gg/wiki/Talent)

**Cataclysm (2010): 31-point trees**
- Trees went from 11 rows to 7, and total points fell from 71 to 41 (one point every two levels, levels 10–85). Players had to spend 31 points in their primary tree before the other trees opened, and only the second tier of a secondary tree was reachable. Blizzard's stated goal was "three separate and distinct specs for each class." — [warcraft.wiki.gg: Talent](https://warcraft.wiki.gg/wiki/Talent); [Engadget: Cataclysm class and mastery systems explained](https://www.engadget.com/2010-07-07-cataclysm-class-and-mastery-systems-explained.html)
- Blizzard's Cataclysm Class & Mastery update (reposted on MMO-Champion), paraphrased in search summaries: the goal was "to remove a lot of the passive (or lame) talents, but we don't think that's possible with the current tree size," so each tree was cut to 31 points. What would change was "all of the filler talents you had to pick up to get to the next fun talent, as well as most talents that required 5 of your hard-earned points." — [MMO-Champion: Cataclysm Class & Mastery Systems Update](https://www.mmo-champion.com/content/1853-Cataclysm-Class-Mastery-Systems-Update)
- Mastery bonuses became flat percentages instead of scaling with points spent in a tree. After 31 points in the primary tree, 10 points could go anywhere. — [MMO-Champion](https://www.mmo-champion.com/content/1853-Cataclysm-Class-Mastery-Systems-Update)
- Beta coverage framed the aim as removing "boring talents that no one ever takes" and must-have passives, for example not spending another point on another 1% increase to crit. (Search-summary paraphrase; the exact source page within the Engadget beta series is unconfirmed.) — [Engadget: Cataclysm Beta talent coverage](https://www.engadget.com/2010-07-19-cataclysm-beta-feral-druid-specialization-and-talents.html)

**Mists of Pandaria (2012): pick 1 of 3 every 15 levels**
- Trees were replaced by 6 tiers of 3 talents, one pick per tier, unlocking at levels 15/30/45/60/75/90. The Tome of the Clear Mind let players change talents in the field, including mid-instance. — [warcraft.wiki.gg: Talent](https://warcraft.wiki.gg/wiki/Talent)
- At BlizzCon 2011, lead systems designer Greg "Ghostcrawler" Street said Blizzard wanted to "move away from cookie-cutter trees" and build "a system where there is no wrong choice." — [Engadget: Ghostcrawler on the philosophy behind the MoP talent trees](https://www.engadget.com/2011-12-08-ghostcrawler-on-seeing-the-forest-for-the-talent-trees.html) (article body did not load, so this is quoted from the search snippet)
- Tom Chilton (class panel, as reported): "I feel like we've been plagued over the years with cookie cutter builds." — [PC Gamer: MoP will fix talents "once and for all"](https://pcgamer.com/mists-of-pandaria-will-fix-talents-once-and-for-all-say-blizzard) (attribution comes from a search summary)
- Blizzard called the old model "unfixable" (headline; the body could not be fetched). — [PC Gamer](https://pcgamer.com/blizzard-tackle-world-of-warcraft-talent-revamp-criticisms-say-old-model-is-unfixable)
- Street reportedly conceded that "We'll still have cookie-cutter builds with the new design," arguing that most deviations would be slightly less effective rather than wrong. — [Prima Games: Street defends WoW talents revamp](https://primagames.com/news/blizzards-street-defends-wow-talents-revamp-142813) (search-summary paraphrase)
- Engadget (2012) said Blizzard was trying to do away with "no-brainer" talents. A few could survive "as long as there are only a few of these talents and the other choices are still reasonably competitive." — [Engadget: No-brainer talent and cookie-cutter builds](https://www.engadget.com/2012-07-10-the-no-brainer-talent-and-cookie-cutter-builds.html)
- PC Gamer (opinion) quoted Ghostcrawler promising "more choices that *matter*." — [PC Gamer opinion](https://www.pcgamer.com/opinion-why-world-of-warcrafts-new-talent-system-doesnt-go-far-enough/)
- A 2013 Engadget retrospective judged that MoP had removed cookie-cutter builds only "in part" and that the developers had "a really long way to go." — [Engadget: Mists' talent system revamp: hit or miss?](https://www.engadget.com/2013-04-25-mists-talent-system-revamp-hit-or-miss.html)
- The "illusion of choice" framing of the old trees came from critics, not developers. A gamedev.net poster argued that even if 80% of the 41 choices were forced by min/max realities, they offered an illusion of choice. — [gamedev.net: talent trees versus sets](https://gamedev.net/forums/topic/613797-talent-trees-versus-sets/4877626/); [Engadget: The myth of the talent tree choice](https://www.engadget.com/2011-10-31-mists-of-pandaria-the-myth-of-the-talent-tree-choice.html). I found no direct developer quote using "illusion of choice."

**Warlords to Shadowlands (rows period)**
- WoD added a 7th tier at level 100 (21 talents per spec). Legion removed Dual Spec, allowed free spec switching and saved talents per spec. From patch 7.0.3, talents could be changed freely in any rested area. Shadowlands' level squish put tiers at 15/25/30/35/40/45/50. — [warcraft.wiki.gg: Talent](https://warcraft.wiki.gg/wiki/Talent)

**Dragonflight (2022): class tree + spec tree**
- Stated goals: "increase player agency over your character's progression and build," "provide meaningful rewards while leveling," and "reinforce your character's connection to both their class and their spec." Trees should have "intuitive paths that lead you to reasonable builds." On the risk: "Exploring a world where many more things are optional has a lot of advantages but requires a lot of care." On feeling pruned: "Openly, our goal is that you don't." — [Blizzard: Dragonflight Talent Preview](https://worldofwarcraft.blizzard.com/news/23797209/)
- Structure: the class tree holds core shared abilities and utility, and the spec tree holds main-role power. They are kept separate so players can take utility without giving up role performance. Most abilities are now taken in the tree rather than granted on level-up. Prerequisite arrows point down or diagonally down. Row gates in the prototypes were row 5 at 8 points spent and row 8 at 20. Octagonal choice nodes allow one of two options at a time. Many talents have multiple ranks, and some basic class nodes are granted free to specific specs. — [Blizzard: Dragonflight Talent Preview](https://worldofwarcraft.blizzard.com/news/23797209/)
- Point economy: the first class point comes at 10 and the first spec point at 11, then they alternate. At 70 a character has 31 class + 30 spec = 61 points, "far more than the 7 talent points" of Shadowlands. — [Blizzard: Dragonflight Talent Preview](https://worldofwarcraft.blizzard.com/news/23797209/); [Wowhead guide](https://wowhead.com/cn/guide/classes/dragonflight-talent-trees)
- Ion Hazzikostas said watching "a new generation play with those talents" in Classic "really underscored" what the team had lost after Mists. — [warcraft.wiki.gg: Talent](https://warcraft.wiki.gg/wiki/Talent)
- Community reaction to the prototypes: some said the Death Knight class tree did not deliver the "utility in class tree, performance in spec tree" split. — [Blizzard forums thread](https://us.forums.blizzard.com/en/wow/t/1256029)
- After Dragonflight: The War Within added Hero Talents (themes that combine two specs) at levels 71–80, with one point per level. Midnight (12.0.1) adds 4-rank Apex talents from level 81, with points alternating among the spec, class and hero trees. — [warcraft.wiki.gg: Talent](https://warcraft.wiki.gg/wiki/Talent)

### Inferences
- The pattern is a pendulum. Big trees give a feeling of growth but produce filler and solved builds. Small rows remove filler but feel thin. Dragonflight's answer mixes the two: a tree for the sense of growth, plus separate point pools, choice nodes and gates to control solved builds and trade-offs.
- Free respec (Tome of the Clear Mind, then free in rested areas) makes per-encounter "correct builds" acceptable. Cookie-cutter builds hurt less when switching costs nothing.
- Keeping utility points apart from power points is a reusable pattern: players stop paying a "tax" in power to take a fun or utility option.

### Gaps
- No primary transcript of the BlizzCon 2011 class panel was retrieved. The Engadget and PC Gamer article bodies would not load, so some quotes come from search snippets.
- No primary source found for the frequently cited "5% crit" vanilla talent example (e.g. Cruelty, Deadliness). The 1% crit line is from beta coverage.

---

## 2. Diablo 2 skill trees vs Diablo 3 skills + runes vs Diablo 4 skill tree + Paragon board

### Takeaway
In Diablo 2, players stacked 20 points into one skill and kept to one trees and stacked synergies, which made builds one-dimensional. Respec arrived only in 1.13. Diablo 3 dropped points and trees entirely and put the choice in a limited set of equipped skills, plus runes and free swapping. Blizzard argued that points were "commitments before you even know what you're committing to." Diablo 4 brought a tree back with costly gold respec and added the Paragon board as horizontal endgame growth. It then reworked the tree twice: first moving passive power to Paragon, then (2026) making nodes change how a skill plays rather than add "more of the same."

### Cited Findings
**Diablo 2**
- One skill point per level, plus quest points: Den of Evil +1, Radament +1, Fallen Angel +2. — [GamerGuides D2R: skill points](https://www.gamerguides.com:443/diablo-ii-resurrected/guide/characters/builds/skill-points)
- Synergies existed from launch. v1.10 made their rules explicit: synergy bonuses come only from real skill points, not +skill gear, except summons. Effect: synergies "greatly improve the damage output of one skill … but this causes characters to become very one-dimensional, with all of their skill points devoted to a single skill or skill tree." — [Diablo Wiki: Synergy](https://diablo2.diablowiki.net/Synergy)
- Respec arrived in patch 1.13: one per difficulty from Akara after Den of Evil, plus the Token of Absolution crafted in the Horadric Cube. — [Diablo Wiki: Respec](https://diablo2.diablowiki.net/Respec)

**Diablo 3: no tree, skills + runes, free swapping**
- Jay Wilson (2009, DiabloFans) said the team had decided to remove the tree architecture and "move into a purely skill-based system." — [GameBanshee: Diablo III interview, skill trees being removed](https://gamebanshee.com/ku6hr); [Tom's Hardware](https://www.tomshardware.com/news/PC-RPG-Game-Diablo-Blizzard,9154.html)
- Bashiok (community manager): "Players invest 20 points into a single skill and use it as much as possible." Because rising damage from points made one skill beat the alternatives, "skill point spending has eroded away combat depth." Skills "need to have different roles." — [Blizzplanet/IGN: Blizzard on ditching skill points in Diablo III](https://blizzplanet.substack.com/p/ign-blizzard-on-ditching-skill-points-in-diablo-iii)
- Jay Wilson said skill points are "commitments before you even know what you're committing to." The team made the limit on equipped skills the interesting decision instead. — [Blizzplanet/IGN](https://blizzplanet.substack.com/p/ign-blizzard-on-ditching-skill-points-in-diablo-iii)
- Bashiok: "We feel that 6 skill choices actually creates more build diversity than 7." Counting rune combinations gives about 2.3 trillion builds per class. Other stated aims were aesthetic flavour, simplicity, and passives that feel impactful. — [Blizzplanet/IGN](https://blizzplanet.substack.com/p/ign-blizzard-on-ditching-skill-points-in-diablo-iii)
- Runes were first planned as items. The official beta blog said carrying and juggling them was "not only un-fun, it was a serious and tedious inventory problem," so they became built-in skill runes "earned simply by leveling up." — [Battle.net D3 blog (via search summary)](https://us.battle.net/d3/en/blog/4475014); [CinemaBlend](https://cinemablend.com/games/Diablo-3-Skill-Rune-Changes-Revealed-39665.html)
- Wilson on iteration: runes could not be designed until the skill itself was locked, and "we're notorious for redoing things." — [Kotaku: BlizzCon, where are Diablo III's runes](https://kotaku.com/blizzcon-where-are-diablo-iiis-runes-5344012)

**Diablo 4 at launch (2023): tree + gold respec**
- One skill point per level from 2 to 49, plus 10 from Renown, for 58 points at max. The tree has 7 clusters that unlock by total points spent, wherever they were spent. — [Maxroll: D4 skill tree overview](https://maxroll.gg/d4/getting-started/skill-trees); [Prima](https://primagames.com/tips/everything-we-know-about-diablo-4s-skill-tree)
- Respec is free up to level 15, then costs gold that scales up. Wowhead calculated that a full 58-point refund at level 100 costs 4,358,642 gold (about 75,149 per point). Blizzard said the respec costs "are final" before launch. — [Wowhead: respec costs at level 100](https://www.wowhead.com/diablo-4/pt/news/calculating-respec-costs-for-level-100-characters-333589); [PC Gamer](https://pcgamer.com/diablo-4s-respec-cost-isnt-changing-before-launch)

**Diablo 4 Paragon board**
- Introduced in the Dec 2021 Quarterly Update with "a heavy emphasis on build customization." Character power should come from player choice rather than mostly from gear, because gear-driven power made customization "feel less rewarding." It unlocks at level 50. — [Blizzard: Diablo IV Quarterly Update, Dec 2021](https://news.blizzard.com/en-us/article/23746639/diablo-iv-quarterly-updatedecember-2021)
- Board structure: Normal tiles (small stats, connective), Magic tiles (clusters), Rare tiles (large boosts, some needing an attribute threshold), and one Legendary tile at the centre of each board after the first. Glyph sockets grant bonuses based on active tiles within a radius that grows as the glyph levels. Gate tiles attach new boards, which can be rotated before placing. — [Blizzard Dec 2021 update](https://news.blizzard.com/en-us/article/23746639/diablo-iv-quarterly-updatedecember-2021)
- Patch 1.0.2d cut glyph scaling by about 34%, because players were stacking Magic and Rare nodes and overlooking the "less impressive Legendary nodes." — [Wowhead: Paragon board nerfs 1.0.2d](https://www.wowhead.com/diablo-4/es/news/paragon-board-nerfs-diablo-4-patch-1-0-2d-build-42131-333306) (search summary)
- Season 6 / 2.0 reworked glyphs and capped equipped boards at 5 including the starter board. — [Dexerto](https://dexerto.com/diablo/all-changes-to-diablo-4s-paragon-system-in-update-2-0-2882030)

**Diablo 4 skill tree reworks**
- Reported: passives were cut from the skill tree and their numerical power moved to Paragon, which the team called the "proper place" for passive growth. Associate game director Joe Piepiora wanted the deep system to be accessible to newcomers, with "pretty targeted" options rather than open-ended ones. A dev Q&A reportedly set a target of endgame characters taking about 30–40% of nodes so builds stay distinct. — [PC Gamer: Blizzard overhauls D4 skill system for more distinct builds](https://pcgamer.com/blizzard-overhauls-diablo-4-skill-system-to-enable-more-distinct-character-builds); [Icy Veins: D4 dev Q&A](https://www.icy-veins.com/d4/news/diablo-4-dev-qa-reveals-major-skill-tree-and-item-changes/); [NME: rework avoids a "scary screen"](https://www.nme.com/news/diablo-4-skill-tree-rework-will-help-new-players-avoid-a-scary-screen-3362395) (from search summaries; exact dates and figures unverified)
- April 2026 (Lord of Hatred, launching April 28): the old tree "often had a tendency to feel like more of the same sap on the same branch." Skills had short, predictable paths with a couple of endpoints and one clear best choice, and upgrades made a skill stronger without changing how it played. The new tree is fully branching, a "canopy of choices," and upgrades change behaviour. Example: Barbarian Rend can become Fire damage, send waves, or reach beyond melee range. Goals: upgrades noticeable at once, "not buried in fine print," and newcomers able to click a node and test it. Chelsea Leah (Blizzard): "Same trunk, completely different branches." — [Xbox Wire: Before-and-after look at Diablo IV's skill trees](https://news.xbox.com/en-us/2026/04/22/diablo-4-skill-tree-overhaul/)

### Inferences
- Diablo's line runs D2 (deep but one-dimensional, locked) → D3 (flexible but shallow-feeling) → D4 (tree with costly respec) → D4 reworks (nodes must change play, raw stats go to a separate grind). Over 20 years Blizzard concluded that numeric passives belong in a separate endgame sink (Paragon), while the skill tree should hold choices that change behaviour.
- The 1.0.2d glyph nerf shows a recurring failure: if generic stat nodes plus multipliers beat the legendary or keystone nodes, players skip the "exciting" nodes.

### Gaps
- No primary Blizzard post retrieved for the 2.0-era "passives moved to Paragon" change, so its timing and figures (30–40% of nodes) rely on secondary summaries.
- No Blizzard statement found on why D3's Paragon was replaced by D4's board.
- Diablo 3's "Elective Mode" and the rune count per skill (5 per skill) are well known but no source was retrieved for them.

---

## 3. ARPG trees: Path of Exile 1 and 2, Grim Dawn devotion, Last Epoch, Torchlight

### Takeaway
PoE showed that a huge shared tree (~1,300 nodes, one tree for all classes, different start points) can be the game's identity. It works because a few keystones radically change mechanics while most nodes are small travel stats, at the cost of heavy cognitive load and reliance on community planners. Grim Dawn and Last Epoch split progression into layers: class trees, a secondary star map (devotion), and per-skill specialization trees. Last Epoch's per-skill trees let one skill transform without bloating the class tree.

### Cited Findings
**Path of Exile 1**
- The official site describes "a vast web of 1325 skills that provide passive bonuses" (original game figure). A Kotaku-published interview gives about 1,315 nodes and notes players "are not allowed to respec their choices very easily." — [pathofexile.com passive tree](https://pathofexile.com/passive-skill-tree); [search summary of Wilson interviews](https://pcgamer.com/the-making-of-path-of-exile)
- Five node types: Small passives, Notables, Keystones, Masteries, Jewel Sockets. Small passives lead to notables and usually give smaller versions of the notable's bonus. Keystones make major mechanic changes that "can reshape your entire playstyle." Points come from levelling and certain quests. — [Maxroll: PoE passive tree for beginners](https://maxroll.gg/poe/getting-started/passive-skill-tree-for-beginners); [Sportskeeda: build-defining nodes](https://www.sportskeeda.com/mmo/all-build-defining-nodes-path-exile-skill-tree)
- Chris Wilson (2012): many keystones "dramatically change how you play your character," which is why the team hesitated to call it a simple passive tree. — [Marooners' Rock interview pt 1](https://maroonersrock.com/2012/02/interview-chris-wilson-path-of-exile-part-1-of-3)
- Wilson (2013, The Awakening): the tree had become part of the game's identity, and the team wanted to make it "even crazier." Because the tree is static, they wanted it more dynamic, which led to jewels. — [RPGamer interview archive](https://archive.rpgamer.com/games/poexile/poexile/poexileint.html)
- Wilson: Ascendancy classes are "a core part of a character build's identity, so it's very important that there is a lot of variety." — [Prima Games: Chris Wilson interview](https://primagames.com/?p=311516)
- Wilson (2025): when designing the PoE2 tree the team asks "what crazy things" they can do, and may find serious problems with the PoE1 tree "that they had been blind to." — [GamesBeat interview](https://gamesbeat.com/path-of-exile-interview-an-expedition-into-some-big-changes/) (search summary)

**Path of Exile 2**
- Everyone uses the same tree regardless of class; only the start nodes differ, with two classes per attribute. Attribute travel nodes let the player choose Str, Dex or Int on each node. Weapon Set ("dual specialization") points are active only with a specific weapon set; their maximum is earned in the campaign, and quest books grant extra points. — [Maxroll: PoE2 passive tree and dual specialization](https://maxroll.gg/poe2/resources/poe-2-passive-tree-and-dual-specialization)
- Respec costs gold, priced dynamically by character level and node depth. It is done at the Hooded One (Act 1) or Doryani, attribute nodes refund at 50% off, and refunds are "much easier" early than in PoE1. — [Maxroll PoE2](https://maxroll.gg/poe2/resources/poe-2-passive-tree-and-dual-specialization)
- GGG later cut respec gold costs after complaints (headline: "Path of Exile 2 passive skill respecs will no longer cost Scrooge McDuck levels of gold"). — [PC Gamer](https://pcgamer.com/games/rpg/path-of-exile-2-passive-skill-respecs-will-no-longer-cost-scrooge-mcduck-levels-of-gold)
- Jonathan Rogers on tree balance: "We'd prefer not to add Life if we don't need to." — [Sportskeeda interview](https://widgets.sportskeeda.com/mmo/we-d-prefer-add-life-need-to-jonathan-rogers-talks-path-exile-2-passive-tree-balance-vaal-gems-transformations)

**Grim Dawn: Devotion constellations**
- Devotion is a star map earned from shrines: up to 50 points across three difficulties, raised to 55 by Ashes of Malmouth. There are more shrines than points. — [grimdawn.com: Devotion guide](https://www.grimdawn.com/guide/character/devotion); [Steam discussion](https://steamcommunity.com/app/219990/discussions/0/1732090362048271754)
- The 2015 design had 79 constellations of 3–8 stars each, 425 stars in all. Most require "Affinity" (colour points) from completed constellations; 16 are open from the start. Some stars grant Celestial Powers that are bound to a skill with matching triggers (on-hit powers go on attacks, on-damaged powers on buffs), one per skill. Powers level to 20/15/10 by tier, plus 5 with Ashes of Malmouth. — [Crate: Grim Misadventure #83](https://forums.crateentertainment.com/t/grim-misadventure-83-your-devoted-questions-answered/29165); [grimdawn.com guide](https://www.grimdawn.com/guide/character/devotion)
- A later community wiki lists about 109 constellations. — [bloxodes community wiki](https://bloxodes.com/wiki/grim-dawn/devotion-constellations) (community source)

**Last Epoch: class passives + per-skill specialization trees**
- Each class has a Base tree plus 3 Mastery trees. Points come one per level from level 3, plus up to 15 from quests, for 113 total. The first half of every Mastery tree is open; the second half only for the chosen Mastery. A progress bar shows the points needed per tree to unlock deeper nodes. — [Maxroll: Last Epoch passives and skills](https://maxroll.gg/last-epoch/resources/passives-and-skills)
- More than 100 skills, each with its own specialization tree. There are 5 specialization slots, unlocking at character levels 4/8/20/35/50. A specialized skill gains XP and levels separately up to 20 (around character level 75); gear can raise the cap. New specializations start at a "Minimum Skill Level," up to 10, with catch-up XP. — [Maxroll LE](https://maxroll.gg/last-epoch/resources/passives-and-skills)
- Skill respec is per point via a Respec button (each point removed lowers the skill's level by one), or a full despecialize. Passive respec is done at a Chronomancer for gold. Points that would invalidate higher nodes cannot be removed, nor more than 20 from the Base tree once Mastery is invested. The Mastery class itself cannot be changed. — [Ginx](https://www.ginx.tv/en/?p=60995); [ProGameGuides](https://progameguides.com/last-epoch/how-to-respec-passives-and-skill-tree-points-in-last-epoch/); [Prima](https://primagames.com/gaming/how-to-respec-in-last-epoch-passives-skills-and-specializations)
- Sources conflict on the maximum specialized skill level: Ginx says 10, Maxroll says 20 by default. Maxroll's "minimum level caps at 10" probably explains the confusion. — [Ginx](https://www.ginx.tv/en/?p=60995) vs [Maxroll](https://maxroll.gg/last-epoch/resources/passives-and-skills)

**Torchlight**
- No sources retrieved (see Gaps).

### Inferences
- PoE's model works because most nodes are cheap travel stats and the meaning sits in a few keystones and notables. The tree is a pathing puzzle, and its readability depends on third-party planners and build guides, which is a heavy load for casual players.
- Last Epoch's per-skill trees fit games whose identity is built around a few signature abilities. In a hero-collecting game, each hero's signature skill could have a small specialization tree instead of one large class tree.
- Grim Dawn's binding of celestial powers to skills is an early version of "the passive modifies a specific active," the same idea as Hades' Duo boons and D4 2026's behaviour-changing nodes.

### Gaps
- poewiki.net and the PoE Fandom wiki blocked fetches, so I have no current keystone count, cluster jewel details, or exact PoE2 node and point totals.
- No Eleventh Hour Games developer quotes retrieved on why skill specialization was designed this way.
- Torchlight 1/2/3/Infinite: no sources retrieved. (Torchlight 2 is commonly described as three 5-point-per-rank trees with a costly respec potion limited to the last 3 points, but this is unverified here.)

---

## 4. Console/single-player RPG progression: FFX Sphere Grid, FFXII License Board, Skyrim, Fallout, Borderlands, Mass Effect, Dragon Age

### Takeaway
JRPG boards (Sphere Grid, License Board) are tree shapes that each later got a "guided" or "class-restricted" variant. The fully open version made party members interchangeable, so Square Enix added job boards (FFXII International) and kept a Standard grid with fixed character paths beside the Expert grid. Bethesda's constellations made perks readable and themed, tied to skills raised by use, and classless. Borderlands' three-tree layout with mid-tier "Gamechanger" and top-tier "Capstone" nodes is the standard shooter-looter template.

### Cited Findings
**Final Fantasy X Sphere Grid**
- The Standard grid gives each character a set path. The Expert grid (originally only in international versions, selectable at the start of the HD Remaster and locked for the playthrough) puts all characters in the middle so they can follow any path. The Standard grid has about 50 more nodes. Guides say the Expert grid needs more planning and is not recommended for beginners. — [GameSkinny: Standard vs Expert Sphere Grid](https://www.gameskinny.com/5aji7/final-fantasy-x-standard-sphere-grid-vs-expert-sphere-grid); [Game8](https://game8.co/games/Final_Fantasy_X/archives/270800)

**Final Fantasy XII License Board**
- In the original, every character used the same License Board. The International Zodiac Job System gave a separate board per job, and The Zodiac Age lets each character take two jobs, each with its own board. One outlet compared this to FFX International's grid redesign "to make it easier to customize characters" (the outlet's interpretation). — [Wikipedia: Final Fantasy XII](https://Wikipedia.com/wiki/Final_Fantasy_XII); [RPG Site: Zodiac Age changes](https://rpgsite.net/feature/5751-final-fantasy-xii-the-zodiac-age-changes-and-additions-what-s-new-in-this-ivalice-remaster); [Siliconera](https://www.siliconera.com/?p=4348)

**Skyrim**
- Classless system: Todd Howard (Game Informer podcast) said it gives "a more natural way" to experience the game. — [PlayStation LifeStyle: Bethesda explains Skyrim's lack of classes](https://www.playstationlifestyle.net/?p=133817)
- Perks are drawn as star constellations, one per skill. Former lead designer Bruce Nesmith reportedly preferred a plain list but later admitted "I was clearly wrong" after players embraced Howard's constellation idea. — [OtakuKart (aggregator)](https://otakukart.com/i-was-clearly-wrong-former-skyrim-lead-bruce-nesmith-admits-todd-howard-was-right-about-constellation-skill-trees/) (secondary source)
- Bethesda's later games keep classless builds "so gamers don't waste time" (headline). — [TweakTown](https://www.tweaktown.com/news/89748/all-new-bethesda-rpgs-to-offer-classless-builds-so-gamers-dont-waste-time/index.html)
- One source gives 280 perks across Warrior/Thief/Mage constellations; the commonly cited 251 could not be verified (UESP blocked). — [Gameranx Skyrim perks guide](https://gameranx.com/features/id/3496/article/skyrim-perks-guide/) (unverified)

**Fallout 4**
- The perk chart was presented in a style "similar to the constellation skill trees from Skyrim," as posters with animated Vault Boys acting out each perk. Howard said most perks have multiple ranks. Coverage framed this as what Bethesda "learned from Skyrim's mistakes." — [Twinfinite: Fallout 4 director talks new perk system](https://twinfinite.net/pc/fallout-4-director-talks-new-perk-system-what-bethesda-learned-from-skryims-mistakes/) (body 403; from search summary)

**Borderlands**
- Borderlands 2: an action skill unlocks at level 5, then three trees. Most skills enhance attributes, while mid-tier "Gamechanger" and top-tier "Capstone" skills "offer additional flexibility in how you approach play." — [Prima eGuide BL2](https://primagames.com/eguides/borderlands-2-game-of-the-year-eguide/hyperions-most-wanted/salvador)
- Gearbox designer Paul Hellquist on Krieg's early tree design: "what we didn't like about that design was that it created a situation where the first 5 points in the tree were very boring." Designers also used the action skill to give each tree a role, e.g. Bloodlust had no way to get health, so the action skill filled that role. — [Gearbox Software dev post](https://www.gearboxsoftware.com/?p=10303) (via search summary)
- Borderlands 4: each Vault Hunter has three trees, each tied to one of three Action Skills. — [SteelSeries BL4 classes guide](https://steelseries.com/ko-kr/blog/borderlands-4-character-classes-guide)
- A low-quality planner site says each BL2 capstone needs 26 points spent in its tree. — [west-games planner](https://west-games.com/?p=29808) (unverified)

**Mass Effect / Dragon Age**
- No sources retrieved (see Gaps).

### Inferences
- Shared open boards (FFX Expert, original FFXII) tend to make party members converge on the same build. Every later fix restored a per-character or per-job identity. For a creature collector, each creature or line needs its own small board or tree to keep its identity.
- Constellation art is a readability device: a theme plus a small node count per skill is easy to scan, unlike PoE's single huge web.
- Hellquist's "first 5 points were very boring" is the same complaint as WoW's filler tiers. Early nodes need a visible effect.

### Gaps
- No sources retrieved on Mass Effect (e.g. ME3's rank 4–6 "evolution" choices) or Dragon Age (Origins specializations, Inquisition trees).
- No FFX node count or developer statements on why the Expert grid was added.
- Skyrim perk count conflicts (251 vs 280), and the Legendary skill reset (patch 1.9) is unverified here.

---

## 5. Creature-collecting progression: Persona/SMT inheritance, Monster Hunter Stories, Pokémon EV/IV, Digimon digivolution

### Takeaway
Monster collectors seldom use visible trees. They put progression in breeding or fusion inheritance (passing skills to a new creature), grids of genes (Monster Hunter Stories' 3×3 bingo), hidden per-stat budgets (Pokémon EVs and IVs), and branching evolution graphs with conditions (Digimon). These systems tie power to collecting more creatures. They are deep, but hidden mechanics such as EVs, IVs and inheritance rules are notoriously opaque without guides.

### Cited Findings
**Persona / Shin Megami Tensei**
- In Persona 5 and Persona 5 Royal, inherited skills can be chosen by hand, but each Persona's "inheritance type" blocks some skill categories. — [Megami Tensei Wiki: Skill Inheritance](https://megatenwiki.com/wiki/Skill_Inheritance) (search snippet; page 403 on fetch); [Steamah P5R fusion guide](https://steamah.com/persona-5-royal-fusion-guide/)
- The number of inheritable skills is not fixed and depends on the source Personas' skill counts and levels (a third-party calculator, which labels its own figures estimates). — [everycalculators P5R](https://everycalculators.com/fusion-calculator-persona-5-royal.html) (low confidence)
- In Persona 4, the inherited count was based on the number of unique skills across all ingredient Personas. — [LP Archive: Persona 4 lesson 2](https://lparchive.org/Persona-4/Lesson2)

**Monster Hunter Stories 2/3: gene grid + Rite of Channeling**
- Each Monstie has a 3×3 grid of genes. Lining up three genes of the same element or attack type horizontally, vertically or diagonally makes a "Bingo" that boosts those attacks; for example, three Thunder/Technique genes in a row raise Thunder and Technique damage. — [PC Gamer: MHS2 gene guide](https://pcgamer.com/monster-hunter-stories-2-gene-rainbow-rite-of-channeling); [GamerGuides MHS3: gene grid and bingos](https://www.gamerguides.com/monster-hunter-stories-3-twisted-reflection/guide/getting-started/gameplay/gene-grid-and-gene-bingos-explained)
- The Rite of Channeling moves genes from one Monstie to another, and in MHS2 the donor "will disappear forever." A rainbow "Free Bingo Gene" counts toward any bingo but gives no skill of its own and can be inserted only once. — [PC Gamer MHS2](https://pcgamer.com/monster-hunter-stories-2-gene-rainbow-rite-of-channeling); [Windows Central](https://www.windowscentral.com/monster-hunter-stories-2-rite-channeling-guide)
- One MHS3 guide says a Power-gene bingo gives +5% damage to all Power attacks. — [G2A MHS3 gene guide](https://www.g2a.com/news/features/monster-hunter-stories-3-gene-guide-to-creating-perfect-monsties/) (secondary)

**Pokémon: EVs and IVs as hidden progression**
- EVs: 510 total per Pokémon and 252 per stat in effect, because 4 EVs equal 1 stat point at level 100 (so a maxed stat gives +63). EVs come mainly from defeating Pokémon, with yields set by the defeated species. Older games and guides cite 255 per stat (Gen III–V). — [OctaAlma: IVs and EVs explained](https://octaalma.github.io/articles/evs_ivs/evs_and_ivs.html); [Pokémon DB: EVs](https://pokemondb.net/ev); [Kotaku: Scarlet/Violet EV/IV](https://kotaku.com/pokemon-scarlet-violet-what-are-ev-iv-training-1849905869)
- IVs are hidden values from 0 to 31 per stat, fixed when a Pokémon is caught or hatched; a 31-IV stat is 31 points higher at level 100 than a 0-IV stat. — [Dot Esports](https://dotesports.com/guides/news/what-are-ivs-and-evs-in-pokemon)
- Smogon documents how the EV/IV system changed by generation (Gen I–II "stat experience" vs Gen III+ EVs). — [Smogon: EVs and IVs Through the Ages](https://www.smogon.com/smog/issue28/evs_ivs)

**Digimon Story: Cyber Sleuth**
- Each form has several digivolution routes (a guide says at least three). Digivolving needs level, stat and sometimes held-item requirements. A Digimon can de-digivolve at any time to a known prior form. — [Player.One digivolution guide](https://www.player.one/stub-52717); [Steam discussion](https://steamcommunity.com/app/1042550/discussions/0/1608274347729613279)
- Cycling digivolve and de-digivolve is the main source of ABI, which raises stat caps; one user gives a formula (Rookie 2 + level/5, Champion 3 + level/5). Normal stats reportedly do not carry over between forms. — [GameRevolution ABI guide](https://www.gamerevolution.com/guides/368559-digimon-story-cyber-sleuth-hackers-memory-abi-guide-raise-digimons-abi); [Steam forum](https://steamcommunity.com/app/1042550/discussions/0/3104637814601971398) (community sources)

### Inferences
- In collectors, the "skill tree" is usually spread across the roster: power comes from combining creatures (inheritance, channeling, de-digivolve loops) rather than spending points on one creature. That ties the progression system to the collection loop.
- MHS' 3×3 bingo is a very readable mini-board: it holds 9 nodes and makes synergy visible as lines. It is a strong pattern for a small per-creature "tree" on a phone screen.
- Pokémon's EVs and IVs show the cost of hidden progression: deep for experts, invisible to most players, and creating a "solved" competitive spread (e.g. 252/252/4).

### Gaps
- Bulbapedia blocked fetches. No primary sources on Pokémon move tutors or move reminders, or on developer statements about why EVs and IVs stay hidden.
- No exact Persona 5 inheritance slot rules or SMT V Essence details from a primary or wiki source.
- No sources on Monster Hunter Stories developer intent, or on Digimon's official digivolution charts.

---

## 6. Slot/loadout systems instead of trees: Hollow Knight charms, Hades boons (Ori: not covered)

### Takeaway
Slot systems swap a permanent tree for a budget of equip capacity (notches) or a run-scoped random draft (boons). The choice comes back every time the player re-equips or starts a new run, so respec is built in and "solved builds" matter less. The trade-offs are found-item gating (Hollow Knight) and readability of the synergy rules (Hades' Duo requirements).

### Cited Findings
**Hollow Knight**
- "Each charm costs a certain amount of notches, depending on how powerful they are. This limits how many you can equip at once, so you'll have to make some tactical decisions." Players find ways to expand notches. Team Cherry framed individual charms as trade-offs, e.g. Wayward Compass "Useful for finding your way, but is the cost worth it?" and Fury of the Fallen "Risky, but powerful in the hands of an expert!" — [Team Cherry blog: Revealing the power of the charms](https://www.teamcherry.com.au/blog/revealing-the-power-of-the-charms)
- The Knight starts with 3 notches and can reach 11 (8 more found). Overcharming lets players equip past the notch limit, but all damage taken is doubled. — [Hollow Knight Wiki: Notch](https://hollowknight.wiki/w/Notch); [Hollow Knight Wiki: Overcharmed](https://hollowknight.wiki/w/Overcharmed). One outlet says 7 more notches, conflicting with the wiki. — [Sportskeeda](https://www.sportskeeda.com/esports/how-many-charm-notches-hollow-knight)

**Hades / Hades II**
- Duo boons appear only when the player already holds compatible boons from both gods (Hermes and Chaos are excluded). — [Screen Rant: Hades Duo boons guide](https://screenrant.com/hades-duo-boons-guide/); [Prima: Legendary, Heroic, Duo boons](https://primagames.com/gaming/hades-guide-legendary-heroic-duo-boons)
- Greg Kasavin, citing Slay the Spire's deck-building variety, said that when players push toward a build "the randomness is going to fight against you," and called that tension a fascinating part of roguelike decisions. — [GameSpot: Hades changes what it means to be a roguelike](https://gamespot.com/articles/hades-changes-what-it-means-to-be-a-roguelike/1100-6483420/)
- Hades II: popular early-access boons were reworked rather than cut. On Smithy Sprint, Kasavin said "we wanted something simpler and easier to use for one of the main Boons from the god of the forge," and "we think it's important not to be too precious about these things." — [GamesRadar](https://www.gamesradar.com/games/hades/hades-2-lead-says-the-best-boons-from-early-access-werent-killed-just-reskinned-we-think-its-important-not-to-be-too-precious-about-these-things); [PC Gamer](https://www.pcgamer.com/games/roguelike/hades-2-lead-says-they-didnt-nerf-the-games-most-popular-boons-but-rather-found-new-homes-for-them-during-early-access-development)
- Players criticise the Duo prerequisites as "very non-intuitive; it's hard to tell which boons each duo requires." — [Steam discussion](https://steamcommunity.com/app/1145350/discussions/2/4353373056338025006)

### Inferences
- A notch budget turns "which perks?" into a repeated packing decision, and expanding the budget gives vertical progression on top of horizontal choice.
- Hades gives "solved build" protection through randomness. That suits run-based modes but not a persistent hero.

### Gaps
- No Team Cherry statement found on why charms replaced levels or trees, or on overcharm intent.
- Ori and the Blind Forest/Will of the Wisps (ability tree → shards with slots): no sources retrieved.
- No Kasavin primary source specifically on Duo boon design intent.

---

## 7. Design lessons summarised: meaningful vs trivial choices, power creep, trap options, solved builds, respec cost, capstones/keystones, vertical vs horizontal, tree size vs cognitive load

### Takeaway
Across 25 years developers keep restating a few lessons. Small "+x%" nodes are filler that creates solved builds. Choices should change play, be clear, and be limited and scarce. Separate utility from power, and numeric grind from behaviour-changing choices. Gates and choice nodes control complexity. Respec cost should match how much the game needs build commitment versus experimentation. Big keystone or capstone moments give trees their identity, but only if generic stat nodes do not outscale them.

### Cited Findings
**Trivial "+x%" nodes and filler**
- Blizzard (Cataclysm): wanted to remove "passive (or lame) talents" and "filler talents you had to pick up to get to the next fun talent." — [MMO-Champion: Blizzard Cataclysm update](https://www.mmo-champion.com/content/1853-Cataclysm-Class-Mastery-Systems-Update)
- Gearbox (BL2 Krieg): "the first 5 points in the tree were very boring." — [Gearbox dev post](https://www.gearboxsoftware.com/?p=10303)
- Blizzard (D4 2026): old upgrades "made a skill slightly stronger but did not change how it played"; new upgrades must be noticeable, "not buried in fine print." — [Xbox Wire](https://news.xbox.com/en-us/2026/04/22/diablo-4-skill-tree-overhaul/)
- Bugnet guide: "most skill trees are secretly boring: a list of upgrades you'll inevitably unlock in a predictable order, dressed up as choices." Choices must be "meaningful in play, not just numerically different," and points should be scarce relative to options. — [Bugnet: How to design a skill tree that's fun to plan](https://bugnet.io/blog/how-to-design-a-skill-tree-thats-fun-to-plan)

**What makes a choice interesting**
- Lars Doucet (Game Developer, 2011): interesting choices are different, balanced, clear and limited. "Clarity is perhaps the biggest design challenge for skill trees," because skills are abstract verbs or adjectives. Effects should be explicit (e.g. "Increases critical hit chance by +15%"). Gating "reduc[es] choice paralysis early on." Points are permanent ("once you assign a point it's spent forever"). Test with fresh players ("Kleenex testing"). — [Game Developer: Upgrades, Equipment, and Skill Trees](https://gamedeveloper.com/design/upgrades-equipment-and-skill-trees)
- Arc Raiders' reworked tree (2025/26 headline): "You can't have everything … we believe that creates more interesting choices and supports more playstyles." — [PC Gamer](https://www.pcgamer.com/games/third-person-shooter/you-cant-have-everything-in-arc-raiders-reworked-skill-tree-we-believe-that-creates-more-interesting-choices-and-supports-more-playstyles/)

**Solved builds, cookie-cutter, no-brainers**
- Street accepted that cookie-cutter builds would remain under MoP. The aim was that alternatives be slightly worse rather than wrong. — [Prima Games](https://primagames.com/news/blizzards-street-defends-wow-talents-revamp-142813)
- A few no-brainer talents are tolerable "as long as … the other choices are still reasonably competitive." — [Engadget](https://www.engadget.com/2012-07-10-the-no-brainer-talent-and-cookie-cutter-builds.html)
- D2 synergies pushed all points into one skill or tree ("one-dimensional"), and D3 cited "20 points into a single skill" as eroding combat depth. — [Diablo Wiki: Synergy](https://diablo2.diablowiki.net/Synergy); [Blizzplanet/IGN](https://blizzplanet.substack.com/p/ign-blizzard-on-ditching-skill-points-in-diablo-iii)
- D4 Paragon: generic Magic/Rare nodes plus glyph multipliers made players skip Legendary nodes, prompting a roughly 34% glyph nerf. — [Wowhead](https://www.wowhead.com/diablo-4/es/news/paragon-board-nerfs-diablo-4-patch-1-0-2d-build-42131-333306)

**Commitment and respec cost**
- D3: points are "commitments before you even know what you're committing to," so the game moved to free swapping. — [Blizzplanet/IGN](https://blizzplanet.substack.com/p/ign-blizzard-on-ditching-skill-points-in-diablo-iii)
- The range across games runs from no respec (D2 pre-1.13), to quest-limited respecs (D2 1.13), escalating gold (vanilla WoW, D4: about 4.36M gold for a full refund at level 100), dynamic gold by depth (PoE2, later reduced), and free in rested areas (WoW from 7.0.3). — [Diablo Wiki: Respec](https://diablo2.diablowiki.net/Respec); [warcraft.wiki.gg](https://warcraft.wiki.gg/wiki/Talent); [Wowhead D4](https://www.wowhead.com/diablo-4/pt/news/calculating-respec-costs-for-level-100-characters-333589); [Maxroll PoE2](https://maxroll.gg/poe2/resources/poe-2-passive-tree-and-dual-specialization); [PC Gamer PoE2 respec](https://pcgamer.com/games/rpg/path-of-exile-2-passive-skill-respecs-will-no-longer-cost-scrooge-mcduck-levels-of-gold)
- Last Epoch lets players respec skill trees per point while protecting tree dependencies (points that would orphan higher nodes cannot be removed), but locks the Mastery choice. — [ProGameGuides](https://progameguides.com/last-epoch/how-to-respec-passives-and-skill-tree-points-in-last-epoch/); [Prima](https://primagames.com/gaming/how-to-respec-in-last-epoch-passives-skills-and-specializations)

**Keystones and capstones**
- PoE keystones "dramatically change how you play," which is why the tree is more than a passive tree. — [Marooners' Rock](https://maroonersrock.com/2012/02/interview-chris-wilson-path-of-exile-part-1-of-3)
- BL2 "Gamechanger" and "Capstone" tiers sit on top of mostly stat-enhancing skills. — [Prima eGuide](https://primagames.com/eguides/borderlands-2-game-of-the-year-eguide/hyperions-most-wanted/salvador)

**Vertical vs horizontal; separating numeric grind**
- D4 moved numeric passive power to the Paragon board, the "proper place" for passive growth, and kept the tree for targeted choices. — [PC Gamer](https://pcgamer.com/blizzard-overhauls-diablo-4-skill-system-to-enable-more-distinct-character-builds) (search summary)
- WoW Dragonflight splits class (utility) and spec (role power) points so utility is not taxed. — [Blizzard](https://worldofwarcraft.blizzard.com/news/23797209/)

**Tree size vs cognitive load**
- D4 reworked its tree partly so new players avoid a "scary screen" (headline). — [NME](https://www.nme.com/news/diablo-4-skill-tree-rework-will-help-new-players-avoid-a-scary-screen-3362395)
- FFX's Expert grid is "not recommended to beginners" by guides; the Standard grid gives fixed paths. — [GameSkinny](https://www.gameskinny.com/5aji7/final-fantasy-x-standard-sphere-grid-vs-expert-sphere-grid)
- Doucet: limit the number of options open at any one time and gate the tree to avoid paralysis. — [Game Developer](https://gamedeveloper.com/design/upgrades-equipment-and-skill-trees)
- Community planners are a standard companion to big trees. Gearbox shipped an official BL2 skill-tree builder web app before launch. — [PC Gamer: BL2 skill trees detailed in web app](https://www.pcgamer.com/borderlands-2-skill-trees-detailed-in-funky-web-app)

### Inferences
These apply the lessons to PokiClash, a mobile hero-collecting card game in which heroes evolve by star level.
- Keep each hero's tree small, roughly 9–20 nodes, in the MHS gene-grid or Dragonflight-gate style, rather than one shared PoE-scale web. Use gates by star level ("row 2 opens at 3★"), which mirrors WoW's 8- and 20-point gates and Doucet's gating advice.
- Avoid pure "+5% ATK" filler. Where stat nodes are needed, put them in a separate sink (D4's Paragon lesson) and keep the tree for 2–3 choice nodes (one of two) and one capstone that changes the hero's skill behaviour (D4 2026, PoE keystones, BL2 capstones).
- Respec: since collection and ownership drive the game, cheap or free respec (WoW 7.0.3, D3) is safer than D4's escalating gold. Players should not feel punished for experimenting, while scarcity of points and resources keeps choices meaningful.
- Readability on a phone screen: few options visible at once, explicit numbers in node text, and a visible behaviour change (Doucet's clarity rule, D4's "not buried in fine print").
- Watch for multipliers from generic nodes outscaling the exciting nodes (the D4 glyph lesson).

### Gaps
- The GMTK "Building Better Skill Trees" transcript was blocked (Amara 403), so its specific lessons are not included.
- No GDC talk on skill-tree design was retrieved (e.g. Blizzard or GGG postmortems on talents or the passive tree).
- No quantitative build-diversity data (e.g. percent of players on the top build) was found for any game.
