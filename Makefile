dc-start: ## Start docker services declared in docker-compose.yml
	docker-compose up -d --build --force-recreate

dc-stop: ## Stop docker services
	docker-compose down

dc-restart: dc-stop dc-start ## Restart docker services

pg-availability:
	chmod +x ./scripts/wait-for-postgres.sh
	sh -x ./scripts/wait-for-postgres.sh

tests: dc-start pg-availability
	docker-compose exec web coverage run manage.py test -v 2
	# docker-compose exec web coverage html
	docker-compose exec web coverage report