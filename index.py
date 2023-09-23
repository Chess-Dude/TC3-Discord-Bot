import os, discord, asyncpg
from discord.ext import commands
from discord.ext.commands import Greedy
from discord.object import Object 
from typing import Optional, Literal
from cogs.mapBingo import BingoCommands
from cogs.informationEmbeds.welcomeEmbed.parentWelcomeView import ParentWelcomeView
from cogs.teamApplicationClasses.teamApplicationDropdown import TournamentDropdownView
from cogs.mapSelectionCommands import RerollDropdown
from cogs.informationChannels import ParentTournamentInformationViews, ParentClanInformationViews
from cogs.informationEmbeds.childTournamentView import ChildTournamentInformationViews  
from cogs.clanPointCommands import ReviewClanPoints
from cogs.clanClasses.clanApplicationClasses.clanApplicationReview import ReviewClanApplication
from cogs.redeemSystem import RedeemTicketPanel
from cogs.redeemClasses.RedeemModalReview import RedeemModalReview 
from cogs.chessTournamentClasses.chessTournamentModalReview import ChessTournamentModalReview
from cogs.chessTournamentForm import ChessTournamentTicketPanel
from cogs.signUpCommands import TournamentTicketPanel
from cogs.clanClasses.clanRosterClasses.DisbandClans import DisbandClansClass
from cogs.signupClasses.skillDivsionDropdown import SkillDivisionDropdownView
from cogs.tc3BugReport import BugReportTicketPanel
from cogs.tc3BugClasses.bugModalReview import BugModalReview
from dotenv import load_dotenv
import psutil

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
token = BOT_TOKEN

class TC3Bot(commands.Bot):
    def __init__(
        self
    ):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.reactions = True
        intents.presences = False
        activity = discord.Activity(
            name="Conquering Noobs on Roblox's best RTS - The Conquerors 3. Play now at: https://www.roblox.com/games/8377997",       # The game name
            type=discord.ActivityType.playing,
            details="Conquering Robloxians",  # Additional details
            large_image="tc3Thumbnail"       # Use the name of the image without the file extension
        )        
        super().__init__(
            command_prefix="!",
            activity=activity,
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
        credentials = {"host": os.getenv("DB_HOST"), "database": os.getenv("DB_NAME"), "user": os.getenv("DB_USERNAME"), "password": os.getenv("DB_PASSWORD")}
        self.pool = await asyncpg.create_pool(min_size=1, max_size=5, **credentials)
        print("pooled successfully")        
        self.add_view(TournamentDropdownView())
        self.add_view(RerollDropdown())
        self.add_view(ParentTournamentInformationViews())
        self.add_view(ChildTournamentInformationViews())
        self.add_view(SkillDivisionDropdownView())
        self.add_view(ReviewClanPoints())
        self.add_view(ReviewClanApplication(self.pool))
        self.add_view(ParentClanInformationViews())
        self.add_view(RedeemModalReview())
        self.add_view(RedeemTicketPanel())
        self.add_view(ChessTournamentModalReview())
        self.add_view(ChessTournamentTicketPanel())
        self.add_view(TournamentTicketPanel())
        self.add_view(DisbandClansClass())        
        self.add_view(BugReportTicketPanel())
        self.add_view(BugModalReview())
        self.add_view(BingoCommands(self))
        print("views loaded successfully")

bot = TC3Bot()
bot.remove_command("help")

@commands.is_owner()
@bot.command()
async def shutdown(ctx):
    await ctx.send("shutting down")
    await bot.pool.close()    
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
async def ram(ctx):
    process = psutil.Process()
    memory_usage = process.memory_info().rss / 1024 ** 2  # Memory usage in MB
    await ctx.send(f"Current RAM usage: {memory_usage:.2f} MB")

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
        await welcome_message_channel.send(f"<@649834100626292746>, <@361170109877977098>, <@898392058077802496>, <@1006873288229793833> \n{msg.jump_url}")

        welcome_information_embed = discord.Embed(
            title=f"The Conquerors 3 Community | Information",
            description=f"Welcome to The Conquerors 3 Discord Server! Please click a button if you would like to learn more about it.",
            color=0x00ffff
        )

        welcome_information_embed.set_image(
            url="https://media.discordapp.net/attachments/350068992045744142/1047732656508510299/IMG_3001.png?width=1193&height=671"
        )

        try:        
            await member.send(
                embed=welcome_information_embed, 
                view=ParentWelcomeView()
            )
        
        except:
            pass

class GoToMessage(discord.ui.View):
    def __init__(self, msg_url: str):
        super().__init__()
        self.add_item(discord.ui.Button(label="Go to Message", url=msg_url))

bot.tree.context_menu(
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


@bot.command()
@commands.is_owner()
async def init_clan_databases(ctx):
    clan_divider_top_role = ctx.guild.get_role(1053050572296704000)
    clan_divider_bottom_role = ctx.guild.get_role(1053050637555880027)

    for role_position in range(clan_divider_top_role.position-1, clan_divider_bottom_role.position, -1):
        clan_role = discord.utils.get(
            ctx.guild.roles, 
            position=role_position
        )

        if clan_role is not None:
            async with bot.pool.acquire() as connection:
                sql = "INSERT INTO clanpointleaderboard (clanName, clanRoleID, weeklyClanPoints, yearlyClanPoints) VALUES ($1, $2, $3, $4)"
                val = (clan_role.name, int(clan_role.id), 0, 0)
                inserted_row = await connection.execute(sql, *val)
                print(inserted_row, "record inserted into ClanPointLeaderboard.")

            for member in clan_role.members:
                if member is not None:
                    async with bot.pool.acquire() as connection:
                        sql = "INSERT INTO ClanPointTracker (robloxUsername, discordUserID, totalClanPoints, currentClanRoleID, currentClanName) VALUES ($1, $2, $3, $4, $5)"
                        val = (f"{member.nick}", member.id, 0, clan_role.id, f"{clan_role.name}")

                        inserted_row = await connection.execute(sql, *val)
                        print(inserted_row, "record inserted into ClanPointTracker.")

@bot.command()
@commands.is_owner()
async def delete_all_from_tables(ctx):
    # SQL queries to delete all rows from the tables
    delete_leaderboard_query = "DELETE FROM ClanPointLeaderboard;"
    delete_tracker_query = "DELETE FROM ClanPointTracker;"
    delete_submission_tracker_query = "DELETE FROM ClanPointSubmissionTracker;"

    # Acquire a connection from the pool
    async with bot.pool.acquire() as connection:
        # Create a transaction to execute the queries
        async with connection.transaction():
            # Execute the DELETE queries
            await connection.execute(delete_leaderboard_query)
            await connection.execute(delete_tracker_query)
            await connection.execute(delete_submission_tracker_query)
            print("deleted all values from tables")

@bot.command()
@commands.is_owner()
async def print_clan_databases(ctx):

    async with bot.pool.acquire() as connection:
        # sql = "SELECT * FROM ClanPointLeaderboard"
        # result = await connection.fetch(sql)
        
        # for row in result:
        #     print(row)

        print("\n\n")
        sql = "SELECT * FROM ClanPointTracker"
        result = await connection.fetch(sql)
        
        for row in result:
            print(row)

        print("\n\n")
        sql = "SELECT * FROM ClanPointSubmissionTracker"
        result = await connection.fetch(sql)
        
        for row in result:
            print(row)            

bot.run(token)