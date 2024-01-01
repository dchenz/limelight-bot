# Limelight Discord Bot

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This bot is used to download every message in a Discord server and keep it in sync with a database. The database is shared with the Limelight backend server (see other repository), which aims to provide better search and filtering than Discord's built-in functions.

## Setup

### With Docker

```
docker build -f Dockerfile.bot -t limelight-bot

docker run --env-file .env limelight-bot
```

### Manual

```sh
# Install python dependencies.
pip3 install -r requirements-bot.txt

# Start the bot.
python3 bot.py
```

## Environment variables

- `DB_CONNECTION_STRING`: Connection string passed to sqlalchemy. Required.
- `BOT_TOKEN`: Discord bot token. Required.
- `BOT_LOG_LEVEL`: Log level. Defaults to ERROR.
- `BOT_LOG_SQLALCHEMY`: Enables debug mode in sqlalchemy. Defaults to false.

The bot can automatically load from a `.env` file.

## Commands

- `/download`: Download messages in the current channel
- `/pending`: Show pending channel downloads
