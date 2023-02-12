import discord, datetime, time, pytz

from discord.ext import commands, tasks

class updateRosters(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.autoUpdateRosters.start()

    async def updateRostersClans(self):
        TC3_SERVER = self.bot.get_guild(350068992045744141)     
        clan_roster_channel = discord.utils.get(
            TC3_SERVER.channels, 
            id=1050289471498756177
        )

        embed_one = await clan_roster_channel.fetch_message(1054999094294220872)
        embed_two = await clan_roster_channel.fetch_message(1054999098404634675)

        top_role = discord.utils.get(
            TC3_SERVER.roles, 
            id=1053050572296704000
        )
        bottom_role = discord.utils.get(
            TC3_SERVER.roles, 
            id=1053050637555880027
        )
        clan_leader_role = discord.utils.get(
            TC3_SERVER.roles, 
            id=1054999374993817700
        )
        co_leader_role = discord.utils.get(
            TC3_SERVER.roles, 
            id=1054999381029429349
        )
        
        first_filled = False
        embed_text = ''
        clans_at_risk = ''
        
        for role_position in range(top_role.position-1, bottom_role.position, -1):
            member_text = "**Members:**"
            clan_leader = None
            co_leader = None
            clan = discord.utils.get(
                TC3_SERVER.roles, 
                position=role_position
            )
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

            embed_text = embed_text + f"\n\n**{clan.mention}\'s Roster:**\n**Leader:**\n{clan_leader}\n**Co-Leader:**\n{co_leader}\n{member_text}\n**Total Members: {total_clan_members}/6**"    
            if len(embed_text) > 3700:
                embed = discord.Embed(
                    title="The Conquering Games Clan Rosters (Organized alphabetically)", 
                    description=embed_text, 
                    color=0x00ffff
                )
                embed.set_footer(text="Last updated")
                embed.timestamp = datetime.datetime.utcnow()
                await embed_one.edit(embed=embed)
                first_filled = True
                embed_text = ''

        embed = discord.Embed(
            title="The Conquering Games Clan Rosters (Organized alphabetically)", 
            description=embed_text, 
            color=0x00ffff
        )
        embed.set_footer(text="Last updated")
        embed.timestamp = datetime.datetime.utcnow()

        if first_filled:
            await embed_two.edit(embed=embed)
            
        else:
            await embed_one.edit(embed=embed)

    @commands.is_owner()
    @commands.group()
    async def updateRosters(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.message.reply(content = '\'!updaterosters 2v2/team/clan\'', mention_author = False)

    @commands.is_owner()
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
                await self.updateRostersClans()

            except:
                print("rosters did not update, error in autoUpdateRosters")

    @autoUpdateRosters.before_loop
    async def wait_until_10pm(self):
        await self.bot.wait_until_ready()
        
async def setup(bot):
    await bot.add_cog(updateRosters(bot))