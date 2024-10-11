set dotenv-load

# List all available commands
default:
    just --list

# Install dependencies
install:
    poetry install
    reflex init

# Run the app locally
run:
    poetry run reflex run