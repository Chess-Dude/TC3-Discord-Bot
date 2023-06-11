import discord, typing
from discord import app_commands
from discord.ext import commands
from .clanClasses.clanPointClasses.clanPointReview import ReviewClanPoints

class ClanPointCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

 
    async def game_mode_autocomplete(
        self, 
        interaction: discord.Interaction,
        current: str,
    ) -> list[app_commands.Choice[str]]:
        type_list = ["Conquest", "Survival", "Free For All", "King Of The Hill", "Territory Conquest", "Tournament Scrimmage/Match", "Clan Scrimmage"]
        return [
            app_commands.Choice(name=type, value=type)
            for type in type_list if current.lower() in type.lower()
        ]

    submit_command_group = app_commands.Group(
        name="submit", 
        description="A Commands That Allows You To Submit Clan Points!"
    )

    clan_command_group = app_commands.Group(
        name="clan", 
        description="A Commands That Allows You To Submit Clan Points!",
        parent=submit_command_group
    )

    @clan_command_group.command(
        name="point",
        description="A Commands That Allows You To Submit Clan Points!")
    @app_commands.describe(damage_dealt_bonus="Specify how many damage coins that were given.")
    @app_commands.describe(damage_healed_bonus="Specify how many healing coins that were given.")
    @app_commands.describe(victory_bonus="Specify how many coins were awareded for winning (0 or 25).")
    @app_commands.describe(game_mode="Specify the game_mode here.")
    @app_commands.describe(image_link="image_link")
    @app_commands.describe(clan_member="Specify the clan member here.")
    @app_commands.rename(damage_dealt_bonus="damage_dealt_bonus")        
    @app_commands.rename(damage_healed_bonus="damage_healed_bonus")        
    @app_commands.rename(waves_survived_bonus="waves_survived_bonus")        
    @app_commands.rename(victory_bonus="victory_bonus")        
    @app_commands.autocomplete(game_mode=game_mode_autocomplete)        
    @app_commands.rename(image_link="image_link")
    @app_commands.rename(clan_member="clan_member")
    async def submit_clan_points(        
        self,
        interaction: discord.Interaction,
        damage_dealt_bonus: int,
        damage_healed_bonus: int,
        waves_survived_bonus: typing.Optional[int],
        victory_bonus: int,
        game_mode: str,
        image_link: str,
        clan_member: discord.Member
    ):

        clan_role_list = []
        top_role = interaction.guild.get_role(1053050572296704000)
        bottom_role = interaction.guild.get_role(1053050637555880027)
        TC3_SERVER = interaction.guild
        
        for role_pos in range(top_role.position, bottom_role.position, -1):
            clan_role = discord.utils.get(
                TC3_SERVER.roles, 
                position=role_pos
            )
            if clan_role == None:
                continue

            elif clan_role in clan_member.roles:
                clan_role_list.append(clan_role)

            else:
                continue

        if len(clan_role_list) >= 1:
            if game_mode.lower() == "conquest":
                game_mode_multiplier = 2
                game_mode_cap = 125
                if damage_healed_bonus > 15:
                    damage_healed_bonus = 15

            elif ((game_mode.lower() == "territory conquest") or 
                (game_mode.lower() == "tc")):
                game_mode_multiplier = 1
                game_mode_cap = 125
                if damage_healed_bonus > 15:
                    damage_healed_bonus = 15

            elif game_mode.lower() == "survival":
                game_mode_multiplier = 1
                game_mode_cap = 250

            elif ((game_mode.lower() == "king of the hill") or 
                (game_mode.lower() == "koth")):
                game_mode_multiplier = 1.5
                game_mode_cap = 90

            elif ((game_mode.lower() == "free for all") or 
                (game_mode.lower() == "ffa")):
                game_mode_multiplier = 2
                game_mode_cap = 300

            elif ((game_mode.lower() == "tournament scrimmage/match") or 
                (game_mode.lower() == "tournament scrimmage/match")):
                game_mode_multiplier = 3
                game_mode_cap = 255
                if damage_healed_bonus > 15:
                    damage_healed_bonus = 15

            elif game_mode.lower() == "clan scrimmage": 
                game_mode_multiplier = 3
                game_mode_cap = 255
                if damage_healed_bonus > 15:
                    damage_healed_bonus = 15

            else:
                game_mode_multiplier = 1
                game_mode_cap = 0

            log_embed = discord.Embed(
                title=f"{clan_member.display_name}'s Clan Point Submission",
                color=0x00ffff,
                timestamp=interaction.created_at
            )

            log_embed.set_author(
                name=f"{clan_member.id}",
                icon_url=clan_member.display_avatar.url
            )

            log_embed.set_footer(
                text=f"The Conquerors 3 • Clan Point Submission",
                icon_url=interaction.guild.icon
            )

            log_embed.set_image(url=image_link)
            
            log_embed.add_field(
                name=f"Clan Of Member:",
                value=f"``{clan_role_list[0].name}``",
                inline=False
            )

            log_embed.add_field(
                name=f"Total Damage Dealt Bonus:",
                value=f"``{damage_dealt_bonus}``",
                inline=False
            )

            log_embed.add_field(
                name=f"Total Damage Healed Bonus:",
                value=f"``{damage_healed_bonus}``",
                inline=False
            )

            if game_mode.lower() == "survival":
                log_embed.add_field(
                    name=f"Total Waves Survived Bonus:",
                    value=f"``{waves_survived_bonus}``",
                    inline=False
                )

            log_embed.add_field(
                name=f"Total Victory Bonus:",
                value=f"``{victory_bonus}``",
                inline=False
            )

            log_embed.add_field(
                name=f"Game Mode:",
                value=f"``{game_mode}``",
                inline=False
            )

            if type(waves_survived_bonus) == int:
                total_clan_points = damage_dealt_bonus + damage_healed_bonus + victory_bonus + waves_survived_bonus
            
            else:
                total_clan_points = damage_dealt_bonus + damage_healed_bonus + victory_bonus
                        
            total_clan_points = float(total_clan_points) * float(game_mode_multiplier)

            if (float(total_clan_points) > float(game_mode_cap)):
                total_clan_points = game_mode_cap

            log_embed.add_field(
                name=f"Total Clan Points:",
                value=f"``{int(total_clan_points)}``",
                inline=False
            )

            success_embed = discord.Embed(
                title="Your Clan Point Submission Will Be Reviewed Shortly!", 
                color=0x00ffff
            )
            
            cp_sub_channel = discord.utils.get(
                TC3_SERVER.channels, 
                id=1050289442017005598
            )
            
            await interaction.response.send_message(embed=success_embed)
            
            view = ReviewClanPoints()            
            await cp_sub_channel.send(
                content=f"{int(total_clan_points)} {clan_role_list[0].name}",
                embed=log_embed,
                view=view
            )
            
        else: 
            await interaction.response.send_message("That member is not in a clan.")


async def setup(bot):
    await bot.add_cog(ClanPointCommands(bot))