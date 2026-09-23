.PHONY: test test-symlinks test-readme-links test-choose-verification-model

test: test-symlinks test-readme-links test-choose-verification-model

test-symlinks:
	./scripts/check-ruleset-symlinks.sh

test-readme-links:
	./scripts/check-ruleset-readme-links.sh

test-choose-verification-model:
	python3 -m unittest discover -s tests/choose-verification-model -p 'test_*.py'
