import os
import sys
import json
import platform
import random

import disnake
from disnake.ext.commands import Bot
from disnake.ext import tasks, commands
from disnake import ApplicationCommandInteraction

import lib.exceptions as exceptions


# Load configuration and system files
if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)


# Setup Discord bot intents and initialize client
intents = disnake.Intents.default()
intents.message_content = True
bot = Bot(
    command_prefix=commands.when_mentioned_or(config["bot_prefix"]),
    intents=intents, help_command=None
)
bot.config = config


@bot.event
async def on_ready() -> None:
    """Called when the connection to Discord has been established."""
    print(f"Logged in as '{bot.user}' v{config['bot_version']}")
    print(f"disnake API version: {disnake.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")
    bot_presence.start()


@tasks.loop(minutes=10.0)
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
    await bot.change_presence(activity=disnake.Game(random.choice(statuses)))


# Loading bot cogs
if __name__ == "__main__":
    print("Crabigator is running setup...")
    for file in os.listdir(f"./lib/cogs"):
        if file.endswith(".py"):
            cog = file[:-3]
            try:
                bot.load_extension(f"lib.cogs.{cog}")
                print(f"- {cog} cog loaded")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"! {cog} cog failed to load:\n  {exception}")
    print("Setup complete\n")


@bot.event
async def on_message(message: disnake.Message) -> None:
    """Triggered every time someone sends a message."""
    if message.author == bot.user or message.author.bot:
        return
    await bot.process_commands(message)


@bot.event
async def on_slash_command(interaction: ApplicationCommandInteraction) -> None:
    """Executed every time a slash command has been *successfully* executed."""
    message = (
        f"Executed {interaction.data.name} command in "
        f"{interaction.guild.name} (ID: {interaction.guild.id}) by "
        f"{interaction.author} (ID: {interaction.author.id})"
    )
    print(message)


@bot.event
async def on_slash_command_error(interaction: ApplicationCommandInteraction, error: Exception) -> None:
    """Executed every time a valid slash command catches an error.

    'ephemeral=True' will make so that only the user who execute the command can see the message.
    """
    if isinstance(error, commands.CommandOnCooldown):
        minutes, seconds = divmod(error.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        message = (
            f"You can use this command again in "
            f"{f'{round(hours)} hours' if round(hours) > 0 else ''} "
            f"{f'{round(minutes)} minutes' if round(minutes) > 0 else ''} "
            f"{f'{round(seconds)} seconds' if round(seconds) > 0 else ''}."
        )
        embed = disnake.Embed(
            title="Hey, please slow down!",
            description=message,
            color=0xE02B2B
        )
        return await interaction.send(embed=embed, ephemeral=True)
    elif isinstance(error, exceptions.UserBlacklisted):
        embed = disnake.Embed(
            title="Error!",
            description="You are blacklisted from using the bot.",
            color=0xE02B2B
        )
        return await interaction.send(embed=embed, ephemeral=True)
    elif isinstance(error, exceptions.UserNotDeveloper):
        embed = disnake.Embed(
            title="Error!",
            description="You are not the developer of the bot!",
            color=0xE02B2B
        )
        return await interaction.send(embed=embed, ephemeral=True)
    elif isinstance(error, commands.MissingPermissions):
        embed = disnake.Embed(
            title="Error!",
            description="You are missing the permission(s) `" + ", ".join(
                error.missing_permissions) + "` to execute this command!",
            color=0xE02B2B
        )
        return await interaction.send(embed=embed, ephemeral=True)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = disnake.Embed(
            title="Error!",
            # Command arguments have no capital letter in the code.
            description=str(error).capitalize(),
            color=0xE02B2B
        )
        await interaction.send(embed=embed, ephemeral=True)
    raise error


# Finally run the bot
bot.run(config["bot_token"])
