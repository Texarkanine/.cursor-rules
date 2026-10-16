# Project Brief

## User Story

When `pick.py` is given a reviewer list that includes a slug the catalog does not know, it still chooses among the slugs it can place. The command prints that slug and exits successfully. It prints nothing about the skipped slug.

## Requirements

- An enabled reviewer slug whose model is not in the catalog is skipped.
- Nothing is written to stderr for that skip.
- If another enabled slug can be chosen, that slug is printed and the process exits 0.
- The pick does not fail because one available model has no catalog row.
