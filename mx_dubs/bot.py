import discord
from discord.ext import commands
import asyncio
import json
from pick_pairs import pick_pairs
import os
from datetime import datetime

TOKEN = os.getenv("MX_DUBS_TOKEN")
CHANNEL_ID = 1414775798212333710
DATA_FILE = 'mx_dubs/attendance.json'

CAPACITY = 4  # Number of teams
MIN_TEAMS = 2
NEXT_SESS = datetime(2025, 9, 16)
START_TIME = '6pm'  # Set as string

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
bot.reg_pairs = []


@bot.event
async def on_ready():
    print('Hello! This bot is ready!')
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send('Hello! This bot is ready!')


@bot.event
async def on_raw_reaction_add(payload):
    user = await bot.fetch_user(payload.user_id)

    if user == bot.user.id:
        return

    channel = bot.get_channel(payload.channel_id)
    if not channel:  # Channel might not be in cache, try fetching
        channel = await bot.fetch_channel(payload.channel_id)

    message = await channel.fetch_message(payload.message_id)
    msg_embed = message.embeds[0]

    # Check for "Poll" type questions that expects reactions as confirmations
    if message.author == bot.user and msg_embed.title == '🎾 Mixed Doubles Confirmation':
        user_choice = str(payload.emoji)

        if user_choice not in ['✅', '❌']:
            return
        
        if user_choice == '✅':
            bot.reg_pairs.append()  # Need to figure out how to implement this
        elif user_choice == '❌':
            bot.reg_pairs.remove()  # Need to figure out how to implement this
        else:
            await channel.send("Something else happened with emojis")

        msg_embed.set_field_at(1, name="Your Status", value=user_choice, inline=False)
        msg_embed.set_footer(text=f"Last Updated: {datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')}")

        await message.edit(embed=msg_embed)

    
@bot.command()
async def join(ctx, player1: discord.Member= None, player2= None):
    """Join as a mixed dubs pair with a partner"""
    if not player1 or not player2:
        await ctx.send(f"Missing Player Names: Use **!join <Player1> <Player2>**")
        return
    
    try:
        p1 = bot.get_user(player1.id)
        # p2 = bot.get_user(player2.id)
    except AttributeError:
        ctx.send(f"Don't forget to @ Players! Try again!")
        return
    
    embed = discord.Embed(
        title=(f"🎾 Mixed Doubles Confirmation")
        , description=(f"\n**{ctx.author}** registered you!")
        , color=discord.Color.green()
    )
    embed.add_field(
        name=f"Can you make {NEXT_SESS.strftime('%a')}, {NEXT_SESS.strftime('%m/%d/%Y')} @ {START_TIME}?"
        , value=(
            "✅ = Yes"
            "\n❌ = No"
        )
        , inline=False
    )
    embed.add_field(name="Your Status", value="Pending...", inline=False)

    if p1 != ctx.author:
        await p1.send(f"You and {player2} registered for Mixed Doubles. Awaiting confirmation from {player2}")
    else:
        try:
            sent_confirmation = await p1.send(embed=embed)
            await sent_confirmation.add_reaction('✅')
            await sent_confirmation.add_reaction('❌')
        except discord.Forbidden:
            await ctx.send("DM could not be sent!")
    # TODO:
    # Single Vote Enforcement to avoid multiple reactions
    
    # pair = (player1, player2)

    # # Avoid duplicates
    # if pair not in bot.reg_pairs and (pair[::-1]) not in bot.reg_pairs:
    #     bot.reg_pairs.append(pair)
    #     embed = discord.Embed(

    #     )
    #     await ctx.send(
    #         f"### Registered Team for {NEXT_SESS.strftime('%a')}, {NEXT_SESS.strftime('%m/%d/%Y')}:"
    #         f"\n{player1} & {player2}"
    #         )
    # else:
    #     await ctx.send("This team is already registered!")


@bot.command()
async def cancel(ctx, player1=None, player2=None):
    if not player1 or not player2:
        await ctx.send(f"Missing Player Names: Use **!cancel <Player1> <Player2>**")
        return

    to_cancel_pair = (player1, player2)

    if to_cancel_pair in bot.reg_pairs or to_cancel_pair[::-1] in bot.reg_pairs:
        bot.reg_pairs.remove(to_cancel_pair)
        await ctx.send(
            f"### Canceled {NEXT_SESS.strftime('%a')}, {NEXT_SESS.strftime('%m/%d/%Y')} Registration for:"
            f"\n{player1} & {player2}"
            )
    else:
        await ctx.send(f"Team: {player1} & {player2} are **not** on the registration list")


@bot.command()
async def pick(ctx):
    """Initiates the selections for the week"""
    # Load or init attendance data
    try:
        with open(DATA_FILE, 'r') as f:
            attendance = json.load(f)
    except FileNotFoundError:
        attendance = {}

    if len(bot.reg_pairs) < MIN_TEAMS:
        embed = discord.Embed(
            title="🚫 Mixed Doubles CANCELLED"
            , description=f"{NEXT_SESS.strftime('%a')}, {NEXT_SESS.strftime('%m/%d/%Y')} @ {START_TIME}"
            , color=discord.Color.green()
        )
    
    else:
        if len(bot.reg_pairs) < CAPACITY:
            chosen_pairs = pick_pairs(bot.reg_pairs, attendance, len(bot.reg_pairs))
        else:
            chosen_pairs = pick_pairs(bot.reg_pairs, attendance, CAPACITY)

        embed = discord.Embed(
            title="🎾 Mixed Doubles"
            , description=f"{NEXT_SESS.strftime('%a')}, {NEXT_SESS.strftime('%m/%d/%Y')} @ {START_TIME}"
            , color=discord.Color.green()
        )

        for i, (p1, p2) in enumerate(chosen_pairs, start=1):
            embed.add_field(name=f"Team {i}: ", value=f"{p1} & {p2}", inline=False)

        with open(DATA_FILE, 'w') as f:
            json.dump(attendance, f)

    await ctx.send(embed=embed)

    bot.reg_pairs = []


bot.run(TOKEN)