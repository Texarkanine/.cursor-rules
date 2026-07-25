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

script_dir() {
	CDPATH= cd -- "$(dirname -- "$0")" && pwd
}

repo_root() {
	CDPATH= cd -- "$(script_dir)/.." && pwd
}

resolve_rulesets_dir() {
	if [ "$#" -ge 1 ] && [ -n "$1" ]; then
		printf '%s\n' "$1"
		return 0
	fi
	printf '%s\n' "$(repo_root)/rulesets"
}

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

	if [ ! -d "${rulesets_dir}" ]; then
		printf 'error: not a directory: %s\n' "${rulesets_dir}" >&2
		return 1
	fi

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
					# Marker for the collector (stderr is the report).
					printf 'FAIL\n'
				fi
			done
		done \
		| {
			failed=0
			while IFS= read -r line; do
				if [ "${line}" = "FAIL" ]; then
					failed=1
				fi
			done
			[ "${failed}" -eq 0 ]
		}
}

main() {
	rulesets_dir=
	rulesets_dir=$(resolve_rulesets_dir "$@")
	check_readme_links "${rulesets_dir}"
}

if [ "${0##*/}" = "check-ruleset-readme-links.sh" ]; then
	main "$@"
fi
