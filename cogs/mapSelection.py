import discord, random, json

from discord.ext import commands

from cogs.information import TC3BotsOrTCGBots

def TC3OrTCGBots(ctx):
    return ctx.channel.id == 351057167706619914 or ctx.channel.id == 408820459279220736

isBots = commands.check(TC3BotsOrTCGBots)


def TCG(ctx):
    return ctx.guild.id == 371817692199518240

isTCG = commands.check(TCG)

class MapSelection(commands.Cog):

    def __init__(self, bot):

        self.bot = bot    
        with open("mapList.json", 'r') as config_reader:
            self.mapImages = json.loads(config_reader.read())
        
    # @commands.command(aliases = ["map"])
    # async def onedaymap(self, ctx):

    #     maps = ["Korea", "Mexico", "Germany Map", "Double Mansion", "Fantasy", "Basalt Peninsula"]

    #     selectedMap = random.choice(maps)

    #     mapEmbed=discord.Embed(title="Randomized One Day Tournament Map (Round 1):", description=f"{ctx.author.mention} Your randomized map is: {selectedMap}!", color=0xff0000)
    #     mapEmbed.set_image(url = self.mapImages[selectedMap])
    #     await ctx.message.reply(embed = mapEmbed, mention_author = True)


    @isBots
    @commands.command(aliases = ["1v1map"])
    async def _1v1map(self, ctx):

        maps = ["Cave Map", "Cavern", "City vs. Nature", "Continent", "Desert vs. Grass", "Desert vs. Grass 2", "Desert vs. Grass 4", "Desert Vs. Grass Spiral", "Double Mansion", "Eygptian Expedition",  "Fantasy", "Fantasy 2", "France", "Gem Mine", "Germany Map", "Golf Course", "Golf Course 2", "Korea", "Last Red City", "Long Islands", "Mansion", "", "Mars", "Medieval Grounds", "Mesa", "Mexico", "Passage", "RETRO: Four Seasons", "Ryry's Oil Map", "Sand Bottom Forest", "Six Small Islands", "Three Corner Cave", "Two Islands Map", "USA vs. Russia", "Void Map"]

        selectedMap = random.choice(maps)

        mapEmbed=discord.Embed(title="Randomized 1v1 Tournaments Map:", description=f"{ctx.author.mention} Your randomized map is: {selectedMap}!", color=0xff0000)
        mapEmbed.set_image(url = self.mapImages[selectedMap])
        await ctx.message.reply(embed = mapEmbed, mention_author = True)


    @isBots
    @commands.command(aliases = ["2v2map"])
    async def _2v2map(self, ctx):

        maps = ["Divided Metropolis", "Middle East", "Ryry's Oil Map", "Snowy Islands", "Three Corner Cave", "Archipelago", "Arctic Circle", "Basalt Peninsula", "Cave Map", "Cavern", "City 3", "City vs. Nature", "Continent", "Corners", "Desert vs. Grass", "Desert vs. Grass 2", "Desert vs. Grass 3", "Desert vs. Grass 4", "Double Mansion", "Europe", "Fantasy", "Fantasy 2", "France", "Frozen River", "Gem Mine", "Germany Map", "Germany vs. France", "Golf Course", "Golf Course 2", "Igneous Islands/Magma", "Korea", "Lake City Map", "Lakebed", "Lasers", "Long Islands", "Mainland", "Mansion", "Mansion: Flooded", "Mars Canyons", "Mars Tunnels", "Maze", "Mesa", "Mexico", "Moon Surface", "Obsidian Atoll", "Passage", "Point blank", "RETRO: Cliffs", "RETRO: Four Seasons", "RETRO: Six Islands", "RETRO: The Moon", "River Banks", "Sand Bottom Forest", "Six Small Islands", "Soviet Union", "States", "Symmetry", "Twisting Isles", "Two Islands Map", "USA vs. Russia", "Void Map", "World"]
        
        selectedMap = random.choice(maps)
        mapEmbed=discord.Embed(title="Randomized 2v2 Tournaments Map:", description=f"{ctx.author.mention} Your randomized map is: {selectedMap}!", color=0xff0000)
        mapEmbed.set_image(url = self.mapImages[selectedMap])
        await ctx.message.reply(embed = mapEmbed, mention_author = True)


    @isBots
    @commands.command(aliases = ["teammap"])
    async def _teammap(self, ctx):
        
        maps = ["Archipelago", "Arctic Circle", "Basalt Peninsula", "Cave Map", "Cavern", "City 3", "City vs. Nature", "Continent", "Corners", "Desert vs. Grass", "Desert vs. Grass 2", "Desert vs. Grass 3", "Desert vs. Grass 4", "Double Mansion", "Europe", "Fantasy", "Fantasy 2", "France", "Frozen River", "Gem Mine", "Germany Map", "Germany vs. France", "Golf Course", "Golf Course 2", "Igneous Islands/Magma", "Korea", "Lake City Map", "Lakebed", "Lasers", "Long Islands", "Mainland", "Mansion", "Mansion: Flooded", "Mars Canyons", "Mars Tunnels", "Maze", "Mesa", "Mexico", "Moon Surface", "Obsidian Atoll", "Passage", "Point blank", "RETRO: Cliffs", "RETRO: Four Seasons", "RETRO: Six Islands", "RETRO: The Moon", "River Banks", "Sand Bottom Forest", "Six Small Islands", "Soviet Union", "States", "Symmetry", "Twisting Isles", "Two Islands Map", "USA vs. Russia", "Void Map", "World"]

        selectedMap = random.choice(maps)

        mapEmbed=discord.Embed(title="Randomized Team Tournaments Map:", description=f"{ctx.author.mention} Your randomized map is: {selectedMap}!", color=0xff0000)
        mapEmbed.set_image(url = self.mapImages[selectedMap])
        await ctx.message.reply(embed = mapEmbed, mention_author = True)

    @isTCG
    @commands.command(aliases=["cf"])
    async def coinflip(self, ctx):
        choices = ["Heads", "Tails"]
        await ctx.message.reply(random.choice(choices), mention_author = True)

def setup(bot):
    bot.add_cog(MapSelection(bot))