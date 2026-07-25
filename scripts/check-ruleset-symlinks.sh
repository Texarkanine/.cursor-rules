#!/bin/sh
#
# Fail if any symlink under a rulesets tree has a missing target.
#
# Usage: check-ruleset-symlinks.sh [rulesets_dir]
#   rulesets_dir defaults to <repo>/rulesets
#

set -eu

script_dir() {
	# Resolve the directory containing this script.
	CDPATH= cd -- "$(dirname -- "$0")" && pwd
}

repo_root() {
	CDPATH= cd -- "$(script_dir)/.." && pwd
}

resolve_rulesets_dir() {
	# Prefer an explicit argument; otherwise use <repo>/rulesets.
	if [ "$#" -ge 1 ] && [ -n "$1" ]; then
		printf '%s\n' "$1"
		return 0
	fi
	printf '%s\n' "$(repo_root)/rulesets"
}

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
