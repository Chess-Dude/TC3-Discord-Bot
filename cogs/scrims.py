import discord
from discord.ext import commands

class Scrims(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
        
    def _1v1(ctx):
        return ctx.channel.id == 666961021096689694

    def _2v2(ctx):
        return ctx.channel.id == 666959897979781146

    def team(ctx):
        return ctx.channel.id == 666957650717835265
    
    def clanChat(ctx):
        return ctx.channel.id == 707220152625791047
    
    def matchmaking(ctx):
        return ctx.channel.id == 359467053284851712

    is1v1CheckIn = commands.check(_1v1)    
    is2v2CheckIn = commands.check(_2v2)
    isTeamCheckIn = commands.check(team)
    isClanChat = commands.check(clanChat)
    isMatchmaking = commands.check(matchmaking)

    @is1v1CheckIn
    @commands.has_role(896542577296306217)
    @commands.cooldown(1, 1800, commands.BucketType.guild)
    @commands.command(aliases = ["1v1scrim"])
    async def _1v1scrim(self, ctx):        
        await ctx.message.reply(content = f'{ctx.author.mention} wants to 1v1 <@&935635762987298836>!', mention_author = True)

    @is2v2CheckIn
    @commands.has_role(896550133309775872)
    @commands.cooldown(1, 1800, commands.BucketType.guild)
    @commands.command(aliases = ["2v2scrim"])
    async def _2v2scrim(self, ctx):        
        await ctx.message.reply(content = f'{ctx.author.mention} and their team want to <@&935635762987298836>!', mention_author = True)

    @isTeamCheckIn
    @commands.has_role(896555065282818079)
    @commands.cooldown(1, 1800, commands.BucketType.guild)
    @commands.command()
    async def teamscrim(self, ctx):        
        await ctx.message.reply(content = f'{ctx.author.mention} and their team want to <@&935635762987298836>!', mention_author = True)

    @isClanChat
    @commands.has_role(896555065282818079)
    @commands.cooldown(1, 1800, commands.BucketType.guild)
    @commands.command()
    async def clanscrim(self, ctx):        
        await ctx.message.reply(content = f'{ctx.author.mention} and their clan want to <@&935635762987298836>!', mention_author = True)

    @isMatchmaking
    @commands.cooldown(1, 1800, commands.BucketType.guild)
    @commands.command()
    async def play(self, ctx):        
        await ctx.message.reply(content = f"{ctx.author.mention} is going to play some TC3, come help them rekt some noobs! @here!\n\n*Don't want to get pinged? Run the command: \n!!rank game*", mention_author = True)

async def setup(bot):
    await bot.add_cog(Scrims(bot))
