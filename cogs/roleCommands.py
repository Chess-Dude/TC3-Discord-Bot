import discord
from discord.ext import commands

class RoleCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot        
    
    def work_channel(ctx):
        return ctx.channel.id == 941567353672589322 or ctx.channel.id == 896440473659519057
    
    async def assign_roles(self, team_name, member1, member2, member3, member4, member5, member6, tournament_division, tournaments_captain_role_id, tournaments_co_captain_role_id, tournaments_role_id, tournaments_team):
        TCG = self.bot.get_guild(371817692199518240)
        tournaments_captain_role = discord.utils.get(TCG.roles, id=tournaments_captain_role_id)
        tournaments_co_captain_role = discord.utils.get(TCG.roles, id=tournaments_co_captain_role_id)
        tournaments_role = discord.utils.get(TCG.roles, id=tournaments_role_id)
        tournament_division_role = tournament_division
        
        await member1.add_roles(team_name)
        await member2.add_roles(team_name)
        await member3.add_roles(team_name)
        await member4.add_roles(team_name)
        await member5.add_roles(team_name)
        await member6.add_roles(team_name)

        await member1.add_roles(tournaments_role)
        await member2.add_roles(tournaments_role)
        await member3.add_roles(tournaments_role)
        await member4.add_roles(tournaments_role)
        await member5.add_roles(tournaments_role)
        await member6.add_roles(tournaments_role)

        await member1.add_roles(tournament_division_role)
        await member2.add_roles(tournament_division_role)
        await member3.add_roles(tournament_division_role)
        await member4.add_roles(tournament_division_role)
        await member5.add_roles(tournament_division_role)
        await member6.add_roles(tournament_division_role)

        await member1.add_roles(tournaments_captain_role)
        
        if tournaments_team: 
            await member2.add_roles(tournaments_co_captain_role)

    async def create_role(self, name, colour, role_divider_id):
        TCG = self.bot.get_guild(371817692199518240)
        role_divider = discord.utils.get(TCG.roles, id=role_divider_id)
        await TCG.create_role(name=name, colour=colour)
        team_name = discord.utils.get(TCG.roles, name=name)
        await team_name.edit(position=role_divider.position-1)
        
        return team_name

    async def create_team(self, ctx, name, colour, role_divider_id, member1, member2, member3, member4, member5, member6, tournament_division, tournaments_captain_role_id, tournaments_co_captain_role_id, tournaments_role_id, tournaments_team):
        if tournament_division.id == 649685824492929034 or tournament_division.id == 798776263040040980 or tournament_division.id == 649685682901483542 or tournament_division.id == 649684979357450282 or tournament_division.id == 649684758691053594:
            loading_message = await ctx.send("----------")
            team_name = await self.create_role(name, colour, role_divider_id)
            await self.assign_roles(team_name, member1, member2, member3, member4, member5, member6, tournament_division, tournaments_captain_role_id, tournaments_co_captain_role_id, tournaments_role_id, tournaments_team)
            await loading_message.edit(content=f"Team Created Successfully! ✅")

    async def disband_role(self, ctx, name, role_divider_top_id, role_divider_bottom_id, tournaments_captain_role_id, tournaments_co_captain_role_id, tournaments_role_id, tournaments_scout_division_role_id, tournaments_mid_division_role_id, tournaments_juggernaut_divion_role_id):
        response = await ctx.send("-----------") 
        TCG = self.bot.get_guild(371817692199518240)
        disbanded = False
        await response.edit(content="fetching roles...")
        team_role = name
        role_divider_top = discord.utils.get(TCG.roles, id=role_divider_top_id)
        role_divider_bottom = discord.utils.get(TCG.roles, id=role_divider_bottom_id)
        for team in range(role_divider_top.position-1, role_divider_bottom.position, -1):
            team_role_loop = discord.utils.get(TCG.roles, position=team)
            
            if team_role_loop == None:
                continue
            
            if team_role_loop.id == team_role.id:
                tournaments_captain_role = discord.utils.get(TCG.roles, id=tournaments_captain_role_id)
                tournaments_co_captain_role = discord.utils.get(TCG.roles, id=tournaments_co_captain_role_id)
                tournaments_role = discord.utils.get(TCG.roles, id=tournaments_role_id)
                tournaments_scout_divion_role = discord.utils.get(TCG.roles, id=tournaments_scout_division_role_id)
                tournaments_mid_division_role = discord.utils.get(TCG.roles, id=tournaments_mid_division_role_id)
                tournaments_juggernaut_divion_role = discord.utils.get(TCG.roles, id=tournaments_juggernaut_divion_role_id)
                await response.edit(content="removing roles...")
                for member in team_role.members:
                    if tournaments_captain_role in member.roles:
                        await member.remove_roles(tournaments_captain_role)
                    
                    if tournaments_co_captain_role in member.roles:
                        await member.remove_roles(tournaments_captain_role)

                    if tournaments_juggernaut_divion_role in member.roles:
                        await member.remove_roles(tournaments_juggernaut_divion_role)
                    
                    if tournaments_mid_division_role in member.roles:
                        await member.remove_roles(tournaments_mid_division_role)

                    if tournaments_scout_divion_role in member.roles:
                        await member.remove_roles(tournaments_scout_divion_role)

                    if tournaments_role in member.roles:
                        await member.remove_roles(tournaments_role)
                await response.edit(content="All roles removed successfully")
                await discord.Role.delete(team_role)
                await response.edit(content="Role deleted")
                disbanded = True
                if disbanded:
                    await response.edit(content="Team has been disbanded successfully ✅") 

                else: 
                    await ctx.send("Their was an error while disbanding team roles <@!621516858205405197>!")
                break
        
    is_work_channel = commands.check(work_channel)

    @is_work_channel
    @commands.command(aliases=["createrole2v2"])
    @commands.cooldown(1, 30, commands.BucketType.guild)
    async def create_2v2_role(self, ctx, name, member1: discord.Member, member2: discord.Member, member3: discord.Member, member4: discord.Member, colour: discord.Color, tournament_division: discord.Role):
        member5 = member4
        member6 = member4
        await ctx.send(f"{member1} {member2} {member3} {member4}")
        await self.create_team(ctx, name, colour, 707250483743424683, member1, member2, member3, member4, member5, member6, tournament_division, 896550746475077672, 716290546519244850, 896550133309775872, False)

    @is_work_channel
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.command(aliases=["createrole3v3"])
    async def create_team_role(self, ctx, name, member1: discord.Member, member2: discord.Member, member3: discord.Member, member4: discord.Member, member5: discord.Member, member6: discord.Member, colour: discord.Color, tournament_division: discord.Role):
        await self.create_team(ctx, name, colour, 707250485702426625, member1, member2, member3, member4, member5, member6, tournament_division, 649683977241886730, 716290546519244850, 896555065282818079, True)

    # @is_work_channel
    # @commands.cooldown(1, 30, commands.BucketType.guild)
    # @commands.command(aliases=["createroleclan"])
    # async def create_team_role(self, ctx, name, member1: discord.Member, member2: discord.Member, member3: discord.Member, member4: discord.Member, member5: discord.Member, member6: discord.Member, colour: discord.Color, tournament_division: discord.Role):
    #     await self.create_team(ctx, name, colour, 707250485702426625, member1, member2, member3, member4, member5, member6, tournament_division, 649683977241886730, 716290546519244850, 896555065282818079, True)

    @is_work_channel
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.command(aliases=["disband2v2"])
    async def disband_2v2(self, ctx, name: discord.Role):
        await self.disband_role(ctx, name, 707250483743424683, 665667383184326657, 896550746475077672, 896550746475077672, 896550133309775872, 649685824492929034, 798776263040040980, 649685682901483542)

    @is_work_channel
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.command(aliases=["disband3v3"])
    async def disband_team(self, ctx, name: discord.Role):
        await self.disband_role(ctx, name, 707250485702426625, 707250483743424683, 649683977241886730, 716290546519244850, 896555065282818079, 649684979357450282, 649684979357450282, 649684758691053594)

async def setup(bot):
    await bot.add_cog(RoleCommands(bot))

