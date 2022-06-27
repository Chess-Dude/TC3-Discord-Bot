from unicodedata import decimal
import discord
from discord.ext import commands
from discord import app_commands

class AdminCommands(commands.Cog):
    def __init__(
        self, 
        bot):
            self.bot = bot

    @commands.is_owner()
    @commands.command()
    async def remove_one_day_role(
        self, 
        ctx):
            await ctx.message.reply("...")
            TCG = ctx.guild
            group_role_list = []
            group_1_role = discord.utils.get(
                TCG.roles, 
                id=701251273349136456)
            group_21_role = discord.utils.get(
                TCG.roles, 
                id=871469192807870504) 
            
            for role_position in range(group_1_role.position, group_21_role.position-1, -1):
                group = discord.utils.get(
                    TCG.roles, 
                    position=role_position)
                group_role_list.append(group)

            one_day_tournament_role = discord.utils.get(TCG.roles, id=701251147046060092)
            backup_role = discord.utils.get(TCG.roles, id=912041460893884536)
            for member in one_day_tournament_role.members:
                if backup_role in member.roles:
                    await member.remove_roles(backup_role)

                for group in group_role_list:
                    if group in member.roles:
                        await member.remove_roles(group)
                        break
                
                await member.remove_roles(one_day_tournament_role)
            await ctx.send("removed all roles successfully")

async def setup(bot):
    await bot.add_cog(AdminCommands(bot))