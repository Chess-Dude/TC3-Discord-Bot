import discord, datetime, pytz

from discord.ext import commands, tasks

class updateRosters(commands.Cog):
    
    
    def __init__(self, bot):
        self.bot = bot
        self.autoUpdateRosters.start()

    def workChannel(ctx):
        return ctx.channel.id == 896440473659519057 or ctx.channel.id == 811380456821227560 or ctx.channel.id == 941567353672589322

    isWorkChannel = commands.check(workChannel)

    async def updateRosters2v2(self):
            
        TCG = self.bot.get_guild(371817692199518240)     
        reminder_channel = discord.utils.get(TCG.channels, id = 666959897979781146)
        rosters_2v2 = discord.utils.get(TCG.channels, id = 874739232827113502)
        embed_one = await rosters_2v2.fetch_message(961670523593556018)
        embed_two = await rosters_2v2.fetch_message(961670524277227550)
        embed_three = await rosters_2v2.fetch_message(961670525082566656)
        top_role = discord.utils.get(TCG.roles, id = 707250483743424683)
        bottom_role = discord.utils.get(TCG.roles, id = 665667383184326657)
        captain_role = discord.utils.get(TCG.roles, id = 896550746475077672)
        first_filled = False
        embed_text = ''
        teams_at_risk = ''
        
        for role_position in range(top_role.position-1, bottom_role.position, -1):
            member_text = "**Members:**"
            captain = None
            team = discord.utils.get(TCG.roles, position = role_position)
            team_members = team.members
            total_team_members = len(team.members)
            
            if team == None:
                continue
            
            if total_team_members < 2:
               teams_at_risk = teams_at_risk + team.mention
                           
            for member in team_members:
                if captain_role in member.roles:
                    captain = member.display_name + " - " + member.mention
                    
                    team_members.remove(member)
                    break

            if captain == None:
                captain = "N/A"

            if len(team_members) == 0:
                member_text = member_text + f"\nN/A"

            else:
                for member in team_members:
                    member_text = member_text + f"\n{member.display_name} - {member.mention}"

            embed_text = embed_text + f"\n\n**{team.mention}\'s Roster:**\n**Captain:**\n{captain}\n{member_text}\n**Total Members: {total_team_members}**"    
            if len(embed_text) > 3700:
                embed = discord.Embed(title="The Conquering Games 2v2 Rosters (Organized alphabetically)", description=embed_text, color=0xff0000)
                embed.set_footer(text = 'Last updated')
                embed.timestamp = datetime.datetime.utcnow()
                await embed_one.edit(embed = embed)
                first_filled = True
                embed_text = ''

        embed = discord.Embed(title='The Conquering Games 2v2 Rosters (Organized alphabetically)', description=embed_text, color=0xff0000)
        embed.set_footer(text = 'Last updated')
        embed.timestamp = datetime.datetime.utcnow()

        if first_filled:
            await embed_two.edit(embed=embed)
            
        else:
            await embed_one.edit(embed=embed)
        
        if len(teams_at_risk) >= 1:
            await reminder_channel.send(f"{teams_at_risk}\n\nYour team has less than 2 players! Please add a member or your team will be disbanded.")

    async def updateRostersTeam(self):
        TCG = self.bot.get_guild(371817692199518240)     
        reminder_channel = discord.utils.get(TCG.channels, id = 666957650717835265)
        rosters_team = discord.utils.get(TCG.channels, id = 876696917260771339)
        embed_one = await rosters_team.fetch_message(961688043801161809)
        embed_two = await rosters_team.fetch_message(961688046238060584)
        embed_three = await rosters_team.fetch_message(961688046808465468)
        top_role = discord.utils.get(TCG.roles, id = 707250485702426625)
        bottom_role = discord.utils.get(TCG.roles, id = 707250483743424683)
        captain_role = discord.utils.get(TCG.roles, id = 649683977241886730)
        co_captain_role = discord.utils.get(TCG.roles, id = 716290546519244850)
        first_filled = False
        embed_text = ''
        teams_at_risk = ''
        
        for role_position in range(top_role.position-1, bottom_role.position, -1):
            member_text = "**Members:**"
            captain = None
            co_captain = None
            team = discord.utils.get(TCG.roles, position = role_position)
            team_members = team.members
            total_team_members = len(team.members)
            
            
            if team == None:
                continue
            
            if total_team_members < 3:
               teams_at_risk = teams_at_risk + team.mention

            for member in team_members:
                if captain_role in member.roles:
                    captain = member.display_name + " - " + member.mention
                    
                    team_members.remove(member)
                    break

            if captain == None:
                captain = "N/A"
            
            for member in team_members:
                if co_captain_role in member.roles:
                    co_captain = member.display_name + " - " + member.mention
                    team_members.remove(member)
                    break

            if co_captain == None:
                co_captain = 'N/A'

            if len(team_members) == 0:
                member_text = member_text + f"\nN/A"

            else:
                for member in team_members:
                    member_text = member_text + f"\n{member.display_name} - {member.mention}"

            embed_text = embed_text + f"\n\n**{team.mention}\'s Roster:**\n**Captain:**\n{captain}\n**Co-Captain:**\n{co_captain}\n{member_text}\n**Total Members: {total_team_members}**"    
            if len(embed_text) > 3700:
                embed = discord.Embed(title="The Conquering Games Team Rosters (Organized alphabetically)", description=embed_text, color=0xff0000)
                embed.set_footer(text = "Last updated")
                embed.timestamp = datetime.datetime.utcnow()
                await embed_one.edit(embed = embed)
                first_filled = True
                embed_text = ''

        embed = discord.Embed(title="The Conquering Games Team Rosters (Organized alphabetically)", description=embed_text, color=0xff0000)
        embed.set_footer(text = "Last updated")
        embed.timestamp = datetime.datetime.utcnow()

        if first_filled:
            await embed_two.edit(embed=embed)
            
        else:
            await embed_one.edit(embed=embed)
            
        if len(teams_at_risk) >= 1:
            await reminder_channel.send(f"{teams_at_risk}\n\nYour team has less than 3 players! Please add a member or your team will be disbanded.")


    async def updateRostersClans(self):
        TCG = self.bot.get_guild(371817692199518240)     
        clanRostersChannel = discord.utils.get(TCG.channels, id = 956406203943125004) 
        embedOne = await clanRostersChannel.fetch_message(956433121195196467)
        embedTwo = await clanRostersChannel.fetch_message(956433199146340432)
        topRole = discord.utils.get(TCG.roles, id = 421099292552331264)
        bottomRole = discord.utils.get(TCG.roles, id = 422255381721514014)
        embedtext = ''
        clanLeader = discord.utils.get(TCG.roles, id = 896533899658821662)
        clanCoLeader = discord.utils.get(TCG.roles, id = 896534077405032550)
        firstFilled = False

        for role_position in range(topRole.position-1, bottomRole.position, -1):

            membertext = '**Members:**'
            leader = None
            coLeader = None
            team = discord.utils.get(TCG.roles, position = role_position)

            if team == None:
                continue
                    
            members = team.members

            for member in members:
                if clanLeader in member.roles:
                    leader = member.display_name + " - " + member.mention
                    members.remove(member)
                    break

            if leader == None:
                leader = 'N/A'    

            for member in members:
                if clanCoLeader in member.roles:
                    coLeader = member.display_name + " - " + member.mention
                    members.remove(member)
                    break

            if coLeader == None:
                coLeader = 'N/A'

            if len(members) == 0:
                membertext = membertext + f'\nN/A'

            else:
                for member in members:
                    membertext = membertext + f'\n{member.display_name} - {member.mention}'

            embedtext = embedtext + f'\n\n**{team.mention}\'s Roster:**\n**Clan Leader:**\n{leader}\n**Clan Co-Leader:**\n{coLeader}\n{membertext}'
            if len(embedtext) > 3700:
                embed = discord.Embed(title='The Conquering Games Clan Rosters (Organized alphabetically)', description=embedtext, color=0xff0000)
                embed.set_footer(text = 'Last updated')
                embed.timestamp = datetime.datetime.utcnow()
                await embedOne.edit(embed = embed)
                firstFilled = True
                embedtext = ""

        embed = discord.Embed(title='The Conquering Games Clan Rosters (Organized alphabetically)', description=embedtext, color=0xff0000)
        embed.set_footer(text = 'Last updated')
        embed.timestamp = datetime.datetime.utcnow()

        if firstFilled:
            await embedTwo.edit(embed = embed)
            #await ctx.message.reply(embed = embed)
        else:
            await embedOne.edit(embed = embed)
            #await ctx.message.reply(embed = embed)
        
    @isWorkChannel
    @commands.has_any_role(896440653406433310, 371840164672045067, 665951855888826369, 899424078836936705) #last one is my server role
    @commands.group()
    async def updateRosters(self, ctx):
        
        if ctx.invoked_subcommand is None:
            await ctx.message.reply(content = '\'!updaterosters 2v2/team/clan\'', mention_author = False)


    @isWorkChannel
    @commands.has_any_role(896440653406433310, 371840164672045067, 665951855888826369, 899424078836936705) #last one is my server role
    @commands.cooldown(1, 60, commands.BucketType.guild)
    @updateRosters.command(aliases = ['2v2'])
    async def _2v2(self, ctx):
        response = await ctx.send('----------')
        await self.updateRosters2v2()
        await response.edit(content = 'Updated :white_check_mark:')

    
    @isWorkChannel
    @commands.has_any_role(896440653406433310, 371840164672045067, 665951855888826369, 899424078836936705) #last one is my role
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @updateRosters.command()
    async def team(self, ctx):
        response = await ctx.send('----------')
        await self.updateRostersTeam()
        await response.edit(content = 'Updated :white_check_mark:')

    @isWorkChannel
    @commands.has_any_role(896440653406433310, 371840164672045067, 665951855888826369, 899424078836936705) #last one is my role
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @updateRosters.command()
    async def clan(self, ctx):
        response = await ctx.send('----------')
        await self.updateRostersClans()
        await response.edit(content = 'Updated :white_check_mark:')

    @tasks.loop(seconds=1.0)
    async def autoUpdateRosters(self):
        now = datetime.datetime.now(pytz.timezone('UTC'))
        time_stamps = []
        time_stamps.append(now.replace(hour=2, minute=0, second=0))
        time_stamps.append(now.replace(hour=14, minute=0, second=0))
        
        if now in time_stamps:
            try:
                await self.updateRosters2v2()
                await self.updateRostersTeam()

            except:
                print("rosters did not update, error in autoUpdateRosters")

    @autoUpdateRosters.before_loop
    async def wait_until_10pm(self):
        await self.bot.wait_until_ready()
    
    @commands.is_owner()
    @commands.command()
    async def testRosters(cself, ctx, role: discord.Role):
        members = "".join(f'{member.display_name}' for member in role.members)
        await ctx.send(members)
                
async def setup(bot):
    await bot.add_cog(updateRosters(bot))
