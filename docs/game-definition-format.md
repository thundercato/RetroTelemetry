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

The manifest is deliberately an index rather than a copy of every definition:
clients resolve a ROM hash to one relative JSON path and then validate the game
file before using it.
