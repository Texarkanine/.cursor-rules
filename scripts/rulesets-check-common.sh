#!/bin/sh
#
# Shared helpers for rulesets layout check scripts.
# Source this file; do not execute it.
#

script_dir() {
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
