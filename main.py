import discord
from discord.ext import commands
import aiosqlite
import requests
import json
import os

with open('config.json') as config_file:
    config = json.load(config_file)
TOKEN = config["token"]
ALLOWED_USER_IDS = config["allowed_user_ids"]

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

DATABASE_URL = "https://github.com/zdashero/demathinator/raw/main/bans.db"
DATABASE_PATH = "bans.db"

async def download_database():
    response = requests.get(DATABASE_URL)
    with open(DATABASE_PATH, 'wb') as file:
        file.write(response.content)

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
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute("SELECT id, reason FROM bans") as cursor:
            rows = await cursor.fetchall()
            for row in rows:
                user_id, reason = row
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

@bot.tree.command(name="count", description="Count the number of users in the filter database")
async def count(interaction: discord.Interaction):
    await interaction.response.defer()
    await download_database()
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute("SELECT COUNT(*) FROM bans") as cursor:
            count = await cursor.fetchone()
            await interaction.followup.send(f"There are {count[0]} users in the database.")

bot.run(TOKEN)
