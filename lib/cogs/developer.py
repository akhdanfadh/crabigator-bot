from typing import Literal

from disnake import ApplicationCommandInteraction
from disnake import Embed
from disnake.ext import commands

from lib.utils import checks


class Developer(commands.Cog, name="developer"):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="shutdown",
        description="Make the bot shutdown.",
    )
    @checks.is_developer()
    async def shutdown(self, interaction: ApplicationCommandInteraction) -> None:
        embed = Embed(
            description="Shutting down. Bye! 👋🏼",
            color=0xFF0000
        )

        channel_announce_id = int(self.bot.config["channel_ids"]["announce"])
        print(channel_announce_id)
        await interaction.send("Got it! Going to #announcement channel.")
        await interaction.guild.get_channel(channel_announce_id).send(embed=embed)
        await self.bot.close()


def setup(bot):
    bot.add_cog(Developer(bot))
