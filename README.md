# Mathy Ban Bot

A Discord bot that contains all of the alts mathy has used and bans them from the server with a single command.

## Features

- Add user IDs to a ban list.
- Ban all users in the ban list with a single command.
- Stores the bot token in a `config.json` file for security.
- Uses SQLite for lightweight database management.

## Prerequisites

- Discord bot token
- `discord.py` library
- `aiosqlite` library

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/yourusername/discord-ban-bot.git
    cd discord-ban-bot
    ```

2. **Install dependencies:**

    ```sh
    pip install discord.py aiosqlite
    ```

3. **Create `config.json` file:**

    Create a `config.json` file in the root directory of the project and add your bot token:

    ```json
    {
        "token": "YOUR_BOT_TOKEN_HERE"
    }
    ```

## Usage

1. **Run the bot:**

    ```sh
    python bot.py
    ```

2. **Commands:**

    - `!addid ID` - Add a user ID to the ban list.
    - `!ban` - Ban all users in the ban list from the server.

## Permissions

Ensure the bot has the necessary permissions to ban members in your Discord server. This can be managed through the Discord Developer Portal and server settings. (needs all intents)
