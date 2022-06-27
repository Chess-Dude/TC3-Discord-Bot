import discord, datetime, time, pytz

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
        rover_bypass_role = discord.utils.get(TCG.roles, id = 896476284220223499)

        embed_text_one = ''
        embed_text_two = ''
        embed_text_three = ''
        teams_at_risk = ''

        for role_position in range(top_role.position-1, bottom_role.position, -1):
            member_text = "**Members:**"
            captain = None
            team = discord.utils.get(TCG.roles, position = role_position)
            if team == None:
                continue
            team_members = team.members
            total_team_members = len(team_members)
            
            if total_team_members < 2:
               teams_at_risk = teams_at_risk + team.mention
            
            for member in team_members:
                
                if " | Team Captain" in member.display_name:
                    await member.edit(nick=member.display_name[:-len(" | Team Captain")])

                try:
                    if captain_role in member.roles:
                        captain = member.display_name + " - " + member.mention
                        team_members.remove(member)
                        await member.add_roles(rover_bypass_role)
                        await member.edit(nick=f"{member.display_name} | Team Captain")

                except:
                    print(f"{member.display_name}'s nickname could not be edited due to their nickname being too long.")

            if captain == None:
                captain = "N/A"

            if len(team_members) == 0:
                member_text = member_text + f"\nN/A"

            else:
                for member in team_members:
                    if " | Team Captain" in member.display_name:
                        member_display_name = member.display_name[:-len(" | Team Captain")]
                        member_text = member_text + f"\n{member_display_name} - {member.mention}"

                    elif " | Team Co-Captain" in member.display_name:
                        member_display_name = member.display_name[:-len(" | Team Co-Captain")]
                        member_text = member_text + f"\n{member_display_name} - {member.mention}"

                    else:
                        member_text = member_text + f"\n{member.display_name} - {member.mention}"
            
            if len(embed_text_one) < 3900:
                embed_text_one = embed_text_one + f"\n\n**{team.mention}\'s Roster:**\n**Captain:**\n{captain}\n{member_text}\n**Total Members: {total_team_members}/4**"    

            elif len(embed_text_one) > 3900 and len(embed_text_two) < 3900:
                embed_text_two = embed_text_two + f"\n\n**{team.mention}\'s Roster:**\n**Captain:**\n{captain}\n{member_text}\n**Total Members: {total_team_members}/4**"    

            elif len(embed_text_one) > 3900 and len(embed_text_two) > 3900 and len(embed_text_three) < 3900:
                embed_text_three = embed_text_three + f"\n\n**{team.mention}\'s Roster:**\n**Captain:**\n{captain}\n{member_text}\n**Total Members: {total_team_members}/4**"    

            else:
                print("an error occured in updaterosters 2v2")

    
        embed = discord.Embed(title="The Conquering Games 2v2 Rosters (Organized alphabetically)", description=embed_text_one, color=0xff0000)
        embed.set_footer(text="Last updated")
        embed.timestamp = datetime.datetime.utcnow()
        await embed_one.edit(embed=embed)

        embed = discord.Embed(title="The Conquering Games 2v2 Rosters (Organized alphabetically)", description=embed_text_two, color=0xff0000)
        embed.set_footer(text="Last updated")
        embed.timestamp = datetime.datetime.utcnow()
        await embed_two.edit(embed=embed)

        embed = discord.Embed(title="The Conquering Games 2v2 Rosters (Organized alphabetically)", description=embed_text_three, color=0xff0000)
        embed.set_footer(text="Last updated")
        embed.timestamp = datetime.datetime.utcnow()
        await embed_three.edit(embed=embed)

        if len(teams_at_risk) >= 1:
            await reminder_channel.send(f"{teams_at_risk}\n\nYour team has less than 2 players! Please add a member or your team will be disbanded.")
            time.sleep(100)

    async def updateRosters3v3(self):
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
        rover_bypass_role = discord.utils.get(TCG.roles, id = 896476284220223499)
        first_filled = False
        embed_text_one = ''
        embed_text_two = ''
        embed_text_three = ''
        teams_at_risk = ''
    
        for role_position in range(top_role.position-1, bottom_role.position, -1):

            member_text = "**Members:**"
            captain = None
            co_captain = None
            team = discord.utils.get(TCG.roles, position = role_position)
            if team == None:
                continue
            team_members = team.members
            total_team_members = len(team_members)
            
            if total_team_members < 3:
               teams_at_risk = teams_at_risk + team.mention

            for member in team_members:
                if " | Team Captain" in member.display_name:
                    await member.edit(nick=member.display_name[:-len(" | Team Captain")])
                    
                elif " | Team Co-Captain" in member.display_name:
                    await member.edit(nick=member.display_name[:-len(" | Team Co-Captain")])

                try:
                    if captain_role in member.roles:
                        team_members.remove(member)
                        captain = member.display_name + " - " + member.mention
                        await member.add_roles(rover_bypass_role)
                        await member.edit(nick=f"{member.display_name} | Team Captain")

                    elif co_captain_role in member.roles:
                        team_members.remove(member)
                        co_captain = member.display_name + " - " + member.mention
                        await member.add_roles(rover_bypass_role)
                        await member.edit(nick=f"{member.display_name} | Team Co-Captain")                        

                except:
                    print(f"{member.display_name}'s nickname could not be edited due to their nickname being too long.")     

            if captain == None:
                captain = "N/A"
            
            if co_captain == None:
                co_captain = "N/A"

            if len(team_members) == 0:
                member_text = member_text + f"\nN/A"

            else:
                for member in team_members:
                    if " | Team Captain" in member.display_name:
                        member_display_name = member.display_name[:-len(" | Team Captain")]
                        member_text = member_text + f"\n{member_display_name} - {member.mention}"

                    elif " | Team Co-Captain" in member.display_name:
                        member_display_name = member.display_name[:-len(" | Team Co-Captain")]
                        member_text = member_text + f"\n{member_display_name} - {member.mention}"

                    else:
                        member_text = member_text + f"\n{member.display_name} - {member.mention}"

            if len(embed_text_one) < 3800:
                embed_text_one = embed_text_one + f"\n\n**{team.mention}\'s Roster:**\n**Captain:**\n{captain}\n**Co-Captain:**\n{co_captain}\n{member_text}\n**Total Members: {total_team_members}/6**"
                
            elif len(embed_text_one) > 3800 and len(embed_text_two) < 3800:
                embed_text_two = embed_text_two + f"\n\n**{team.mention}\'s Roster:**\n**Captain:**\n{captain}\n**Co-Captain:**\n{co_captain}\n{member_text}\n**Total Members: {total_team_members}/6**"    
                
            elif len(embed_text_one) > 3800 and len(embed_text_two) > 3800 and len(embed_text_three) < 3800:
                embed_text_three = embed_text_three + f"\n\n**{team.mention}\'s Roster:**\n**Captain:**\n{captain}\n**Co-Captain:**\n{co_captain}\n{member_text}\n**Total Members: {total_team_members}/6**"    

            else:
                print("an error occured in updaterosters 3v3")

        embed = discord.Embed(title="The Conquering Games 3v3 Rosters (Organized alphabetically)", description=embed_text_one, color=0xff0000)
        embed.set_footer(text="Last updated")
        embed.timestamp = datetime.datetime.utcnow()
        await embed_one.edit(embed=embed)
        
        embed = discord.Embed(title="The Conquering Games 3v3 Rosters (Organized alphabetically)", description=embed_text_two, color=0xff0000)
        embed.set_footer(text="Last updated")
        embed.timestamp = datetime.datetime.utcnow()
        await embed_two.edit(embed=embed)

        embed = discord.Embed(title="The Conquering Games 3v3 Rosters (Organized alphabetically)", description=embed_text_three, color=0xff0000)
        embed.set_footer(text="Last updated")
        embed.timestamp = datetime.datetime.utcnow()
        await embed_three.edit(embed=embed)

        if len(teams_at_risk) >= 1:
            await reminder_channel.send(f"{teams_at_risk}\n\nYour 3v3 team has less than 3 players! Please add a member or your team will be disbanded.")
            time.sleep(100)

    async def updateRostersClans(self):
        TCG = self.bot.get_guild(371817692199518240)     
        reminder_channel = discord.utils.get(TCG.channels, id = 707220152625791047)
        clan_rosters = discord.utils.get(TCG.channels, id = 956406203943125004)
        embed_one = await clan_rosters.fetch_message(967235300172632064)
        embed_two = await clan_rosters.fetch_message(967235316501061643)
        embed_three = await clan_rosters.fetch_message(967235330669445162)
        top_role = discord.utils.get(TCG.roles, id = 421099292552331264)
        bottom_role = discord.utils.get(TCG.roles, id = 422255381721514014)
        clan_leader_role = discord.utils.get(TCG.roles, id = 896533899658821662)
        co_leader_role = discord.utils.get(TCG.roles, id = 896534077405032550)
        first_filled = False
        embed_text = ''
        clans_at_risk = ''
        
        for role_position in range(top_role.position-1, bottom_role.position, -1):
            member_text = "**Members:**"
            clan_leader = None
            co_leader = None
            clan = discord.utils.get(TCG.roles, position = role_position)
            if clan == None:
                continue
            clan_members = clan.members
            total_clan_members = len(clan.members)
        
            
            if total_clan_members < 5:
               clans_at_risk = clans_at_risk + clan.mention

            for member in clan_members:
                if clan_leader_role in member.roles:
                    clan_leader = member.display_name + " - " + member.mention
                    clan_members.remove(member)
                    break

            if clan_leader == None:
                clan_leader = "N/A"
            
            for member in clan_members:
                if co_leader_role in member.roles:
                    co_leader = member.display_name + " - " + member.mention
                    clan_members.remove(member)
                    break

            if co_leader_role == None:
                co_leader = 'N/A'

            if len(clan_members) == 0:
                member_text = member_text + f"\nN/A"

            else:
                for member in clan_members:
                    member_text = member_text + f"\n{member.display_name} - {member.mention}"

            embed_text = embed_text + f"\n\n**{clan.mention}\'s Roster:**\n**Leader:**\n{clan_leader}\n**Co-Leader:**\n{co_leader}\n{member_text}\n**Total Members: {total_clan_members}/10**"    
            if len(embed_text) > 3700:
                embed = discord.Embed(title="The Conquering Games Clan Rosters (Organized alphabetically)", description=embed_text, color=0xff0000)
                embed.set_footer(text = "Last updated")
                embed.timestamp = datetime.datetime.utcnow()
                await embed_one.edit(embed = embed)
                first_filled = True
                embed_text = ''

        embed = discord.Embed(title="The Conquering Games Clan Rosters (Organized alphabetically)", description=embed_text, color=0xff0000)
        embed.set_footer(text = "Last updated")
        embed.timestamp = datetime.datetime.utcnow()

        if first_filled:
            await embed_two.edit(embed=embed)
            
        else:
            await embed_one.edit(embed=embed)
            
        if len(clans_at_risk) >= 1:
            await reminder_channel.send(f"{clans_at_risk}\n\nYour clan has less than 5 players! Please add a member or your clan will be disbanded.")
            time.sleep(100)

    @isWorkChannel
    @commands.has_any_role(896440653406433310, 371840164672045067, 665951855888826369)
    @commands.group()
    async def updateRosters(self, ctx):
        
        if ctx.invoked_subcommand is None:
            await ctx.message.reply(content = '\'!updaterosters 2v2/team/clan\'', mention_author = False)


    @isWorkChannel
    @commands.has_any_role(896440653406433310, 371840164672045067, 665951855888826369)
    @commands.cooldown(1, 60, commands.BucketType.guild)
    @updateRosters.command(aliases = ['2v2'])
    async def _2v2(self, ctx):
        response = await ctx.send('----------')
        await self.updateRosters2v2()
        await response.edit(content = 'Updated :white_check_mark:')

    
    @isWorkChannel
    @commands.has_any_role(896440653406433310, 371840164672045067, 665951855888826369)
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @updateRosters.command(aliases = ['3v3'])
    async def _3v3(self, ctx):
        response = await ctx.send('----------')
        await self.updateRosters3v3()
        await response.edit(content = 'Updated :white_check_mark:')

    @isWorkChannel
    @commands.has_any_role(896440653406433310, 371840164672045067, 665951855888826369)
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
                await self.updateRosters3v3()
                await self.updateRostersClans()

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
