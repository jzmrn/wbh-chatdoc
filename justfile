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

# build docker image
build:
    docker build -t chatdoc .
    docker tag chatdoc:latest chatdoc:dev
