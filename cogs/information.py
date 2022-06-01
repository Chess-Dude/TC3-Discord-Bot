import discord, gspread, datetime, json, asyncio
from oauth2client.service_account import ServiceAccountCredentials
from discord.ext import commands

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client = gspread.authorize(creds)

sheet = client.open("Copy of TC3 Unit Information").sheet1

class Information(commands.Cog):


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

    def TC3BotsOrTCGBots(ctx):
        return ctx.channel.id == 351057167706619914 or ctx.channel.id == 408820459279220736 or 941567353672589322

    isTC3BotsOrTCGBots = commands.check(TC3BotsOrTCGBots)

    @isTC3BotsOrTCGBots
    @commands.group(invoke_without_command=True)
    async def info(self, ctx, *, inputUnit): 
        
        
        if ctx.invoked_subcommand is None:
            async with ctx.typing():
                    
                data = sheet.get_all_records()
                resultEntry = None

                for entry in data:
                    if inputUnit.lower() == entry["Unit"].lower() or inputUnit.lower() == entry["Unit"].lower().replace(" ", ""):
                        resultEntry = entry
                
                if resultEntry == None:
                    return
                
                unitStats = ["Type", "Produced in", "Cost", "Build Time", "Health", "Damage (DPS)", "Speed", "Range", "Garrisonable", "Garrisons", "Researchable", "Produces", "Unit Slots", "Wiki Link", "Image Link"]
                embed = discord.Embed(title=f'{resultEntry["Unit"]}', description=f'Unit Stats for the {resultEntry["Unit"]}', color=0xff0000)
                embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.avatar.url}")
                embed.timestamp = ctx.message.created_at
                embed.set_thumbnail(url=f'{resultEntry["Image Link"]}')

                for stat in unitStats:
                    # if resultEntry[stat] != "N/A":
                    embed.add_field(name = stat, value = f'{resultEntry[stat]}')
                
            await ctx.message.reply(embed = embed, mention_author = True)
        
    @isTC3BotsOrTCGBots
    @info.command()
    async def tc1(self, ctx):
        await ctx.message.reply('https://www.roblox.com/games/172585743/')
            
    @isTC3BotsOrTCGBots
    @info.command()
    async def tc2(self, ctx):
        await ctx.message.reply('https://www.roblox.com/games/13149917/')

    @isTC3BotsOrTCGBots  
    @info.command()
    async def tc3(self, ctx):
        await ctx.message.reply('https://www.roblox.com/games/8377997/')

    @isTC3BotsOrTCGBots 
    @info.command()
    async def wiki(self, ctx):
        await ctx.message.reply('http://theofficialconquerorswikia.wikia.com/wiki/The_official_conquerors_wiki')
    
    @isTC3BotsOrTCGBots
    @info.command()
    async def twitter(self, ctx):
        await ctx.message.reply('https://twitter.com/BrokenBoneRBLX\nhttps://twitter.com/ConquerorsRBLX')

    @isTC3BotsOrTCGBots   
    @info.command()
    async def tcg(self, ctx):
        await ctx.message.reply('https://www.roblox.com/My/Groups.aspx?gid=3559196\nhttps://discord.gg/vcAzC5f')

    @isTC3BotsOrTCGBots   
    @info.command()
    async def map(self, ctx, *, args=None):
        
        if ctx.invoked_subcommand is None:
            async with ctx.typing():
                chosenMap = args.lower()
                mapEmbed = discord.Embed(title=f"{chosenMap}", description=f"{ctx.author.mention} {chosenMap}!", color=0xff0000)
                mapEmbed.set_image(url = self.new_data[chosenMap])
                mapEmbed.timestamp = ctx.message.created_at
            await ctx.message.reply(embed=mapEmbed)
        
    @isTC3BotsOrTCGBots
    @info.command()
    async def user(self, ctx, member: discord.Member = None):
        async with ctx.typing():
            if member == None:
                member = ctx.author
            roles = [role for role in member.roles]
            embed = discord.Embed(title=f"{member}", colour=0xff0000, timestamp=ctx.message.created_at)
            embed.set_author(name=f"{member.display_name}", icon_url=f"{member.avatar.url}")
            embed.set_thumbnail(url=member.avatar.url)
        
            embed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
            embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
            embed.add_field(name="Roles:", value="".join([role.mention for role in roles[1: ]]), inline=False)
            embed.set_footer(text=f"User ID: {member.id}")
            
        await ctx.message.reply(embed=embed, mention_author=True)

async def setup(bot):
    await bot.add_cog(Information(bot))