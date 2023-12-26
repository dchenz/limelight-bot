from bot import LimelightBot


if __name__ == "__main__":
    import json
    import os

    import dotenv

    def load_discord_ids_config(filename: str) -> list[int]:
        loaded = []
        try:
            with open(filename, "r") as f:
                ids = json.load(f)
                loaded.extend(int(x) for x in ids)
        except FileNotFoundError:
            print("Could not load " + filename)
            exit(1)
        except json.JSONDecodeError:
            pass
        except ValueError:
            print("Invalid ID in " + filename)
            exit(1)
        print(f"Loaded {len(loaded)} from {filename}")
        return loaded

    # Users who can run bot commands
    allowed_users = load_discord_ids_config("config/allowed_users.json")

    # Channels ignored by sync jobs
    # Bot can still listen for commands here
    ignored_channels = load_discord_ids_config("config/ignored_channels.json")

    dotenv.load_dotenv()
    bot = LimelightBot(
        "&lime", allowed_users=allowed_users, ignored_channels=ignored_channels
    )
    token = os.environ.get("TOKEN")
    if not token:
        print("Missing bot token")
        exit(1)
    bot.run(token)
