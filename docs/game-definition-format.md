# RetroTelemetry Game Definition Format

The canonical game-definition extension is `.json`. Version 1 is described by
`schemas/retrotelemetry-game.schema.json` and validated by
`tools/retrotelemetry.py`.

Top-level fields are `format`, `schema_version`, `definition_version`, `game`,
`roms`, `telemetry_layouts`, and `provenance`.

`game` identifies the logical game. `roms` identifies individual revisions or
translations and links each one to a telemetry layout. A ROM has one required
primary hash and optional CRC32, MD5, and SHA-1 lists. `telemetry_layouts`
holds raw properties plus optional derived properties and events. Properties may
describe type, units, range, value map, endianness, polling, and their own
verification status.

Where a property has a clear cross-game gameplay meaning, add `canonical_id`.
This is a stable semantic label for consumers such as EDAS; it does not replace
the original game terminology in `id`, `edas_alias`, or `friendly_name`. For
example, Sonic's `rings` maps to `player.1.collectable.primary`, while its
`zone` maps to `game.level`. Use `notes` only for meaningful limitations such
as two-player-only data, signed direction, or a value whose unit depends on
gameplay context. Add `minimum` and `maximum` only when they are genuinely
fixed for the property.

The manifest is deliberately an index rather than a copy of every definition:
clients resolve a ROM hash to one relative JSON path and then validate the game
file before using it.
