import os, discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Greedy
from discord.object import Object 
from typing import Optional, Literal
from cogs.tourneyApplicationCommands import DropdownView
from cogs.mapSelectionCommands import RerollDropdown
from cogs.informationChannels import ParentTournamentInformationViews, ChildTournamentInformationViews, ParentGeneralInformationViews, ParentClanInformationViews 
from cogs.tc3StrategyChannel import ReviewStrategies
from cogs.clanPointsCommands import ReviewClanPoints
from cogs.clanCommands import ReviewClanApplication
from cogs.redeemSystem import RedeemModalReview, RedeemTicketPanel
from cogs.chessTournamentForm import ChessTournamentTicketPanel, ChessTournamentModalReview

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
        self.add_view(ReviewClanPoints())
        self.add_view(ReviewClanApplication())
        self.add_view(ParentClanInformationViews())
        self.add_view(RedeemModalReview())
        self.add_view(RedeemTicketPanel())
        self.add_view(ChessTournamentModalReview())
        self.add_view(ChessTournamentTicketPanel())
        print("views loaded successfully")

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
async def clan_lb(ctx):
    clan_lb_embed = discord.Embed(
        title="Clan Point Yearly Leaderboard",
        description="CRC - 60\nFresh Pickles - 0\nShambhala - 0\nFederal Republic of the Montreal - 0\n Glory to Sentigosedge - 0\nThe Marching Conquerors - 0",
        color=0x00ffff
    )

    await ctx.send(embed=clan_lb_embed)

    clan_lb_embed = discord.Embed(
        title="Clan Point Weekly Leaderboard",
        description="CRC - 60\nFresh Pickles - 0\nShambhala - 0\nFederal Republic of the Montreal - 0\n Glory to Sentigosedge - 0\nThe Marching Conquerors - 1000\nThe Marching Conquerors - 0\n",
        color=0x00ffff
    )

    await ctx.send(embed=clan_lb_embed)

class GoToMessage(discord.ui.View):
    def __init__(self, msg_url: str):
        super().__init__()
        self.add_item(discord.ui.Button(label="Go to Message", url=msg_url))

@bot.tree.context_menu(
    name="Report to Moderators"
)
async def report_user(
    interaction: discord.Interaction, 
    message: discord.Message
):
    log_channel = interaction.guild.get_channel(442447501325369345)

    log_embed = discord.Embed(
        title=f"User Report: {message.author}", 
        description=f"{message.content}", 
        color=0x00ffff
        )        

    log_embed.set_author(
        name=interaction.user.display_name,
        icon_url=interaction.user.display_avatar.url
    )

    await log_channel.send(
        content=f"<@&351166789700550679> <@&363125947635073025>",
        embed=log_embed,
        view=GoToMessage(message.jump_url)
    )

    success_embed = discord.Embed(
        title=f"Successfully Notified Moderators!", 
        color=0x00ffff
        )        

    await interaction.response.send_message(
        embed=success_embed, 
        ephemeral=True
    )

bot.run(token)