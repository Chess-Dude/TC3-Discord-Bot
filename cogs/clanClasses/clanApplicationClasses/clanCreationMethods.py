import discord, matplotlib
from discord import Colour
from .clanApplicationReview import ReviewClanApplication

class ClanCreationMethods():
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
        clan_roster,
        pool
    ):
        TC3_SERVER = interaction.guild
        applications_channel = TC3_SERVER.get_channel(1043644487949357157)

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
                        
        log_embed.add_field(
            name="Bot Information:",
            value=f'"{clan_name}" {clan_members_id} {clan_color}',
            inline=False
        )

        view = ReviewClanApplication(pool)
        await applications_channel.send(
            content=f"``<@711003479430266972>, <@768259026084429896>, <@282761998326824961>``",
            embed=log_embed,
            view=view
        )
