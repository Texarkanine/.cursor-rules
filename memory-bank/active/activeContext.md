# Active Context

- **Current Task:** Place the Gemini 4 gas models and refresh BenchLM scores
- **Phase:** BUILD - IN PROGRESS
- **What Was Done:** The operator chose the published overall as the catalog score, with the three-category mean only when that overall is missing. That change is in `modelpool.py`, and refresh has written the catalog. Carbon is S at 88.2, Neon is A at 91.8, Hydrogen is B at 78.8, Argon stays A at 79.1. The old preflight FAIL was about the category-mean plan and is stale.
- **Next Step:** Review the score flags. The rank window is one distinct score step among enabled same-tier models, so a Neon author draws the next enabled model when Argon is not in that list.
