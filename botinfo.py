import discord
import platform

from datetime import datetime, timezone
from discord import app_commands
from discord.ext import commands


class BotInfo(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.now(timezone.utc)

    @app_commands.command(
        name="botinfo",
        description="Show J.A.R.V.I.S Bot Information"
    )
    async def botinfo(self, interaction: discord.Interaction):

        bot = self.bot

        uptime = datetime.now(timezone.utc) - self.start_time

        days = uptime.days
        hours, rem = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(rem, 60)

        embed = discord.Embed(
            title="🤖 TIC TAC TOE BOT INFORMATION",
            description=(
                "**Tic Tac Bot**\n"
                "Powered By Jarvis Quantum Core"
            ),
            color=discord.Color.blue()
        )

        embed.add_field(
            name="👤 Bot Name",
            value=f"`{bot.user.name}`",
            inline=False
        )

        embed.add_field(
            name="🟢 Status",
            value="`ONLINE`",
            inline=True
        )

        embed.add_field(
            name="🌐 Total Servers",
            value=f"`{len(bot.guilds)}`",
            inline=True
        )

        embed.add_field(
            name="⏱️ Bot Uptime",
            value=f"`{days}d {hours}h {minutes}m {seconds}s`",
            inline=False
        )

        embed.add_field(
            name="💻 Operating System",
            value="`Jarvis Quantum Core`",
            inline=False
        )

        embed.add_field(
            name="⚙️ Host Platform",
            value=f"`{platform.system()} {platform.release()}`",
            inline=False
        )

        embed.add_field(
            name="👑 Developer",
            value="`Tony Stark`",
            inline=True
        )

        embed.add_field(
            name="🎮 Activity",
            value="`🎮 Tik Tac Toe Quantum Guardians Official Bot`",
            inline=False
        )

        embed.set_thumbnail(
            url=bot.user.display_avatar.url
        )

        embed.set_footer(
            text="J.A.R.V.I.S Quantum Core | Developed By Tony Stark"
        )

        await interaction.response.send_message(
            embed=embed
        )


async def setup(bot):
    await bot.add_cog(BotInfo(bot))