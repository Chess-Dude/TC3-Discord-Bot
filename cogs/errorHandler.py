import discord

from discord.ext import commands

class errorHandler(commands.Cog):    
    
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print('TC3 BOT online.')


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == 235148962103951360 and message.channel.id == 351057661925654528 and len(message.embeds) != 0:
            dupe = discord.Embed(title = f"The Conquerors 3 Suggestion", description=f"{message.embeds[0].description}", color=0xff0000)
            scChannel = discord.utils.get(message.guild.channels, id = 896871616967999530)
            msg = await scChannel.send(embed = dupe)

            approve = self.bot.get_emoji(896882817080901632)
            consider = self.bot.get_emoji(896882836039155733)
            deny = self.bot.get_emoji(896882859539824680)
            await msg.add_reaction(approve)
            await msg.add_reaction(consider)
            await msg.add_reaction(deny)

    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.NotOwner):
            pass
        elif isinstance(error, commands.MissingRequiredArgument):
            pass
        elif isinstance(error, commands.MissingRole):
            pass
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'Error: Command on cooldown, try again in {int(int(error.retry_after)/60)}m{int(error.retry_after)%60}s.')
        elif isinstance(error, commands.CheckFailure):
            pass
        else:
            await ctx.send('Error: Unknown error occured. <@621516858205405197>')
            print(str(error))
    
    
async def setup(bot):
    await bot.add_cog(errorHandler(bot))