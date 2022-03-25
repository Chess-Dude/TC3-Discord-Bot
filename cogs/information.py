import discord, gspread, datetime

from oauth2client.service_account import ServiceAccountCredentials
from discord.ext import commands

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client = gspread.authorize(creds)

sheet = client.open("TC3 Unit Information").sheet1

def TC3BotsOrTCGBots(ctx):
    return ctx.channel.id == 351057167706619914 or ctx.channel.id == 408820459279220736

isTC3BotsOrTCGBots = commands.check(TC3BotsOrTCGBots)

class Information(commands.Cog):


    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command()
    async def test(self, ctx):
        mapEmbed=discord.Embed(title="Desert Vs Grass", description="Map Info for Desert vs Grass", color=0xff0000)
        mapEmbed.set_image(url = "https://static.wikia.nocookie.net/the-roblox-conquerors-3/images/c/c0/KoreaRadar.png")
        mapEmbed.timestamp = datetime.datetime.utcnow()
        mapEmbed.set_thumbnail(url = "https://static.wikia.nocookie.net/the-roblox-conquerors-3/images/1/1d/Desert_and_grass.png/revision/latest?cb=20171028152322")
        mapEmbed.set_image(url = "https://static.wikia.nocookie.net/the-roblox-conquerors-3/images/4/4f/DesertGrassMap.png")
        mapEmbed.add_field(name = "Gamemode", value = "3v3")
        mapEmbed.add_field(name = "Map Type", value = "Land & Naval")
        mapEmbed.add_field(name = "Crystals", value = "4 Super Crystals 8 Normal Crystals")
        mapEmbed.add_field(name = "Oil Spots", value = "6")
    

        await ctx.message.reply(embed = mapEmbed, mention_author = False)

    @isTC3BotsOrTCGBots
    @commands.group(invoke_without_command=True)
    async def info(self, ctx, *, inputUnit): 
        
        
        if ctx.invoked_subcommand is None:

            data = sheet.get_all_records()
            resultEntry = None

            for entry in data:
                if inputUnit.lower() == entry["Unit"].lower() or inputUnit.lower() == entry["Unit"].lower().replace(" ", ""):
                    resultEntry = entry
            
            if resultEntry == None:
                return

            unitStats = ["Type", "Produced in", "Cost", "Build Time", "Health", "Damage (DPS)", "Speed", "Range", "Garrisonable", "Garrisons", "Researchable", "Produces", "Unit Slots", "Wiki Link"]
            
            embed = discord.Embed(title = f'{resultEntry["Unit"]}', description = f'Unit Stats for the {resultEntry["Unit"]}', color = 0xff0000)
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_thumbnail(url = f'{resultEntry["Image Link"]}')

            for stat in unitStats:
                if resultEntry[stat] != "N/A":
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

def setup(bot):
    bot.add_cog(Information(bot))