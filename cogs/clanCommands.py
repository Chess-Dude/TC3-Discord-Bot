import discord, typing, matplotlib, json
from discord import app_commands, Colour
from discord.ext import commands
from cogs.tourneyApplicationCommands import tournament_application_commands
from cogs.roleUtilityAppCommands import RoleUtilityCommands

class TeamCreation():
    async def create_role(
        self, 
        interaction: discord.Interaction, 
        role_name, 
        colour: discord.Colour, 
        role_divider_id
    ): 
        
        TC3_SERVER = interaction.guild
        role_divider = discord.utils.get(
            TC3_SERVER.roles, 
            id=role_divider_id
        )
        await TC3_SERVER.create_role(
            name=role_name, 
            colour=colour
        )
        team_role = discord.utils.get(
            TC3_SERVER.roles, 
            name=role_name
        )
        await team_role.edit(position=role_divider.position-1)
        
        return team_role

    async def assign_roles(
        self, 
        interaction: discord.Interaction, 
        clan_roster,
        clan_role, # custom tournament team role
        clan_leader_role_id, # team captain
        clan_co_leader_role_id # team co captain 
    ):

        TC3_SERVER = interaction.guild
        clan_leader_role = discord.utils.get(
            TC3_SERVER.roles, 
            id=clan_leader_role_id
        )
        clan_co_leader_role = discord.utils.get(
            TC3_SERVER.roles, 
            id=clan_co_leader_role_id
        )

        clans_role_ping = discord.utils.get(
            TC3_SERVER.roles,
            id=1057043814797295646
        )

        for member in clan_roster:
            if member == clan_roster[0]:
                await member.add_roles(clan_leader_role)

            if member == clan_roster[1]: 
                await member.add_roles(clan_co_leader_role)

            if member != None:
                await member.add_roles(clan_role)
                await member.add_roles(clans_role_ping)
            
     
class ReviewClanApplication(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def update_leaderboard(
        self,
        clan_lb_channel,
        clan_lb_message_id,
        clan_role_name
    ):
        clan_lb_message = await clan_lb_channel.fetch_message(clan_lb_message_id)
        
        clan_lb_embed = clan_lb_message.embeds[0].to_dict()
        all_clan_points = clan_lb_embed['description']

        # Split the input string into a list of strings
        clan_point_list = all_clan_points.split("\n")

        # Create a list of tuples from the list of strings
        clan_list_list = []
        for clan_item in clan_point_list:
            clan, lb_clan_points = clan_item.split(" - ")
            clan_list_list.append([clan, int(lb_clan_points)])

        clan_list_list.append([clan_role_name, int(0)])

        # Sort the list of lists in ascending order by the number following the clan's name
        sorted_list_list = sorted(clan_list_list, key=lambda x: x[1])

        # Reverse the sorted list of tuples
        reversed_tuple_list = reversed(sorted_list_list)

        # Create a list of strings from the reversed list of tuples
        sorted_strings = []
        for clan, lb_clan_points in reversed_tuple_list:
            sorted_strings.append(f"{clan} - {lb_clan_points}")

        # Join the list of strings into a single string
        result = "\n".join(sorted_strings)

        return result


    @discord.ui.button(label="Approve", style=discord.ButtonStyle.green, emoji='✅', custom_id="persistent_view:approve_clan_app")
    async def approve_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"loading...")

        log_embed_message =  interaction.message
        log_embed = log_embed_message.embeds[0].to_dict()
        log_embed_fields = log_embed['fields']
        create_role_field = log_embed_fields[-1]
        info_str = create_role_field["value"]

        if info_str[0] == '"':
            start_index = 1 
            end_index = 2
            clan_roster_str_index = -1

        else:
            start_index = 0
            end_index = 0
            clan_roster_str_index = 0

        clan_name = info_str[start_index:-len(" 621516858205405197 585991378400706570 585991378400706570 585991378400706570 585991378400706570 585991378400706570 #36393E") - end_index]
        clan_roster_str = info_str[(clan_roster_str_index - len("621516858205405197 585991378400706570 585991378400706570 585991378400706570 585991378400706570 585991378400706570 #36393E")) :-len(" #36393E")]            
        clan_roster_list = clan_roster_str.split(' ')
        clan_hex_color = info_str[-len("#36393E"):-1]
        clan_leader = interaction.guild.get_member(int(clan_roster_list[0]))
        clan_co_leader = interaction.guild.get_member(int(clan_roster_list[1]))            
        clan_member_1 = interaction.guild.get_member(int(clan_roster_list[2]))            
        clan_member_2 = interaction.guild.get_member(int(clan_roster_list[3]))            
        clan_member_3 = interaction.guild.get_member(int(clan_roster_list[4]))            
        clan_member_4 = interaction.guild.get_member(int(clan_roster_list[5]))
        role_divider_id = 1053050572296704000    
        clan_leader_role_id = 1054999374993817700 
        clan_co_leader_role_id = 1054999381029429349 

        clan_roster_list = [clan_leader, clan_co_leader, clan_member_1, clan_member_2, clan_member_3, clan_member_4]
        clan_hex_color = discord.Color.from_str(clan_hex_color)

        clan_role = await TeamCreation.create_role(
            self, 
            interaction, 
            role_name=clan_name, 
            colour=clan_hex_color, 
            role_divider_id=role_divider_id
        )

        await TeamCreation.assign_roles(
            self, 
            interaction=interaction, 
            clan_roster=clan_roster_list, 
            clan_role=clan_role,
            clan_leader_role_id=clan_leader_role_id, 
            clan_co_leader_role_id=clan_co_leader_role_id, 
        )
        
        clan_lb_channel = interaction.guild.get_channel(1050289500783386655)
        
        new_weekly_result = await ReviewClanApplication.update_leaderboard(
            self=self,
            clan_lb_channel=clan_lb_channel,
            clan_lb_message_id=1056413563209650228,
            clan_role_name=clan_name
        )

        new_weekly_clan_lb = discord.Embed(
            title="Clan Point Weekly Leaderboard",
            description=new_weekly_result,
            color=0x00ffff,
            timestamp=interaction.created_at
        )

        new_yearly_result = await ReviewClanApplication.update_leaderboard(
            self=self,
            clan_lb_channel=clan_lb_channel,
            clan_lb_message_id=1056413562525974608,
            clan_role_name=clan_name
        )

        new_yearly_clan_lb = discord.Embed(
            title="Clan Point Yearly Leaderboard",
            description=new_yearly_result,
            color=0x00ffff,
            timestamp=interaction.created_at
        )

        clan_weekly_lb_message = await clan_lb_channel.fetch_message(1056413563209650228)
        clan_yearly_lb_message = await clan_lb_channel.fetch_message(1056413562525974608)
        await clan_weekly_lb_message.edit(embed=new_weekly_clan_lb)
        await clan_yearly_lb_message.edit(embed=new_yearly_clan_lb)
        await interaction.channel.send(f"{interaction.user.mention} Created ``{clan_role.mention}`` ")
        await interaction.message.edit(view=None)

    @discord.ui.button(label="Reject", style=discord.ButtonStyle.red, emoji='❌', custom_id="persistent_view:reject_clan_app")
    async def reject_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.message.edit(view=None)
        await interaction.response.send_message(content=f"Rejected by: {interaction.user.mention}")


class ClanCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def bots_or_work_channel(interaction):
        return interaction.channel.id == 941567353672589322 or interaction.channel.id == 896440473659519057 or interaction.channel.id == 351057167706619914

    async def colour_converter(
        self,
        clan_color
        ):
        
        try:
            hex_color: Colour = Colour.from_str(clan_color)
            hex_color = str(hex_color)
        except ValueError:
            try:
                hex_color = matplotlib.colors.cnames[clan_color]
            except KeyError:
                hex_color = "#000000"

        return hex_color 

    async def application_log_embed(
        self, 
        interaction: discord.Interaction, 
        clan_name,
        clan_color,        
        clan_roster
    ):
        TC3_SERVER = interaction.guild
        applications_channel = TC3_SERVER.get_channel(1043644487949357157)
        ec_role = discord.utils.get(
            TC3_SERVER.roles, 
            id=475669961990471680
        )

        log_embed = discord.Embed(
            title=f"The Conqeurors 3 Clan Application", 
            color=0x00ffff,
            timestamp=interaction.created_at
        )

        log_embed.set_author(
            name=f"Submitted By: {interaction.user.display_name}",
            icon_url=interaction.user.display_avatar.url
        )

        log_embed.set_footer(
            text=f"The Conquering 3 Clan Application",
            icon_url=interaction.guild.icon
        )

        log_embed.add_field(
            name=f"Clan Name:",
            value=f"``{clan_name}``",
            inline=False
        )

        log_embed.add_field(
            name=f"Clan Color:",
            value=f"``{clan_color}``",
            inline=False
        )

        clan_member_count = 0
        clan_members_id = []
        for iteration, player in enumerate(clan_roster):
            if player == clan_roster[0]:
                log_embed.add_field(
                    name=f"Clan Leader:",
                    value=f"{clan_roster[0].mention}, ``{clan_roster[0].id}``",
                    inline=False
                )
                clan_members_id.append(player.id)
                continue

            if player == clan_roster[1]:
                log_embed.add_field(
                    name=f"Clan Co-Leader:",
                    value=f"{clan_roster[1].mention}, ``{clan_roster[1].id}``",
                    inline=False
                )
                clan_members_id.append(player.id)
                continue
                
            if player != None:
                clan_member_count = clan_member_count + 1
                log_embed.add_field(
                    name=f"Clan Member {clan_member_count}:",
                    value=f"{player.mention}, ``{player.id}``",
                    inline=False
                )
                clan_members_id.append(player.id)

            else:
                clan_members_id.append(clan_members_id[iteration-1])
        
        clan_members_id = str(clan_members_id)[1:-1]
        clan_members_id = clan_members_id.replace(',', "")
        
        if ' ' in clan_name:
            clan_name = f'"{clan_name}"'                
        log_embed.add_field(
            name="Bot Information:",
            value=f'{clan_name} {clan_members_id} {clan_color}',
            inline=False
        )

        view = ReviewClanApplication()
        await applications_channel.send(
            content=f"<@650847350042132514>, <@818729621029388338>, <@319573094731874304>, <@198273107205685248>, <@711003479430266972>, <@768259026084429896>, <@820952452739891281>, <@282761998326824961>",
            embed=log_embed,
            view=view
        )

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

            all_members_verified = await tournament_application_commands.check_verified(
                self,
                interaction=interaction, 
                team_roster=clan_roster
            )

            if all_members_verified:
                clan_color = await ClanCommands.colour_converter(
                    self,
                    clan_color=clan_color
                )

                await ClanCommands.application_log_embed(
                    self,
                    interaction=interaction,
                    clan_name=clan_name,
                    clan_color=str(clan_color),
                    clan_roster=clan_roster
                )

                await tournament_application_commands.success_embed(
                    self,
                    interaction=interaction,
                    description=f"{interaction.user.mention} Thank You For Submitting Your Clan Application!"
                )

    async def update_clan_hex_color(
        self,
        clan_role,
        new_tournament_team_hex_color
    ):
        if clan_role.color != new_tournament_team_hex_color:
            await clan_role.edit(color=new_tournament_team_hex_color)

    async def update_clan_leader(
        self,
        interaction,
        roles_to_config,
        new_clan_leader
    ):
            for role in roles_to_config:                
                await new_clan_leader.add_roles(role)
                await interaction.user.remove_roles(role)
    
    async def update_clan_co_leader(
        self,
        roles_to_add,
        new_clan_co_leader
    ):
        for role in roles_to_add:
            await new_clan_co_leader.add_roles(role)
        
    async def add_clan_member(
        self,
        roles_to_add,
        new_clan_member
    ):
        for role in roles_to_add:
            await new_clan_member.add_roles(role)
            

    async def remove_clan_member(
        self,
        interaction: discord.Interaction,
        roles_to_remove,
        remove_clan_member
    ):
        if roles_to_remove[-1] not in interaction.user.roles:
            for role in roles_to_remove:
                await interaction.user.remove_roles(role)              

        else:
            for role in roles_to_remove:
                await remove_clan_member.remove_roles(role)              

    async def get_clan_role(
        self,
        interaction: discord.Interaction,
        top_role_divider,
        bottom_role_divider,
        ):
            for role_position in range(top_role_divider.position - 1, bottom_role_divider.position, - 1):
                clan_role = discord.utils.get(interaction.guild.roles, position=role_position)
                if clan_role in interaction.user.roles:
                    return clan_role
                
                else:
                    continue

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

        clan_role = await ClanCommands.get_clan_role(
            self=self,
            interaction=interaction,
            top_role_divider=interaction.guild.get_role(1053050572296704000),
            bottom_role_divider=interaction.guild.get_role(1053050637555880027)
        )
        if clan_role != None:
            clan_leader_role = interaction.guild.get_role(1054999374993817700)
            clan_co_leader_role = interaction.guild.get_role(1054999381029429349)
            roles_to_remove = [clan_role, clan_co_leader_role, clan_leader_role]            
            await ClanCommands.remove_clan_member(
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

        clan_role = await ClanCommands.get_clan_role(
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
                new_clan_hex_color = await ClanCommands.colour_converter(
                    self=self,
                    clan_color=new_clan_hex_color
                )

                await ClanCommands.update_clan_hex_color(
                    self=self,
                    clan_role=clan_role,
                    new_tournament_team_hex_color=discord.Color.from_str(new_clan_hex_color)
                )
        
            if new_clan_leader != None:
                roles_to_config = [clan_role, clan_leader_role, clans_role_ping]            
                
                await ClanCommands.update_clan_leader(
                    self=self,
                    interaction=interaction,
                    roles_to_config=roles_to_config,
                    new_clan_leader=new_clan_leader,
                )
            
            if new_clan_co_leader != None:
                roles_to_add = [clan_role, clan_co_leader_role, clan_leader_role, clans_role_ping]            

                await ClanCommands.update_clan_co_leader(
                    self=self,
                    roles_to_add=roles_to_add,
                    new_clan_co_leader=new_clan_co_leader,
                )

            if new_clan_member != None:
                roles_to_add = [clan_role, clans_role_ping]
                await ClanCommands.add_clan_member(
                    self=self,
                    roles_to_add=roles_to_add,
                    new_clan_member=new_clan_member
                )

        if remove_clan_member != None:
            clan_leader_role = interaction.guild.get_role(1054999374993817700)
            clan_co_leader_role = interaction.guild.get_role(1054999381029429349)
            roles_to_remove = [clan_role, clan_co_leader_role, clan_leader_role]            
            await ClanCommands.remove_clan_member(
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
        
            clan_role = await ClanCommands.get_clan_role(
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
        clan_info, 
        new_value
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
        all_clan_points = clan_lb_embed['description']

        new_description = ClanCommands.replace_name_value(
            self,
            input_string=all_clan_points,
            clan_info=clan_info, 
            new_value=''
        )

        new_weekly_lb = discord.Embed(
            title="Clan Point Weekly Leaderboard",
            description=new_description,
            timestamp=interaction.created_at,
            color=0x00ffff
        )

        new_yearly_lb = discord.Embed(
            title="Clan Point Yearly Leaderboard",
            description=new_description,
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
        # )

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

        with open('/Users/lodhi/OneDrive/Desktop/TC3-Discord-Bot_CLANS/clanPointsTracker.json', 'r') as f:
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