ifndef VERBOSE
MAKEFLAGS += --no-print-directory -s
endif

refactory: ## Run autoflake
	@echo "---- Refactorying ----"
	@autoflake --remove-all-unused-imports --remove-duplicate-keys --remove-unused-variables --in-place --exclude globs -r *

.PHONY: clean
clean: ## Delete All pyc and pycache files
	@echo "-- [$(NAME)] clean --"
	@find . -name '*.pyc' -delete
	@find . -name '*__pycache__*' -delete

.PHONY: test
test: ## Run tests
	@python3 -m unittest discover

coverage: ## Run tests opening html coverage
	@coverage html --include=events_protocol/*
	@firefox htmlcov/index.html

dev: ## Install dev needed packages
	@pipenv install --dev
	@pipenv shell
	@pre-commit install

help: ## Show some help
	@echo
	@echo '  Usage:'
	@echo '    make <target>'
	@echo
	@echo '  Targets:'
	@egrep '^(.+)\:\ ##\ (.+)' ${MAKEFILE_LIST} | column -t -c 2 -s ':#'
	@echo