# Project Memory

Shared memory for this repository is managed through SumMem: run `.summem/summem -h` for usage information. Scoped memory stores may exist; `--path` aimed at a file retrieves memories from the nearest store.

## At Session Start: Activating SumMem (Mandatory)

If you can see a prior **root** SumMem wake in this conversation, skip `wake`.

Otherwise run `.summem/summem wake` from the repository root.

## While Working: Register Memories (Mandatory)

`.summem/summem note "…"` records one short line. Call it whenever you learn a fact about this project that another contributor would still need: designs, decisions, invariants, and the like. It has to belong in a fresh clone on another machine. Personal, machine-local, and user preference facts stay out. If `note` asks for a nap, the note is already stored; the nap is extra work on two older view nodes. Do that nap before your next action.

Do not register redundant memories.

Never invent filenames, rewrite note bytes, or delete memory files by hand. The script is the only writer. The files it writes are part of your work; do not leave them untracked.

## Other commands

- `.summem/summem recall <regex>` — search remembered text word for word
- `.summem/summem zoom <id>` — any memory with a `x<N> <hash>: …` prefix is a nap that can be zoomed in on. A leaf is `x1 YYYY-MM-DD:` and is not a zoom target.
- `.summem/summem wake --path <path>` — when you work under a cataloged path, pull that store if its wake is not already in this conversation. Ignore `--path` if the root wake didn't have a catalog.
