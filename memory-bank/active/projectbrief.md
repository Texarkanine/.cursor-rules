# Project Brief: Add Backwards Compatibility Guidance to Niko System

## User Story

As an operator using the Niko system, I want agents to stop treating backwards compatibility as an implicit requirement, so that they make clean-break changes by default and only consider compatibility when explicitly identified as a constraint.

## Requirements

1. Add a principle statement to `niko-core.mdc` Core Persona & Approach (after "Be disagreeable") establishing that backwards compatibility is not a default obligation
2. Add an operationalizing bullet to `niko-core.mdc` Research & Planning (after "Dependency & Impact Analysis") requiring public interface identification before compatibility analysis
3. Sharpen existing language in L3-plan "Boundary Changes" bullet to clarify that internal implementation changes are not boundary changes
4. Sharpen existing language in preflight "Conflict Detection" to scope "contracts or interfaces" to *public* contracts and *published* interfaces

## Constraints

- Content must match the density and tone of `niko-core.mdc`
- Changes to workflow phases must be minimal (sharpen existing language, not add new sections)
- All edits to canonical sources only (`rules/` and `rulesets/`)

## Creative Phase Reference

Design decision documented in `memory-bank/active/creative/creative-backcompat-guidance-placement.md`
