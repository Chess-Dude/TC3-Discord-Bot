import discord, gspread, datetime, json, asyncio, typing
from oauth2client.service_account import ServiceAccountCredentials
from discord import Member, app_commands
from discord.app_commands import Choice
from discord.ext import commands

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client = gspread.authorize(creds)

sheet = client.open("Copy of TC3 Unit Information").sheet1

class InformationAppCommands(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
    #     with open("mapList.json", 'r') as config_reader:
    #         self.mapImages = json.loads(config_reader.read())
        
    #     self.new_data = {}
    #     for key, value in self.mapImages.items():
    #         self.new_data[key.lower()] = value

    # # @commands.is_owner()
    # # @commands.command()
    # # async def testmap(self, ctx):
    # #     mapEmbed=discord.Embed(title="Desert Vs Grass", description="Map Info for Desert vs Grass", color=0xff0000)
    # #     mapEmbed.set_image(url = "https://static.wikia.nocookie.net/the-roblox-conquerors-3/images/c/c0/KoreaRadar.png")
    # #     mapEmbed.timestamp = datetime.datetime.utcnow()
    # #     mapEmbed.set_thumbnail(url = "https://static.wikia.nocookie.net/the-roblox-conquerors-3/images/1/1d/Desert_and_grass.png/revision/latest?cb=20171028152322")
    # #     mapEmbed.set_image(url = "https://static.wikia.nocookie.net/the-roblox-conquerors-3/images/4/4f/DesertGrassMap.png")
    # #     mapEmbed.add_field(name = "Gamemode", value = "3v3")
    # #     mapEmbed.add_field(name = "Map Type", value = "Land & Naval")
    # #     mapEmbed.add_field(name = "Crystals", value = "4 Super Crystals 8 Normal Crystals")
    # #     mapEmbed.add_field(name = "Oil Spots", value = "6")
    

    # #     await ctx.message.reply(embed = mapEmbed, mention_author = False)

    def bots_channels(interaction):
        return interaction.channel.id == 941567353672589322 or interaction.channel.id == 351057167706619914 or interaction.channel.id == 408820459279220736 

    is_bots = app_commands.check(bots_channels)
    
    info_group = app_commands.Group(
        name="info",
        description="A Command That Allows You To Get Information On A Certain Object!")

    @is_bots
    @info_group.command(
        name="unit", 
        description="A Command That Allows You To Get Information On A Certain TC3 Unit!!")
    @app_commands.describe(unit="Type The Unit You Would Like Info on...")
    @app_commands.rename(unit="unit")
    async def info_unit(
        self, 
        interaction: discord.Interaction, 
        unit: typing.Optional[str],
        ):         
            
            input_unit = unit
            data = sheet.get_all_records()
            result_entry = None

            for entry in data:
                if input_unit.lower() == entry["Unit"].lower() or input_unit.lower() == entry["Unit"].lower().replace(" ", ""):
                    result_entry = entry
            
            if result_entry == None:
                return
            
            unit_stats = ["Type", "Produced in", "Cost", "Build Time", "Health", "Damage (DPS)", "Speed", "Range", "Garrisonable", "Garrisons", "Researchable", "Produces", "Unit Slots", "Wiki Link", "Image Link"]
            info_embed = discord.Embed(
                title=f'{result_entry["Unit"]}', 
                description=f'Unit Stats for the {result_entry["Unit"]}', 
                color=0xff0000)

            info_embed.set_author(
                name=f"{interaction.user.display_name}", 
                icon_url=f"{interaction.user.display_avatar.url}")

            info_embed.set_thumbnail(url=f'{result_entry["Image Link"]}')

            for stat in unit_stats:
                info_embed.add_field(
                    name=stat, 
                    value = f'{result_entry[stat]}')
            
            info_embed.set_footer(
                text=f"The Conquerors 3 {input_unit} information",
                icon_url=interaction.guild.icon
            )
            
            info_embed.timestamp = interaction.created_at
            
            await interaction.response.send_message(embed=info_embed)

    # @isTC3BotsOrTCGBots   
    # @info.command()
    # async def map(self, ctx, *, args=None):
        
    #     if ctx.invoked_subcommand is None:
    #         async with ctx.typing():
    #             chosenMap = args.lower()
    #             mapEmbed = discord.Embed(title=f"{chosenMap}", description=f"{ctx.author.mention} {chosenMap}!", color=0xff0000)
    #             mapEmbed.set_image(url = self.new_data[chosenMap])
    #             mapEmbed.timestamp = ctx.message.created_at
    #         await ctx.message.reply(embed=mapEmbed)
        
    @is_bots
    @info_group.command(
        name="user", 
        description="A Command That Allows You To Get Info On A Discord Member!")
    @app_commands.describe(user="Ping The Member That You Would Like Info On!")
    @app_commands.rename(user="member")    
    async def user(
        self, 
        interaction: discord.Interaction,
        user: discord.Member
        ):
            member = user
            roles = [role for role in member.roles]
            embed = discord.Embed(
                title=f"{member}", 
                colour=0xff0000, 
                timestamp=interaction.created_at)
            
            embed.set_author(
                name=f"{member.display_name}", 
                icon_url=f"{member.avatar.url}")
            
            embed.set_thumbnail(url=member.avatar.url)
        
            embed.add_field(
                name="Created Account On:", 
                value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
            embed.add_field(
                name="Joined Server On:", 
                value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
            embed.add_field(
                name="Roles:", 
                value="".join([role.mention for role in roles[1: ]]), inline=False)
            
            embed.set_footer(
                text=f"User ID: {member.id}")
            
            await interaction.response.send_message(embed=embed)

    @is_bots
    @app_commands.command(
        name="link",
        description="A Command That Allows You To Get A Link To A Site!"
    )
    @app_commands.choices(resource=[
        Choice(name="tc1", value=1),
        Choice(name="tc2", value=2),
        Choice(name="tc3", value=3),
        Choice(name="tcg", value=4),
        Choice(name="wiki", value=5),
        Choice(name="twitter", value=6)
    ])    
    async def link_resource(
        self,
        interaction: discord.Interaction,
        resource: Choice[int]
    ):
        if resource.name == "tc1":
            await interaction.response.send_message(content="https://www.roblox.com/games/172585743/")

        elif resource.name == "tc2":
            await interaction.response.send_message(content="https://www.roblox.com/games/13149917/")

        elif resource.name == "tc3":
            await interaction.response.send_message(content="https://www.roblox.com/games/8377997/")

        elif resource.name == "tcg":
            await interaction.response.send_message(content="https://www.roblox.com/My/Groups.aspx?gid=3559196\nhttps://discord.gg/vcAzC5f")

        elif resource.name == "wiki":
            await interaction.response.send_message(content="http://theofficialconquerorswikia.wikia.com/wiki/The_official_conquerors_wiki")

        elif resource.name == "twitter":
            await interaction.response.send_message(content="https://twitter.com/BrokenBoneRBLX\nhttps://twitter.com/ConquerorsRBLX")

    @info_group.command(
        name="matchmaking", 
        description="A Command That Allows You To Get Info On The Matchmaking Channel!")    
    async def matchmaking(
        self, 
        interaction: discord.Interaction
        ):
            await interaction.response.send_message("If you wish to find another member to play TC3 with, please run the ``!!rank game`` command in <#351057167706619914>. This will give you access to the matchmaking channel. Upon gaining access, you may run the ``!play`` command (in the matchmaking channel) to find a fellow player!")

async def setup(bot):
    await bot.add_cog(InformationAppCommands(bot))