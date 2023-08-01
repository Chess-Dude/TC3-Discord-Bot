import discord
from discord.ext import commands
from discord import Interaction, app_commands

class errorHandler(commands.Cog):    
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):        
        print('TC3 BOT online.')

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
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(f"Error: Member was not found! Please try again.")
        elif isinstance(error, commands.RoleNotFound):
            await ctx.send(f"Error: Role was not found! Please try again!")
        elif isinstance(error, ZeroDivisionError):
            pass
        else:
            await ctx.send('Error: Unknown error occured. <@621516858205405197>')
            print(str(error))
    
async def setup(bot):
    await bot.add_cog(errorHandler(bot))