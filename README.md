# chatdoc

Chatbot using RAG architecture to answer document related questions

## Requirements

The following tools are required to run the app locally:

- python
- poetry
- reflex
- just

## Installation

Run the following command to install the dependencies:

```bash
just install
```

## Run

Create an `.env` file with the following variables:

- AZURE_CLIENT_ID
- AZURE_CLIENT_SECRET
- AZURE_TENANT_ID
- OPENAI_API_KEY
- PINECONE_API_KEY

Run the following command to start the app locally (env file loaded automatically):

```bash
just run
```