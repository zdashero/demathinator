import discord
from discord.ext import commands
import aiosqlite
import requests
import json

with open('config.json') as config_file:
    config = json.load(config_file)

TOKEN = config["token"]
ALLOWED_USER_IDS = config["allowed_user_ids"]

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
client = requests.Session()

DATABASE_URL = "https://github.com/zdashero/demathinator/raw/main/bans.db"
DATABASE_PATH = "bans.db"
COMMITS_URL = "https://api.github.com/repos/zdashero/demathinator/commits"
LAST_COMMIT = None

async def download_database():
    global LAST_COMMIT
    commits = client.get(COMMITS_URL).json()
    commit_sha = commits[0]["sha"]

    if LAST_COMMIT != commit_sha:
        response = requests.get(DATABASE_URL)

        with open(DATABASE_PATH, 'wb') as file:
            file.write(response.content)

        LAST_COMMIT = commit_sha

async def isBanned(member: discord.Member, guild: discord.Guild) -> bool:
    try:
        banData = await guild.fetch_ban(member)
        return True
    except discord.NotFound:
        return False

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
                    banned = await isBanned(user, interaction.guild)
                    if banned:
                        continue
                    
                    try:
                        await interaction.guild.ban(user, reason=reason)
                        await interaction.followup.send(f"Banned {user.mention} ({user.id}) for: {reason}")
                    except discord.Forbidden:
                        await interaction.followup.send(f"Failed to ban {user.mention} ({user.id}): Forbidden")
                    except discord.HTTPException as e:
                        await interaction.followup.send(f"Failed to ban {user.mention} ({user.id}): {e}")
                else:
                    await interaction.followup.send(f"User with ID {user_id} not found")
    
    await interaction.followup.send("Complete.")

@bot.tree.command(name="count", description="Count the number of users in the filter database")
async def count(interaction: discord.Interaction):
    await interaction.response.defer()
    await download_database()
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute("SELECT COUNT(*) FROM bans") as cursor:
            count = await cursor.fetchone()
            await interaction.followup.send(f"There are {count[0]} users in the database.")

bot.run(TOKEN)
