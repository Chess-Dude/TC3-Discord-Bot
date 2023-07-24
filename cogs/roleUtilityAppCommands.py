import discord, typing
from discord import app_commands
from discord.ext import commands

class RoleUtilityCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def member_role_update(
        self,
        role,
        member_list,
        add_role,
        remove_role
    ):

        if add_role:
            for member in member_list:
                if member != None:
                    await member.add_roles(role)
                else:
                    break
            
        elif remove_role:
            for member in member_list:
                if member != None:
                    await member.remove_roles(role)
                else:
                    break

    role_command_group = app_commands.Group(
        name="role", 
        description="A Group Of Commands That Allows You To Manage Roles!",
        guild_ids=[350068992045744141])

    async def type_autocomplete(
        self, 
        interaction: discord.Interaction,
        current: str,
    ) -> list[app_commands.Choice[str]]:
        type_list = ["add", "remove"]
        return [
            app_commands.Choice(name=type, value=type)
            for type in type_list if current.lower() in type.lower()
        ]

    @app_commands.checks.has_any_role(351074813055336458, 475669961990471680)
    @role_command_group.command(
        name="division",
        description="A Command That Allows You To Add Or Remove A Division Role From Members!")
    @app_commands.autocomplete(type=type_autocomplete)
    @app_commands.describe(division="Ping a discord role to be added to a member here!")
    @app_commands.describe(member_1="Ping a discord member here!")
    @app_commands.describe(member_2="Ping a discord member here!")
    @app_commands.describe(member_3="Ping a discord member here!")
    @app_commands.describe(member_4="Ping a discord member here!")
    @app_commands.rename(division="division")
    @app_commands.rename(member_1="member_1")
    @app_commands.rename(member_2="member_2")
    @app_commands.rename(member_3="member_3")
    @app_commands.rename(member_4="member_4")
    async def role_remove_division(        
        self,
        interaction: discord.Interaction,
        type: str,
        division: discord.Role,
        member_1: discord.Member,
        member_2: typing.Optional[discord.Member],
        member_3: typing.Optional[discord.Member],
        member_4: typing.Optional[discord.Member]       
    ):
        add_flag = False
        remove_flag = False
        if type.lower() == "add":
            add_flag = True

        elif type.lower() == "remove":
            remove_flag = True
        
        else:
            await interaction.response.send_message("Error: Unknown Type. Please specify if you would like to add or remove a division role.")

        if add_flag or remove_flag:
            division_list = []
            top_role = interaction.guild.get_role(1047715900515700847)
            bottom_role = interaction.guild.get_role(1048286357858046003)

            for role_pos in range(top_role.position-1, bottom_role.position, -1):
                division_role = discord.utils.get(
                    interaction.guild.roles, 
                    position=role_pos
                )
                if division_list == None:
                    continue

                division_list.append(division_role)

            if division in division_list:
                await RoleUtilityCommands.member_role_update(
                    self=self,
                    role=division,
                    member_list=[member_1, member_2, member_3, member_4],
                    add_role=add_flag,
                    remove_role=remove_flag
                )
                
                await interaction.channel.send("Completed")

            else: 
                await interaction.channel.send("You do not have permission to assign or remove that role")

    @app_commands.checks.has_any_role(351074813055336458, 475669961990471680)
    @role_command_group.command(
        name="one_day",
        description="A Command That Allows You To Add Or Remove A one-day tournament Role From Members!")
    @app_commands.autocomplete(type=type_autocomplete)
    @app_commands.describe(role="Ping a discord role to be added to a member here!")
    @app_commands.describe(member_1="Ping a discord member here!")
    @app_commands.describe(member_2="Ping a discord member here!")
    @app_commands.describe(member_3="Ping a discord member here!")
    @app_commands.describe(member_4="Ping a discord member here!")
    @app_commands.rename(role="role")
    @app_commands.rename(member_1="member_1")
    @app_commands.rename(member_2="member_2")
    @app_commands.rename(member_3="member_3")
    @app_commands.rename(member_4="member_4")
    async def role_manage_oneday(        
        self,
        interaction: discord.Interaction,
        type: str,
        role: discord.Role,
        member_1: discord.Member,
        member_2: typing.Optional[discord.Member],
        member_3: typing.Optional[discord.Member],
        member_4: typing.Optional[discord.Member]       
    ):
        add_flag = False
        remove_flag = False
        if type.lower() == "add":
            add_flag = True

        elif type.lower() == "remove":
            remove_flag = True
        
        else:
            await interaction.response.send_message("Error: Unknown Type. Please specify if you would like to add or remove a division role.")

        if add_flag or remove_flag:
            role_list = []
            top_role = interaction.guild.get_role(589808867999875072)
            bottom_role = interaction.guild.get_role(411712513672216586)

            for role_pos in range(top_role.position-1, bottom_role.position, -1):
                server_role = discord.utils.get(
                    interaction.guild.roles, 
                    position=role_pos
                )
                if role_list == None:
                    continue

                role_list.append(server_role)

            if role in role_list:
                await RoleUtilityCommands.member_role_update(
                    self=self,
                    role=role,
                    member_list=[member_1, member_2, member_3, member_4],
                    add_role=add_flag,
                    remove_role=remove_flag
                )
                
                await interaction.channel.send("Completed")

            else: 
                await interaction.channel.send("You do not have permission to assign or remove that role")

    @app_commands.checks.has_any_role(351074813055336458)
    @role_command_group.command(
        name="any",
        description="A Command That Allows You To Add Or Remove A Division Role From Members!")
    @app_commands.autocomplete(type=type_autocomplete)
    @app_commands.describe(role="Ping a discord role to be added to a member here!")
    @app_commands.describe(member_1="Ping a discord member here!")
    @app_commands.describe(member_2="Ping a discord member here!")
    @app_commands.describe(member_3="Ping a discord member here!")
    @app_commands.describe(member_4="Ping a discord member here!")
    @app_commands.rename(role="role")
    @app_commands.rename(member_1="member_1")
    @app_commands.rename(member_2="member_2")
    @app_commands.rename(member_3="member_3")
    @app_commands.rename(member_4="member_4")
    async def role_any_admin(        
        self,
        interaction: discord.Interaction,
        type: str,
        role: discord.Role,
        member_1: discord.Member,
        member_2: typing.Optional[discord.Member],
        member_3: typing.Optional[discord.Member],
        member_4: typing.Optional[discord.Member]       
    ):
        add_flag = False
        remove_flag = False
        if type.lower() == "add":
            add_flag = True

        elif type.lower() == "remove":
            remove_flag = True
        
        else:
            await interaction.response.send_message("Error: Unknown Type. Please specify if you would like to add or remove a division role.")

        await RoleUtilityCommands.member_role_update(
            self=self,
            role=role,
            member_list=[member_1, member_2, member_3, member_4],
            add_role=add_flag,
            remove_role=remove_flag
        )
        
        await interaction.channel.send("Completed")

async def setup(bot):
    await bot.add_cog(RoleUtilityCommands(bot))