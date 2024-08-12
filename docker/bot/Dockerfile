FROM python:3.12-bullseye

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
WORKDIR /NewsGatorBot

# Установка зависимостей и очистка кэша
RUN --mount=type=cache,target=/var/cache/apt apt-get update \
    && apt-get install --no-install-recommends -yqq curl poppler-utils \
    && curl -sSL https://install.python-poetry.org | python - \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update -y && apt-get install -y wget xvfb curl unzip jq

RUN apt-get install -y libxss1 libappindicator1 libgconf-2-4 \
    fonts-liberation libasound2 libnspr4 libnss3 libx11-xcb1 libxtst6 lsb-release xdg-utils \
    libgbm1 libnss3 libatk-bridge2.0-0 libgtk-3-0 libx11-xcb1 libxcb-dri3-0

RUN curl -s https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json > /tmp/versions.json

RUN CHROME_URL=$(jq -r '.channels.Stable.downloads.chrome[] | select(.platform=="linux64") | .url' /tmp/versions.json) && \
    wget -q --continue -O /tmp/chrome-linux64.zip $CHROME_URL && \
    unzip /tmp/chrome-linux64.zip -d /opt/chrome

RUN chmod +x /opt/chrome/chrome-linux64/chrome


RUN CHROMEDRIVER_URL=$(jq -r '.channels.Stable.downloads.chromedriver[] | select(.platform=="linux64") | .url' /tmp/versions.json) && \
    wget -q --continue -O /tmp/chromedriver-linux64.zip $CHROMEDRIVER_URL && \
    unzip /tmp/chromedriver-linux64.zip -d /opt/chromedriver && \
    chmod +x /opt/chromedriver/chromedriver-linux64/chromedriver

ENV CHROMEDRIVER_DIR /opt/chromedriver
ENV PATH $CHROMEDRIVER_DIR:$PATH

RUN rm /tmp/chrome-linux64.zip /tmp/chromedriver-linux64.zip /tmp/versions.json

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
  && sed -i 's/\r$//g' '/docker-entrypoint.sh' \
  && sed -i 's/\r$//g' '/wait-for-it.sh'

# С помощью пользовательской точки входа мы настраиваем, как загружается наше приложение:
ENTRYPOINT ["/docker-entrypoint.sh"]
