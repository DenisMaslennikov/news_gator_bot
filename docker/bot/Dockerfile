FROM python:3.12

# Set environment variables
ENV TZ=Europe/Moscow \
  # python:
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  # poetry:
  POETRY_VERSION=1.8.3 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local'

SHELL ["/bin/bash", "-eo", "pipefail", "-c"]

# Set the working directory in the container
WORKDIR /app

# Установка зависимостей и очистка кэша
RUN --mount=type=cache,target=/var/cache/apt apt-get update \
    && apt-get install --no-install-recommends -yqq curl poppler-utils \
    && curl -sSL https://install.python-poetry.org | python - \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

# Копировать только pyproject.toml, чтобы кэшировать их в слое docker
COPY ./pyproject.toml .

# Установка зависимостей:
RUN --mount=type=cache,target="$POETRY_CACHE_DIR" \
  poetry version \
  && poetry run pip install -U pip \
  && poetry install --no-interaction --no-ansi

# Ставим wait-for-it https://github.com/vishnubob/wait-for-it
COPY ./docker/utils/wait-for-it.sh /wait-for-it.sh

COPY ./docker/utils/entrypoint.sh /docker-entrypoint.sh

# Установка соответствующих разрешений:
RUN chmod +x '/wait-for-it.sh' \
  && chmod +x '/docker-entrypoint.sh' \
  # Замена разделителя строк CRLF на LF для пользователей Windows:
  && sed -i 's/\r$//g' '/docker-entrypoint.sh'

# С помощью пользовательской точки входа мы настраиваем, как загружается наше приложение:
ENTRYPOINT ["/docker-entrypoint.sh"]
