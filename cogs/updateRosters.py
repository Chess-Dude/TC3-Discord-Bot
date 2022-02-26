import discord, datetime, pytz

from discord.ext import commands, tasks

def workChannel(ctx):
    return ctx.channel.id == 896440473659519057 or ctx.channel.id == 811380456821227560

isWorkChannel = commands.check(workChannel)

async def updateRosters2v2(TCG : discord.Guild):

    _2v2rosters = discord.utils.get(TCG.channels, id = 874739232827113502)
    embedOne = await _2v2rosters.fetch_message(876695076389146624)
    embedTwo = await _2v2rosters.fetch_message(932030864173432833)
    topRole = discord.utils.get(TCG.roles, id = 707250483743424683)
    bottomRole = discord.utils.get(TCG.roles, id = 665667383184326657)
    embedtext = ''
    _2v2Captain = discord.utils.get(TCG.roles, id = 896550746475077672)
    firstFilled = False
        
    for role_position in range(topRole.position-1, bottomRole.position, -1):
        membertext = '**Members:**'
        captain = None
        team = discord.utils.get(TCG.roles, position = role_position)

        if team == None:
            continue

        members = team.members

        for member in members:
            if _2v2Captain in member.roles:
                captain = member.display_name + " - " + member.mention
                members.remove(member)
                break

        if captain == None:
            captain = 'N/A'

        if len(members) == 0:
            membertext = membertext + f'\nN/A'

        else:
            for member in members:
                membertext = membertext + f'\n{member.display_name}'

        embedtext = embedtext + f'\n\n**{team.mention}\'s Roster:**\n**Captain:**\n{captain}\n{membertext}'
        if len(embedtext) > 3700:
            embed = discord.Embed(title='The Conquering Games 2v2 Rosters (Organized alphabetically)', description=embedtext, color=0xff0000)
            embed.set_footer(text = 'Last updated')
            embed.timestamp = datetime.datetime.utcnow()
            await embedOne.edit(embed = embed)
            firstFilled = True
            embedtext = ""

    embed = discord.Embed(title='The Conquering Games 2v2 Rosters (Organized alphabetically)', description=embedtext, color=0xff0000)
    embed.set_footer(text = 'Last updated')
    embed.timestamp = datetime.datetime.utcnow()

    if firstFilled:
        await embedTwo.edit(embed = embed)
    else:
        await embedOne.edit(embed = embed)

async def updateRostersTeam(TCG : discord.Guild):

    teamRosters = discord.utils.get(TCG.channels, id = 876696917260771339)
    embedOne = await teamRosters.fetch_message(876704301744009226)
    topRole = discord.utils.get(TCG.roles, id = 707250485702426625)
    bottomRole = discord.utils.get(TCG.roles, id = 707250483743424683)
    embedtext = ''
    teamCaptain = discord.utils.get(TCG.roles, id = 649683977241886730)
    teamCoCaptain = discord.utils.get(TCG.roles, id = 716290546519244850)

    for role_position in range(topRole.position-1, bottomRole.position, -1):

        membertext = '**Members:**'
        captain = None
        coCaptain = None
        team = discord.utils.get(TCG.roles, position = role_position)

        if team == None:
            continue
                
        members = team.members

        for member in members:
            if teamCaptain in member.roles:
                captain = member.display_name + " - " + member.mention
                members.remove(member)
                break

        if captain == None:
            captain = 'N/A'    

        for member in members:
            if teamCoCaptain in member.roles:
                coCaptain = member.display_name + " - " + member.mention
                members.remove(member)
                break

        if coCaptain == None:
            coCaptain = 'N/A'

        if len(members) == 0:
            membertext = membertext + f'\nN/A'

        else:
            for member in members:
                membertext = membertext + f'\n{member.display_name}'

        embedtext = embedtext + f'\n\n**{team.mention}\'s Roster:**\n**Captain:**\n{captain}\n**Co-Captain:**\n{coCaptain}\n{membertext}'

    embed = discord.Embed(title='The Conquering Games Team Rosters (Organized alphabetically)', description=embedtext, color=0xff0000)
    embed.set_footer(text = 'Last updated')
    embed.timestamp = datetime.datetime.utcnow()
    await embedOne.edit(embed = embed)

class updateRosters(commands.Cog):
    
    
    def __init__(self, bot):
        self.bot = bot
        self.autoUpdateRosters.start()

    @isWorkChannel
    @commands.has_any_role(896440653406433310, 371840164672045067, 665951855888826369, 899424078836936705) #last one is my server role
    @commands.group()
    async def updateRosters(self, ctx):
        
        if ctx.invoked_subcommand is None:
            await ctx.message.reply(content = '\'!updaterosters 2v2/team\'', mention_author = False)


    @isWorkChannel
    @commands.has_any_role(896440653406433310, 371840164672045067, 665951855888826369, 899424078836936705) #last one is my server role
    @commands.cooldown(1, 60, commands.BucketType.guild)
    @updateRosters.command(aliases = ['2v2'])
    async def _2v2(self, ctx):
        TCG = self.bot.get_guild(371817692199518240)
        response = await ctx.send('----------')
        await updateRosters2v2(TCG)
        await response.edit(content = 'Updated :white_check_mark:')

    
    @isWorkChannel
    @commands.has_any_role(896440653406433310, 371840164672045067, 665951855888826369, 899424078836936705) #last one is my role
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @updateRosters.command()
    async def team(self, ctx):
        TCG = self.bot.get_guild(371817692199518240)
        response = await ctx.send('----------')
        await updateRostersTeam(TCG)
        await response.edit(content = 'Updated :white_check_mark:')

    @tasks.loop(hours = 24)
    async def autoUpdateRosters(self):
        TCG = self.bot.get_guild(371817692199518240)
        await updateRosters2v2(TCG)
        await updateRostersTeam(TCG)


    @autoUpdateRosters.before_loop
    async def wait_until_10pm(self):
        now = datetime.datetime.now(pytz.timezone("US/Eastern"))
        next_run = now.replace(hour=22, minute=0, second=0)

        if next_run < now:
            next_run += datetime.timedelta(days=1)

        await discord.utils.sleep_until(next_run)

def setup(bot):
    bot.add_cog(updateRosters(bot))