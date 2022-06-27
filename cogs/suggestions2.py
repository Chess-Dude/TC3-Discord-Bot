import discord, datetime
from discord import app_commands
from discord.ext import commands

class SuggestionModal(discord.ui.Modal, title="Server Suggestion Form"):
    # Our modal classes MUST subclass `discord.ui.Modal`,
    # but the title can be whatever you want.

    # This is a longer, paragraph style input, where user can submit feedback
    # Unlike the name, it is not required. If filled out, however, it will
    # only accept a maximum of 300 characters, as denoted by the
    # `max_length=300` kwarg.
    name = discord.ui.TextInput(
        label="What is your suggestion?",
        style=discord.TextStyle.short,
        placeholder="Suggestion Title Here...",
        required=True,
        min_length=10,
        max_length=50
    )

    description = discord.ui.TextInput(
        label="Why should your suggestion be added?",
        style=discord.TextStyle.long,
        placeholder="Suggestion Description Here...",
        required=True,
        min_length=100,
        max_length=500
    )
    async def on_submit(
        self, 
        interaction: discord.Interaction
        ):

            suggestion_channel = interaction.guild.get_channel(724424911791325214)
            
            suggestion_embed = discord.Embed(
                title=f"{self.name.value}",
                description=f"{self.description.value}",
                color=0xff0000
                )
            
            suggestion_embed.set_author(
                name=f"Suggested by: {interaction.user.display_name}", 
                icon_url=interaction.user.display_avatar.url)
            suggestion_embed.timestamp = interaction.created_at

            suggestion_embed.add_field(
                name="**Votes**",
                value=f"Upvotes: 0 ``0%``\nDownvotes: 0 ``0%``",
                inline=False
            )

            msg = await suggestion_channel.send(embed=suggestion_embed)

            thumbs_up = '\U0001F44D'
            thumbs_down = '\U0001f44e'

            await msg.add_reaction(thumbs_up)
            await msg.add_reaction(thumbs_down)

            success_embed=discord.Embed(
                title="Suggestion Accepted", 
                description=f"{interaction.user.mention} Thanks for submitting your suggestion!", 
                color=0xff0000
                )

            await interaction.response.send_message(embed=success_embed)
        
class SuggestionsUpdated(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def tcg_bots(interaction):
        return interaction.channel.id == 941567353672589322 or interaction.channel.id == 408820459279220736

    def tcg_suggestion_channel(interaction):
        return interaction.channel.id == 724424911791325214 or interaction.channel.id == 941567353672589322
    
    server_group = app_commands.Group(
        name="server", 
        description="A Command That Allows You To Submit A Server Suggestion!",
        guild_ids=[371817692199518240])
    
    @app_commands.check(tcg_bots)
    @server_group.command(
        name="suggest",
        description="A Command That Allows You To Make A Server Suggestion!")

    async def server_suggest(
        self,
        interaction: discord.Interaction,
        ):    
            await interaction.response.send_modal(SuggestionModal())
    
    # @commands.Cog.listener()
    # async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
    #     TCG = self.bot.get_guild(371817692199518240)
    #     suggestion_channel = discord.utils.get(TCG.channels, id=724424911791325214)
    #     tc3_bot = self.bot.get_user(953017055236456448)
    #     if payload.channel_id == suggestion_channel.id:
    #         suggestion_message = await suggestion_channel.fetch_message(payload.message_id)
    #         if suggestion_message.author.id == tc3_bot.id: 
    #             for reaction in suggestion_message.reactions:
    #                 if str(reaction.emoji) == '👍':
    #                     user_upvote_list = [user async for user in reaction.users()]
                    
    #                 elif str(reaction.emoji) == '👎': 
    #                     user_downvote_list = [user async for user in reaction.users()]
    #             user_upvote_list, user_downvote_list = list(set(user_upvote_list).difference(user_downvote_list)), list(set(user_downvote_list).difference(user_upvote_list))

    #             total_thumbs_up = len(user_upvote_list)
    #             total_thumbs_down = len(user_downvote_list)
    #             total_reactions = total_thumbs_up + total_thumbs_down
    #             try:
    #                 total_upvote_percentage = round((total_thumbs_up / total_reactions) * 100, 2)
    #                 total_downvote_percentage = round(((total_thumbs_down / total_reactions) * 100), 2)
    #             except ZeroDivisionError:
    #                 return 0
                
    #             suggestion_embed = suggestion_message.embeds[0].to_dict()
    #             author_dictionary = dict(suggestion_embed["author"])
    #             new_suggestion_embed = discord.Embed(title=suggestion_embed["title"], colour=suggestion_embed["color"], timestamp=datetime.datetime.utcnow())
            
    #             new_suggestion_embed.description = (f"{suggestion_embed['description']}")
    #             new_suggestion_embed.add_field(name="**Votes**", value=f"Upvotes: {total_thumbs_up} ``{total_upvote_percentage}%``\nDownvotes: {total_thumbs_down} ``{total_downvote_percentage}%``")
    #             # new_suggestion_embed.set_author(name="TheM1ndGamer | HMS", icon_url="https://images-ext-2.discordapp.net/external/H66Y2mHl-1Ui4ReJRH1wruRy5ZrKUah1KTaF4JWGMUc/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/621516858205405197/e34d486c4b1e10ed2df889085eb631be.png?width=473&height=473")
    #             new_suggestion_embed.set_author(name=author_dictionary["name"], icon_url=author_dictionary["icon_url"])
    #             await suggestion_message.edit(embed=new_suggestion_embed)

    # @commands.Cog.listener()
    # async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
    #     TCG = self.bot.get_guild(371817692199518240)
    #     suggestion_channel = discord.utils.get(TCG.channels, id=724424911791325214)
    #     tc3_bot = self.bot.get_user(953017055236456448)
    #     if payload.channel_id == suggestion_channel.id:
    #         suggestion_message = await suggestion_channel.fetch_message(payload.message_id)
    #         if suggestion_message.author.id == tc3_bot.id: 
    #             for reaction in suggestion_message.reactions:
    #                 if str(reaction.emoji) == '👍':
    #                     user_upvote_list = [user async for user in reaction.users()]
                    
    #                 elif str(reaction.emoji) == '👎': 
    #                     user_downvote_list = [user async for user in reaction.users()]
    #             user_upvote_list, user_downvote_list = list(set(user_upvote_list).difference(user_downvote_list)), list(set(user_downvote_list).difference(user_upvote_list))

    #             total_thumbs_up = len(user_upvote_list)
    #             total_thumbs_down = len(user_downvote_list)
    #             total_reactions = total_thumbs_up + total_thumbs_down

    #             try:
    #                 total_upvote_percentage = round((total_thumbs_up / total_reactions) * 100, 2)
    #                 total_downvote_percentage = round(((total_thumbs_down / total_reactions) * 100), 2)
    #             except ZeroDivisionError:
    #                 return 0            
                
    #             suggestion_embed = suggestion_message.embeds[0].to_dict()
    #             author_dictionary = dict(suggestion_embed["author"])
    #             new_suggestion_embed = discord.Embed(title=suggestion_embed["title"], colour=suggestion_embed["color"], timestamp=datetime.datetime.utcnow())
            
    #             new_suggestion_embed.description = (f"{suggestion_embed['description']}")
    #             new_suggestion_embed.add_field(name="**Votes**", value=f"Upvotes: {total_thumbs_up} ``{total_upvote_percentage}%``\nDownvotes: {total_thumbs_down} ``{total_downvote_percentage}%``")
    #             # new_suggestion_embed.set_author(name="TheM1ndGamer | HMS", icon_url="https://images-ext-2.discordapp.net/external/H66Y2mHl-1Ui4ReJRH1wruRy5ZrKUah1KTaF4JWGMUc/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/621516858205405197/e34d486c4b1e10ed2df889085eb631be.png?width=473&height=473")
    #             new_suggestion_embed.set_author(name=author_dictionary["name"], icon_url=author_dictionary["icon_url"])
    #             await suggestion_message.edit(embed=new_suggestion_embed)

async def setup(bot):
    await bot.add_cog(SuggestionsUpdated(bot))
