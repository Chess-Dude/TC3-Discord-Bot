import discord, datetime
from discord.ext import commands
from discord import Intents

class Applications(commands.Cog):

    def __init__(self, bot):
        self.bot = bot        
    
    def botsOrWorkChannel(ctx):
        return ctx.channel.id == 408820459279220736 or ctx.channel.id == 896440473659519057 or ctx.channel.id == 941567353672589322

    def createInfoEmbed(self, infoMessage):
        infoEmbed = discord.Embed(description = infoMessage.content, color = 0xff0000)
        infoEmbed.add_field(name = '**Jump**', value = f'[Go to message!]({infoMessage.jump_url})')
        infoEmbed.set_footer(text = f'#{infoMessage.channel.name}')
        infoEmbed.timestamp = infoMessage.created_at
        infoEmbed.set_author(name = infoMessage.author.display_name, icon_url = infoMessage.author.avatar.url) 
        return infoEmbed
    
    async def sendMessage(self, ctx, args, activityType, infoChannelID, infoMessageID, logChannelID, appType):                
        if args == None:
            infoChannel = discord.utils.get(ctx.guild.channels, id = infoChannelID)
            infoMessage = await infoChannel.fetch_message(infoMessageID)

            embed = self.createInfoEmbed(infoMessage)
            await ctx.message.reply(content = "Missing information, please read:", embed = embed, mention_author = True)
            return

        logChannel = discord.utils.get(ctx.guild.channels, id = logChannelID)
        matchStaffPing = '<@&935698898251567124> <@&896440653406433310>'
        thumbsUp = '\U0001F44D'
        thumbsDown = '\U0001f44e'
        
        logEmbed = discord.Embed(title = f"The Conquering Games {activityType} {appType}",description=f"**{appType}**\n{args}\n\n**Submitted by**\n{ctx.author.mention}", color=0xff0000)
        logEmbed.timestamp = datetime.datetime.utcnow()
        successEmbed = discord.Embed(title='Match Staff Notified!', description=f"{ctx.author.mention} Thanks For Submitting Your {activityType} {appType}!", color=0xff0000)
        
        msg = await logChannel.send(matchStaffPing, embed = logEmbed)
        
        await msg.add_reaction(thumbsUp)
        await msg.add_reaction(thumbsDown)

        await ctx.message.reply(embed = successEmbed, mention_author = True)

    isBotsOrWorkChannel = commands.check(botsOrWorkChannel)

    @isBotsOrWorkChannel
    @commands.command(aliases = ["1v1app"])
    async def _1v1app(self, ctx, *, args = None):
        await self.sendMessage(ctx, args, "1v1", 886952755367903233, 886969424463134730, 896444200432861237, "Application")

    @isBotsOrWorkChannel
    @commands.command(aliases = ["2v2app"])
    async def _2v2app(self, ctx, *, args = None):
        await self.sendMessage(ctx, args, "2v2", 886962032753131560, 886971602141585508, 896444200432861237, "Application")

    @isBotsOrWorkChannel
    @commands.command()
    async def teamapp(self, ctx, *, args = None):
        await self.sendMessage(ctx, args, "Team", 886972024885481493, 886973611221598238, 896444200432861237, "Application")
        
    @isBotsOrWorkChannel
    @commands.command()
    async def clanapp(self, ctx, *, args = None):
        await self.sendMessage(ctx, args, "Clan", 886988714436354068, 887029203457941526, 896444227578376192, "Application")    

    @isBotsOrWorkChannel
    @commands.command()
    async def clanchange(self, ctx, *, args = None):
        await self.sendMessage(ctx, args, "Clan", 886988714436354068, 887029203457941526, 896444227578376192, "Change")    

    @isBotsOrWorkChannel
    @commands.command(aliases = ["2v2change"])
    async def _2v2change(self, ctx, *, args = None):
        await self.sendMessage(ctx, args, "2v2", 886962032753131560, 886971602141585508, 896479412617359361, "Change")    

    @isBotsOrWorkChannel
    @commands.command()
    async def teamchange(self, ctx, *, args = None):
        await self.sendMessage(ctx, args, "Team", 886972024885481493, 886973611221598238, 896479412617359361, "Change")    

    @commands.is_owner()
    @isBotsOrWorkChannel
    @commands.command(aliases = ["testapp"])
    async def test(self, ctx, *, args = None):
   
        await self.sendMessage(ctx, args, "Test", 886972024885481493, 886973611221598238, 941567353672589322, "Application")

async def setup(bot):
    await bot.add_cog(Applications(bot))
