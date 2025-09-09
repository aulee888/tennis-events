import discord
from discord.ext import commands
import asyncio
import json
from pick_pairs import pick_pairs
import os

TOKEN = os.getenv("MX_DUBS_TOKEN")
CHANNEL_ID = 1414775798212333710
CAPACITY = 8
DATA_FILE = 'mx_dubs/attendance.json'

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
bot.reg_pairs = []


@bot.event
async def on_ready():
    print('Hello! This bot is ready!')
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send('Hello! This bot is ready!')

    
@bot.command()
async def join(ctx, partner: discord.Member):
    """Join as a mixed dubs pair with a partner"""
    user = ctx.author
    pair = (user, partner)

    # Avoid duplicates
    if pair not in bot.reg_pairs and (pair[::-1]) not in bot.reg_pairs:
        bot.reg_pairs.append(pair)
        await ctx.send(f'{user.mention} and {partner.mention} registered!')
    else:
        await ctx.send('This team is already registered!')


@bot.command()
async def cancel(ctx, partner: discord.member):
    user = ctx.author
    pair = (user, partner)

    if pair in bot.reg_pairs:
        bot.reg_pair.remove(pair)
        await ctx.send(f'{user.mention} and {partner.mention} have been removed from the registration list!')
        return

    elif pair[::-1] in bot.reg_pairs:
        bot.reg_pair.remove(pair[::-1])
        await ctx.send(f'{user.mention} and {partner.mention} have been removed from the registration list!')
        return

    await ctx.send(f'Team: {user.mention} & {partner.mention} are **not** on the registration list. Try again.')


@bot.command()
async def pick(ctx):
    """Initiates the selections for the week"""
    # Load or init attendance data
    try:
        with open(DATA_FILE, 'r') as f:
            attendance = json.load(f)
    except FileNotFoundError:
        attendance = {}
        
    num_pairs = CAPACITY // 2

    if len(bot.reg_pairs) < num_pairs:
        await ctx.send("No Mixed Dubs this week! Not enough players!")
        bot.reg_pairs = []

        return
    else:
        chosen_pairs = pick_pairs(bot.reg_pairs, attendance, num_pairs)

        with open(DATA_FILE, 'w') as f:
            json.dump(attendance, f)

        mentions = [f'{p1.mention} & {p2.mention}' for p1, p2 in chosen_pairs]

        await ctx.send(f'Selected Teams this weeek: {", ".join(mentions)}')
        bot.reg_pairs = []

        return


bot.run(TOKEN)