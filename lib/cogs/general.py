import discord
from discord import Cog, Embed, ui

from lib.utils import checks


class General(Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name="abot",
        description="Get some useful (or not) information about the bot.",
    )
    @checks.not_blacklisted()
    async def abot(self, ctx):
        embed = Embed(
            title="Holy Crabigator Bot Information",
            description="Python-based discord bot developed for WaniKani visual mnemonic project.",
            color=0xe377c2  # tab:pink matplotlib
        )
        embed.set_thumbnail(
            url="https://wk-mnemonic-images.b-cdn.net/bot_icon.png")
        embed.set_footer(
            text="Use / (slash) for command")
        embed.add_field(
            name="Owner:",
            value="[akhdanfadh#4717](https://discord.com/users/590328553481175080)",
            inline=True
        )
        embed.add_field(
            name="Developer:",
            value=f"[mhh#3346](https://discord.com/users/363705186650423300)\n"
            "[Chiara#9001](https://discord.com/users/319878959649259533)\n",
            inline=True
        )
        embed.add_field(
            name="Bot Version:",
            value=f"{self.bot.version}",
            inline=True
        )

        view = ui.View()
        view.add_item(ui.Button(
            label='GitHub',
            url='https://github.com/akhdanfadh/crabigator-bot',
            row=0
        ))
        view.add_item(ui.Button(
            label='WaniKani Script',
            url='https://greasyfork.org/en/scripts/448713-wanikani-ai-mnemonic-images',
            row=0
        ))

        await ctx.send_response(embed=embed, view=view)

    @discord.slash_command(
        name="wani",
        description="Check if the bot is alive.",
    )
    @checks.not_blacklisted()
    async def wani(self, ctx):
        embed = Embed(
            title="🦀 Kani!",
            description=f"The bot latency is {round(self.bot.latency * 1000)}ms.",
            color=0xe377c2  # tab:pink matplotlib
        )
        await ctx.send_response(embed=embed)


def setup(bot):
    bot.add_cog(General(bot))
