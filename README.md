# user filter Bot

This Discord bot is designed to serve as a preemptive user filter by banning unsavory users listed in an filter database before they have a chance to join your server. The database is updated in real-time. If you want to add someone to the filter list, please contact `zdashero` on Discord. (check bottom for filter coverage)

## Repo name
This bot was made in the start to ban a user named mathy and his alts so I named it the demathinator, I kept it the repo name because it is funny

## Features

- Bans users based on an up-to-date filter database.
- Restricts the `/filterban` command to specific user IDs.
- Provides a `/count` command to display the number of users in the database.

## Prerequisites

- Python 3.8 or higher
- Discord bot token
- List of user IDs that are allowed to use the `/filterban` command

## Installation

1. Clone the repository or download the `main.py` and `config.json` files.

2. Install the required libraries:
    ```bash
    pip install discord.py aiosqlite requests
    ```

3. Create a `config.json` file in the same directory as `main.py` with the following content:
    ```json
    {
        "token": "YOUR_BOT_TOKEN",
        "allowed_user_ids": [123456789012345678, 234567890123456789]
    }
    ```
    Replace `"YOUR_BOT_TOKEN"` with your actual bot token and update the `allowed_user_ids` array with the user IDs that should have access to the `/filterban` command.

## Usage

### Running the Bot

1. Save the `config.json` and `main.py` files.
2. Run the bot using:
    ```bash
    python main.py
    ```

### Commands

- **/filterban**: Bans users listed in the filter database. This command is restricted to user IDs specified in `config.json`.
- **/count**: Displays the number of users in the filter database.

## Filter coverage
this is a list of every type of user the database filters 

- extreme homophobia
- transphobia
- extreme racism
- witch hunting innocent people/groups
- doxxing
- pedophilia
- malware spreading
- nazism
- spreading gore

any more ideas of what to cover contact me
