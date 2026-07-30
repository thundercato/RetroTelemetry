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

## Game identification

ROM versions are identified primarily by CRC32, with optional MD5 and SHA-1 hashes for additional verification.

One logical game definition may support multiple ROM revisions, regions, translations and modifications.

Each ROM version can reference a shared telemetry layout or its own version-specific layout.

## Contributions

Community contributions will be accepted through GitHub Pull Requests.

All changes must be reviewed and approved by a RetroTelemetry maintainer before they become part of the official database.

## Licence

This project is released under the MIT License.
