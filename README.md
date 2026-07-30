# RetroTelemetry

RetroTelemetry is an open, community-maintained database of memory addresses, game state values, events and telemetry definitions for retro and classic games.

It is designed to be usable by any compatible application, emulator, haptic system, streaming tool, accessibility tool or immersion platform.

RetroTelemetry is an independent community project and is not tied to any single application.

## Repository structure

- `manifest.json` provides the master ROM-hash index.
- `games/` contains individual game definitions.
- `schemas/` contains the official JSON schemas.
- `docs/` contains project documentation.
- `tools/` contains validation and manifest-generation tools.
- `.github/workflows/` contains repository automation.

## First Definition

`games/mega-drive/sonic-the-hedgehog.json` is the first official definition. It
contains one verified ROM identifier (CRC32 `F9394E97`) and its verified Mega
Drive memory layout. The definition contains no ROM data or game assets.

## Working Locally

Use Python 3.11 or newer:

```powershell
python tools/retrotelemetry.py validate
python tools/retrotelemetry.py generate
python tools/retrotelemetry.py check
python -m unittest discover -s tests -v
```

`generate` rebuilds `manifest.json`. `check` compares the committed manifest to
the generated content while deliberately ignoring its generation timestamp.

## Definition Model

Each JSON file represents one logical game. A game can contain multiple ROMs,
and each ROM can carry CRC32, MD5, and SHA-1 identifiers and reference a shared
or revision-specific telemetry layout. Layouts contain raw properties, optional
derived properties, and optional events. Definitions are data only: consumers
must not execute expressions or scripts supplied by a definition.

Verification states are `verified`, `expected`, `experimental`, `broken`, and
`unverified`. A ROM must not be labelled verified merely because it uses another
ROM's layout.

## Maintainer Workflow

Create or update a game JSON file, run validation and manifest generation, then
submit both the definition and generated manifest in a pull request. The pull
request workflow validates all definitions, checks internal references and
hash conflicts, verifies the manifest, and runs the test suite. The main-branch
workflow regenerates the manifest only after a valid merge.

## Security

Definitions describe read-only data interpretation. They must not contain ROMs,
credentials, executable code, local paths, or instructions to call third-party
services. Clients should validate downloaded JSON, use a local cache, and keep
working when offline.

## Game identification

ROM versions are identified primarily by CRC32, with optional MD5 and SHA-1 hashes for additional verification.

One logical game definition may support multiple ROM revisions, regions, translations and modifications.

Each ROM version can reference a shared telemetry layout or its own version-specific layout.

## Contributions

Community contributions will be accepted through GitHub Pull Requests.

All changes must be reviewed and approved by a RetroTelemetry maintainer before they become part of the official database.

## Licence

This project is released under the MIT License.
