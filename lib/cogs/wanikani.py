import discord
from discord import Cog, Embed, ui
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
            description='The meaning or characters (not reading) of the item (e.g. "大" or "big").',
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
            await ctx.respond(f"Sorry, but the requested item ({name}) could not be found! Try specifying the item type.")
        else:
            colors = {'rad': 0x00AAFF, 'kan': 0xFF00AA, 'voc': 0xAA00FF}
            meanings = ', '.join(item['meanings'])
            embed = Embed(
                title=f"> **{item['char'] if item['char'] != None else meanings}**",
                description=f"A level {item['level']} **{self.bot.item_names[type]}**",
                color=colors[type]
            )
            embed.set_footer(text=f"Requested by {ctx.author}")
            embed.add_field(
                name="Meaning(s):",
                value=meanings,
                inline=True
            )
            if type == 'kan':
                readings = ""
                for reading_type, reading in item['readings'].items():
                    if reading is None: continue
                    unpack = ', '.join(reading)
                    if readings == "":
                        readings += f"{reading_type.capitalize()}: {unpack}"
                    else:
                        readings += f", {reading_type.capitalize()}: {unpack}"
                embed.add_field(
                    name="Reading(s):",
                    value=readings,
                    inline=True
                )
            elif type == 'voc':
                embed.add_field(
                    name="Reading(s):",
                    value=', '.join(item['readings']),
                    inline=True
                )
            embed.add_field(
                name="Meaning mnemonic:",
                value=f"{item['meaning_mnemonic']}",
                inline=False
            )
            if type == 'kan' or type == 'voc':
                embed.add_field(
                    name="Reading mnemonic:",
                    value=f"{item['reading_mnemonic']}",
                    inline=False
                )
            if type =='rad':
                embed.set_thumbnail(url=f"{item['char_image']}")

            view = ui.View()
            view.add_item(ui.Button(
                label='Details',
                url=f"{item['url']}",
                row=0
            ))
            
            await ctx.send_response(embed=embed, view=view)


def setup(bot):
    bot.add_cog(Wanikani(bot))
