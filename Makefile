.PHONY: test test-symlinks test-readme-links

test: test-symlinks test-readme-links

test-symlinks:
	./scripts/check-ruleset-symlinks.sh

test-readme-links:
	./scripts/check-ruleset-readme-links.sh
