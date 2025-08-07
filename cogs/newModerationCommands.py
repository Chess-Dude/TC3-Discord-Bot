import discord, datetime
from discord.ext import commands
from discord import app_commands
from .moderationClasses.muteModeration import MuteModeration
from .moderationClasses.kickModeration import KickModeration
from .moderationClasses.banModeration import BanModeration
from .moderationClasses.userModeration import UserModeration
from decimal import Decimal, ROUND_HALF_UP

class newModerationCommands(commands.Cog):
    def __init__(
        self, 
        bot
    ):
        self.bot = bot
        self.TC3_SERVER = 350068992045744141

    test_command_group = app_commands.Group(
        name="test", 
        description="A test cmd",
        guild_ids=[350068992045744141])


    @commands.is_owner()
    @commands.command()
    async def create_mod_db(self, ctx):
        async with self.bot.pool.acquire() as connection:
            # Drop tables first to clear all existing data
            await connection.execute("DROP TABLE IF EXISTS UserModlogs;")
            await connection.execute("DROP TABLE IF EXISTS UserTotalModlogs;")
            await connection.execute("DROP TABLE IF EXISTS ActiveBannedUsers;")        

            # UserModlogs table (damageTaken and beforeBan as REAL)
            await connection.execute("""
            CREATE TABLE IF NOT EXISTS UserModlogs (
                modlogID SERIAL PRIMARY KEY,
                guildID BIGINT NOT NULL,
                userID BIGINT NOT NULL,
                robloxUsername TEXT,
                damageTaken REAL,
                moderatorID BIGINT NOT NULL,
                reason TEXT,
                beforeBan REAL,
                date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            """)

            # UserTotalModlogs table (all damage columns as REAL)
            await connection.execute("""
            CREATE TABLE IF NOT EXISTS UserTotalModlogs (
                record SERIAL PRIMARY KEY,
                guildID BIGINT NOT NULL,
                userID BIGINT NOT NULL,
                robloxUsername TEXT,
                activeDamage REAL,
                healedDamage REAL,                
                totalDamage REAL,
                totalBans INTEGER
            );
            """)

            # ActiveBannedUsers table (unchanged)
            await connection.execute("""
            CREATE TABLE IF NOT EXISTS ActiveBannedUsers (
                record SERIAL PRIMARY KEY,
                guildID BIGINT NOT NULL,
                userID BIGINT NOT NULL,
                robloxUsername TEXT,
                unbanDate TIMESTAMP NOT NULL,
                bannedDate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            """)

            print("success")
        await ctx.send("✅ All moderation tables have been dropped and recreated with float-compatible damage columns.")


    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.command(
        name="mute",
        description="Mutes a user from the server")
    @app_commands.describe(user="specify which member to mute")
    @app_commands.describe(time="specify length of mute: (1m, 1h, 1d)")
    @app_commands.describe(reason="specify reason of mute")
    @app_commands.describe(damage="specify damage amount")    
    @app_commands.rename(user="user")
    @app_commands.rename(time="time") 
    @app_commands.rename(reason="reason")
    @app_commands.rename(damage="damage")    
    async def mute_command(        
        self,
        interaction: discord.Interaction,
        user: discord.User,
        time: str,
        reason: str,
        damage: float       
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
        mute_time = user_mute_obj.calculate_mute_time()
        if interaction.guild.id != self.TC3_SERVER:
            
            if (mute_time):
                await user_mute_obj.mute_user()
                await interaction.response.send_message(f"Muted {user.mention} successfully for {time}")
            return    

        if not await user_mute_obj.is_staff():        
            
            if (mute_time):
                await user_mute_obj.mute_user()

        if interaction.guild.id == 350068992045744141:
            async with self.bot.pool.acquire() as connection:
                # Adds entry of mod-log in the Table UserModlogs
                await user_mute_obj.create_new_modlog(connection=connection)
                
                # Ensures/Updates the damage in Table UserTotalModLogs
                has_prior_modlogs = await user_mute_obj.has_prior_modlogs(connection=connection)
                if (not has_prior_modlogs):
                    await user_mute_obj.create_user_main_record(connection=connection)
                
                else:
                    await user_mute_obj.update_total_modlogs(connection=connection)

                # sends embeds and notifies if required to ban
                await user_mute_obj.send_log_embed(connection=connection)
                user_reached_dmg_camp = await user_mute_obj.reached_damage_cap(connection=connection)
                if (user_reached_dmg_camp):
                    await user_mute_obj.notify_to_ban()
                    await user_mute_obj.perm_mute_user()
                    # Possibly Auto-ban?

    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.command(
        name="kick",
        description="Kicks a user from the server")
    @app_commands.describe(user="specify which member to Kick")
    @app_commands.describe(reason="specify reason of Kick")
    @app_commands.rename(user="user")
    @app_commands.rename(reason="reason")
    async def kick_command(        
        self,
        interaction: discord.Interaction,
        user: discord.User,
        reason: str
    ):
        user_kick_obj = KickModeration(
            bot=self.bot, 
            user=user,
            interaction=interaction,
            modlog_reason=reason, 
            moderator_id=interaction.user.id
        )

        if interaction.guild.id != self.TC3_SERVER:
            await user_kick_obj.kick_user()
            return

        # If user a staff member, issue warning
        if await user_kick_obj.is_staff():        
            await interaction.response.send_message(f"Error: {user.mention} is a staff member. Cannot kick.")
            return
        
        async with self.bot.pool.acquire() as connection:
            # Adds entry of mod-log in the Table UserModlogs
            await user_kick_obj.create_new_modlog(connection=connection)
            
            # Ensures/Updates the damage in Table UserTotalModLogs
            has_prior_modlogs = await user_kick_obj.has_prior_modlogs(connection=connection)
            if (not has_prior_modlogs):
                await user_kick_obj.create_user_main_record(connection=connection)
            else:
                await user_kick_obj.update_total_modlogs(connection=connection)

            await user_kick_obj.send_log_embed(connection=connection)
            await user_kick_obj.kick_user()
    

    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.command(
        name="ban",
        description="A Command that allows moderators to ban a member")
    @app_commands.describe(user="specify which member to ban")
    @app_commands.describe(reason="specify reason of ban")
    @app_commands.describe(ban_length="specify ban length in terms of days (e.g 30d)")
    @app_commands.rename(user="user")
    @app_commands.rename(reason="reason")
    @app_commands.rename(ban_length="ban_length")
    async def ban_command(        
        self,
        interaction: discord.Interaction,
        user: discord.User,
        reason: str,
        ban_length: str # Note ban_length is just being used as a raw string value. Not actually doing anything with it.
    ):  
        user_ban_obj = BanModeration(
            bot=self.bot, 
            user=user,
            interaction=interaction,
            modlog_reason=reason, 
            moderator_id=interaction.user.id,
            ban_length=ban_length
        )

        if interaction.guild.id != self.TC3_SERVER:
            await user_ban_obj.ban_user()
            return
        
        # If user a staff member, issue warning
        if await user_ban_obj.is_staff():        
            await interaction.response.send_message(f"Error: {user.mention} is a staff member. Cannot ban.")
            return

        async with self.bot.pool.acquire() as connection:
            # Adds entry of mod-log in the Table UserModlogs
            await user_ban_obj.create_new_modlog(connection=connection)
            
            # Ensures/Updates the damage in Table UserTotalModLogs
            has_prior_modlogs = await user_ban_obj.has_prior_modlogs(connection=connection)
            if (not has_prior_modlogs):
                await user_ban_obj.create_user_main_record(connection=connection)
            else:
                await user_ban_obj.update_total_modlogs(connection=connection)
            await user_ban_obj.update_total_bans(connection=connection)
                
            await user_ban_obj.send_log_embed(connection=connection)
            
            await user_ban_obj.ban_user()


    @app_commands.command(
        name="modlogs",
        description="Gets user's modlog history"
    )
    @app_commands.describe(user="Specify which member to get modlogs for")
    @app_commands.rename(user="user")            
    async def get_modlogs(
        self,
        interaction: discord.Interaction,
        user: discord.User,
    ):
        # Acquire a connection from the pool.
        async with self.bot.pool.acquire() as connection:
            embed = await UserModeration.get_modlogs(
                user=user,
                interaction=interaction,
                connection=connection
            )
    
        await interaction.response.send_message(embed=embed)


    @app_commands.command(
        name="decay",
        description="Decays user active damage by 0.1, adds it to healed damage, and unbans users past their unban date."
    )
    @app_commands.checks.has_permissions(ban_members=True)
    async def decay(
        self,
        interaction: discord.Interaction,
    ):
        # Check if the command is run in the proper guild.
        if interaction.guild.id != self.TC3_SERVER:
            await interaction.response.send_message("Only a TC3 admin can run this command. L Bozo.", ephemeral=True)
            return

        async with self.bot.pool.acquire() as connection:
            # --- DECAY LOGIC ---
            # Fetch users with activeDamage > 0
            users = await connection.fetch("""
                SELECT record, activeDamage, healedDamage
                FROM UserTotalModlogs
                WHERE activeDamage > 0
            """)

            # If no users need to be decayed, send a message and return.
            if not users:
                await interaction.response.send_message("✅ No users to decay. Everyone is already at 0 active damage.")
                # Exit immediately to avoid further processing.

            else:
                # Notify that the process has started using followup.
                await interaction.channel.send("Loading...")

                # Process each user: subtract 0.1 from activeDamage and add 0.1 to healedDamage using Decimal for precision.
                for user in users:
                    # Convert current values to Decimal.
                    active_decimal = Decimal(str(user["activedamage"]))
                    healed_decimal = Decimal(str(user["healeddamage"]))
                    
                    # Calculate new values using Decimal arithmetic.
                    new_active = max(Decimal('0.0'), active_decimal - Decimal('0.1'))
                    new_healed = healed_decimal + Decimal('0.1')
                    
                    # Quantize to one decimal place to ensure consistent formatting.
                    new_active = new_active.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
                    new_healed = new_healed.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
                    
                    await connection.execute("""
                        UPDATE UserTotalModlogs
                        SET activeDamage = $1, healedDamage = $2
                        WHERE record = $3
                    """, float(new_active), float(new_healed), user["record"])

            # --- UNBAN LOGIC ---
            # Fetch all banned users for the guild from ActiveBannedUsers.
            banned_users = await connection.fetch("""
                SELECT record, userID, unbanDate 
                FROM ActiveBannedUsers 
                WHERE guildID = $1
            """, interaction.guild.id)

            unbanned_count = 0
            now = datetime.datetime.utcnow()
            for banned in banned_users:
                # If the current time is equal to or later than unbanDate, unban the user.
                if now >= banned["unbandate"]:
                    try:
                        # Create a discord.Object from the user ID.
                        user_object = discord.Object(id=banned["userid"])
                        await interaction.guild.unban(user_object)
                        unbanned_count += 1
                    except Exception as e:
                        print(f"Error unbanning user {banned['userid']}: {e}")
                    # Remove the record from ActiveBannedUsers once processed.
                    await connection.execute("DELETE FROM ActiveBannedUsers WHERE record = $1", banned["record"])

        # Send a final follow-up message summarizing the decay and unban actions.
        await interaction.channel.send(
            f"✅ Decay complete. Updated {len(users)} users. Unbanned {unbanned_count} users."
        )



    @app_commands.command(
        name="appeal",
        description="Removes a mod-log from a user."
    )
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(user="Specify the user that you would like to appeal a modlog from")
    @app_commands.describe(modlog_id="Specify the modlog id ")
    @app_commands.describe(remove_damage="specify ban length in terms of days (e.g 30d)")
    @app_commands.rename(user="user")
    @app_commands.rename(modlog_id="modlog_id")
    @app_commands.rename(remove_damage="remove_damage")
    async def appeal(
        self,
        interaction: discord.Interaction,
        user: discord.User,
        modlog_id: int,
        remove_damage: int 
    ):
        # Check if the command is run in the proper guild.
        if interaction.guild.id != self.TC3_SERVER:
            await interaction.response.send_message("Only a TC3 admin can run this command. L Bozo.", ephemeral=True)
            return

        async with self.bot.pool.acquire() as connection:
            # Convert current values to Decimal.
            active_decimal = Decimal(str(user["activedamage"]))
            healed_decimal = Decimal(str(user["healeddamage"]))
            
            # Calculate new values using Decimal arithmetic.
            new_active = max(Decimal('0.0'), active_decimal - Decimal('0.1'))
            new_healed = healed_decimal + Decimal('0.1')
            
            # Quantize to one decimal place to ensure consistent formatting.
            new_active = new_active.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
            new_healed = new_healed.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
            
            await connection.execute("""
                UPDATE UserTotalModlogs
                SET activeDamage = $1, healedDamage = $2
                WHERE record = $3
            """, float(new_active), float(new_healed), user["record"])


async def setup(bot):
    await bot.add_cog(newModerationCommands(bot))