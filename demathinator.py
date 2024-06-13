import discord
from discord.ext import commands
import aiosqlite
import json

DATABASE = 'bans.db'
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

async def initialize_db():
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS bans (id INTEGER PRIMARY KEY)''')
        await db.commit()

async def add_id(user_id):
    async with aiosqlite.connect(DATABASE) as db:
        await db.execute('INSERT INTO bans (id) VALUES (?)', (user_id,))
        await db.commit()

async def get_all_ids():
    async with aiosqlite.connect(DATABASE) as db:
        async with db.execute('SELECT id FROM bans') as cursor:
            return [row[0] for row in await cursor.fetchall()]

@bot.event
async def on_ready():
    await initialize_db()
    print(f'Logged in as {bot.user}')

@bot.command()
async def addid(ctx, user_id: int):
    await add_id(user_id)
    await ctx.send(f'Added ID {user_id} to the alt list.')

@bot.command()
async def ban(ctx):
    ids_to_ban = await get_all_ids()
    for user_id in ids_to_ban:
        try:
            user = await bot.fetch_user(user_id)
            await ctx.guild.ban(user, reason="Banned by demathinator")
            await ctx.send(f'Banned mathy {user.name} ({user_id}).')
        except discord.NotFound:
            await ctx.send(f'mathy with ID {user_id} not found.')
        except discord.Forbidden:
            await ctx.send(f'Bot does not have permission to ban mathy with ID {user_id}.')
        except discord.HTTPException as e:
            await ctx.send(f'Failed to ban mathy with ID {user_id}: {e}')

with open('config.json') as config_file:
    config = json.load(config_file)

bot.run(config['token'])