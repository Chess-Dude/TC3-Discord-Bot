import discord, re
from discord.ext import commands

class MatchReminders(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def work_channel(ctx):
        return ctx.channel.id == 941567353672589322 or ctx.channel.id == 896440473659519057

    is_work_channel = commands.check(work_channel)

    @is_work_channel
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.command(aliases=["1v1remind"])
    async def _1v1_remind(self, ctx, args):
        member_list = re.split(',', args)
        response = await ctx.send(f"---------")
        for member_mention in member_list:
            member_mention = member_mention.replace('<', '')
            member_mention = member_mention.replace('>', '')
            member_mention = member_mention.replace('!', '')
            member_mention = member_mention.replace('@', '')
            member_obj = self.bot.get_user(int(member_mention))
            try:
                await member_obj.send("This is a automated **__REMINDER__** that you have **__1 day__** remaining to play your __1v1 Tournament Match__ for The Conquering Games. Please complete it and upload your results to the dedicated match result channel. If you fail to submit your match, you may be at risk for being __temporarily **BANNED** from **ALL** tournaments__.\n\nIf your opponent is not cooperating or you need a match extension, please direct message <@!621516858205405197> (Mind Gamer#5738).")
                await response.edit(content=f"{member_obj.mention} successfully dm'd ✅")
    
            except:
                await ctx.send(f"Could not DM {member_obj.mention} due to them having direct messages off.")

        await response.edit(content=f"All Players Have Been Reminded!")

    @is_work_channel
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.command(aliases=["2v2remind"])
    async def _2v2_remind(self, ctx, args):
        team_list = re.split(',', args)
        response = await ctx.send(f"---------")
        for team_mention in team_list:
            team_mention = team_mention.replace('<', '')
            team_mention = team_mention.replace('>', '')
            team_mention = team_mention.replace('&', '')
            team_mention = team_mention.replace('@', '')
            team = discord.utils.get(ctx.guild.roles, id=int(team_mention))
            for member in team.members:
                try:
                    await member.send("This is a automated **__REMINDER__** that you have **__1 day__** remaining to play your __2v2 Tournament Match__ for The Conquering Games. Please complete it and upload your results to the dedicated match result channel. If you fail to submit your match, you may be at risk for being __temporarily **BANNED** from **ALL** tournaments__.\n\nIf your opponent is not cooperating or you need a match extension, please direct message <@!621516858205405197> (Mind Gamer#5738).")
                    await response.edit(content=f"{team.mention} successfully dm'd ✅")
        
                except:
                    await ctx.send(f"There was an error while reminding users <@!621516858205405197>")
                    continue

        await response.edit(content=f"All Teams Have Been Reminded!")

    @is_work_channel
    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.command(aliases=["teamremind"])
    async def _2v2_remind(self, ctx, args):
        team_list = re.split(',', args)
        response = await ctx.send(f"---------")
        for team_mention in team_list:
            team_mention = team_mention.replace('<', '')
            team_mention = team_mention.replace('>', '')
            team_mention = team_mention.replace('&', '')
            team_mention = team_mention.replace('@', '')
            team = discord.utils.get(ctx.guild.roles, id=int(team_mention))
            for member in team.members:
                try:
                    await member.send("This is a automated **__REMINDER__** that you have **__1 day__** remaining to play your __Team Tournament Match__ for The Conquering Games. Please complete it and upload your results to the dedicated match result channel. If you fail to submit your match, you may be at risk for being __temporarily **BANNED** from **ALL** tournaments__.\n\nIf your opponent is not cooperating or you need a match extension, please direct message <@!621516858205405197> (Mind Gamer#5738).")
                    await response.edit(content=f"{team.mention} successfully dm'd ✅")
        
                except:
                    await ctx.send(f"There was an error while reminding users <@!621516858205405197>")
                    continue

        await response.edit(content=f"All Teams Have Been Reminded!")
            
async def setup(bot):
    await bot.add_cog(MatchReminders(bot))