# Active Context

## Current Task: standing-contract-reconcile-guard
**Phase:** PLAN - COMPLETE

## What Was Done
- Level 2 plan written: rewrite `reconcile-persistent.md` (probe + asymmetric skip + receipts), soften `systemPatterns.mdc` When to Update, extend `techContext.mdc` process/oracle examples
- Design constraints locked: skip-biased for noise; deliberate incompleteness; never pollute; no write-when-unsure; canonical `rulesets/` only
- Verification via review gates + `rg` + `make test` (no prose change-detector tests)

## Next Step
- Preflight validation
