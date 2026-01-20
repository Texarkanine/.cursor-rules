# Project Brief: Cursor Rules Repository

## Project Overview
This repository contains reusable Cursor IDE rules, including the Niko Memory Bank system - a structured approach to task management, context preservation, and knowledge archival for AI-assisted development.

## Core Components
- **Niko System**: Memory Bank-based workflow management with complexity-based routing
- **Cursor Rules**: Reusable `.mdc` rule files for consistent AI behavior
- **Command System**: Slash commands for mode transitions (`/niko`, `/niko/plan`, `/niko/build`, etc.)

## Repository Structure
- `.cursor/rules/shared/` - Active rules loaded by Cursor
- `rulesets/niko/` - Source ruleset files (synced to .cursor/rules/shared/)
- `rules/` - Standalone reusable rules

## Key Principles
1. Rules should be self-contained and reusable across projects
2. Memory Bank files are ephemeral working documents; archives are permanent records
3. Progressive rule loading to optimize context usage
