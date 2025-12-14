# Task List: Niko Ruleset Integration

## Overview
Integrating Memory Bank system into Niko ruleset with proper UI/UX changes and conflict resolution.

**Installation Path**: `.cursor/rules/shared/niko/...` (ai-rizz shared rules)

## Task Breakdown

### 1. UI/UX Changes
- [ ] 1.1: Verify `/niko` entrypoint command naming (change from `/van`)
- [ ] 1.2: Verify sub-command paths (`/niko/build`, `/niko/plan`, etc.)
- [ ] 1.3: Update all internal references to commands in documentation

### 2. Path Corrections
- [ ] 2.1: Update all `.cursor/rules/isolation_rules/` references to `.cursor/rules/shared/niko/isolation_rules/`
- [ ] 2.2: Update command file references to new paths
- [ ] 2.3: Verify all mdc: links work with new structure

### 3. Bug Fixes
- [ ] 3.1: Fix missing `creative-phase-algorithm.mdc` reference
- [ ] 3.2: Fix XML/PowerShell syntax errors in `rule-calling-help.mdc`

### 4. TDD Integration
- [ ] 4.1: Analyze conflicts between isolation_rules and always-tdd.mdc
- [ ] 4.2: Determine integration strategy
- [ ] 4.3: Implement chosen strategy

### 5. Niko-Core Integration
- [ ] 5.1: Analyze conflicts between isolation_rules and niko-core.mdc
- [ ] 5.2: Determine integration strategy
- [ ] 5.3: Document relationship

### 6. Niko-Refresh Command
- [ ] 6.1: Analyze niko-refresh.mdc for command conversion
- [ ] 6.2: Create `/niko/refresh` command
- [ ] 6.3: Update references

### 7. Verification
- [ ] 7.1: Cross-check all file paths
- [ ] 7.2: Verify command structure
- [ ] 7.3: Test rule loading paths

## Current Status
- Phase: Analysis and Planning
- Current Task: 1.1 - Verifying `/niko` entrypoint

## Notes
- Source inspiration: cursor-memory-bank repo
- Customizations already in ai-rizz repo
- Must maintain backward compatibility where possible

