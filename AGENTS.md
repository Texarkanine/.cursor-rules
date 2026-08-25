# Project Memory

Shared memory for this repository is managed through SumMem, invoked as `.summem/summem`.

## At Session Start: Activating SumMem

Run `.summem/summem wake` from the repository root. If you can see a prior project-root SumMem wake in this conversation's history, do not run it again.

## While Working: Register Memories

`.summem/summem note "…"` records one short line for a fact another contributor would still need. Personal, machine-local, and user preference facts stay out. `note` may sometimes print further instructions; always follow them.

Never invent filenames, rewrite note bytes, or delete memory files by hand. The script is the only writer. The files it writes are part of your work; do not leave them untracked.
