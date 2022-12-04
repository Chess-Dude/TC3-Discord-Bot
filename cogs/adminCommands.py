import discord, typing, random
from discord.ext import commands
from discord import app_commands

class AdminCommands(commands.Cog):
    def __init__(
        self, 
        bot):
            self.bot = bot

    @commands.is_owner()
    @commands.command()
    async def remove_gamenight_tournament_role(
        self, 
        ctx):
            await ctx.message.reply("...")
            server = ctx.guild
            group_role_list = []
            group_1_role = discord.utils.get(
                server.roles, 
                id=695667390125441074)
            group_12_role = discord.utils.get(
                server.roles, 
                id=695722292537196616) 
            
            for role_position in range(group_1_role.position, group_12_role.position-1, -1):
                group = discord.utils.get(
                    server.roles, 
                    position=role_position
                )
                
                group_role_list.append(group)

            game_night_tournament_role = discord.utils.get(
                server.roles, 
                id=690624687004319804
            )
            
            backup_role = discord.utils.get(
                server.roles, 
                id=695683985510236220
            )
            
            for member in game_night_tournament_role.members:
                if backup_role in member.roles:
                    await member.remove_roles(backup_role)

                for group in group_role_list:
                    if group in member.roles:
                        await member.remove_roles(group)
                        break
                
                await member.remove_roles(game_night_tournament_role)
            await ctx.send("removed all roles successfully")

    @commands.is_owner()
    @commands.command(aliases=["createmultistagetourneychannels"])
    async def create_event_channel(
        self,
        ctx,
        category_name, 
        role: discord.Role,
    ):
        ec_role = discord.utils.get(
            ctx.guild.roles, 
            id=475669961990471680
        )
        
        mod_role = discord.utils.get(
            ctx.guild.roles, 
            id=351166789700550679
        )
        
        mit_role = discord.utils.get(
            ctx.guild.roles, 
            id=363125947635073025
        )
        
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
            role: discord.PermissionOverwrite(read_messages=True),
            ec_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            mod_role: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_message=True),
            mit_role: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_message=True),                        
        }

        category = await ctx.guild.create_category(name=f"group-{category_name}", overwrites=overwrites)
        await ctx.guild.create_text_channel(name=f"{category_name}-bracket", overwrites=overwrites, category=category)
        await ctx.guild.create_text_channel(name=f"{category_name}-match-results", overwrites=overwrites, category=category)
        await ctx.guild.create_text_channel(name=f"{category_name}-check-in", overwrites=overwrites, category=category)        

    @commands.is_owner()
    @commands.command(aliases=["removeallroles"])
    async def remove_all_role(
        self,
        ctx,
        role_1: discord.Role,
        role_2: typing.Optional[discord.Role],
        role_3: typing.Optional[discord.Role],
        role_4: typing.Optional[discord.Role],
        role_5: typing.Optional[discord.Role],
        role_6: typing.Optional[discord.Role],
        role_7: typing.Optional[discord.Role],
        role_8: typing.Optional[discord.Role],
    ):
        msg = await ctx.message.reply(content="...")
        roles_to_remove = [role_1, role_2, role_3, role_4, role_5, role_6, role_7, role_8]
        for role in roles_to_remove:
            if role != None:
                for member in role.members:
                    await member.remove_roles(role)
            else:
                break
        await msg.edit(content="Removed All Roles Successfully")

    @commands.is_owner()
    @commands.command(aliases=["randomizeteams"])
    async def randomize_teams(
        self,
        ctx,
        *player_tuple: discord.Member
    ):  
        if type(len(player_tuple) // 3) == int:
            player_list = list(player_tuple)
            player_shuffled_list = random.sample(player_list, len(player_list))
            team_list = []
            count = 0
            player_names = ''
            for player in player_shuffled_list:
                count = count + 1
                team_list.append(player)
                if len(team_list) == 3:
                    group_num = int(count / 3)
                    group_role = discord.utils.get(ctx.guild.roles, name=f"Group {group_num}")
                    for player in team_list:
                        await player.add_roles(group_role)
                        player_names = player_names + player.mention + ' ' 
                    await ctx.send(f"**__{group_role.mention}__**\n{player_names}")
                    team_list = []
                    player_names = ''

        else:
            await ctx.send(f"You provided {len(player_tuple)} members")
    
    @commands.has_any_role(351074813055336458, 743302990001340559, 554152645192056842)
    @commands.command(aliases=["balanceteams"])
    async def balance_teams(
        self,
        ctx,
        *player_tuple: discord.Member
    ):  
        if type(len(player_tuple) // 3) == int:
            level_role_list = []
            low_level_list = [] # between level 0-30
            mid_level_list = [] # between level 40-60
            high_level_list = [] # level 70+
            top_role = discord.utils.get(
                ctx.guild.roles, 
                id=589808867999875072
            )        
            bottom_role = discord.utils.get(
                ctx.guild.roles, 
                id=1046102834363519017
            )
            team_list = []

            for level_role_pos in range(top_role.position-1, bottom_role.position, -1):
                level_role = discord.utils.get(
                    ctx.guild.roles, 
                    position=level_role_pos
                )
                if level_role == None:
                    continue

                level_role_list.append(level_role)
            # index 0 = 100, index 1 = 70, index 2 = 60, index 3 = 50, index 4 = 40, index 5 = 30, index 6 = 20, index 7 = 10, index 8 = 5
            
            for player in player_tuple:
                if ((level_role_list[0] in player.roles) or 
                (level_role_list[1] in player.roles)):
                    high_level_list.append(player)
                    continue

                if ((level_role_list[2] in player.roles) or 
                (level_role_list[3] in player.roles) or 
                (level_role_list[4] in player.roles)):
                    mid_level_list.append(player)
                    continue
                
                else:
                    low_level_list.append(player)
            count = 0
            while (len(high_level_list) + len(mid_level_list) + len(low_level_list) >= 3):
                count = count + 1
                try:
                    team_list.append(high_level_list[0])
                    high_level_list.remove(high_level_list[0])                
                except:
                    try:
                        team_list.append(mid_level_list[0])
                        mid_level_list.remove(mid_level_list[0])
                    except:
                        team_list.append(low_level_list[0])
                        low_level_list.remove(low_level_list[0])
                
                try:
                    team_list.append(mid_level_list[0])
                    mid_level_list.remove(mid_level_list[0])
                except:
                    try:
                        team_list.append(low_level_list[0])
                        low_level_list.remove(low_level_list[0])
                    except:
                        team_list.append(high_level_list[0])
                        high_level_list.remove(high_level_list[0])

                try:
                    team_list.append(low_level_list[0])
                    low_level_list.remove(low_level_list[0])
                except:
                    try:
                        team_list.append(mid_level_list[0])
                        mid_level_list.remove(mid_level_list[0])
                    except:
                        team_list.append(high_level_list[0])                    
                        high_level_list.remove(high_level_list[0])
                
                player_names = ''
                group_num = count 
                group_role = discord.utils.get(
                    ctx.guild.roles, 
                    name=f"Group {group_num}"
                )
                
                for player in team_list:
                    await player.add_roles(group_role)
                    player_names = player_names + player.mention + ' ' 
                await ctx.send(f"**__{group_role.mention}__**\n{player_names}")
                team_list = []

        else:
            await ctx.send(f"You provided {len(player_tuple)} members")
            
async def setup(bot):
    await bot.add_cog(AdminCommands(bot))