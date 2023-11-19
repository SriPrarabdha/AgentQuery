# Multi-Agent Postgres Data Analytics
*The way we interact with our data is changing.*

This repo is an **_experiment_** and **_learning tool_** for building multi-agent systems.

## 💻 Multi-Agent Postgres Data Analytics Tool 💻
This is a multi-agent system that allows you to ask questions about your postgres database in natural language.

The codebase is powered by GPT-4, Assistance API, AutoGen, Postgres, and Guidance.

It's the first of many multi-agent applications that utilize LLMs (large language models) to enable reasoning and decision making with reduced need for explicit rules or logic.

## 💻 Setup 💻
- **Read the codebase first**. Remember, this is an experiment and learning tool. It's not meant to be a framework or library.
- Run `git branch -a` to view all branches. Each branch is a video in the series.
  - `git checkout <branch-name>` you want to view.
- `poetry install`
- `cp .env.sample .env`
- Fill out `.env` with your postgres url and openai api key
- Run a prompt against your database
  - `poetry run start --prompt "<ask your agent a question about your postgres database>"`
    - Start with something simple to get a feel for it and then build up to more complex questions.
