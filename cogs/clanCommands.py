import discord, typing, mysql.connector, os
from discord import app_commands
from discord.ext import commands
from cogs.teamApplicationClasses.teamCreation import TeamCreation
from .clanClasses.clanApplicationClasses.clanCreationMethods import ClanCreationMethods
from .clanClasses.clanApplicationClasses.clanChangeMethods import ClanChangesMethods
from .clanClasses.clanApplicationClasses.clanDisbandMethods import ClanDisbandMethods
from .clanClasses.clanRosterClasses.generateClanRoster import GenerateClanRoster
from dotenv import load_dotenv

class ClanCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        load_dotenv()
        # self.mydb = mysql.connector.connect(
        #     host=os.getenv("IP_ADDRESS"),
        #     user=os.getenv("DB_USERNAME"),
        #     password=os.getenv("DB_PASSWORD"),
        #     database="clanPointDatabase"
        # )

        # self.cursor = self.mydb.cursor() 

    def bots_or_work_channel(interaction):
        return interaction.channel.id == 941567353672589322 or interaction.channel.id == 896440473659519057 or interaction.channel.id == 351057167706619914

    clan_group = app_commands.Group(
        name="clan", 
        description="A Command That Allows You To Submit A Clan Application!",
        guild_ids=[350068992045744141])
    
    @app_commands.check(bots_or_work_channel)
    @clan_group.command(
        name="application",
        description="A Command That Allows You To Submit A 3v3 Tournament Application!")
    @app_commands.describe(clan_leader="Ping Your Team Clan Leader Here!")
    @app_commands.describe(clan_co_leader="Ping Your Clan Co-Leader Here!")
    @app_commands.describe(clan_member_1="Ping Your 1st Clan Member Here!")
    @app_commands.describe(clan_member_2="Ping Your 2nd Clan Member Here!")
    @app_commands.describe(clan_member_3="Ping Your 3rd Clan Member Here!")
    @app_commands.describe(clan_member_4="Ping Your 4th Clan Member Here!")
    @app_commands.rename(clan_leader="clan_leader")
    @app_commands.rename(clan_co_leader="clan_co_leader")
    @app_commands.rename(clan_member_1="clan_member_1")
    @app_commands.rename(clan_member_2="clan_member_2")
    @app_commands.rename(clan_member_3="clan_member_3")
    @app_commands.rename(clan_member_4="clan_member_4")
    async def clan_application(        
        self,
        interaction: discord.Interaction,
        clan_name: str,
        clan_color: str,
        clan_leader: discord.Member,
        clan_co_leader: discord.Member,
        clan_member_1: discord.Member,
        clan_member_2: discord.Member,
        clan_member_3: typing.Optional[discord.Member],
        clan_member_4: typing.Optional[discord.Member]
    ):
            clan_roster = [clan_leader, clan_co_leader, clan_member_1, clan_member_2, clan_member_3, clan_member_4]

            all_members_verified = await TeamCreation.check_verified(
                self,
                interaction=interaction, 
                team_roster=clan_roster
            )

            if all_members_verified:
                clan_color = await ClanCreationMethods.colour_converter(
                    self,
                    clan_color=clan_color
                )

                await ClanCreationMethods.application_log_embed(
                    self,
                    interaction=interaction,
                    clan_name=clan_name,
                    clan_color=str(clan_color),
                    clan_roster=clan_roster,
                    pool=self.bot.pool
                )

                await TeamCreation.success_embed(
                    self,
                    interaction=interaction,
                    description=f"{interaction.user.mention} Thank You For Submitting Your Clan Application!"
                )
            

    @app_commands.check(bots_or_work_channel)
    @clan_group.command(
        name="leave",
        description="A Command That Alows You To Leave Your Clan!")
    async def clan_change(
        self,
        interaction: discord.Interaction
    ): 
        success_embed = discord.Embed(
            title="Your Clan Has Been Updated!",
            description="Your Clan Has Been Updated With The According Changes",
            color=0x00ffff
        )

        await interaction.response.send_message(embed=success_embed)

        clan_role = await ClanChangesMethods.get_clan_role(
            self=self,
            interaction=interaction,
            top_role_divider=interaction.guild.get_role(1053050572296704000),
            bottom_role_divider=interaction.guild.get_role(1053050637555880027)
        )
        if clan_role != None:
            clan_leader_role = interaction.guild.get_role(1054999374993817700)
            clan_co_leader_role = interaction.guild.get_role(1054999381029429349)
            roles_to_remove = [clan_role, clan_co_leader_role, clan_leader_role]            
            await ClanChangesMethods.remove_clan_member(
                self=self,
                interaction=interaction,
                roles_to_remove=roles_to_remove,
                remove_clan_member=interaction.user,
                pool=self.bot.pool
            )


    @app_commands.check(bots_or_work_channel)
    @app_commands.checks.has_any_role(1054999374993817700, 1054999381029429349)
    @clan_group.command(
        name="change",
        description="A Command That Alows You To Make Changes To Your Clan!")
    @app_commands.describe(new_clan_hex_color="Put Your New Clan Hex Color Here!")
    @app_commands.describe(new_clan_leader="Ping Your New Clan Leader Here!")
    @app_commands.describe(new_clan_co_leader="Ping Your New Clan Co-Leader Here!")
    @app_commands.describe(new_clan_member="Ping A Member You Would Like To Add To Your Clan!")
    @app_commands.describe(remove_clan_member="Ping A Member You Would Like To Remove From Your Clan")    
    @app_commands.rename(new_clan_hex_color="new_clan_hex_color")
    @app_commands.rename(new_clan_leader="new_clan_leader")
    @app_commands.rename(new_clan_co_leader="new_clan_co_leader")
    @app_commands.rename(new_clan_member="new_clan_member")
    @app_commands.rename(remove_clan_member="remove_clan_member")
    async def clan_change(
        self,
        interaction: discord.Interaction,
        new_clan_hex_color: typing.Optional[str],
        new_clan_leader: typing.Optional[discord.Member],
        new_clan_co_leader: typing.Optional[discord.Member],
        new_clan_member: typing.Optional[discord.Member],
        remove_clan_member: typing.Optional[discord.Member]
    ):    
        
        success_embed = discord.Embed(
            title="Your Clan Has Been Updated!",
            description="Your Clan Has Been Updated With The According Changes",
            color=0x00ffff
        )

        update_embed = discord.Embed(
            title="Your Clan Has Been Updated with the following changes:",
            description="Updated clan",
            color=0x2f3136
        )

        await interaction.response.send_message(embed=success_embed)

        clan_role = await ClanChangesMethods.get_clan_role(
            self=self,
            interaction=interaction,
            top_role_divider=interaction.guild.get_role(1053050572296704000),
            bottom_role_divider=interaction.guild.get_role(1053050637555880027)
        )

        clans_role_ping = interaction.guild.get_role(1057043814797295646)

        clan_leader_role = interaction.guild.get_role(1054999374993817700) 
        clan_co_leader_role = interaction.guild.get_role(1054999381029429349)
        if ((clan_leader_role in interaction.user.roles) or 
        (clan_co_leader_role in interaction.user.roles)):

            clan_roster = [new_clan_leader, new_clan_co_leader, new_clan_member]

            all_members_verified = await TeamCreation.check_verified(
                self,
                interaction=interaction, 
                team_roster=clan_roster
            )

            if new_clan_hex_color != None:            
                new_clan_hex_color = await ClanCreationMethods.colour_converter(
                    self=self,
                    clan_color=new_clan_hex_color
                )

                await ClanChangesMethods.update_clan_hex_color(
                    self=self,
                    clan_role=clan_role,
                    new_tournament_team_hex_color=discord.Color.from_str(new_clan_hex_color)
                )

                update_embed.add_field(
                    name="Color:",
                    value=f"Changed to {new_clan_hex_color}"
                )

            if new_clan_leader != None and all_members_verified:
                if clan_role in new_clan_leader.roles:
                    roles_to_config = [clan_role, clan_leader_role, clans_role_ping]            
                    
                    await ClanChangesMethods.update_clan_leader(
                        self=self,
                        interaction=interaction,
                        roles_to_config=roles_to_config,
                        new_clan_leader=new_clan_leader,
                    )

                    update_embed.add_field(
                        name="New Leader:",
                        value=f"Changed to {new_clan_leader.mention}"
                    )

                else:
                    await interaction.channel.send("Error: The new clan leader must be an existing clan member.")
                    return                
            
            if new_clan_co_leader != None and all_members_verified:
                if clan_role in new_clan_co_leader.roles:
                    roles_to_add = [clan_role, clan_co_leader_role, clan_leader_role, clans_role_ping]            

                    await ClanChangesMethods.update_clan_co_leader(
                        self=self,
                        roles_to_add=roles_to_add,
                        new_clan_co_leader=new_clan_co_leader,
                    )

                    update_embed.add_field(
                        name="New Co-Leader:",
                        value=f"Changed to {new_clan_co_leader.mention}"
                    )

                else:
                    await interaction.channel.send("Error: The new clan leader must be an existing clan member.")
                    return
                
            if new_clan_member != None and all_members_verified:
                if len(clan_role.members) < 10: 
                    roles_to_add = [clan_role, clans_role_ping]
                    await ClanChangesMethods.add_clan_member(
                        self=self,
                        roles_to_add=roles_to_add,
                        new_clan_member=new_clan_member,
                        pool=self.bot.pool
                    )
                    
                    update_embed.add_field(
                        name="New Member:",
                        value=f"Added {new_clan_member.mention}"
                    )
                
                else:
                    await interaction.channel.send(content="Error: You have 10 People in your clan. Please remove a member and retry")

        if remove_clan_member != None:
            if clan_role in remove_clan_member.roles:
                clan_leader_role = interaction.guild.get_role(1054999374993817700)
                clan_co_leader_role = interaction.guild.get_role(1054999381029429349)
                roles_to_remove = [clan_role, clan_co_leader_role, clan_leader_role]            
                await ClanChangesMethods.remove_clan_member(
                    self=self,
                    interaction=interaction,
                    roles_to_remove=roles_to_remove,
                    remove_clan_member=remove_clan_member,
                    pool=self.bot.pool
                )
                
                update_embed.add_field(
                    name="Remove Member:",
                    value=f"Removed {remove_clan_member.mention}"
                )
            
            else:
                await interaction.channel.send(content="Error: You cannot remove a clan member that is not in your clan.")
        
        await interaction.channel.send(embed=update_embed)

    @app_commands.checks.has_any_role(1054999374993817700, 1054999381029429349)
    @app_commands.check(bots_or_work_channel)
    @clan_group.command(
        name="disband",
        description="A Command That Disbands Your Team!")
    async def disband_clan(
        self,
        interaction: discord.Interaction
    ):        
        success_embed = discord.Embed(
            title="Your Clan Has Been Disbanded!",
            description="Your Clan Has Been Updated With The According Changes",
            color=0x00ffff
        )

        await interaction.response.send_message(embed=success_embed)
    
        clan_leader_role = interaction.guild.get_role(1054999374993817700)
        clan_co_leader_role = interaction.guild.get_role(1054999381029429349)
        clans_role_ping = interaction.guild.get_role(1057043814797295646)

        if ((clan_leader_role in interaction.user.roles) or 
            (clan_co_leader_role in interaction.user.roles)): 
        
            clan_role = await ClanChangesMethods.get_clan_role(
                self=self,
                interaction=interaction,
                top_role_divider=interaction.guild.get_role(1053050572296704000),
                bottom_role_divider=interaction.guild.get_role(1053050637555880027)
            )

            await ClanDisbandMethods.delete_clan_role(
                self=self,
                clan_role=clan_role,
                role_config_list=[clan_role, clan_co_leader_role, clan_leader_role, clans_role_ping],
                bot=self.bot                
            )

    @app_commands.describe(member="member")
    @app_commands.rename(member="member")      
    @clan_group.command(
        name="points",
        description="get this users clan points grinded!")
    async def get_member_clan_points (
        self,
        interaction,
        member: discord.Member
    ):
        async with self.bot.pool.acquire() as connection:
            # Select data from the ClanPointTracker table
            sql = "SELECT * FROM ClanPointTracker WHERE discordUserID = $1"
            member_clan_point_data = await connection.fetch(sql, member.id)

            print(member_clan_point_data)
            if len(member_clan_point_data) != 0:
                response_embed = discord.Embed(
                    title=f"{member.nick}'s total clan points are: {member_clan_point_data[0][3]}",
                    color=0x00ffff
                )
                await interaction.response.send_message(
                    embed=response_embed
                )
            else:
                response_embed = discord.Embed(
                    title=f"{member.nick}'s total clan points were not found. Please try again later.",
                    color=0x00ffff
                )
                await interaction.response.send_message(
                    embed=response_embed
                )
    
    @app_commands.describe(clan_role="clan_role")
    @app_commands.rename(clan_role="clan_role")      
    @clan_group.command(
        name="roster",
        description="get the clans roster!")
    async def send_clan_roster (
        self,
        interaction,
        clan_role: discord.Role
    ):
        generate_clan_roster_obj = GenerateClanRoster()
        
        clan_list = generate_clan_roster_obj.get_clans(
            interaction=interaction
        )

        if clan_role in clan_list:
            clan_info_list = generate_clan_roster_obj.get_clan_info(
                interaction=interaction,
                clan_role=clan_role
            )

            clan_roster_embed = await generate_clan_roster_obj.send_clan_roster(
                interaction=interaction,
                clan_role=clan_role,
                clan_info_list=clan_info_list
            )

            await interaction.response.send_message(
                embed=clan_roster_embed
            )

            await generate_clan_roster_obj.clan_disband_check(
                interaction=interaction,
                clan_role=clan_role
            )

        else:
            response_embed = discord.Embed(
                title="Error: You did not specify a clan role",
                color=0x2f3136
            )

            await interaction.response.send_message(
                embed=response_embed
            )
            
async def setup(bot):
    await bot.add_cog(ClanCommands(bot))