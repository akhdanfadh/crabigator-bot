import discord
from discord import Cog, Embed, ui
from discord import ApplicationContext, Option, OptionChoice

from lib.utils import checks
from lib.utils.constants import ITEM_TYPE, EMBED_COLOR
from lib.handlers.wk_item import find_item


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
            str,
            name='name',
            description='The meaning or characters (not reading) of the item (e.g. "大" or "big").',
            required=True
        ),
        item_type: Option(
            str,
            name='item_type',
            description="Type of the item (radical, kanji, or vocab).",
            required=False,
            choices=[OptionChoice(value=key, name=value)
                    for key, value in ITEM_TYPE.items()]
        ),
    ):
        # Find the corresponding item
        if item_type == None:
            for found_type in ITEM_TYPE.keys():
                item = find_item(name, self.bot.item_data[found_type])
                if item != None:
                    item_type = found_type
                    break
        else:
            item = find_item(name, self.bot.item_data[item_type])

        # Bot response
        if item == None:
            await ctx.respond(f"Sorry, the requested item ({name}) could not be found! Try specifying the item type.")
        else:
            meanings = ', '.join(item['meanings'])
            embed = Embed(
                title=f"**{item['char'] if item['char'] != None else meanings}**",
                description=f"A level {item['level']} **{ITEM_TYPE[item_type]}**",
                color=EMBED_COLOR[item_type]
            )
            embed.set_footer(text=f"Requested by {ctx.author}")
            embed.add_field(
                name="Meaning(s):",
                value=meanings,
                inline=True
            )
            if item_type == 'kan':
                readings = []
                for reading_type, reading in item['readings'].items():
                    if reading is None: continue
                    reading_text = f"{reading_type.capitalize()}: {', '.join(reading)}"
                    readings.append(reading_text)
                embed.add_field(
                    name="Reading(s):",
                    value='\n'.join(readings),
                    inline=True
                )
            elif item_type == 'voc':
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
            if item_type == 'kan' or item_type == 'voc':
                embed.add_field(
                    name="Reading mnemonic:",
                    value=f"{item['reading_mnemonic']}",
                    inline=False
                )
            if item_type =='rad':
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
