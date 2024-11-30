# # This Dockerfile is used to deploy a single-container Reflex app instance
# # to services like Render, Railway, Heroku, GCP, and others.

# # It uses a reverse proxy to serve the frontend statically and proxy to backend
# # from a single exposed port, expecting TLS termination to be handled at the
# # edge by the given platform.
# FROM python:3.11

# ENV POETRY_VIRTUALENVS_CREATE=false \
#   POETRY_CACHE_DIR='/var/cache/pypoetry' \
#   POETRY_HOME='/usr/local' \
#   POETRY_VERSION=1.8.3

# # If the service expects a different port, provide it here (f.e Render expects port 10000)
# ARG PORT=8080
# # Only set for local/direct access. When TLS is used, the API_URL is assumed to be the same as the frontend.
# ARG API_URL
# ENV PORT=$PORT API_URL=${API_URL:-http://localhost:$PORT} REDIS_URL=redis://localhost PYTHONUNBUFFERED=1

# # Install Caddy and redis server inside image
# RUN apt-get update -y && apt-get install -y caddy redis-server && rm -rf /var/lib/apt/lists/*

# WORKDIR /app

# # Copy local context to `/app` inside container (see .dockerignore)
# COPY . .

# # Install app requirements and reflex in the container

# RUN curl -sSL https://install.python-poetry.org | python3 -

# COPY poetry.lock pyproject.toml /app/

# # Project initialization
# RUN poetry install

# # Deploy templates and prepare app
# RUN poetry run reflex init

# # Download all npm dependencies and compile frontend
# RUN poetry run reflex export --frontend-only --no-zip && mv .web/_static/* /srv/ && rm -rf .web

# # Needed until Reflex properly passes SIGTERM on backend.
# STOPSIGNAL SIGKILL

# EXPOSE $PORT

# # Apply migrations before starting the backend.
# CMD caddy start && \
#     redis-server --daemonize yes && \
#     exec poetry run reflex run --env prod --backend-only

FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

ENV POETRY_HOME="/opt/poetry" \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_VIRTUALENVS_IN_PROJECT=false \
  POETRY_NO_INTERACTION=1 \
  POETRY_VERSION=1.8.3

ENV PATH="$PATH:$POETRY_HOME/bin"

WORKDIR /app
COPY . .

RUN apt-get update && apt-get install --no-install-recommends -y curl

# Install app requirements and reflex in the container
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN poetry install --only=main --no-root

ENTRYPOINT ["poetry", "run", "reflex", "run", "--env", "prod", "--backend-only", "--loglevel", "debug" ]
