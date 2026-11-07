import discord

async def set_bot_status(bot):
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game(
            name="🎮 Tic Tac Toe Quantum Guardians Official Bot "
        )
    )
    