import discord, random, json, datetime
from discord.ext import commands


class MapSelection(commands.Cog):

    def __init__(self, bot):

        self.bot = bot    
        with open("mapList.json", 'r') as config_reader:
            self.mapImages = json.loads(config_reader.read())
    
    def TC3OrTCGBots(ctx):
        return ctx.channel.id == 941567353672589322 or ctx.channel.id == 408820459279220736 or ctx.channel.id == 351057167706619914

    isBots = commands.check(TC3OrTCGBots)
    
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

        maps = ["British Isles", "Cave Map", "Cavern", "City vs. Nature", "Continent", "Desert vs. Grass", "Desert vs. Grass 2", "Desert vs. Grass 4", "Desert Vs. Grass Spiral", "Double Mansion", "Eygptian Expedition",  "Fantasy", "Fantasy 2", "France", "Gem Mine", "Germany Map", "Golf Course", "Golf Course 2", "Korea", "Last Red City", "Long Islands", "Mansion", "", "Mars", "Medieval Grounds", "Mesa", "Mexico", "Passage", "RETRO: Four Seasons", "Ryry's Oil Map", "Sand Bottom Forest", "Six Small Islands", "Three Corner Cave", "Two Islands Map", "USA vs. Russia", "Void Map"]

        selectedMap = random.choice(maps)

        mapEmbed=discord.Embed(title="Randomized 1v1 Map:", description=f"{ctx.author.mention} Your randomized map is: {selectedMap}!", color=0xff0000)
        mapEmbed.set_image(url = self.mapImages[selectedMap])
        await ctx.message.reply(embed = mapEmbed, mention_author = True)

    @isBots
    @commands.command(aliases = ["2v2map"])
    async def _2v2map(self, ctx):

        maps = ["Arctic Canal Map", "Basalt Peninsula", "British Isles", "Cavern", "Continent", "Desert vs. Grass", "Desert vs. Grass 2", "Desert vs. Grass 3", "Desert vs. Grass Spiral", "Europe", "Fantasy", "Fantasy 2", "France", "Germany Map", "Golf Course", "Ice Catalyst", "Korea", "Lakebed", "Lasers", "Mainland", "Mansion: Flooded", "Mesa", "Mexico", "Passage", "River Banks", "Sandy Floors", "Six Small Islands", "Snow Battlefield", "Soviet Union", "USA vs. Russia", "Void Map", "World", "", "", "", "",]
        
        selectedMap = random.choice(maps)
        print(selectedMap, datetime.datetime.utcnow)
        mapEmbed=discord.Embed(title="Randomized 2v2 Map:", description=f"{ctx.author.mention} Your randomized map is: {selectedMap}!", color=0xff0000)
        mapEmbed.set_image(url = self.mapImages[selectedMap])
        await ctx.message.reply(embed = mapEmbed, mention_author = True)

    @isBots
    @commands.command(aliases = ["3v3map"])
    async def _3v3map(self, ctx):
        
        maps = ["Archipelago", "Arctic Canal Map", "Arctic Circle", "Basalt Peninsula", "British Isles", "Cave Map", "Cavern", "City 3", "City vs. Nature", "Continent", "Corners", "Desert vs. Grass", "Desert vs. Grass 2", "Desert vs. Grass 3", "Desert vs. Grass 4", "Double Mansion", "Europe", "Fantasy", "Fantasy 2", "France", "Frozen River", "Gem Mine", "Germany Map", "Germany vs. France", "Golf Course", "Golf Course 2", "Ice Catalyst", "Igneous Islands/Magma", "Korea", "Lake City Map", "Lakebed", "Lasers", "Long Islands", "Mainland", "Mansion", "Mansion: Flooded", "Mars Canyons", "Mars Tunnels", "Maze", "Mesa", "Mexico", "Moon Surface", "Obsidian Atoll", "Passage", "Point blank", "RETRO: Cliffs", "RETRO: Four Seasons", "RETRO: Six Islands", "RETRO: The Moon", "River Banks", "Sand Bottom Forest", "Sandy Floors", "Six Small Islands", "Snow Battlefield", "Soviet Union", "States", "Symmetry", "Twisting Isles", "Two Islands Map", "USA vs. Russia", "Void Map", "World"]

        selectedMap = random.choice(maps)

        mapEmbed=discord.Embed(title="Randomized 3v3 Map:", description=f"{ctx.author.mention} Your randomized map is: {selectedMap}!", color=0xff0000)
        mapEmbed.set_image(url = self.mapImages[selectedMap])
        await ctx.message.reply(embed = mapEmbed, mention_author = True)

    @isBots
    @commands.command(aliases = ["4v4map"])
    async def _4v4map(self, ctx):
        
        maps = ["Archipelago", "Arctic Canal Map", "Arctic Circle", "Basalt Peninsula", "British Isles", "Cave Map", "Cavern" "Desert vs. Grass", "Desert vs. Grass 2", "Desert vs. Grass 3", "Desert vs. Grass 4", "Double Mansion", "Europe", "Fantasy", "Fantasy 2", "France", "Frozen River", "Gem Mine", "Germany Map", "Germany vs. France", "Golf Course", "Golf Course 2", "Ice Catalyst", "Igneous Islands/Magma", "Korea", "Lakebed", "Lasers", "Long Islands", "Mainland", "Mansion", "Mars 4", "Mars Canyons", "Maze", "Mesa", "Mexico", "Middle East", "Obsidian Atoll", "Passage", "Point blank", "River Banks", "Sand Bottom Forest", "Sandy Floors", "Six Small Islands", "Snow Battlefield", "Soviet Union", "States", "USA vs. Russia", "World"]

        selectedMap = random.choice(maps)

        mapEmbed=discord.Embed(title="Randomized 4v4 Map:", description=f"{ctx.author.mention} Your randomized map is: {selectedMap}!", color=0xff0000)
        mapEmbed.set_image(url = self.mapImages[selectedMap])
        await ctx.message.reply(embed = mapEmbed, mention_author = True)    

    @isBots
    @commands.command(aliases = ["5v5map"])
    async def _5v5map(self, ctx):
        
        maps = ["Archipelago", "Desert vs. Grass", "Desert vs. Grass 2", "Double Mansion", "Gem Mine", "Mediterranean", "Soviet Union", "States", "World"]

        selectedMap = random.choice(maps)

        mapEmbed=discord.Embed(title="Randomized 5v5 Map:", description=f"{ctx.author.mention} Your randomized map is: {selectedMap}!", color=0xff0000)
        mapEmbed.set_image(url = self.mapImages[selectedMap])
        await ctx.message.reply(embed = mapEmbed, mention_author = True)    

    @isBots
    @commands.command(aliases=["cf"])
    async def coinflip(self, ctx):
        choices = ["Heads", "Tails"]
        await ctx.message.reply(random.choice(choices), mention_author = True)

def setup(bot):
    bot.add_cog(MapSelection(bot))