# Limelight Discord Bot

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This bot is used to download every message in a Discord server and keep it in sync with a database. The database is shared with the Limelight backend server (see other repository), which aims to provide better search and filtering than Discord's built-in functions.

## Setup

```sh
# Edit the placeholder values with your bot configuration.
cp config.example.yaml config.yaml && vim config.yaml

# Install python dependencies.
pip3 install -r requirements.txt

# Start the bot.
python3 run.py
```

## Commands

- `/download`: Download messages in the current channel
- `/pending`: Show pending channel downloads
