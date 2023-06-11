import discord, typing, json
from discord import app_commands
from discord.ext import commands
from cogs.teamApplicationClasses.teamCreation import TeamCreation
from .clanClasses.clanApplicationClasses.clanCreationMethods import ClanCreationmethods
from .clanClasses.clanApplicationClasses.clanChangeMethods import ClanChangesMethods

class ClanCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
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
                clan_color = await ClanCreationmethods.colour_converter(
                    self,
                    clan_color=clan_color
                )

                await ClanCreationmethods.application_log_embed(
                    self,
                    interaction=interaction,
                    clan_name=clan_name,
                    clan_color=str(clan_color),
                    clan_roster=clan_roster
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
                remove_clan_member=interaction.user
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

            if new_clan_hex_color != None:            
                new_clan_hex_color = await ClanCreationmethods.colour_converter(
                    self=self,
                    clan_color=new_clan_hex_color
                )

                await ClanChangesMethods.update_clan_hex_color(
                    self=self,
                    clan_role=clan_role,
                    new_tournament_team_hex_color=discord.Color.from_str(new_clan_hex_color)
                )
        
            if new_clan_leader != None:
                roles_to_config = [clan_role, clan_leader_role, clans_role_ping]            
                
                await ClanChangesMethods.update_clan_leader(
                    self=self,
                    interaction=interaction,
                    roles_to_config=roles_to_config,
                    new_clan_leader=new_clan_leader,
                )
            
            if new_clan_co_leader != None:
                roles_to_add = [clan_role, clan_co_leader_role, clan_leader_role, clans_role_ping]            

                await ClanChangesMethods.update_clan_co_leader(
                    self=self,
                    roles_to_add=roles_to_add,
                    new_clan_co_leader=new_clan_co_leader,
                )

            if new_clan_member != None:
                roles_to_add = [clan_role, clans_role_ping]
                await ClanChangesMethods.add_clan_member(
                    self=self,
                    roles_to_add=roles_to_add,
                    new_clan_member=new_clan_member
                )

        if remove_clan_member != None:
            clan_leader_role = interaction.guild.get_role(1054999374993817700)
            clan_co_leader_role = interaction.guild.get_role(1054999381029429349)
            roles_to_remove = [clan_role, clan_co_leader_role, clan_leader_role]            
            await ClanChangesMethods.remove_clan_member(
                self=self,
                interaction=interaction,
                roles_to_remove=roles_to_remove,
                remove_clan_member=remove_clan_member
            )

    async def disband_tournament_team(
        self,
        clan_role,
        role_config_list
        ):
            for member in clan_role.members:
                for role in role_config_list:
                    await member.remove_roles(role)
                                                                                   
            await discord.Role.delete(clan_role)

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

            await ClanCommands.disband_tournament_team(
                self=self,
                clan_role=clan_role,
                role_config_list=[clan_role, clan_co_leader_role, clan_leader_role, clans_role_ping]                
            )

    def remove_name_value(
        self, 
        input_string
    ):
        name_value_pairs = input_string.split('\n')
        name_value_dict = {}
        for pair in name_value_pairs:
            name, value = pair.split('-')
            name_value_dict[name] = value
        return name_value_dict

    def replace_name_value(
        self,
        input_string,
        clan_info
    ):
        name_value_dict = ClanCommands.remove_name_value(
            self, 
            input_string=input_string
        )
    
        if clan_info in name_value_dict:
            del name_value_dict[clan_info]
        new_input_string = "\n".join(["{} - {}".format(name, value) for name, value in name_value_dict.items()])
        return new_input_string

    @app_commands.checks.has_any_role(475669961990471680, 351074813055336458, 743302990001340559)
    @clan_group.command(
        name="remove_clan_name",
        description="A Commands That Allows You To Remove A Clan from the leaderboards!")
    @app_commands.describe(clan_info="Specify the clan info here. EG - Clan Name - 0")
    @app_commands.rename(clan_info="clan_info")      
    async def remove_clan_name(        
        self,
        interaction: discord.Interaction,
        clan_info: str
    ):
        clan_lb_channel = interaction.guild.get_channel(1050289500783386655)
        clan_weekly_lb_message = await clan_lb_channel.fetch_message(1056413563209650228)
        clan_yearly_lb_message = await clan_lb_channel.fetch_message(1056413562525974608)
        clan_lb_embed = clan_weekly_lb_message.embeds[0].to_dict()
        clan_lb_embed_yearly = clan_yearly_lb_message.embeds[0].to_dict()
        all_clan_points_weekly = clan_lb_embed['description']
        all_clan_points_yearly = clan_lb_embed_yearly['description']

        new_description_weekly = ClanCommands.replace_name_value(
            self,
            input_string=all_clan_points_weekly,
            clan_info=clan_info
        )

        new_description_yearly = ClanCommands.replace_name_value(
            self,
            input_string=all_clan_points_yearly,
            clan_info=clan_info
        )

        new_weekly_lb = discord.Embed(
            title="Clan Point Weekly Leaderboard",
            description=new_description_weekly,
            timestamp=interaction.created_at,
            color=0x00ffff
        )

        new_yearly_lb = discord.Embed(
            title="Clan Point Yearly Leaderboard",
            description=new_description_yearly,
            timestamp=interaction.created_at,
            color=0x00ffff
        )

        await clan_weekly_lb_message.edit(embed=new_weekly_lb)
        await clan_yearly_lb_message.edit(embed=new_yearly_lb)
        await interaction.response.send_message("Completed")
    
    async def leaderboard_type_autocomplete(
        self, 
        interaction: discord.Interaction,
        current: str,
    ) -> list[app_commands.Choice[str]]:
        type_list = ["Weekly", "Yearly", "Both"]
        return [
            app_commands.Choice(name=type, value=type)
            for type in type_list if current.lower() in type.lower()
        ]

    @app_commands.checks.has_any_role(475669961990471680, 351074813055336458, 743302990001340559)
    @clan_group.command(
        name="add_clan_points",
        description="A Commands That Allows You To Add Clan Points To the leaderboards!")
    @app_commands.describe(leaderboard_type="Specify the leaderboard (Weekly/Yearly)")       
    @app_commands.describe(clan_name="Specify the clan info here.")
    @app_commands.describe(clan_points="Specify the clan points to add here.")
    @app_commands.autocomplete(leaderboard_type=leaderboard_type_autocomplete)       
    @app_commands.rename(clan_points="clan_points")      
    @app_commands.rename(clan_name="clan_name")      
    async def add_clan_points(        
        self,
        interaction: discord.Interaction,
        leaderboard_type: str,
        clan_name: str,
        clan_points: int
    ):
        if leaderboard_type == "Weekly":
            lb_message_id = 1056413563209650228
        
        elif leaderboard_type == "Yearly":
            lb_message_id = 1056413562525974608

        clan_lb_channel = interaction.guild.get_channel(1050289500783386655)
        clan_lb_message = await clan_lb_channel.fetch_message(lb_message_id)
        clan_lb_embed = clan_lb_message.embeds[0].to_dict()
        all_clan_points = clan_lb_embed['description']
        name_value_pairs = all_clan_points.split('\n')
        name_value_dict = {}

        for pair in name_value_pairs:

            try: 
                name, value = pair.split('-')
                name_value_dict[name] = value
            except:
                name = "Lose 4 Cry"
                name_value_dict[name] = 0
                await interaction.channel.send(f"Set {pair} to 0 due to ValueError: Too Many values to unpack (expected 2) - potential cause is negative clan points (two -)")

        print(name_value_dict)
        
        while clan_name not in name_value_dict:
            clan_name = clan_name + ' '

        name_value_dict[clan_name] = str(int(name_value_dict[clan_name]) + clan_points)
        new_description = "\n".join(["{} - {}".format(name, value) for name, value in name_value_dict.items()])

        new_lb = discord.Embed(
            title=f"Clan Point {leaderboard_type} Leaderboard",
            description=new_description,
            timestamp=interaction.created_at,
            color=0x00ffff
        )

        await clan_lb_message.edit(embed=new_lb)
        await interaction.response.send_message("Completed")

    @app_commands.checks.has_any_role(475669961990471680, 351074813055336458, 743302990001340559)
    @clan_group.command(
        name="remove_clan_points",
        description="A Commands That Allows You To Add Clan Points To the leaderboards!")
    @app_commands.describe(clan_name="Specify the clan info here.")
    @app_commands.describe(clan_points="Specify the clan points to add here.")
    @app_commands.rename(clan_points="clan_points")      
    @app_commands.rename(clan_name="clan_name")      
    async def remove_clan_points(        
        self,
        interaction: discord.Interaction,
        clan_name: str,
        clan_points: int
    ):
        clan_lb_channel = interaction.guild.get_channel(1050289500783386655)
        # clan_weekly_lb_message = await clan_lb_channel.fetch_message(1056413563209650228)
        clan_yearly_lb_message = await clan_lb_channel.fetch_message(1056413562525974608)
        clan_lb_embed = clan_yearly_lb_message.embeds[0].to_dict()
        all_clan_points = clan_lb_embed['description']

        name_value_pairs = all_clan_points.split('\n')
        name_value_dict = {}
        for pair in name_value_pairs:
            name, value = pair.split('-')
            name_value_dict[name] = value
        print(name_value_dict)
        
        while clan_name not in name_value_dict:
            clan_name = clan_name + ' '

        name_value_dict[clan_name] = str(int(name_value_dict[clan_name]) - clan_points)
        new_description = "\n".join(["{} - {}".format(name, value) for name, value in name_value_dict.items()])

        # new_weekly_lb = discord.Embed(
        #     title="Clan Point Weekly Leaderboard",
        #     description=new_description,
        #     timestamp=interaction.created_at,
        #     color=0x00ffff
        # )141

        new_yearly_lb = discord.Embed(
            title="Clan Point Yearly Leaderboard",
            description=new_description,
            timestamp=interaction.created_at,
            color=0x00ffff
        )

        # await clan_weekly_lb_message.edit(embed=new_weekly_lb)
        await clan_yearly_lb_message.edit(embed=new_yearly_lb)
        await interaction.response.send_message("Completed")

    @app_commands.checks.has_any_role(475669961990471680, 351074813055336458, 743302990001340559)
    @clan_group.command(
        name="weekly_lb_reset",
        description="A Commands That Allows You To Submit Clan Points!")
    async def reset_clan_points(        
        self,
        interaction: discord.Interaction,
    ):
        clan_lb_channel = interaction.guild.get_channel(1050289500783386655)
        clan_lb_message = await clan_lb_channel.fetch_message(1056413563209650228)
        
        clan_lb_embed = clan_lb_message.embeds[0].to_dict()
        all_clan_points = clan_lb_embed['description']
        lines = all_clan_points.strip().split('\n')
        reset_lines = [' '.join(line.split()[:-1]) + ' 0' for line in lines]
        new_description = ('\n'.join(reset_lines))

        new_weekly_lb = discord.Embed(
            title="Clan Point Weekly Leaderboard",
            description=new_description,
            timestamp=interaction.created_at,
            color=0x00ffff
        )

        await clan_lb_message.edit(embed=new_weekly_lb)
        await interaction.response.send_message("Completed")

    @app_commands.describe(member="member")
    @app_commands.rename(member="member")      
    @clan_group.command(
        name="points",
        description="get this users clan points grinded!")
    async def get_clan_points (
        self,
        interaction,
        member: discord.Member
    ):

        with open('clanPointsTracker.json', 'r') as f:
            users = json.load(f)

        try:
            current_clan_points = users[f'{member.id}']['clan_points']
            
            response_embed = discord.Embed(
                title=f"{member.name}'s total clan points are: {current_clan_points}",
                color=0x00ffff
            )
            await interaction.response.send_message(
                embed=response_embed
            )

        except KeyError:
            response_embed = discord.Embed(
                title=f"{member.name}'s total clan points were not found. Please try again later.",
                color=0x00ffff
            )
            await interaction.response.send_message(
                embed=response_embed
            )
            
async def setup(bot):
    await bot.add_cog(ClanCommands(bot))