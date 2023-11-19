# Multi-Agent Postgres Data Analytics
*The way we interact with our data is changing.*

This repo is an **_experiment_** and **_learning tool_** for building multi-agent systems.

## 💻 Multi-Agent Postgres Data Analytics Tool 💻
This is a multi-agent system that allows you to ask questions about your postgres database in natural language.

The codebase is powered by GPT-4, Assistance API, AutoGen, Postgres, and Guidance.

It's the first of many multi-agent applications that utilize LLMs (large language models) to enable reasoning and decision making with reduced need for explicit rules or logic.

## 💻 Setup 💻
- **Read the codebase first**. 
- 
- Run `git clone https://github.com/SriPrarabdha/AgentQuery` to clone the repo on your local machine

- `poetry install`
- `cp .env.sample .env`
- Fill out `.env` with your postgres url and openai api key
- Run a prompt against your database
  - `poetry run start --prompt "<ask your agent a question about your postgres database>"`
    - Start with something simple to get a feel for it and then build up to more complex questions.
