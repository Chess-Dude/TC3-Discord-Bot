import discord, datetime
import discord.reaction
from discord.ext import commands
#from discord.ui import Button
from discord.utils import get
import time


def tcg_bots(ctx):
    return ctx.channel.id == 408820459279220736 or ctx.channel.id == 941567353672589322

is_tcg_bots = commands.check(tcg_bots)

hms_ping = '<@&665951855888826369>'

STEP_STATUS = {
                "STEP_1": 0,
                "STEP_2": 1,
                "STEP_3": 2,
                "STEP_4": 3, 
                "ADDITIONAL_NOTES": 4
              }

step_progress = 0

def createInfoEmbed(infoMessage : discord.Message):

    embed = discord.Embed(description = infoMessage.content, color = 0xff0000)
    embed.add_field(name = '**Jump**', value = f'[Go to message!]({infoMessage.jump_url})')
    embed.set_footer(text = f'#{infoMessage.channel.name}')
    embed.timestamp = infoMessage.created_at
    embed.set_author(name = infoMessage.author.display_name, icon_url = infoMessage.author.avatar.url)
    return embed

def steps():
    """
    creates steps
    """
    
    if step_progress == STEP_STATUS["STEP_1"]:
        pass

    elif step_progress == STEP_STATUS["STEP_2"]:
        pass

    elif step_progress == STEP_STATUS["STEP_3"]:
        pass
    
    elif step_progress == STEP_STATUS["STEP_4"]:
        pass
    
    elif step_progress == STEP_STATUS["ADDITIONAL_NOTES"]:
        pass

class PrizeDistribution(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
        for guild in self.bot.guilds:
            for channel in guild.channels:
                print(channel)  


    @is_tcg_bots
    @commands.has_any_role(896542577296306217, 896550746475077672, 716290546519244850, 649683977241886730)
    @commands.command(aliases = ["cd"])
    async def coindistribution(self, ctx, *, args = None):

        if args == None:
            instructions = discord.utils.get(ctx.guild.channels, id = 408820459279220736)
            infoMessage = await instructions.fetch_message(949151674323337286)

            embed = createInfoEmbed(infoMessage)
            await ctx.message.reply(content = "Missing information, please read:", embed = embed, mention_author = True)
            return

        
        success_embed = discord.Embed(title='Head Match Staff Notified!', description=f"{ctx.author.mention} Thanks for submitting your coin distribution!", color=0xff0000)
        await ctx.message.reply(embed = success_embed, mention_author = True)
        
        coin_distribtuion_channel = discord.utils.get(ctx.guild.channels, id = 945447870243422299)
        
        log_embed = discord.Embed(title = f"The Conquering Games Coin Distribution",description=f"**Distribution**\n{args}\n\n**Submitted by**\n{ctx.author.mention}", color=0xff0000)
        log_embed.timestamp = datetime.datetime.utcnow()
        msg = await coin_distribtuion_channel.send(hms_ping, embed = log_embed)

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
            coins_approved_embed = discord.Embed(title='Your Coins Are Now Validated!', description=f"{ctx.author.mention} Direct message the <@!731872828474916934> to recieve your prize!", color=0xff0000)
            await ctx.message.reply(embed = coins_approved_embed, mention_author = True)
            
            TC3RC = self.bot.get_guild(676112926918049813)
            latest_prizes = discord.utils.get(TC3RC.channels, id = 732411044886216715)
            await latest_prizes.send(embed = log_embed, mention_author = True)

        
        if str(reaction.emoji) == '❌': 
            coins_rejected_embed = discord.Embed(title='Your Coins Were Rejected!', description=f"{ctx.author.mention} Please recheck your total coin distribution and or format. Then resubmit your coin distribution again.", color=0xff0000)
            await ctx.message.reply(embed = coins_rejected_embed, mention_author = True)
            

def setup(bot):
    bot.add_cog(PrizeDistribution(bot))