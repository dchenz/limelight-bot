# Limelight Discord Bot

This bot is used to download every message in a Discord server and keep it in sync with a database. The database is shared with the Limelight backend server (see other repository), which aims to provide better search and filtering than Discord's built-in functions.

## Setup

```sh
# Clone the repository

echo "TOKEN=YOUR_SECRET_BOT_TOKEN" > .env
# or
export TOKEN=YOUR_SECRET_BOT_TOKEN

pip3 install -r requirements.txt
python3 __init__.py

# Before starting the bot,
# create/edit the config files if you need them
cd config
cp allowed_users.example.json allowed_users.json
cp ignored_channels.example.json ignored_channels.json
```

## Commands

```
PREFIX sync start [--with-channels|--without-channels]
```
- Starts a sync job that downloads all messages in the specified channels
- If ``--with-channels`` is not specified, the bot will target all channels where it has read/history permissions.
- The two options are mutually-exclusive and cannot be used together.
- Channel IDs can be supplied as an integer (98765432123456) or by tagging the channel (#general).