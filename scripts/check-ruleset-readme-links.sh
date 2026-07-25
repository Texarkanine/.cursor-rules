#!/bin/sh
#
# Fail if any internal Markdown link in rulesets README files
# points at a path that does not exist.
#
# Usage: check-ruleset-readme-links.sh [rulesets_dir]
#   rulesets_dir defaults to <repo>/rulesets
#
# Checks inline links of the form [text](target). Skips http(s),
# mailto, and fragment-only targets. Strips #fragments before
# testing path existence.
#

set -eu

# Shared path helpers (script_dir / repo_root / resolve_rulesets_dir).
# shellcheck disable=SC1091
. "$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)/rulesets-check-common.sh"

# Return 0 if the target should not be checked on the filesystem.
is_skippable_target() {
	target=$1

	case "${target}" in
		''|\#*)
			return 0
			;;
		http://*|https://*|mailto:*)
			return 0
			;;
	esac
	return 1
}

# Emit one raw link target per line from a Markdown file.
extract_link_targets() {
	file=$1

	# POSIX awk: peel off successive [text](target) matches per line.
	awk '
	{
		s = $0
		while (match(s, /\[[^]]*\]\([^)]*\)/)) {
			m = substr(s, RSTART, RLENGTH)
			sub(/^\[[^]]*\]\(/, "", m)
			sub(/\)$/, "", m)
			print m
			s = substr(s, RSTART + RLENGTH)
		}
	}
	' "${file}"
}

check_readme_links() {
	rulesets_dir=$1
	fail_marker=

	if [ ! -d "${rulesets_dir}" ]; then
		printf 'error: not a directory: %s\n' "${rulesets_dir}" >&2
		return 1
	fi

	fail_marker=$(mktemp)
	# Clean up the marker file when the shell exits.
	trap 'rm -f "${fail_marker}"' EXIT HUP INT TERM

	# Find README files (regular or symlink). Empty tree is success.
	find "${rulesets_dir}" \( -name 'README' -o -name 'README.*' \) \
		\( -type f -o -type l \) -print \
		| sort \
		| while IFS= read -r readme; do
			[ -n "${readme}" ] || continue
			dir=$(CDPATH= cd -- "$(dirname -- "${readme}")" && pwd)

			extract_link_targets "${readme}" | while IFS= read -r target; do
				[ -n "${target}" ] || continue

				if is_skippable_target "${target}"; then
					continue
				fi

				# Drop fragment before testing path existence.
				path=${target%%#*}
				[ -n "${path}" ] || continue

				case "${path}" in
					/*)
						;;
					*)
						path="${dir}/${path}"
						;;
				esac

				if [ ! -e "${path}" ]; then
					printf 'broken link: %s -> %s\n' \
						"${readme}" "${target}" >&2
					# Subshell-safe failure flag (no pipefail in POSIX).
					printf 'x\n' >> "${fail_marker}"
				fi
			done
		done

	if [ -s "${fail_marker}" ]; then
		return 1
	fi
	return 0
}

main() {
	rulesets_dir=
	rulesets_dir=$(resolve_rulesets_dir "$@")
	check_readme_links "${rulesets_dir}"
}

if [ "${0##*/}" = "check-ruleset-readme-links.sh" ]; then
	main "$@"
fi
