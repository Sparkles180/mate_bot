import os

config = {
    "api_key": os.environ["google_api_key"],
    "discord_token": os.environ["DISCORD_BOT_TOKEN"],
    "mysql_password": os.environ["mysql_password"]
}