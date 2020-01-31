
refactory:
	@echo "---- Refactorying ----"
	@autoflake --remove-all-unused-imports --remove-duplicate-keys --remove-unused-variables --in-place --exclude globs -r *

.PHONY: clean
clean:
	@echo "-- [$(NAME)] clean --"
	@find . -name '*.pyc' -delete
	@find . -name '*__pycache__*' -delete

.PHONY: test
test:
	@python3 -m unittest discover

coverage:
	@coverage html --include=events_protocol/*
	@firefox htmlcov/index.html

