.PHONY: up down build prune logs backend-logs frontend-logs migrate createsuperuser shell

up:
	docker compose up --build

down:
	docker compose down

build:
	docker compose build

prune:
	docker system prune -f

logs:
	docker compose logs -f

backend-logs:
	docker compose logs -f backend

frontend-logs:
	docker compose logs -f frontend

migrate:
	docker compose exec backend python manage.py migrate

createsuperuser:
	docker compose exec backend python manage.py createsuperuser

shell:
	docker compose exec backend python manage.py shell
