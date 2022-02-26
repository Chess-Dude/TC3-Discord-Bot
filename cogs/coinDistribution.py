import discord, datetime
import discord.reaction
from discord.ext import commands
from discord.utils import get
import time

from psutil import users

def tcg_bots(ctx):
    return ctx.channel.id == 408820459279220736 or ctx.channel.id == 941567353672589322

is_tcg_bots = commands.check(tcg_bots)

hms_ping = '<@&665951855888826369>'

# def createInfoEmbed(infoMessage : discord.Message):

#     embed = discord.Embed(description = infoMessage.content, color = 0xff0000)
#     embed.add_field(name = '**Jump**', value = f'[Go to message!]({infoMessage.jump_url})')
#     embed.set_footer(text = f'#{infoMessage.channel.name}')
#     embed.timestamp = infoMessage.created_at
#     embed.set_author(name = infoMessage.author.display_name, icon_url = infoMessage.author.avatar_url)
#     return embed


class CoinDistribution(commands.Cog):


    def __init__(self, bot):
        self.bot = bot


    @is_tcg_bots
    @commands.has_any_role(896542577296306217, 896550746475077672, 716290546519244850, 649683977241886730)
    @commands.command(aliases = ["cd"])
    async def coindistribution(self, ctx, *, args = None):

        # if args == None:
        #     _1v1info = discord.utils.get(ctx.guild.channels, id = 886952755367903233)
        #     infoMessage = await _1v1info.fetch_message(886969424463134730)

        #     embed = createInfoEmbed(infoMessage)
        #     await ctx.message.reply(content = "Missing information, please read:", embed = embed, mention_author = False)
        #     return

        
        success_embed = discord.Embed(title='Head Match Staff Notified!', description=f"{ctx.author.mention} Thanks for submitting your coin distribution!", color=0xff0000)
        await ctx.message.reply(embed = success_embed, mention_author = True)
        
        coin_distribtuion = discord.utils.get(ctx.guild.channels, id = 945447870243422299)
        
        log_embed = discord.Embed(title = f"The Conquering Games Coin Distribution",description=f"**Distribution**\n{args}\n\n**Submitted by**\n{ctx.author.mention}", color=0xff0000)
        log_embed.timestamp = datetime.datetime.utcnow()
        msg = await coin_distribtuion.send(hms_ping, embed = log_embed)

        # await msg.add_reaction('✅')
        # await msg.add_reaction('❌')

        def check(r, u):
            return str(r.emoji) in "✅❌"
        
        reaction, user = await self.bot.wait_for("reaction_add", check=check, timeout=None)
        
        
        
        if str(reaction.emoji) == '✅':
            coins_approved_embed = discord.Embed(title='Your Coins Are Now Validated!', description=f"{ctx.author.mention} Direct message the <@!731872828474916934> to recieve your prize!", color=0xff0000)
            await ctx.message.reply(embed = coins_approved_embed, mention_author = True)
            
            TC3RC = self.bot.get_guild(676112926918049813)
            latest_prizes = discord.utils.get(TC3RC.channels, id = 732411044886216715)
            await latest_prizes.send(embed = log_embed, mention_author = True)

        
        if str(reaction.emoji) == '❌': 
            coins_rejected_embed = discord.Embed(title='Your Coins Were Rejected!', description=f"{ctx.author.mention} Please recheck your total coin distribution and or format. Then resubmit your coin distribution again.", color=0xff0000)
            await ctx.message.reply(embed = coins_rejected_embed, mention_author = True)
        
        
            
    # async def checkreacts(self, ctx, bot):
    #     msg1 = await ctx.say("React to me!")
    #     custom_emoji = get(ctx.message.server.emojis, name="custom_emoji")
    #     reaction = await bot.wait_for_reaction(['\N{SMILE}', custom_emoji], msg1)
    #     await bot.say("You responded with {}".format(reaction.emoji))
    #         :thumbsup:
    # async def on_reaction_add(self, reaction, user):
    #     if user != self.bot.user:
    #         if str(reaction.emoji) == '\U0001F44D':
    #             print("thumbs up detected")


def setup(bot):
    bot.add_cog(CoinDistribution(bot))
