.PHONY: build init start bootstrap-up stop status restart clean migrate dev down


help:
	@echo "Help"
	@echo "-----------------------"
	@echo "  make build"
	@echo "    Build docker environment"
	@echo "  make init"
	@echo "    Build docker environment"
	@echo "  make start"
	@echo "    Run all service in docker environment"
	@echo "  make bootstrap-up"
	@echo "    Run ONLY bootstrap services(as DBs, redis, etc.)"
	@echo "  make stop"
	@echo "    Stop service in docker environment"
	@echo "  make down"
	@echo "    Stop service and remove temporary images"
	@echo "  make status"
	@echo "    Currently running docker containers(status)"
	@echo "  make clean"
	@echo "    Stop and remove all environment containers"
	@echo "  make dev"
	@echo "    Create docker-compose.override for development"
	@echo "-----------------------"

build:
	@docker-compose build

rebuild: clean
	@docker-compose build

init:
	@echo "Start init configuration"
	@docker-compose run --rm app python manage.py createsuperuser

migrate: bootstrap-up
	@docker-compose run --rm app python manage.py migrate --noinput
	@docker-compose run --rm app python manage.py collectstatic --noinput

messages: bootstrap-up
	@docker-compose run --rm app python manage.py makemessages
	@docker-compose run --rm app python manage.py compilemessages

bootstrap-up:
	@docker-compose up -d database minio
	@docker-compose ps

start: bootstrap-up
	@docker-compose up -d
	@docker-compose ps

stop:
	@docker-compose stop

down:
	@docker-compose down

status:
	@docker-compose ps

restart: stop start

clean: stop
	@docker-compose rm --force
