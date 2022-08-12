import discord
from discord import Cog, Embed
from discord import Attachment, User
from discord import ApplicationContext, Option, OptionChoice
from discord.commands import option

from lib.utils import checks
from lib.utils.constants import ITEM_TYPE, MNEMONIC_TYPE, LICENSE_TYPE, EMBED_COLOR
from lib.handlers.submission import verify_submission, add_submission


class Submission(Cog, name="submission"):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name="submit",
        description="Submit an AI visual mnemonic to the database.",
    )
    @checks.not_blacklisted()
    async def submit(
        self, ctx: ApplicationContext,
        char: Option(
            str,
            name='char',
            description='Characters of the item (e.g. "大", "大人"). Use the meaning for radical item (e.g. "barb").',
            required=True
        ),
        meaning: Option(
            str,
            name='meaning',
            description='Meaning of the item (e.g. "big", "adult", "barb").',
            required=True
        ),
        item_type: Option(
            str,
            name='item_type',
            description="Type of the item (radical, kanji, or vocab).",
            required=True,
            choices=[OptionChoice(value=key, name=value)
                    for key, value in ITEM_TYPE.items()]
        ),
        mnemonic_type: Option(
            str,
            name='mnemonic_type',
            description="What type of mnemonic this submission for (meaning, reading, or both)",
            required=True,
            choices=[OptionChoice(value=key, name=value)
                    for key, value in MNEMONIC_TYPE.items()]
        ),
        image: Option(
            Attachment,
            name='image',
            description='The generated image.',
            required=True
        ),
        license: Option(
            str,
            name='license',
            description='AI model used to generate the image (or other possible source).',
            required=True,
            choices=[OptionChoice(value=key, name=value)
                    for key, value in LICENSE_TYPE.items()]
        ),
        prompt: Option(
            str,
            name='prompt',
            description='The prompt that was inputted into the AI to generate the image.',
            required=True
        ),
        remarks: Option(
            str,
            name='remarks',
            description='(Optional) Other important details.',
            required=False
        ),
        author_dc: Option(
            User,
            name='author_dc',
            description='(Optional) Who prompted the image? This option is if the author is in this server.',
            required=False
        ),
        author_out: Option(
            str,
            name='author_out',
            description='(Optional) Same with author_dc, but ONLY if the author is not in this server.',
            required=False
        ),
    ):
        # find a matching item in item database for current submission
        match_item = verify_submission(char, meaning, item_type, self.bot.item_data[item_type])
        if match_item == None:
            error_embed = Embed(
                title=f"{ITEM_TYPE[item_type]} Submission - {char}",
                description='**Error:** Sorry, the submitted item could not be found in WaniKani database!',
                color=EMBED_COLOR['red']
            )
            await ctx.send_response(embed=error_embed)
        
        # execute submission
        else:
            new_submission, error_status = await add_submission(
                match_item, mnemonic_type, image.url, license, prompt, remarks,
                (ctx.user if author_out == None else author_out) if author_dc == None else author_dc
            )

            # return error embed if there was an error
            if error_status != None:
                error_embed = Embed(
                    title=f"{ITEM_TYPE[item_type]} Submission - {match_item['char']}",
                    color=EMBED_COLOR['red']
                )
                if error_status == 'SubmissionDatabaseError':
                    error_embed.description = '**Error:** Sorry, there was a database error!'
                else:
                    error_embed.description = '**Error:** Sorry, an unknown error occurred!'
                await ctx.send_response(embed=error_embed)
            
            # finalize submission output
            else:
                meanings = ', '.join(match_item['meanings'])
                submission_embed = Embed(
                    title=f"{ITEM_TYPE[item_type]} Submission - {match_item['char']}",
                    color=EMBED_COLOR['green']
                )
                submission_embed.set_image(url=new_submission["image_url"])
                submission_embed.add_field(
                    name="Description:",
                    value=f"**{MNEMONIC_TYPE[mnemonic_type]}** visual mnemonic for level {match_item['level']} {ITEM_TYPE[item_type].lower()} - **{match_item['char']}**"
                        f"Item meaning(s): {meanings}",
                    inline=True
                )
                submission_embed.add_field(
                    name="Image Generation:",
                    value=f"Generated with {LICENSE_TYPE[license]} using the prompt:"
                        f"{prompt}",
                    inline=False
                )
                submission_embed.add_field(
                    name="Remarks:",
                    value=f"{new_submission['remarks']}",
                    inline=False
                )
                submission_embed.set_footer(text=f"Submission ID: {new_submission['id']}. Image author: {new_submission['author'][1]}.")
                await ctx.send_response(embed=submission_embed)


def setup(bot):
    bot.add_cog(Submission(bot))
