import discord, typing
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands

class TournamentDisbandCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def bots_or_work_channel(interaction: discord.Interaction):
        return interaction.channel.id == 941567353672589322 or interaction.channel.id == 351057167706619914 or interaction.channel.id == 896440473659519057
    
    is_bots = app_commands.check(bots_or_work_channel)

    team_group = app_commands.Group(
        name="team", 
        description="A Command That Allows You To Make Changes To Your Tournament Team!",
        guild_ids=[350068992045744141])

    async def disband_log_embed(
        self,
        interaction: discord.Interaction,
        tournament_type,
        tournament_team_name
        ):
            tournament_applications_channel = discord.utils.get(
                interaction.guild.channels, 
                id=1043644487949357157
            )

            log_embed = discord.Embed(
            title=f"The Conquering Games {tournament_type} Team Disband Application", 
            color=0x00ffff,
            timestamp=interaction.created_at
            )

            log_embed.set_author(
                name=f"Submitted By: {interaction.user.display_name}",
                icon_url=interaction.user.display_avatar.url
            )

            log_embed.set_footer(
                text=f"The Conquering 3 • {tournament_type} Disband Application",
                icon_url=interaction.guild.icon
            )

            log_embed.add_field(
                name=f"{tournament_type} Team Name", 
                value=f"``{tournament_team_name}``",
                inline=False
                )

            await tournament_applications_channel.send(
                content=f"<@650847350042132514>, <@818729621029388338>, <@319573094731874304>, <@198273107205685248>, <@711003479430266972>, <@768259026084429896>, <@820952452739891281>, <@282761998326824961>",
                embed=log_embed
            )

    async def type_autocomplete(
        self, 
        interaction: discord.Interaction,
        current: str,
    ) -> list[app_commands.Choice[str]]:
        type_list = ["2v2 Tournaments", "3v3 Tournaments"]
        return [
            app_commands.Choice(name=type, value=type)
            for type in type_list if current.lower() in type.lower()
        ]

    @is_bots
    @team_group.command(
        name="disband",
        description="A Command That Disbands Your Team!")
    @app_commands.autocomplete(type=type_autocomplete)
    @app_commands.describe(team_name="Enter your team name here")
    @app_commands.rename(team_name="team_name")
    async def disband_team(
        self,
        interaction: discord.Interaction,
        type: str,
        team_name: str
    ):        

        success_embed = discord.Embed(
            title="Match Staff Have Been Notified To Disband Your Team!",
            description=f"We're sad to see you go 😢",
            color=0x00ffff
        )

        await interaction.response.send_message(embed=success_embed)            
    
        await TournamentDisbandCommands.disband_log_embed(
            self=self,
            interaction=interaction,
            tournament_type=type,
            tournament_team_name=team_name
        )

async def setup(bot):
    await bot.add_cog(TournamentDisbandCommands(bot))