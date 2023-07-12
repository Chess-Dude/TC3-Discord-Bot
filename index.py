import os, discord
from discord.ext import commands
from discord.ext.commands import Greedy
from discord.object import Object 
from typing import Optional, Literal
from cogs.teamApplicationClasses.teamApplicationDropdown import TournamentDropdownView
from cogs.mapSelectionCommands import RerollDropdown
from cogs.informationChannels import ParentTournamentInformationViews, ParentClanInformationViews
from cogs.informationEmbeds.childTournamentView import ChildTournamentInformationViews  
from cogs.strategyClasses.reviewStrategies import ReviewStrategies
from cogs.clanPointsCommands import ReviewClanPoints
from cogs.clanClasses.clanApplicationClasses.clanApplicationReview import ReviewClanApplication
from cogs.redeemSystem import RedeemTicketPanel
from cogs.redeemClasses.RedeemModalReview import RedeemModalReview 
from cogs.chessTournamentClasses.chessTournamentModalReview import ChessTournamentModalReview
from cogs.chessTournamentForm import ChessTournamentTicketPanel
from cogs.signUpCommands import TournamentTicketPanel
from cogs.clanClasses.clanRosterClasses.DisbandClans import DisbandClansClass
from cogs.signupClasses.skillDivsionDropdown import SkillDivisionDropdownView
from dotenv import load_dotenv, set_key

load_dotenv()
token = os.getenv("BOT_TOKEN")
#token = BOT_TOKEN
if token == None:
    token = input("Please enter your bot token: ")
    set_key(".env", "BOT_TOKEN", token)

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
        self.add_view(TournamentDropdownView())
        self.add_view(RerollDropdown())
        #self.add_view(MapChooserDropdown())
        #self.add_view(TroopChooserDropdown()) #map chooser comming... eventually
        #self.add_view(ChooseDropdown())
        self.add_view(ParentTournamentInformationViews())
        self.add_view(ChildTournamentInformationViews())
        self.add_view(SkillDivisionDropdownView())
        self.add_view(ReviewStrategies())
        self.add_view(ReviewClanPoints())
        self.add_view(ReviewClanApplication())
        self.add_view(ParentClanInformationViews())
        self.add_view(RedeemModalReview())
        self.add_view(RedeemTicketPanel())
        self.add_view(ChessTournamentModalReview())
        self.add_view(ChessTournamentTicketPanel())
        self.add_view(TournamentTicketPanel())
        self.add_view(DisbandClansClass())        
        print("views loaded successfully")

bot = MyBot()
bot.remove_command("help")

@commands.is_owner()
@bot.command()
async def shutdown(ctx):
    await ctx.send("shutting down")
    await bot.close()
    bot.clear()
    exit(0) #Exit with success status code
    
@bot.command()
@commands.is_owner()
async def reload(ctx, args):
    for filename in os.listdir('./cogs'):
        if filename == args:
            await bot.unload_extension(f'cogs.{filename[:-3]}')
            print((f'cogs.{filename[:-3]} unloaded successfully!'))
            await bot.load_extension(f'cogs.{filename[:-3]}')
            await ctx.send(f'cogs.{filename[:-3]} re-loaded successfully!')
            print(f'cogs.{filename[:-3]} loaded successfully!')

@bot.command()
@commands.is_owner()
async def echo(ctx, *, args):
    await ctx.send(f"{args}")

@bot.command()
@commands.is_owner()
async def sync(ctx: commands.Context, guilds: Greedy[Object], spec: Optional[Literal["~", "*"]] = None):
    if not guilds:
        if spec == "~":
            fmt = await bot.tree.sync(guild=ctx.guild)   
        elif spec == "*":
            bot.tree.copy_global_to(guild=ctx.guild) #type: ignore
            fmt = await bot.tree.sync(guild=ctx.guild)
        else:
            fmt = await bot.tree.sync()

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
async def on_member_join(member:discord.Member):
    TC3_SERVER = bot.get_guild(350068992045744141)
    if member.guild == TC3_SERVER:
        LOBBY_CHANNEL = bot.get_channel(350068992045744142)
        welcome_message_channel = bot.get_channel(351084557929283585)

        msg = await LOBBY_CHANNEL.send(f"Welcome to The Official Conquerors 3 Discord {member.mention}! If you have any questions feel free to ping <@585991378400706570>! Make sure to checkout <#351057978381828096> and <#696086223009218682> to stay up to date with the latest The Conquerors 3 content! Before you post, please read <#731499115573280828> to keep our server running smoothly and without any problems.") #type: ignore
        await welcome_message_channel.send(f"<@563066303015944198>, <@361170109877977098>, <@898392058077802496>, <@450662444612845580>, <@646463139977625623>, <@897020169958883348>, <@1006873288229793833> \n{member.display_name} joined!\n**`Jump Link`**:\n{msg.jump_url}") #type: ignore

@bot.command()
@commands.is_owner()
async def clan_lb(ctx):
    import discord
    clan_lb_channel = bot.get_channel(1050289500783386655)
    clan_yearly_lb_message = await clan_lb_channel.fetch_message(1056413562525974608) #type: ignore

    description = """
Omnipotent - 32638
The Marching Conquerors - 29083
CRC - 25849
goom - 18741
The Hivemind - 11993
NylonW - 10268
Total Victory - 9092
The Bozos - 7159
Ablogical - 5594
Lose 4 Cry - 4604
CR - 3051
i hate tc3 the clan - 2081
Fresh Pickles - 2060
The Bots - 1887
Glory to Sentigosedge - 1577
The Dairy Mafia - 1313
Shambhala - 232
"""
    clan_lb_embed = discord.Embed(
        title="Clan Point Yearly Leaderboard",
        description=f"{description}",
        #color=0x00ffff
        color=discord.Color.from_rgb(0, 255, 255)
    )

    await clan_yearly_lb_message.edit(embed=clan_lb_embed)
    await ctx.send("completed")
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
    assert interaction.guild is not None
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

    await log_channel.send( #type: ignore
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