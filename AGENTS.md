# Project Memory

Shared memory for this repository is managed through SumMem, invoked as `.summem/summem`.

## At Session Start: Activating SumMem (mandatory)

Run `.summem/summem wake` from the repository root. Read `wake` output to the end; never truncate it - it is important memory and you need all of it. If you can see a prior project-root SumMem wake in this conversation's history, do not run it again.

## While Working: Register Memories

When something matches the write rule below, record it with SumMem's `note`. Record each note in the store nearest the code it is about; use the root store only when it applies to the whole project.

One short line another contributor needs to work on this repository: gotchas, norms, failed approaches, lore and tribal knowledge, etc. Not merely "news" - e.g. that a PR opened, checks passed, or a task completed. Personal, machine-local, and user preference facts stay out. Skip if nothing qualifies or it is already remembered.
