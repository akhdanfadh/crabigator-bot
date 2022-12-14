import os
import sys
import json
import platform
import random

import discord
from discord import Intents, Bot, Embed
from discord.ext import tasks, commands

import lib.exceptions as exceptions
from lib.handlers.wk_item import load_item_db, load_item_db


VERSION = '0.2.3'
UPDATE_WK_ITEMS = False


# Load configuration and system files
if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)


# Setup Discord bot intents and initialize client
intents = Intents.default()
intents.message_content = True
bot = Bot(
    intents=intents,
    debug_guilds=[int(config["guild_id"])]
)
bot.config = config
bot.version = VERSION


@bot.event
async def on_ready() -> None:
    """Called when the connection to Discord has been established."""
    print("\n-------------------")
    print(f"Logged in as '{bot.user}' v{bot.version}")
    print(f"PyCord API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------\n")
    bot_presence.start()

    embed = Embed(
        description="I'm online! 🤟🏼",
        color=0x2ca02c  # tab:green matplotlib
    )
    channel_announce_id = int(config["channel_ids"]["announce"])
    await bot.get_channel(channel_announce_id).send(embed=embed)


@tasks.loop(minutes=1.0)
async def bot_presence() -> None:
    """Bot discord presence status updated every minute."""
    statuses = [
        "Learning ALL the Kanji!",
        "Doing my reviews.",
        "WaniKani Simulator.",
        "Crabigator Dance Party!",
        "Simulating Weeb-speak.",
        "Writing a WaniKani anime.",
        "Using ALL the vocab!",
        "Inventing new mnemonics.",
        "Sleeping on the job...",
        "On a crabigator date.",
        "Yell 助けて for help!",
    ]
    await bot.change_presence(activity=discord.Game(random.choice(statuses)))


@bot.event
async def on_application_command(ctx) -> None:
    """Executed every time a slash command has been successfully executed."""
    message = (
        f"Executed '/{ctx.command.name}' command in "
        f"{ctx.guild.name} (ID: {ctx.guild.id}) by "
        f"{ctx.author} (ID: {ctx.author.id})"
    )
    print(message)


@bot.event
async def on_application_command_error(ctx, exception) -> None:
    """Executed every time a valid slash command catches an error."""
    if isinstance(exception, commands.CommandOnCooldown):
        minutes, seconds = divmod(exception.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        message = (
            f"You can use this command again in "
            f"{f'{round(hours)} hours' if round(hours) > 0 else ''} "
            f"{f'{round(minutes)} minutes' if round(minutes) > 0 else ''} "
            f"{f'{round(seconds)} seconds' if round(seconds) > 0 else ''}."
        )
        embed = Embed(
            title="Hey, please slow down!",
            description=message,
            color=0xFF0000
        )
        return await ctx.send(embed=embed, ephemeral=True)
    elif isinstance(exception, exceptions.UserBlacklisted):
        embed = Embed(
            title="Error!",
            description="You are blacklisted from using the bot.",
            color=0xFF0000
        )
        return await ctx.send(embed=embed, ephemeral=True)
    elif isinstance(exception, exceptions.UserNotDeveloper):
        embed = Embed(
            title="Error!",
            description="You are not the developer of the bot!",
            color=0xFF0000
        )
        return await ctx.send(embed=embed, ephemeral=True)
    elif isinstance(exception, commands.MissingPermissions):
        embed = Embed(
            title="Error!",
            description="You are missing the permission(s) `" + ", ".join(
                exception.missing_permissions) + "` to execute this command!",
            color=0xFF0000
        )
        return await ctx.send(embed=embed, ephemeral=True)
    elif isinstance(exception, commands.MissingRequiredArgument):
        embed = Embed(
            title="Error!",
            # Command arguments have no capital letter in the code.
            description=str(exception).capitalize(),
            color=0xFF0000
        )
        await ctx.send(embed=embed, ephemeral=True)
    raise exception


if __name__ == "__main__":
    # Loading bot cogs
    print("\nLoading Crabigator cogs:")
    for file in os.listdir("lib/cogs"):
        if file.endswith(".py"):
            cog = file[:-3]
            try:
                bot.load_extension(f"lib.cogs.{cog}")
                print(f"- {cog} cog loaded")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"! {cog} cog failed to load:\n  {exception}")
    print("Finished loading the cogs.")

    # Loading WaniKani items
    print("\nLoading WaniKani items:")
    bot.item_data = {}
    load_item_db(config["wk_token"], bot.item_data, UPDATE_WK_ITEMS)
    print("Finished loading all items.")


# Finally run the bot
bot.run(config["bot_token"])