import json
from typing import TypeVar, Callable

from disnake.ext import commands

from lib.exceptions import *

T = TypeVar("T")


def is_developer() -> Callable[[T], T]:
    """Check if the user executing the command is a developer of the bot."""
    async def predicate(context: commands.Context) -> bool:
        with open("config.json") as file:
            data = json.load(file)
        if context.author.id not in data["developer_ids"]:
            raise UserNotDeveloper
        return True
    return commands.check(predicate)


def not_blacklisted() -> Callable[[T], T]:
    """Check if the user executing the command is blacklisted."""
    async def predicate(context: commands.Context) -> bool:
        with open("data/users/blacklisted.json") as file:
            data = json.load(file)
        if context.author.id in data["ids"]:
            raise UserBlacklisted
        return True
    return commands.check(predicate)
