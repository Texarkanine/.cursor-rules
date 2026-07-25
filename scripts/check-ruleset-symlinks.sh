#!/bin/sh
#
# Fail if any symlink under a rulesets tree has a missing target.
#
# Usage: check-ruleset-symlinks.sh [rulesets_dir]
#   rulesets_dir defaults to <repo>/rulesets
#

set -eu

# Shared path helpers (script_dir / repo_root / resolve_rulesets_dir).
# shellcheck disable=SC1091
. "$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)/rulesets-check-common.sh"

check_symlinks() {
	rulesets_dir=$1
	broken_list=

	if [ ! -d "${rulesets_dir}" ]; then
		printf 'error: not a directory: %s\n' "${rulesets_dir}" >&2
		return 1
	fi

	# Collect symlinks whose targets do not exist.
	broken_list=$(
		find "${rulesets_dir}" -type l ! -exec test -e {} \; -print
	) || true

	if [ -z "${broken_list}" ]; then
		return 0
	fi

	printf '%s\n' "${broken_list}" | while IFS= read -r link; do
		[ -n "${link}" ] || continue
		printf 'broken symlink: %s -> %s\n' \
			"${link}" "$(readlink "${link}")" >&2
	done
	return 1
}

main() {
	rulesets_dir=
	rulesets_dir=$(resolve_rulesets_dir "$@")
	check_symlinks "${rulesets_dir}"
}

if [ "${0##*/}" = "check-ruleset-symlinks.sh" ]; then
	main "$@"
fi
