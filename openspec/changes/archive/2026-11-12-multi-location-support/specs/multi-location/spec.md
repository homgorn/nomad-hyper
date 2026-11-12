# multi-location Specification

## ADDED Requirements

### Requirement: Location catalog
The system SHALL expose a curated catalog of locations.

#### Scenario: List locations
- WHEN a client requests the catalog
- THEN it receives locations with id, name, country, coordinates, lora_frequency

### Requirement: Multi-select selection
The system SHALL allow selecting zero or more locations; empty selection means unrestricted access.

#### Scenario: Set selection
- WHEN a client PUT /api/locations with a list of catalog ids
- THEN the selection is persisted and returned

#### Scenario: Invalid id
- WHEN a client PUTs an id not in the catalog
- THEN the request is rejected with a validation error

#### Scenario: Corrupted stored selection
- WHEN the stored selection is invalid JSON
- THEN it resolves to an empty selection (unrestricted), not an error