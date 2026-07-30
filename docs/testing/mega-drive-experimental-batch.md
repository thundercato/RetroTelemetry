# Mega Drive Experimental Batch Testing

All definitions in this batch are **experimental**. They were generated from
the public Stable-Retro Genesis integration metadata, which supplies a SHA-1
and labelled memory fields, but none has been tested with RetroTelemetry or
EDAS. The source does not reliably identify region or revision. The SHA-1 in
each file is the published Stable-Retro integration identifier, not a claim of
compatibility with another dump.

Stable-Retro's Genesis work-RAM addresses are converted from the 24-bit
`0xFF0000`-`0xFFFFFF` range to RetroArch `core_ram` by subtracting `0xFF0000`.
The EDAS Sonic 1 reference mapping (`swap16`, big-endian) is applied to these
ordinary work-RAM properties and is itself part of what needs validation.

| Game | Definition | Primary SHA-1 | Layout | Properties | Source quality | Known uncertainties | First properties to test | Runtime status |
| --- | --- | --- | --- | ---: | --- | --- | --- | --- |
| Alien Soldier | `games/mega-drive/alien-soldier.json` | `FA141778BD6540775194D77318F27D2A934E1AC1` | `alien-soldier-stable-retro-experimental` | 3 | Stable-Retro labels | Region/revision and byte order untested | health, score, time | Not tested |
| Altered Beast | `games/mega-drive/altered-beast.json` | `38945360D824D2FB9535B4FD7F25B9AA9B32F019` | `altered-beast-stable-retro-experimental` | 3 | Stable-Retro labels | BCD score and byte order untested | health, lives, score | Not tested |
| Battletoads | `games/mega-drive/battletoads.json` | `5EF3C29B6BDD04D24552AB200D0530F647AFDB08` | `battletoads-stable-retro-experimental` | 3 | Stable-Retro labels | BCD score and revision untested | health, lives, score | Not tested |
| Castlevania: Bloodlines | `games/mega-drive/castlevania-bloodlines.json` | `4809CF80CED70E77BC7479BB652A9D9FE22CE7E6` | `castlevania-bloodlines-stable-retro-experimental` | 7 | Stable-Retro labels | Split level fields need interpretation | health, gems, lives, map | Not tested |
| Columns | `games/mega-drive/columns.json` | `17AE2595E4D3FB705C9F8F66D5938DECA3F95C4E` | `columns-stable-retro-experimental` | 2 | Stable-Retro labels | Score interpretation untested | gameover, score | Not tested |
| Comix Zone | `games/mega-drive/comix-zone.json` | `E8747EEFDF61172BE9DA8787BA5BE447EC73180F` | `comix-zone-stable-retro-experimental` | 5 | Stable-Retro labels | Progress/final score semantics untested | health, combos, progress | Not tested |
| Dr. Robotnik's Mean Bean Machine | `games/mega-drive/dr-robotniks-mean-bean-machine.json` | `AA6B60103FA92BC95FCC824BF1675E411627C8D3` | `dr-robotniks-mean-bean-machine-stable-retro-experimental` | 2 | Stable-Retro labels | Game-over polarity untested | gameover, score | Not tested |
| Dynamite Headdy | `games/mega-drive/dynamite-headdy.json` | `E843DECDFF262791B1237F1545F5B17C56712D5F` | `dynamite-headdy-stable-retro-experimental` | 4 | Stable-Retro labels | Stage score semantics untested | health, lives, score | Not tested |
| Golden Axe | `games/mega-drive/golden-axe.json` | `2CE17105CA916FBBE3AC9AE3A2086E66B07996DD` | `golden-axe-stable-retro-experimental` | 2 | Stable-Retro labels | BCD score and multiplayer behavior untested | lives, score | Not tested |
| Golden Axe III | `games/mega-drive/golden-axe-iii.json` | `CD9ECC1DF4E01D69AF9BEBCF45BBD944F1B17F9F` | `golden-axe-iii-stable-retro-experimental` | 3 | Stable-Retro labels | Level score semantics untested | health, lives, level score | Not tested |
| Mega Turrican | `games/mega-drive/mega-turrican.json` | `180285DBFC1613489F1C20E9FD6C2B154DEC7FE2` | `mega-turrican-stable-retro-experimental` | 4 | Stable-Retro labels | Time/score encoding untested | health, lives, time | Not tested |
| Mortal Kombat II | `games/mega-drive/mortal-kombat-ii.json` | `AF6D2DB16F2B76940FF5A9738F1E00C4E7EA485E` | `mortal-kombat-ii-stable-retro-experimental` | 9 | Stable-Retro labels | Player/enemy coordinate behavior untested | health, enemy health, rounds won | Not tested |
| MUSHA | `games/mega-drive/musha.json` | `821EEA5D357F26710A4E2430A2F349A80DF5F2F6` | `musha-stable-retro-experimental` | 2 | Stable-Retro labels | BCD score untested | lives, score | Not tested |
| Ristar | `games/mega-drive/ristar.json` | `1D15FF596DD4F3B2C1212A2E0C6E2B72F62C001E` | `ristar-stable-retro-experimental` | 2 | Stable-Retro labels | Score encoding untested | lives, score | Not tested |
| Rocket Knight Adventures | `games/mega-drive/rocket-knight-adventures.json` | `49634BB09C38FA03549577F977E6AFB6CEBAAC48` | `rocket-knight-adventures-stable-retro-experimental` | 3 | Stable-Retro labels | Score encoding untested | health, lives, score | Not tested |
| Shadow Dancer: The Secret of Shinobi | `games/mega-drive/shadow-dancer-the-secret-of-shinobi.json` | `A3A1C2CB8BD202C5E1B9745B35B2FFB12B2B90F5` | `shadow-dancer-the-secret-of-shinobi-stable-retro-experimental` | 2 | Stable-Retro labels | BCD fields and region untested | lives, score | Not tested |
| Shinobi III: Return of the Ninja Master | `games/mega-drive/shinobi-iii-return-of-the-ninja-master.json` | `1E07D7998E3048FCFBA4238AE96496460E91B3A5` | `shinobi-iii-return-of-the-ninja-master-stable-retro-experimental` | 3 | Stable-Retro labels | BCD score and revision untested | health, lives, score | Not tested |
| Sonic & Knuckles | `games/mega-drive/sonic-and-knuckles.json` | `88D6499D874DCB5721FF58D76FE1B9AF811192E3` | `sonic-and-knuckles-stable-retro-experimental` | 5 | Stable-Retro labels | Stable-Retro marks its state misaligned | lives, rings, position x/y | Not tested |
| Sonic 3 & Knuckles | `games/mega-drive/sonic-3-and-knuckles.json` | `B711A909CCE238CA4AF3E517A2EDCA306228EFA5` | `sonic-3-and-knuckles-stable-retro-experimental` | 12 | Stable-Retro labels | Two published SHA-1s; layout untested | zone, act, rings, lives | Not tested |
| Sonic the Hedgehog 2 | `games/mega-drive/sonic-the-hedgehog-2.json` | `8BCA5DCEF1AF3E00098666FD892DC1C2A76333F9` | `sonic-the-hedgehog-2-stable-retro-experimental` | 12 | Stable-Retro labels | Mode/level-complete values untested | zone, act, rings, lives | Not tested |
| Sonic the Hedgehog 3 | `games/mega-drive/sonic-the-hedgehog-3.json` | `75E9C4705259D84112B3E697A6C00A0813D47D71` | `sonic-the-hedgehog-3-stable-retro-experimental` | 6 | Stable-Retro labels | Time representation untested | rings, lives, position x/y | Not tested |
| Splatterhouse 2 | `games/mega-drive/splatterhouse-2.json` | `59EC19EC442989D2738C055B9290661661D13F8F` | `splatterhouse-2-stable-retro-experimental` | 3 | Stable-Retro labels | BCD score and health range untested | health, lives, score | Not tested |
| Streets of Rage | `games/mega-drive/streets-of-rage.json` | `731CDF182FE647E4977477BA4DD2E2B46B9B878A` | `streets-of-rage-stable-retro-experimental` | 2 | Stable-Retro labels | Only player-one-like labels available | lives, score | Not tested |
| Streets of Rage 2 | `games/mega-drive/streets-of-rage-2.json` | `8B656EEC9692D88BBBB84787142AA732B44CE0BE` | `streets-of-rage-2-stable-retro-experimental` | 2 | Stable-Retro labels | Only player-one-like labels available | lives, score | Not tested |
| Streets of Rage 3 | `games/mega-drive/streets-of-rage-3.json` | `40A33DD6F9DAB0AFF26C7525C9B8F342482C7AF6` | `streets-of-rage-3-stable-retro-experimental` | 2 | Stable-Retro labels | Score has a three-byte raw representation | lives, score | Not tested |
| Strider | `games/mega-drive/strider.json` | `26FE42D13A01C8789BBAD722EBAC05B8A829EB37` | `strider-stable-retro-experimental` | 3 | Stable-Retro labels | BCD score and revision untested | health, lives, score | Not tested |
| Super Hang-On | `games/mega-drive/super-hang-on.json` | `E58A8E6C472A34D9ECF3B450137DF8A63EC9C791` | `super-hang-on-stable-retro-experimental` | 3 | Stable-Retro labels | All fields declared BCD by source | speed, time, score | Not tested |
| The Revenge of Shinobi | `games/mega-drive/the-revenge-of-shinobi.json` | `B1044E3B782351E69EBA0ABC94A3F08C379C27BC` | `the-revenge-of-shinobi-stable-retro-experimental` | 2 | Stable-Retro labels | Score encoding and revision untested | lives, score | Not tested |
| Thunder Force IV | `games/mega-drive/thunder-force-iv.json` | `ECBC2BFC4F3D8BBD46B398274ED2F5CC3DB68454` | `thunder-force-iv-stable-retro-experimental` | 2 | Stable-Retro labels | BCD score and revision untested | lives, score | Not tested |
| Vectorman | `games/mega-drive/vectorman.json` | `57A64D08028B539DC236A693D383F2E1269A5DD4` | `vectorman-stable-retro-experimental` | 2 | Stable-Retro labels | Score and life values untested | lives, score | Not tested |

## Suggested Test Sequence

1. Start the ROM that matches the listed SHA-1 and confirm the manifest selects
   the definition.
2. Watch the listed first properties while changing them in obvious gameplay.
3. For action games, take damage, lose a life, score points, and enter another
   area. For driving games, change speed and let the timer advance. For puzzle
   games, clear a line or complete a round.
4. Compare raw values with the game HUD; do not treat a BCD-labelled score as a
   decimal number until it has been confirmed.
5. Test pause/title/continue state only where a definition exposes it. These
   first-pass files intentionally do not infer missing state addresses.

## Reporting Results

For each tested ROM, report the game title, SHA-1, emulator/core, and EDAS
build. Mark each property as correct, static, changing-with-wrong-meaning, or
incorrect. Include observed raw values and HUD values when types, byte order,
or BCD encoding appear wrong. State any regional/revision mismatch explicitly.
This is enough evidence to promote individual properties later without
overstating compatibility for the rest of the layout.
