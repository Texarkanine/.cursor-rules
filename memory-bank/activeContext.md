# Active Context

## Current Focus
Wiggum-Niko CodeRabbit PR Integration - Reflection Complete

## Summary
Created `rules/wiggum-niko-coderabbit-pr.md` (138 lines) that delegates to Niko's `/build` and `/reflect` commands.

## Key Insight
Original was already partially Niko-integrated (used `memory-bank/wiggum/`). This version tightens integration by using `tasks.md` directly and adding the `/reflect` step before commit/push.

## Next Step
User to delete original `rules/wiggum-coderabbit-pr.md` and optionally rename the new file.
