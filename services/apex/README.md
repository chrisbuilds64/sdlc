# services/apex/

APEX application exports — version-controlled as SQL and YAML.

## Export Format

Applications are exported using Oracle SQLcl `project` command with split, readable YAML format:

```bash
sql /nolog
project export -split -expType APPLICATION_SOURCE,READABLE_YAML
```

This produces a human-readable, AI-friendly format that diffs cleanly in Git.

## Structure

```
apex/
└── f100/                   # Application 100 (example)
    ├── application/
    └── ...
```

## Phase

Phase 1 (after Oracle and ORDS are running locally).
