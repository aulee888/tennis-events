import discord
from discord.ext import commands
import asyncio
import json
from pick_players import pick_players
import os
 
TOKEN = os.getenv("MX_DUBS_TOKEN")
CHANNEL_ID = 1414775798212333710
CAPACITY = 8
MIN_PLAYERS = 2
DATA_FILE = 'uts/attendance.json'
 
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
bot.participants = []
 
@bot.event
async def on_ready():
    print('Hello! This bot is ready!')
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send('Hello! This bot is ready!')


@bot.command()
async def poll(ctx, *players):
    mentions = []
    for p in players:
        bot.participants.append(p)
        mentions.append(p)

    await ctx.send(f'Registered: {", ".join(mentions)} ')
 
    if len(bot.participants) < MIN_PLAYERS:
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
#                     bot.participants.append(str(user.id))  # use Discord ID as key
 
#     if len(bot.participants) < MIN_PLAYERS:
#         await ctx.send("No UTS this week! Not enough players!")
#         return
 
 
@bot.command()
async def remove(ctx, player):
    if player in bot.participants:
        bot.participants.remove(player)
        await ctx.send(f'{player} has been removed from registration list!')
    else:
        await ctx.send(f'{player} is not found on registration list!')

 
 
@bot.command()
async def pick(ctx):
    """Initiates the selections for the week"""
    # Load or init attendance data
    try:
        with open(DATA_FILE, 'r') as f:
            attendance = json.load(f)
    except FileNotFoundError:
        attendance = {}
    chosen_players = pick_players(bot.participants, attendance, CAPACITY)
 
    with open(DATA_FILE, 'w') as f:
        json.dump(attendance, f)
 
    mentions = [p for p in chosen_players]
    # mentions = [f'{bot.get_user(int(p)).mention}' for p in chosen_players]
    await ctx.send(f'Selected players this week: {", ".join(mentions)}')
 
    bot.participants = []
 
    return
 
bot.run(TOKEN)