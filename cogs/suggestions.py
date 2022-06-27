import discord, datetime

from discord.ext import commands

class Suggestions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    def TC3Bots(ctx):
        return ctx.channel.id == 351057167706619914

    isTC3Bots = commands.check(TC3Bots)

    def tcg_bots(ctx):
        return ctx.channel.id == 408820459279220736

    def tcg_suggestion_channel(ctx):
        return ctx.channel.id == 724424911791325214 or ctx.channel.id == 941567353672589322

    is_tcg_bots = commands.check(tcg_bots)
    is_tcg_suggestion_channel = commands.check(tcg_suggestion_channel)
    
    """
    @isTC3Bots
    @commands.has_role(359803793891656023)
    @commands.command()
    async def dsuggest(self, ctx, *, args):

        discordSuggestions = discord.utils.get(ctx.guild.channels, id = 543955592088387584)
        
        suggestionEmbed = discord.Embed(title = f"The Conquerors 3 Discord Suggestion",description=f"**Suggestion**\n{args}\n\n**Suggested by**\n{ctx.author.mention}", color=0xff0000)
        suggestionEmbed.timestamp = datetime.datetime.utcnow()
                
        if ctx.message.attachments:
            suggestionEmbed.set_image(url = ctx.message.attachments[0].proxy_url)

        msg = await discordSuggestions.send(embed = suggestionEmbed)
        await globalFunctions.addVotes(msg)

        successEmbed=discord.Embed(title="Suggestion Accepted", description=f"{ctx.author.mention} Thanks for submitting your suggestion!", color=0xff0000)
        await ctx.message.reply(embed = successEmbed)
    """
    
    @is_tcg_bots
    @commands.command(aliases=["suggest"])
    async def tcgsuggest(self, ctx, *, args):

        suggestions = discord.utils.get(ctx.guild.channels, id = 724424911791325214)
        
        suggestionEmbed = discord.Embed(title = f"The Conquering Games Suggestions",description=f"**Suggestion**\n{args}\n", color=0xff0000)
        suggestionEmbed.set_author(name=f"Suggested by: {ctx.author.display_name}", icon_url=ctx.author.display_avatar.url)
        suggestionEmbed.timestamp = datetime.datetime.utcnow()
        
        if ctx.message.attachments:
            suggestionEmbed.set_image(url = ctx.message.attachments[0].proxy_url)

        msg = await suggestions.send(embed = suggestionEmbed)

        thumbsUp = '\U0001F44D'
        thumbsDown = '\U0001f44e'

        await msg.add_reaction(thumbsUp)
        await msg.add_reaction(thumbsDown)

        successEmbed=discord.Embed(title="Suggestion Accepted", description=f"{ctx.author.mention} Thanks for submitting your suggestion!", color=0xff0000)
        await ctx.message.reply(embed = successEmbed, mention_author = True)
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        TCG = self.bot.get_guild(371817692199518240)
        suggestion_channel = discord.utils.get(TCG.channels, id=724424911791325214)
        tc3_bot = self.bot.get_user(953017055236456448)
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
                author_dictionary = dict(suggestion_embed["author"])
                new_suggestion_embed = discord.Embed(title=suggestion_embed["title"], colour=suggestion_embed["color"], timestamp=datetime.datetime.utcnow())
            
                new_suggestion_embed.description = (f"{suggestion_embed['description']}")
                new_suggestion_embed.add_field(name="**Votes**", value=f"Upvotes: {total_thumbs_up} ``{total_upvote_percentage}%``\nDownvotes: {total_thumbs_down} ``{total_downvote_percentage}%``")
                # new_suggestion_embed.set_author(name="TheM1ndGamer | HMS", icon_url="https://images-ext-2.discordapp.net/external/H66Y2mHl-1Ui4ReJRH1wruRy5ZrKUah1KTaF4JWGMUc/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/621516858205405197/e34d486c4b1e10ed2df889085eb631be.png?width=473&height=473")
                new_suggestion_embed.set_author(name=author_dictionary["name"], icon_url=author_dictionary["icon_url"])
                await suggestion_message.edit(embed=new_suggestion_embed)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        TCG = self.bot.get_guild(371817692199518240)
        suggestion_channel = discord.utils.get(TCG.channels, id=724424911791325214)
        tc3_bot = self.bot.get_user(953017055236456448)
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
                author_dictionary = dict(suggestion_embed["author"])
                new_suggestion_embed = discord.Embed(title=suggestion_embed["title"], colour=suggestion_embed["color"], timestamp=datetime.datetime.utcnow())
            
                new_suggestion_embed.description = (f"{suggestion_embed['description']}")
                new_suggestion_embed.add_field(name="**Votes**", value=f"Upvotes: {total_thumbs_up} ``{total_upvote_percentage}%``\nDownvotes: {total_thumbs_down} ``{total_downvote_percentage}%``")
                # new_suggestion_embed.set_author(name="TheM1ndGamer | HMS", icon_url="https://images-ext-2.discordapp.net/external/H66Y2mHl-1Ui4ReJRH1wruRy5ZrKUah1KTaF4JWGMUc/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/621516858205405197/e34d486c4b1e10ed2df889085eb631be.png?width=473&height=473")
                new_suggestion_embed.set_author(name=author_dictionary["name"], icon_url=author_dictionary["icon_url"])
                await suggestion_message.edit(embed=new_suggestion_embed)

    @is_tcg_suggestion_channel
    @commands.command()
    async def respond(self, ctx, suggestion_id=None):
        TCG = self.bot.get_guild(371817692199518240)
        suggestion_channel = discord.utils.get(TCG.channels, id=724424911791325214)
        suggestion_embed = await suggestion_channel.fetch_message(suggestion_id)
        thumbs_up_reaction = discord.utils.get(suggestion_embed.reactions, emoji='✅')
        thumbs_down_reaction = discord.utils.get(suggestion_embed.reactions, emoji='❌')
        await ctx.send(f"Total Upvotes: {thumbs_up_reaction.count}.")
        await ctx.send(f"Total Downvotes: {thumbs_down_reaction.count}.")

async def setup(bot):
    await bot.add_cog(Suggestions(bot))
