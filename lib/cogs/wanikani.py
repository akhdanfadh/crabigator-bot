import discord
from discord import Cog, Embed
from discord import ApplicationContext, Option, OptionChoice

from lib.utils import checks
from lib.utils.manage_item import find_item


class Wanikani(Cog, name="wanikani"):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name="search",
        description="Get the detail of a specific WaniKani item.",
    )
    @checks.not_blacklisted()
    async def search(
        self, ctx: ApplicationContext,
        name: Option(
            input_type=str,
            name='name',
            description='Name of the item (e.g. "大 or "big").',
            required=True
        ),
        type: Option(
            input_type=str,
            name='type',
            description="Type of the item (radical, kanji, or vocab).",
            required=False,
            choices=[
                        OptionChoice(value='rad', name='Radical'),
                        OptionChoice(value='kan', name='Kanji'),
                        OptionChoice(value='voc', name='Vocabulary')
            ]
        )
    ):
        # Find the corresponding item
        item = None
        if type is None:
            for found_type in ['rad', 'kan', 'voc']:
                item = find_item(self.bot.item_data[found_type], name)
                if item != None:
                    type = found_type
                    break
        else:
            item = find_item(self.bot.item_data[type], name)

        # Bot response
        if item == None:
            await ctx.respond("Sorry, but the requested item could not be found! Try specifying the item type.")
        else:
            embed = Embed(
                title=f"**{item['char'] if item['char'] != None else item['meaning']}**",
                description=f"A Level {item['level']} **{self.bot.item_names[type]}**",
                color=0xe377c2  # tab:pink matplotlib
            )
            embed.set_footer(text=f"Requested by {ctx.author}")
            embed.add_field(
                name="Meaning:",
                value=f"{item['meaning']}",
                inline=True
            )
            embed.add_field(
                name="Meaning mnemonic:",
                value=f"{item['mnemonic']}",
                inline=False
            )
            if type == 'kan':
                embed.add_field(
                    name="Kanji hint:",
                    value=f"{item['hint']}",
                    inline=False
                )

            await ctx.send_response(embed=embed)


def setup(bot):
    bot.add_cog(Wanikani(bot))
