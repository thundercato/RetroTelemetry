# Mega Drive Research Batch 01

This batch adds 50 **experimental** Mega Drive definitions. It is intended for
runtime validation in EDAS, not as a claim that any new address is verified.

## Source and conversion

Each definition records its exact Stable-Retro source folder, `data.json`, and
`rom.sha` path in `provenance`. The source provides labelled variables and a
SHA-1 ROM identity. Its Genesis addresses use 24-bit work-RAM notation; EDAS
uses a 64 KiB `core_ram` block, so values in `0xFF0000`-`0xFFFFFF` are stored as
offsets after subtracting `0xFF0000`.

`source_label`, `source_type`, and `source_address` preserve the imported
technical record. `canonical_id` is added only where the label has a clear
cross-game meaning. Scores marked `bcd` or `bcd_low_nybble` require particular
attention during testing.

## Runtime test workflow

1. Confirm EDAS selects the definition using the displayed SHA-1.
2. Watch lives, health, score, position, timer, or game state values relevant
   to that title.
3. Change one value at a time in normal play.
4. Record static values, incorrect movement, byte-order issues, unexpected
   scaling, and ROM/revision mismatches.
5. Promote only individually tested properties, layouts, and ROMs. Do not
   promote a whole definition because one value appears correct.

## Included families

- Sonic: Sonic 2, Sonic 3, Sonic & Knuckles, Sonic 3 & Knuckles.
- Beat-'em-ups and action: Streets of Rage 1-3, Golden Axe, Golden Axe III,
  Revenge of Shinobi, Shadow Dancer, Shinobi III, Cyborg Justice, General Chaos.
- Fighters: Mortal Kombat 1-3, Street Fighter II' Special Champion Edition,
  TMNT Tournament Fighters.
- Shooters and arcade action: After Burner II, Space Harrier II, Thunder Force
  IV, MUSHA, Phelios, Alien Soldier, Pulseman.
- Platform/adventure: Comix Zone, Ristar, Rocket Knight Adventures, Vectorman
  1-2, Strider, Altered Beast, Battletoads, Battletoads & Double Dragon,
  Dynamite Headdy, Splatterhouse 2, Shadow of the Beast, Castle of Illusion,
  The Jungle Book, Mega Man: The Wily Wars, QuackShot, The Great Circus Mystery.
- Other: Castlevania: Bloodlines, Mega Turrican, The Adventures of Batman &
  Robin, RoboCop 3, Desert Strike, Cannon Fodder, Columns.

Every included file remains `experimental` until its own runtime evidence is
recorded.
