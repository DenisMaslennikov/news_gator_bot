CONTAINER_NAME = bot

start: ## Запустить dev версию бота
	docker compose up --build

bash: ## Открыть оболочку bash в контейнере 'bot'
	docker compose exec $(CONTAINER_NAME) bash

drop: ## Остановить и удалить контейнеры Docker
	docker compose down -v

lock: ## Обновить зависимости проекта с использованием poetry
	docker compose run --build --user=root --rm $(CONTAINER_NAME) poetry lock

migration:  ## Создать миграции make migrations MSG="Добавить новую таблицу users"
	docker compose --env-file config/.env run --user=root --rm $(CONTAINER_NAME) ./run_alembic.sh "$(MSG)"
