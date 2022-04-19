import os
import discord
from discord.ext import commands

# #oldtoken = 'ODY5OTc0MTA4MzEyNTY3ODE4.YQGAhg.VMq38SL5ltLLe2OkgyZXRyF1FAg'
token = "OTUzMDE3MDU1MjM2NDU2NDQ4.Yi-cTA.scAFqrVOE3vynhnYkzQuCFpYkWI"
class MyBot(commands.Bot):
    
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(
            command_prefix="!",
            case_insensitive=True, 
            intents = intents,    
            allowed_mentions=discord.AllowedMentions(
                users=True,        
                everyone=True,     
                roles=True,         
                replied_user=True, 
            ),  
            application_id=953017055236456448
        )
        
    async def setup_hook(self):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'cogs.{filename[:-3]} loaded')
        await bot.tree.sync(guild=discord.Object(id=945417589235023963))

bot = MyBot()
bot.remove_command("help")

@bot.command()
@commands.is_owner() 
async def AdminRole(ctx, member:discord.Member, role:discord.Role):
    if role in member.roles:
        await member.remove_roles(role)
    else:
        await member.add_roles(role)
    await ctx.send('did')

@bot.command()
@commands.is_owner()
async def echo(ctx, *, args): 
    await ctx.send(args)

bot.run(token)