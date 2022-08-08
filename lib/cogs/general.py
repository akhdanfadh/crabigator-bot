from disnake import ApplicationCommandInteraction
from disnake import Embed, File, ui
from disnake.ext import commands

from lib.utils import checks


class General(commands.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="botinfo",
        description="Get some useful (or not) information about the bot.",
    )
    @checks.not_blacklisted()
    async def botinfo(self, interaction: ApplicationCommandInteraction) -> None:
        embed = Embed(
            title="Holy Crabigator Bot Information",
            description="Python-based discord bot developed for WaniKani visual mnemonic project.",
            color=0xFF0000
        )
        embed.set_thumbnail(file=File("./data/images/bot_icon.png"))
        embed.add_field(
            name="Owner:",
            value="[akhdanfadh#4717](https://discord.com/users/590328553481175080)",
            inline=True
        )
        embed.add_field(
            name="Developer:",
            value=f"[mhh#3346](https://discord.com/users/363705186650423300)\n"
            "[Chiara#9001](https://discord.com/users/319878959649259533)\n",
            inline=False
        )
        embed.add_field(
            name="Bot Version:",
            value=f"{self.bot.config['bot_version']}",
            inline=True
        )
        embed.add_field(
            name="Prefix:",
            value=f"/ (Slash Commands) or {self.bot.config['prefix']}",
            inline=False)

        view = ui.View()
        view.add_item(ui.Button(
            label='GitHub',
            url='https://github.com/saraqael-m/CrabigatorBot',
            row=0
        ))
        view.add_item(ui.Button(
            label='WaniKani Script',
            url='https://greasyfork.org/en/scripts/448713-wanikani-ai-mnemonic-images',
            row=0
        ))

        await interaction.send(embed=embed, view=view)

    @commands.slash_command(
        name="wani",
        description="Check if the bot is alive.",
    )
    @checks.not_blacklisted()
    async def ping(self, interaction: ApplicationCommandInteraction) -> None:
        embed = Embed(
            title="🦀 Kani!",
            description=f"The bot latency is {round(self.bot.latency * 1000)}ms.",
            color=0xFF0000
        )
        await interaction.send(embed=embed)


def setup(bot):
    bot.add_cog(General(bot))
