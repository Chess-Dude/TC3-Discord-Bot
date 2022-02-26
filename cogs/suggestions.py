import discord, datetime

from discord.ext import commands

def TC3Bots(ctx):
    return ctx.channel.id == 351057167706619914

isTC3Bots = commands.check(TC3Bots)

def TCGBots(ctx):
    return ctx.channel.id == 408820459279220736

isTCGBots = commands.check(TCGBots)


class Suggestions(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
    
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

    @isTCGBots
    @commands.command()
    async def tcgsuggest(self, ctx, *, args):

        suggestions = discord.utils.get(ctx.guild.channels, id = 724424911791325214)
        
        suggestionEmbed = discord.Embed(title = f"The Conquering Games Suggestions",description=f"**Suggestion**\n{args}\n\n**Suggested by**\n{ctx.author.mention}", color=0xff0000)
        suggestionEmbed.timestamp = datetime.datetime.utcnow()
        
        if ctx.message.attachments:
            suggestionEmbed.set_image(url = ctx.message.attachments[0].proxy_url)

        msg = await suggestions.send(embed = suggestionEmbed)

        thumbsUp = '\U0001F44D'
        thumbsDown = '\U0001f44e'

        await msg.add_reaction(thumbsUp)
        await msg.add_reaction(thumbsDown)

        successEmbed=discord.Embed(title="Suggestion Accepted", description=f"{ctx.author.mention} Thanks for submitting your suggestion!", color=0xff0000)
        await ctx.message.reply(embed = successEmbed, mention_author = False)
    

def setup(bot):
    bot.add_cog(Suggestions(bot))
