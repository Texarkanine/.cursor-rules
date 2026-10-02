# Executing Dependabot Dispositions

Follow this file only after a disposition index has been shown and you are explicitly asked to execute. Do not merge Merge Ready pull requests from this file.

## Tools

Use stock `git` and stock `gh` only. Every command below is upstream git or GitHub CLI. Do not call shell aliases, wrapper scripts, or any other CLI.

## Isolated Checkout

Do this once per repository you will modify. Do not assume the current directory is that repository.

1. Use a local clone of `<owner>/<repo>` when you already have one. Otherwise:
   ```bash
   gh repo clone <owner>/<repo>
   ```
2. Use the `baseRefName` recorded while triaging. If you do not have it, read it with `gh pr view`. That is the branch to build on. For a combine, every included PR must share that base; if they do not, stop and leave them in Caution.
3. From inside the clone, fetch that base and add a linked worktree on a **new** branch. The branch name must not already exist. `<path>` is a new directory outside the clone's current checkout (a sibling directory is enough).
   ```bash
   git fetch origin <base-branch>
   git worktree add -b <new-branch> <path> origin/<base-branch>
   ```
   Use `-b`. Do not use `-B` or `git branch -f`; those reset an existing branch. If the clone's upstream remote is not named `origin`, substitute that remote's name.
4. Do the rest of the work in `<path>`.
5. After the new branch is pushed, remove the worktree from the clone:
   ```bash
   git worktree remove <path>
   ```
   `git worktree remove` refuses a dirty tree. If it refuses, stop. Do not force-remove it. Leave the branch in place while its pull request is open.

## Combining Interdependent Bumps

1. Create the isolated checkout above, one worktree for the whole set.
2. Apply every version from the PRs you are combining, in the same manifest files those PRs changed. A subdirectory bump stays in that subdirectory.
3. Refresh the lockfile with the package manager that owns it. The lockfile and the repository's CI config identify that manager. Do not assume npm.
4. Run the checks that gate pull requests on this repository. If you cannot run them, stop before opening the PR and name the check you could not run.
5. If `.github/dependabot.yml` or `.github/dependabot.yaml` already exists, keep that filename and add a `groups` entry on the matching `updates` item (same ecosystem and directory) so the next bump arrives as one pull request. Patterns are the packages you just combined:
   ```yaml
   groups:
     <group-name>:
       patterns:
         - "<package>"
         - "<scope>/*"
   ```
   If neither config file exists, do not create one. The pull request body in step 7 must say that.
6. Commit in the style already used on the base branch. The commit includes the `groups` edit from step 5 when that edit happened. When that history has no clear style, use Dependabot's own subject for this bump (`fix(deps):`, `chore(deps):`, or `fix(deps-dev):`).
7. Push the branch, then open the pull request. `gh pr create` with no title and body exits when it cannot prompt, and with no `--base` it targets the repository's default branch.
   ```bash
   git push -u origin <new-branch>
   gh pr create --repo <owner>/<repo> --base <base-branch> --title "<subject>" --body-file <body-file>
   ```
   Start `<body-file>` from the repository's pull request template when it has one. When step 5 found no Dependabot config file, say that in the body. `<base-branch>` is the `baseRefName` from triage. If the upstream remote is not named `origin`, use that name in `git push` too.
8. Close each superseded PR:
   ```bash
   gh pr close <original_number> --repo <owner>/<repo> --comment "Superseded by #<new_number>, which bumps <packages> together so their peer requirements resolve."
   ```
9. Remove the worktree as in Isolated Checkout.

## Adding Dependabot Excludes

1. Create the isolated checkout above.
2. Edit the existing `.github/dependabot.yml` or `.github/dependabot.yaml`. Keep the filename the repository already uses. If neither file exists, stop and report that; do not create a Dependabot config from scratch.
3. Add one `ignore` rule under the `updates` entry for that ecosystem and directory. Pick the shape that matches the reason.

   Version floor, when everything at or above a release is wrong:

   ```yaml
   ignore:
     - dependency-name: "<package>"
       versions:
         - ">=<major>.0.0"
   ```

   Update type, when every major bump is wrong:

   ```yaml
   ignore:
     - dependency-name: "<package>"
       update-types:
         - "version-update:semver-major"
   ```
4. Commit in the repository's existing style. A sound default when history has no clear style: `chore(deps): ignore <package> <constraint> in Dependabot`.
5. Push the branch, then open the pull request. Use the same non-interactive push and create as Combining Interdependent Bumps. `<base-branch>` is the `baseRefName` from triage:
   ```bash
   git push -u origin <new-branch>
   gh pr create --repo <owner>/<repo> --base <base-branch> --title "<subject>" --body-file <body-file>
   ```
   Start `<body-file>` from the repository's pull request template when it has one.
6. Close the original PR. The comment must contain both why and when. This quoting is bash; another shell must pass the same comment text:
   ```bash
   gh pr close <original_number> --repo <owner>/<repo> --comment "$(cat <<'EOF'
   Closing in favor of #<new_number>, which tells Dependabot to ignore <package> <constraint>.

   ### Why excluding is correct
   <The concrete break or pin: compiler, engine floor, or platform constraint.>

   ### When to stop excluding
   <The concrete condition that makes a deliberate upgrade appropriate.>
   EOF
   )"
   ```
7. Remove the worktree as in Isolated Checkout.

## Final Queue Summary

Query the assigned queue again and show what changed. Merge Ready items stay listed for the maintainer. Do not merge them unless you are explicitly asked to merge, and then use the merge method that repository already uses.
