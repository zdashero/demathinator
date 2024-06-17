import discord
from discord.ext import commands
import aiosqlite
import aiohttp
import json
import os

with open('config.json') as config_file:
    config = json.load(config_file)

TOKEN = config["token"]
ALLOWED_USER_IDS = config["allowed_user_ids"]

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="mm!", intents=intents)

DATABASE_URL = "https://github.com/zdashero/demathinator/raw/main/bans.db"
LATEST_COMMIT_URL = "https://api.github.com/repos/zdashero/demathinator/commits?path=bans.db&page=1&per_page=1"
DATABASE_PATH = "bans.db"
COMMIT_HASH_PATH = "latest_commit.txt"

async def get_latest_commit_hash():
    async with aiohttp.ClientSession() as session:
        async with session.get(LATEST_COMMIT_URL) as response:
            if response.status == 200:
                commits = await response.json()
                return commits[0]["sha"]
            else:
                raise Exception(f"Failed to fetch latest commit. Status code: {response.status}")

async def download_database():
    latest_commit_hash = await get_latest_commit_hash()
    
    if os.path.exists(COMMIT_HASH_PATH):
        with open(COMMIT_HASH_PATH, 'r') as file:
            local_commit_hash = file.read().strip()
    else:
        local_commit_hash = None

    if local_commit_hash != latest_commit_hash:
        async with aiohttp.ClientSession() as session:
            async with session.get(DATABASE_URL) as response:
                if response.status == 200:
                    with open(DATABASE_PATH, 'wb') as file:
                        file.write(await response.read())
                    with open(COMMIT_HASH_PATH, 'w') as file:
                        file.write(latest_commit_hash)
                else:
                    raise Exception(f"Failed to download database. Status code: {response.status}")

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Bot is ready. Logged in as {bot.user}')

@bot.tree.command(name="filterban", description="Ban users based on the filter database")
async def filterban(interaction: discord.Interaction):
    if interaction.user.id not in ALLOWED_USER_IDS:
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        return

    await interaction.response.defer()
    await download_database()
    try:
        async with aiosqlite.connect(DATABASE_PATH) as db:
            async with db.execute("SELECT id, reason FROM bans") as cursor:
                rows = await cursor.fetchall()
                banned_users = [entry async for entry in interaction.guild.bans()]
                banned_user_ids = {entry.user.id for entry in banned_users}

                for row in rows:
                    user_id = int(row[0])
                    reason = row[1]

                    if user_id in banned_user_ids:
                        print(f"User with ID {user_id} is already banned")
                        continue
                    user = await bot.fetch_user(user_id)
                    if user:
                        try:
                            await interaction.guild.ban(user, reason=reason)
                            await interaction.followup.send(f"Banned {user.name} for: {reason}")
                        except discord.Forbidden:
                            await interaction.followup.send(f"Failed to ban {user.name}: Forbidden")
                        except discord.HTTPException as e:
                            await interaction.followup.send(f"Failed to ban {user.name}: {e}")
                    else:
                        await interaction.followup.send(f"User with ID {user_id} not found")
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {e}")

@bot.tree.command(name="count", description="Count the number of users in the filter database")
async def count(interaction: discord.Interaction):
    await interaction.response.defer()
    await download_database()
    try:
        async with aiosqlite.connect(DATABASE_PATH) as db:
            async with db.execute("SELECT COUNT(*) FROM bans") as cursor:
                count = await cursor.fetchone()
                await interaction.followup.send(f"There are {count[0]} users in the database.")
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {e}")

bot.run(TOKEN)
