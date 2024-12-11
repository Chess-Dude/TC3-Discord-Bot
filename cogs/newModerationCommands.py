import discord, datetime
from discord.ext import commands
from discord import app_commands
from .moderationClasses.muteModeration import MuteModeration

class newModerationCommands(commands.Cog):
    def __init__(
        self, 
        bot
    ):
        self.bot = bot


    test_command_group = app_commands.Group(
        name="test", 
        description="A test cmd",
        guild_ids=[350068992045744141])
    
    @commands.is_owner()
    @commands.command()
    async def create_mod_db(
        self, 
        ctx
    ):
        async with self.bot.pool.acquire() as connection:
            sql = """
            CREATE TABLE IF NOT EXISTS UserModlogs (
                modlogID SERIAL PRIMARY KEY,
                guildID BIGINT NOT NULL,
                userID BIGINT NOT NULL,
                robloxUsername TEXT,
                damageTaken INTEGER,
                moderatorID BIGINT NOT NULL,
                reason TEXT,
                beforeBan INTEGER,
                date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            """

            await connection.execute(sql)

            sql = """
            CREATE TABLE IF NOT EXISTS UserTotalModlogs (
                record SERIAL PRIMARY KEY,
                guildID BIGINT NOT NULL,
                userID BIGINT NOT NULL,
                robloxUsername TEXT,
                activeDamage INTEGER,
                healedDamage INTEGER,                
                totalDamage INTEGER,
                totalBans INTEGER
            );
            """

            await connection.execute(sql)                        

            sql = """
            CREATE TABLE IF NOT EXISTS ActiveBannedUsers (
                record SERIAL PRIMARY KEY,
                guildID BIGINT NOT NULL,
                userID BIGINT NOT NULL,
                robloxUsername TEXT,
                unbanDate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                bannedDate TIMESTAMP
            );
            """

            await connection.execute(sql)                        

    @app_commands.checks.has_permissions(administrator=True)
    @test_command_group.command(
        name="mute",
        description="Mute a user")
    @app_commands.describe(user="specify which member to mute")
    @app_commands.describe(time="specify length of mute: (1m, 1h, 1d)")
    @app_commands.describe(reason="specify reason of mute")
    @app_commands.describe(damage="specify damage amount")    
    @app_commands.rename(user="user")
    @app_commands.rename(time="time") 
    @app_commands.rename(reason="reason")
    @app_commands.rename(damage="damage")    
    async def new_mute_command(        
        self,
        interaction: discord.Interaction,
        user: discord.User,
        time: str,
        reason: str,
        damage: int       
    ):
        user_mute_obj = MuteModeration(
            bot=self.bot, 
            user=user,
            interaction=interaction,
            modlog_reason=reason, 
            raw_mute_length=time, 
            damage_taken=damage, 
            moderator_id=interaction.user.id
        )

        if not await user_mute_obj.is_staff():        
            mute_time = user_mute_obj.calculate_mute_time()
            
            if (mute_time):
                await user_mute_obj.mute_user()

            await user_mute_obj.send_log_embed()

        # async with self.bot.pool.acquire() as connection:
        #     sql = "SELECT * FROM UserTotalModlogs WHERE guildID = $1 AND userID = $2"
        #     values = (interaction.guild_id, user.id)
        #     user_total_modlogs = await connection.fetch(sql, *values)

        #     if len(user_total_modlogs) == 0:
        #         sql = "INSERT INTO UserTotalModlogs (robloxUsername, discordUserID, totalClanPoints, currentClanRoleID, currentClanName) VALUES ($1, $2, $3, $4, $5)"
        #         values = (new_clan_member.nick, new_clan_member.id, 0, roles_to_add[0].id, roles_to_add[0].name)
        #         await connection.execute(sql, *values)
        #     else:
        #         sql = "UPDATE ClanPointTracker SET currentClanRoleID = $1, currentClanName = $2 WHERE discordUserID = $3"
        #         values = (roles_to_add[0].id, roles_to_add[0].name, new_clan_member.id)
        #         await connection.execute(sql, *values)

            # sql = """
            # INSERT INTO UserModlogs (guildID, userID, robloxUsername, damageTaken, moderatorID, reason, beforeBan, date)
            # VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            # """
            # values = (
            #     interaction.guild.id,
            #     user.id,       
            #     "",
            #     damage,               
            #     interaction.user.id,          
            #     reason,       
            #     True,                   # beforeBan (replace with actual value)
            #     datetime.datetime.now(datetime.date.utc)  
            # )

async def setup(bot):
    await bot.add_cog(newModerationCommands(bot))