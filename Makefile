ifneq (,$(wildcard ./.env))
    include .env
    export
endif

dc-start: ## Start docker services declared in docker-compose.yml
	docker-compose up -d --build --force-recreate

dc-stop: ## Stop docker services
	docker-compose down

dc-restart: dc-stop dc-start ## Restart docker services

pg-availability:
	chmod +x ./scripts/wait-for-postgres.sh
	sh -x ./scripts/wait-for-postgres.sh

install-requirements:
	python3.10 -m venv ./sprout-ai
	source ./sprout-ai/bin/activate; \
	pip install -r dev-requirements.txt

tests: install-requirements
	coverage run manage.py test -v 2
	coverage html
	open htmlcov/index.html
