import discord
from discord.ext import commands
import asyncio
import json
from pick_players import pick_players

TOKEN = 'blank'
CAPACITY = 8
MIN_PLAYERS = 2
DATA_FILE = 'attendance.json'

participants = []

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@bot.event
async def on_ready():
    print('Hello! This bot is ready!')


@bot.command()
async def poll(ctx, *players):
    for p in players:
        participants.append(p)

    if len(participants) < MIN_PLAYERS:
        await ctx.send("No UTS this week! Not enough players!")
        return
# async def poll(ctx):
#     """Start a poll asking who is available this week"""
#     message = await ctx.send('If you are available for UTS this week, react with ✅')
#     await message.add_reaction('✅')

#     await asyncio.sleep(30)  # wait 30s for responses
#     message = await ctx.channel.fetch_message(message.id)

#     for reaction in message.reactions:
#         if str(reaction.emoji) == '✅':
#             async for user in reaction.users():
#                 if not user.bot:
#                     participants.append(str(user.id))  # use Discord ID as key

#     if len(participants) < MIN_PLAYERS:
#         await ctx.send("No UTS this week! Not enough players!")
#         return


@bot.command()
async def remove(ctx, player):
    await participants.remove(player)
    ctx.send(f'{player} has been removed and is no longer available')


@bot.command()
async def pick(ctx):
    """Initiates the selections for the week"""
    # Load or init attendance data
    try:
        with open(DATA_FILE, 'r') as f:
            attendance = json.load(f)
    except FileNotFoundError:
        attendance = {}

    chosen_players = pick_players(participants, attendance, CAPACITY)

    with open(DATA_FILE, 'w') as f:
        json.dump(attendance, f)

    mentions = [p for p in chosen_players]
    # mentions = [f'{bot.get_user(int(p)).mention}' for p in chosen_players]
    await ctx.send(f'Selected players this weeek: {', '.join(mentions)}')

    participants = []

    return