# EDAS Sonic Migration Audit

Date: 2026-07-30

## Source definition

EDAS Bridge currently stores its Sonic the Hedgehog definition at
`retro_telemetry/profiles/mega_drive/Sonic the Hedgehog/Sonic the Hedgehog.rts.json`.
The extension is `.rts.json`. It is an EDAS-specific schema version 1 profile,
not a generic RetroTelemetry file.

The definition identifies the tested Mega Drive ROM as CRC32 `F9394E97` and
contains 25 `core_ram` memory fields. It uses `byte_order: swap16` with big
endian numeric decoding. This is required by the existing RetroArch Mega Drive
RAM response behaviour and must be retained.

## EDAS loading path

`APIs/edas_retroarch_api.py` obtains `GET_STATUS` from RetroArch's documented
UDP Network Control Interface. It receives system id, content basename, and a
RetroArch-reported CRC32. EDAS does not currently read the ROM file or calculate
CRC32, MD5, or SHA-1 itself.

`APIs/edas_retro_telemetry_api.py` scans `*.rts.json`, converts each field into
`RetroTelemetryField`, constructs grouped memory read plans, and decodes values
into stable `RetroArch.Telemetry.*` property ids. Profile selection currently
prefers a matching CRC32, then basename or RetroAchievements game id.

## Migration constraints

All 25 addresses, types, byte order, endianness, scaling, enumerations,
categories, descriptions, and property ids are carried forward unchanged. The
universal definition represents the same logical game, one tested ROM, and one
shared telemetry layout. EDAS retains legacy loading as a transition fallback.

## Reusable EDAS infrastructure

`APIs/edas_config_api.py` provides UTF-8 atomic JSON writes with flush, fsync,
and `os.replace`. RetroArch already runs its provider on a background thread.
RetroAchievements has independent cache/download helpers, but no reusable game
definition manifest client exists yet.
