# Agentic OS Responsibility Boot Template

## Purpose

Defines the universal boot lifecycle for all Responsibilities.

## Boot Phases

Phase 0: Static files\
Phase 1: Orientation boot\
Phase 2: BOOT_SUMMARY persistence\
Phase 3: Task execution rehydration

## Canonical BOOT_SUMMARY Schema

``` json
{
  "responsibility_id": "string",
  "role_summary": "string",
  "always_rules": ["string"],
  "tool_usage_rules": [
    {
      "tool_name": "string",
      "when_to_use": "string",
      "safety_notes": "string"
    }
  ],
  "known_tools": ["string"],
  "open_state_threads": ["string"],
  "context_gaps": ["string"],
  "boot_timestamp": "iso8601"
}
```

## Runtime Rules

BOOT_SUMMARY overrides raw files. Reboot required on policy or tool
change.
