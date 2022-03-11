import discord, datetime
import discord.reaction
from discord.ext import commands
#from discord.ui import Button
from discord.utils import get
import time

class PrizeDistribution(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
        self.hmsPing = '<@&665951855888826369>'

    def tcgBots(self, ctx):
        return ctx.channel.id == 408820459279220736 or ctx.channel.id == 941567353672589322

    def createInfoEmbed(self, infoMessage : discord.Message):

        embed = discord.Embed(description = infoMessage.content, color = 0xff0000)
        embed.add_field(name = '**Jump**', value = f'[Go to message!]({infoMessage.jump_url})')
        embed.set_footer(text = f'#{infoMessage.channel.name}')
        embed.timestamp = infoMessage.created_at
        embed.set_author(name = infoMessage.author.display_name, icon_url = infoMessage.author.avatar.url)
        return embed

    isTcgBots = commands.check(tcgBots)

    @isTcgBots
    @commands.has_any_role(896542577296306217, 896550746475077672, 716290546519244850, 649683977241886730)
    @commands.command(aliases = ["cd"])
    async def coindistribution(self, ctx, *, args = None):

        if args == None:
            instructions = discord.utils.get(ctx.guild.channels, id = 408820459279220736)
            infoMessage = await instructions.fetch_message(949151674323337286)

            embed = self.createInfoEmbed(infoMessage)
            await ctx.message.reply(content = "Missing information, please read:", embed = embed, mention_author = True)
            return

        successEmbed = discord.Embed(title='Head Match Staff Notified!', description=f"{ctx.author.mention} Thanks for submitting your coin distribution!", color=0xff0000)
        await ctx.message.reply(embed = successEmbed, mention_author = True)
        
        coin_distribtuion_channel = discord.utils.get(ctx.guild.channels, id = 945447870243422299)
        
        logEmbed = discord.Embed(title = f"The Conquering Games Coin Distribution",description=f"**Distribution**\n{args}\n\n**Submitted by**\n{ctx.author.mention}", color=0xff0000)
        logEmbed.timestamp = datetime.datetime.utcnow()
        msg = await coin_distribtuion_channel.send(self.hmsPing, embed = logEmbed)

        # await msg.add_reaction('✅')
        # await msg.add_reaction('❌')

        # Should later be made into a lambda function
        def check(r, u):
            return str(r.emoji) in "✅❌"
        
        reaction, user = await self.bot.wait_for("reaction_add", check=check, timeout=None)
        
        """ for guild in self.bot.guilds:
            for channel in guild.channels:
                print(channel) """
        
        if str(reaction.emoji) == '✅':
            coinsApprovedEmbed = discord.Embed(title='Your Coins Are Now Validated!', description=f"{ctx.author.mention} Direct message the <@!731872828474916934> to recieve your prize!", color=0xff0000)
            await ctx.message.reply(embed = coinsApprovedEmbed, mention_author = True)
            
            TC3RC = self.bot.get_guild(676112926918049813)
            latestPrizes = discord.utils.get(TC3RC.channels, id = 732411044886216715)
            await latestPrizes.send(embed = logEmbed, mention_author = True)

        if str(reaction.emoji) == '❌': 
            coinsRejectedEmbed = discord.Embed(title='Your Coins Were Rejected!', description=f"{ctx.author.mention} Please recheck your total coin distribution and or format. Then resubmit your coin distribution again.", color=0xff0000)
            await ctx.message.reply(embed = coinsRejectedEmbed, mention_author = True)
            

def setup(bot):
    bot.add_cog(PrizeDistribution(bot))