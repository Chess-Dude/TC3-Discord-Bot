import os, discord, datetime
from discord.ext import commands
from discord.ext.commands import Greedy
from discord.object import Object 
from typing import Optional, Literal
from discord import app_commands
from cogs.appCommandsTest import DropdownView
from cogs.mapSelectionAppCommands import RerollDropdown

token = "OTUzMDE3MDU1MjM2NDU2NDQ4.Gp0q6l.8VIj98FK-wkozHMSXUYKdZa62D-1k5899DTS-I"
class MyBot(commands.Bot):
    
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.reactions = True
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
        self.add_view(DropdownView())
        self.add_view(RerollDropdown())
        print("view loaded successfully")

bot = MyBot()
bot.remove_command("help")

@commands.is_owner()
@bot.command()
async def shutdown(ctx):
    await ctx.send("shutting down")
    await bot.close()
    bot.clear()
    
@bot.command()
@commands.is_owner()
async def reload(ctx, args):
    for filename in os.listdir('./cogs'):
        if filename == args:
            await bot.unload_extension(f'cogs.{filename[:-3]}')
            print((f'cogs.{filename[:-3]} unloaded'))
            await bot.load_extension(f'cogs.{filename[:-3]}')
            await ctx.send(f'cogs.{filename[:-3]} loaded')
            print(f'cogs.{filename[:-3]} re-loaded')

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
    await ctx.send(f"{args}")

@bot.command()
@commands.is_owner()
async def sync(ctx, guilds: Greedy[Object], spec: Optional[Literal["~", "*"]] = None):
    if not guilds:
        if spec == "~":
            fmt = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            fmt = await ctx.bot.tree.sync(guild=ctx.guild)
        else:
            fmt = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(fmt)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    fmt = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            fmt += 1

    await ctx.send(f"Synced the tree to {fmt}/{len(guilds)} guilds.")
    
@commands.is_owner()
@bot.command(aliases=["renamerole"])
async def rename_role(ctx, role: discord.Role, args):
    await role.edit(name=args)
    await ctx.reply(f"renamed {role.mention} to {args}")

@bot.command()
@commands.is_owner()
async def embed(ctx):
    await ctx.send(embed=discord.Embed(title="N/A", description="", color=0xff0000))

bot.run(token)