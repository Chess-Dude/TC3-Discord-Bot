import discord
from .disbandClans import DisbandClansClass

class GenerateClanRoster():
    
    async def purge_channel_messages(
        self,
        interaction
    ):
        """
        Deletes all messages in the roster channel
        """
        clan_roster_channel = interaction.guild.get_channel(1101934520212656158)
        await clan_roster_channel.purge(limit=100)

    def get_clans(
        self,
        interaction
    ):
        """
        returns a list of all clans
        """        
        clan_divider_top_role = interaction.guild.get_role(1053050572296704000)
        clan_divider_bottom_role = interaction.guild.get_role(1053050637555880027)
        clan_role_list = [] 
        for role_position in range(clan_divider_top_role.position-1, clan_divider_bottom_role.position, -1):
            clan_role = discord.utils.get(
                interaction.guild.roles, 
                position=role_position
            )

            clan_role_list.append(clan_role)

        return clan_role_list


    def get_clan_info(
        self,
        interaction,
        clan_role
    ):
        """
        return clan info (list of leader, co-leader and members)
        """        
        clan_leader_role = interaction.guild.get_role(1054999374993817700)
        clan_co_leader_role = interaction.guild.get_role(1054999381029429349)
        clan_leader = []
        clan_co_leader = []
        clan_members = []

        for member in clan_role.members: 
            if clan_leader_role in member.roles:
                clan_leader.append(member)

            elif clan_co_leader_role in member.roles:
                clan_co_leader.append(member)

            else:
                clan_members.append(member)

        clan_info_list = [clan_leader, clan_co_leader, clan_members]
        return clan_info_list


    async def send_clan_roster(
        self,
        interaction,
        clan_role,
        clan_info_list
    ):
        """
        uses the lists returned from the get_clan_info method to put it into an embed and sends it  
        """                
        clan_leader = clan_info_list[0]
        clan_co_leader = clan_info_list[1]
        clan_members = clan_info_list[2]
        clan_leader_text = ''
        co_leader_text = '' 
        member_text = ''

        if len(clan_leader) == 0:
            clan_leader_text = "• N/A"

        else:
            clan_leader_text = f"• {(clan_leader[0]).display_name}" + " - " + (clan_leader[0]).mention
        
        if len(clan_co_leader) == 0:
            co_leader_text = "• N/A"

        else:
            co_leader_text = f"• {(clan_co_leader[0]).display_name}" + " - " + (clan_co_leader[0]).mention

        if len(clan_members) == 0:
            member_text = f"\n• N/A"

        else:
            for member in clan_members:
                member_text = member_text + f"\n• {member.display_name} - {member.mention}"

        embed_text = f"``Leader:``\n{clan_leader_text}\n\n``Co-Leader:``\n{co_leader_text}\n\n``Members:``{member_text}\n\n``Total Members:``\n• {(len(clan_role.members))}/10"        
        clan_roster_embed = discord.Embed(
            title=f"``{clan_role.name}'s Roster:\n``",
            description=embed_text,
            color=int(clan_role.color),
            timestamp=interaction.created_at
        )

        return clan_roster_embed

    async def clan_disband_check(
        self,
        interaction,
        clan_role
    ):
        if len(clan_role.members) < 4 or (len(clan_role.members) > 10):
            notif_embed = discord.Embed(
                title="Notice: Clan Disbandment At Risk!",
                description="Your clan has either too many or too less members currently! If you fail to recruit the required amount of members soon, your clan will be disbanded.\nRun the ``/clan roster`` command in <#351057167706619914> to view your clan roster.",
                color=0xffffff
            )
            for member in clan_role.members:
                try:
                    await member.send(embed=notif_embed)
                except:
                    pass

            log_channel = interaction.guild.get_channel(1043644487949357157)
            notif_embed.add_field(
                name=f"Clan:",
                value=f"• {clan_role.name}"
            )

            notif_embed.add_field(
                name=f"Bot Information:",
                value=f"{clan_role.id}"
            )

            await log_channel.send(
                embed=notif_embed,
                view=DisbandClansClass()
            )
        
        else:
            return