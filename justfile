set dotenv-load

# List all available commands
@default:
    just --unsorted --list


# Install dependencies
install:
    poetry install
    # reflex init

# Run the app locally
run:
    poetry run reflex run

# build frontend docker image
frontend:
    docker build -t chatdoc-frontend -f Dockerfile.web  .
    docker tag chatdoc-frontend:latest chatdoc-frontend:dev

# build backend docker image
backend:
    docker build -t chatdoc-backend .
    docker tag chatdoc-backend:latest chatdoc-backend:dev

# Run the app in a docker container
compose:
    docker compose up