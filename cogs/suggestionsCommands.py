import discord, datetime
from discord import app_commands
from discord.ext import commands

class SuggestionModal(discord.ui.Modal, title="Suggestion Form"):
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

    explanation = discord.ui.TextInput(
        label="Explanation of Suggestion",
        style=discord.TextStyle.long,
        placeholder="Explanation Here...",
        required=True,
        min_length=100,
        max_length=1000
    )

    description = discord.ui.TextInput(
        label="Why should your suggestion be added?",
        style=discord.TextStyle.long,
        placeholder="Suggestion Description Here...",
        required=True,
        min_length=50,
        max_length=500
    )

    links_1 = discord.ui.TextInput(
        label="1st link to media",
        style=discord.TextStyle.short,
        placeholder="Insert Link Here...",
        required=False,
        min_length=0,
        max_length=100
    )

    links_2 = discord.ui.TextInput(
        label="2nd link to media",
        style=discord.TextStyle.short,
        placeholder="Insert Link Here...",
        required=False,
        min_length=0,
        max_length=100
    )

    async def on_submit(
        self, 
        interaction: discord.Interaction
        ):

            if interaction.guild.id == 350068992045744141: 
                suggestion_channel = interaction.guild.get_channel(351057661925654528)
                server_name = "The Conquerors 3"
            else:
                suggestion_channel = interaction.guild.get_channel(724424911791325214)
                server_name = "The Conquerors Games"

            suggestion_embed = discord.Embed(
                title=f"{self.name.value}",
                description=f"**Explanation of Suggestion**\n{self.explanation.value}\n\n**Why should your suggestion be added?**\n{self.description.value}\n\n**Links**\n{self.links_1.value}\n{self.links_2.value}",
                color=0xff0000
                )
            
            suggestion_embed.set_author(
                name=f"Suggested by: {interaction.user.display_name}", 
                icon_url=interaction.user.display_avatar.url)
            
            suggestion_embed.timestamp = interaction.created_at

            if len(self.links_1.value) == 0:
                suggestion_embed.set_image(
                    url=self.links_2.value
                )
            else:
                suggestion_embed.set_image(
                    url=self.links_1.value
                )

            suggestion_embed.add_field(
                name="**Votes**",
                value=f"Upvotes: 0 ``0%``\nDownvotes: 0 ``0%``",
                inline=False
            )
        
            suggestion_embed.set_footer(
                text=f"{server_name} Suggestions",
                icon_url=interaction.guild.icon
            )

            suggestion_embed.set_thumbnail(
                url=interaction.user.avatar.url
            )

            msg = await suggestion_channel.send(embed=suggestion_embed)

            await msg.create_thread(name=f"{self.name.value}")

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
        
class SuggestionCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def bots_channels(interaction):
        return interaction.channel.id == 941567353672589322 or interaction.channel.id == 351057167706619914

    is_bots = app_commands.check(bots_channels)

    @is_bots
    @app_commands.guilds(350068992045744141)
    @app_commands.command(
        name="suggest",
        description="A Command that allows you to suggest concepts!")
    async def suggest(
        self,
        interaction:discord.Interaction
    ):
        await interaction.response.send_modal(SuggestionModal())


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        
        TC3 = self.bot.get_guild(350068992045744141)
        suggestion_channel = discord.utils.get(TC3.channels, id=351057661925654528)

        tc3_bot = self.bot.get_user(953017055236456448)
        if payload.user_id != tc3_bot.id:
            if payload.channel_id == suggestion_channel.id:
                suggestion_message = await suggestion_channel.fetch_message(payload.message_id)
                if suggestion_message.author.id == tc3_bot.id: 
                    for reaction in suggestion_message.reactions:
                        if str(reaction.emoji) == '👍':
                            user_upvote_list = [user async for user in reaction.users()]
                        
                        elif str(reaction.emoji) == '👎': 
                            user_downvote_list = [user async for user in reaction.users()]
                    user_upvote_list, user_downvote_list = list(set(user_upvote_list).difference(user_downvote_list)), list(set(user_downvote_list).difference(user_upvote_list))

                    total_thumbs_up = len(user_upvote_list)
                    total_thumbs_down = len(user_downvote_list)
                    total_reactions = total_thumbs_up + total_thumbs_down
                    try:
                        total_upvote_percentage = round((total_thumbs_up / total_reactions) * 100, 2)
                        total_downvote_percentage = round(((total_thumbs_down / total_reactions) * 100), 2)
                    except ZeroDivisionError:
                        return 0
                    
                    suggestion_embed = suggestion_message.embeds[0].to_dict()
                    footer_dictionary = dict(suggestion_embed["footer"])
                    thumbnail_dictionary = dict(suggestion_embed["thumbnail"])
                    author_dictionary = dict(suggestion_embed["author"])
                    timestamp_dictionary = suggestion_embed["timestamp"]

                    new_suggestion_embed = discord.Embed(title=suggestion_embed["title"], colour=suggestion_embed["color"], timestamp=datetime.datetime.utcnow())

                    try:
                        image_dictionary = dict(suggestion_embed["image"])                
                        new_suggestion_embed.set_image(url=image_dictionary["url"])
                    except:
                        pass
                    
                    new_suggestion_embed.description = (f"{suggestion_embed['description']}")
                    new_suggestion_embed.add_field(name="**Votes**", value=f"Upvotes: {total_thumbs_up} ``{total_upvote_percentage}%``\nDownvotes: {total_thumbs_down} ``{total_downvote_percentage}%``")
                    # new_suggestion_embed.set_author(name="TheM1ndGamer | HMS", icon_url="https://images-ext-2.discordapp.net/external/H66Y2mHl-1Ui4ReJRH1wruRy5ZrKUah1KTaF4JWGMUc/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/621516858205405197/e34d486c4b1e10ed2df889085eb631be.png?width=473&height=473")
                    new_suggestion_embed.set_author(name=author_dictionary["name"], icon_url=author_dictionary["icon_url"])
                    new_suggestion_embed.set_thumbnail(url=thumbnail_dictionary["url"])
                    new_suggestion_embed.set_footer(text=footer_dictionary["text"], icon_url=footer_dictionary["icon_url"])
                    await suggestion_message.edit(embed=new_suggestion_embed)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        
        TC3 = self.bot.get_guild(350068992045744141)
        suggestion_channel = discord.utils.get(TC3.channels, id=351057661925654528)

        tc3_bot = self.bot.get_user(953017055236456448)
        if payload.user_id != tc3_bot.id:
            if payload.channel_id == suggestion_channel.id:
                suggestion_message = await suggestion_channel.fetch_message(payload.message_id)
                if suggestion_message.author.id == tc3_bot.id: 
                    for reaction in suggestion_message.reactions:
                        if str(reaction.emoji) == '👍':
                            user_upvote_list = [user async for user in reaction.users()]
                        
                        elif str(reaction.emoji) == '👎': 
                            user_downvote_list = [user async for user in reaction.users()]
                    user_upvote_list, user_downvote_list = list(set(user_upvote_list).difference(user_downvote_list)), list(set(user_downvote_list).difference(user_upvote_list))

                    total_thumbs_up = len(user_upvote_list)
                    total_thumbs_down = len(user_downvote_list)
                    total_reactions = total_thumbs_up + total_thumbs_down

                    try:
                        total_upvote_percentage = round((total_thumbs_up / total_reactions) * 100, 2)
                        total_downvote_percentage = round(((total_thumbs_down / total_reactions) * 100), 2)
                    except ZeroDivisionError:
                        return 0            
                    
                    suggestion_embed = suggestion_message.embeds[0].to_dict()
                    footer_dictionary = dict(suggestion_embed["footer"])
                    thumbnail_dictionary = dict(suggestion_embed["thumbnail"])
                    author_dictionary = dict(suggestion_embed["author"])
                    timestamp_dictionary = suggestion_embed["timestamp"]

                    new_suggestion_embed = discord.Embed(title=suggestion_embed["title"], colour=suggestion_embed["color"], timestamp=datetime.datetime.utcnow())

                    try:
                        image_dictionary = dict(suggestion_embed["image"])                
                        new_suggestion_embed.set_image(url=image_dictionary["url"])
                    except:
                        pass
                    new_suggestion_embed.description = (f"{suggestion_embed['description']}")
                    new_suggestion_embed.add_field(name="**Votes**", value=f"Upvotes: {total_thumbs_up} ``{total_upvote_percentage}%``\nDownvotes: {total_thumbs_down} ``{total_downvote_percentage}%``")
                    # new_suggestion_embed.set_author(name="TheM1ndGamer | HMS", icon_url="https://images-ext-2.discordapp.net/external/H66Y2mHl-1Ui4ReJRH1wruRy5ZrKUah1KTaF4JWGMUc/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/621516858205405197/e34d486c4b1e10ed2df889085eb631be.png?width=473&height=473")
                    new_suggestion_embed.set_author(name=author_dictionary["name"], icon_url=author_dictionary["icon_url"])
                    new_suggestion_embed.set_thumbnail(url=thumbnail_dictionary["url"])
                    new_suggestion_embed.set_footer(text=footer_dictionary["text"], icon_url=footer_dictionary["icon_url"])
                    await suggestion_message.edit(embed=new_suggestion_embed)

async def setup(bot):
    await bot.add_cog(SuggestionCommands(bot))
