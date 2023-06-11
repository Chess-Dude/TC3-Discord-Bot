from .clanCreation import ClanCreation
import discord, re

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

        clan_name = info_str.split('"')[1]

        # Removing the clan name from the string
        copy_info_str = info_str.replace(clan_name, '', 1)

        # Removing any non-numeric characters and whitespace
        clan_roster_str = re.sub(r'[^\d\s]+', '', copy_info_str)

        # Removing leading/trailing whitespace
        clan_roster_str = clan_roster_str.strip()

        # Splitting the roster string into a list of member IDs
        clan_roster_list = clan_roster_str.split(' ')
        del clan_roster_list[-1]

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

        clan_role = await ClanCreation.create_role(
            self, 
            interaction, 
            role_name=clan_name, 
            colour=clan_hex_color, 
            role_divider_id=role_divider_id
        )

        await ClanCreation.assign_roles(
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
