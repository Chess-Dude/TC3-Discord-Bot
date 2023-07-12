import discord, typing, ast
from discord.ext import commands, tasks
from discord import app_commands
from .clanClasses.clanPointClassesREWORKED.clanPointBotMethods import ClanPointBotMethods
from .clanClasses.clanPointClasses.clanPointReview import ReviewClanPoints
from .clanClasses.clanPointClassesREWORKED.clanPointAPIMethods import ClanPointAPIMethods

class ClanPointCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot     
        self.looped_update_leaderboard.start()
        self.looped_send_clan_point_notif.start()
        self.clan_point_bot_methods_obj = ClanPointBotMethods()
        self.clan_point_api_methods_obj = ClanPointAPIMethods()

    @tasks.loop(hours=6.0)
    async def looped_update_leaderboard(self):
        self.LEADERBOARD_CHANNEL = self.bot.get_channel(1121947513981779978)
        await self.LEADERBOARD_CHANNEL.purge(limit=1)
        embeds_list = await self.clan_point_bot_methods_obj.get_updated_leaderboards(bot=self.bot)
        await self.LEADERBOARD_CHANNEL.send(
            embeds=embeds_list
        )

    @looped_update_leaderboard.before_loop       
    async def before_update_leaderboard_task(self):
        await self.bot.wait_until_ready()

    @tasks.loop(minutes=5.0)
    async def looped_send_clan_point_notif(
        self
    ):
        end_of_round_bonus_results = await self.clan_point_bot_methods_obj.get_end_of_round_bonus(
            bot=self.bot
        )

        for end_of_round_bonus_record in end_of_round_bonus_results:
            endofroundbonusstring = end_of_round_bonus_record["endofroundbonusstring"]
            end_of_round_bonus_list = ast.literal_eval(endofroundbonusstring)
            
            if len(end_of_round_bonus_list) != 0:                
                total_clan_points = self.clan_point_api_methods_obj.calculate_total_clan_points(
                    end_of_round_bonus_list=end_of_round_bonus_list
                )
                
                await self.clan_point_bot_methods_obj.send_log_embed(
                    end_of_round_bonus_list=end_of_round_bonus_list,
                    bot=self.bot,
                    total_clan_points=total_clan_points               
                )

    @looped_send_clan_point_notif.before_loop       
    async def before_update_clan_point_task(self):
        await self.bot.wait_until_ready()

    manage_clan_points = app_commands.Group(
        name="manage",
        description="allows you to manage clans",
        guild_ids=[350068992045744141]
    )

    @app_commands.checks.has_any_role(554152645192056842, 743302990001340559, 351074813055336458)
    @manage_clan_points.command(
        name="clan_leaderboard_update",
        description="A Command That Allows You To Update Clan Leaderboards!")
    async def update_clan_leaderboard(
        self, 
        interaction: discord.Interaction
    ):
        await self.looped_update_leaderboard()

    @app_commands.checks.has_any_role(554152645192056842, 743302990001340559, 351074813055336458)
    @manage_clan_points.command(
        name="reset_weekly_leaderboard",
        description="A Command That Allows You To Reset Weekly Clan Leaderboards!")
    async def reset_weekly_leaderboard(
        self, 
        interaction: discord.Interaction
    ):
        await self.looped_update_leaderboard()
        embeds_list = await self.clan_point_bot_methods_obj.get_updated_leaderboards(cursor=self.cursor)
        await interaction.channel.send(
            content=f"Final leaderboard for this week:",
            embeds=embeds_list
        )

        async with self.bot.pool.acquire() as connection:
            sql = "UPDATE ClanPointLeaderboard SET yearlyClanPoints = 0"
            await connection.execute(sql)
            await connection.commit()
        
        await interaction.channel.send(
            content="Successfully Reset Weekly Leaderboard. Please run the ``/manage clan_leaderboard_update`` command to view the updated leaderboard."
        )

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