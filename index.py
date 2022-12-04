import os, discord
from discord.ext import commands
from discord.ext.commands import Greedy
from discord.object import Object 
from typing import Optional, Literal
from cogs.tourneyApplicationCommands import DropdownView
from cogs.mapSelectionCommands import RerollDropdown
from cogs.informationChannels import ParentTournamentInformationViews, ChildTournamentInformationViews, ParentGeneralInformationViews 
from cogs.tc3StrategyChannel import ReviewStrategies

token = ""
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
        self.add_view(ParentTournamentInformationViews())
        self.add_view(ChildTournamentInformationViews())
        self.add_view(ParentGeneralInformationViews())
        self.add_view(ReviewStrategies())
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
    
@bot.command()
@commands.is_owner()
async def embed(ctx):
    await ctx.send(embed=discord.Embed(title="N/A", description="", color=0xff0000))

@bot.event
async def on_member_join(member):
    TC3_SERVER = bot.get_guild(350068992045744141)
    if member.guild == TC3_SERVER:
        LOBBY_CHANNEL = bot.get_channel(350068992045744142)
        welcome_message_channel = bot.get_channel(351084557929283585)

        msg = await LOBBY_CHANNEL.send(f"Welcome to The Official Conquerors 3 Discord {member.mention}! If you have any questions feel free to ping <@585991378400706570>! Make sure to checkout <#351057978381828096> and <#696086223009218682> to stay up to date with the latest The Conquerors 3 content! Before you post, please read <#731499115573280828> to keep our server running smoothly and without any problems.")
        await welcome_message_channel.send(f"<@563066303015944198>, <@361170109877977098>, <@898392058077802496>, <@804726051166617652>, <@450662444612845580> \n{msg.jump_url}")

@bot.command()
@commands.is_owner()
async def archive_tcg(ctx):
    _3v3_category = discord.utils.get(
        ctx.guild.categories, 
        id=666965988373299211
    )   

    _2v2_category = discord.utils.get(
        ctx.guild.categories, 
        id=666965988373299211
    )   

    _1v1_category = discord.utils.get(
        ctx.guild.categories, 
        id=666965988373299211
    )   


bot.run(token)