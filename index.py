import asyncio
from operator import truediv
import os
import discord
from discord.ext import commands

token = 'ODY5OTc0MTA4MzEyNTY3ODE4.YQGAhg.VMq38SL5ltLLe2OkgyZXRyF1FAg'
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    case_insensitive=True, 
    intents = intents,
    allowed_mentions=discord.AllowedMentions(
        users=True,        
        everyone=False,     
        roles=True,         
        replied_user=True, 
    ),
)

bot.remove_command('help')
bot.owner_id = 621516858205405197

async def initialiseCogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
            print(f'cogs.{filename[:-3]} loaded')

async def main():
    async with bot:
        await initialiseCogs()
        await bot.start(token)

@bot.command()
@commands.is_owner() 
async def AdminRole(ctx, member:discord.Member, role:discord.Role):
    if role in member.roles:
        await member.remove_roles(role)
    else:
        await member.add_roles(role)
    await ctx.send('did')

@bot.command(aliases = ["load"])
@commands.is_owner()
async def enable(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    await ctx.send('done')

@bot.command()
@commands.is_owner()
async def echo(ctx, *, args): 
    await ctx.send(args)
        
@bot.command(aliases = ["unload"])
@commands.is_owner()
async def disable(ctx, extension):
    bot.unload_extension(f'cogs.{extension}') 
    await ctx.send('done')
 
@bot.command()
@commands.is_owner()
async def rerun(ctx):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                bot.unload_extension(f'cogs.{filename[:-3]}')    
                bot.load_extension(f'cogs.{filename[:-3]}')
            except commands.ExtensionNotLoaded:
                bot.load_extension(f'cogs.{filename[:-3]}')
  
    await ctx.send('Restarted :white_check_mark:')
    
asyncio.run(main())