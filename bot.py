import discord
from discord.ext import commands
from discord import app_commands

# ==============================
# BOT CONFIGURATION
# ==============================

TOKEN = "MTU2ODI2Mjk2NjMyNjA3MTI5Ng.GEfTAb.1Sbs4-Be_LBV-jAVeqzdYxsbz3UHNvmM6XJ0HM"

intents = discord.Intents.default()

class MyBot(commands.Bot):
    async def setup_hook(self):
        await self.load_extension("botinfo")


bot = MyBot(
    command_prefix="!",
    intents=intents
)

async def setup_hook():
    await bot.load_extension("botinfo")

bot.setup_hook = setup_hook

# ==============================
# TIC TAC TOE GAME
# ==============================

class TicTacToe(discord.ui.View):

    def __init__(self, player1, player2):

        super().__init__(timeout=300)

        self.player1 = player1
        self.player2 = player2

        self.current_player = player1

        self.board = [""] * 9

        self.game_over = False

        self.message = None

        self.create_buttons()

    # ==========================
    # CREATE GAME BUTTONS
    # ==========================

    def create_buttons(self):

        for i in range(9):

            button = discord.ui.Button(
                label="\u200b",
                style=discord.ButtonStyle.secondary,
                row=i // 3
            )

            button.callback = self.make_callback(i)

            self.add_item(button)

    # ==========================
    # BUTTON CALLBACK
    # ==========================

    def make_callback(self, position):

        async def callback(interaction: discord.Interaction):

            if self.game_over:

                await interaction.response.send_message(
                    "❌ This game is already finished!",
                    ephemeral=True
                )
                return

            if interaction.user.id != self.current_player.id:

                await interaction.response.send_message(
                    "⏳ It's not your turn!",
                    ephemeral=True
                )
                return

            if self.board[position] != "":

                await interaction.response.send_message(
                    "❌ This box is already occupied!",
                    ephemeral=True
                )
                return

            # Player symbol

            symbol = (
                "❌" if self.current_player == self.player1
                else "⭕"
            )

            self.board[position] = symbol

            button = self.children[position]

            button.label = symbol

            button.style = (
                discord.ButtonStyle.danger
                if symbol == "❌"
                else discord.ButtonStyle.primary
            )

            button.disabled = True

            # Check winner

            winner = self.check_winner()

            if winner:

                self.game_over = True

                for child in self.children:
                    child.disabled = True

                embed = discord.Embed(
                    title="🏆 TIC TAC TOE",
                    description=(
                        f"🎉 Congratulations {winner.mention}!\n\n"
                        f"**{symbol} Wins The Game!**"
                    ),
                    color=discord.Color.green()
                )

                embed.add_field(
                    name="Players",
                    value=(
                        f"❌ {self.player1.mention}\n"
                        f"⭕ {self.player2.mention}"
                    ),
                    inline=False
                )

                await interaction.response.edit_message(
                    embed=embed,
                    view=self
                )

                return

            # Check draw

            if "" not in self.board:

                self.game_over = True

                for child in self.children:
                    child.disabled = True

                embed = discord.Embed(
                    title="🤝 TIC TAC TOE",
                    description="**It's a Draw!**",
                    color=discord.Color.orange()
                )

                await interaction.response.edit_message(
                    embed=embed,
                    view=self
                )

                return

            # Switch player

            self.current_player = (
                self.player2
                if self.current_player == self.player1
                else self.player1
            )

            await interaction.response.edit_message(
                embed=self.get_embed(),
                view=self
            )

        return callback

    # ==========================
    # WINNER CHECK
    # ==========================

    def check_winner(self):

        winning_positions = [

            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),

            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),

            (0, 4, 8),
            (2, 4, 6)

        ]

        for a, b, c in winning_positions:

            if (
                self.board[a] != ""
                and self.board[a] == self.board[b]
                and self.board[b] == self.board[c]
            ):

                return (
                    self.player1
                    if self.board[a] == "❌"
                    else self.player2
                )

        return None

    # ==========================
    # GAME EMBED
    # ==========================

    def get_embed(self):

        embed = discord.Embed(
            title="🎮 TIC TAC TOE",
            description=(
                f"❌ **X:** {self.player1.mention}\n"
                f"⭕ **O:** {self.player2.mention}\n\n"
                f"🎯 **Current Turn:** "
                f"{self.current_player.mention}"
            ),
            color=discord.Color.blurple()
        )

        embed.set_footer(
            text="Quantum Guardians • Tic Tac Toe"
        )

        return embed

    # ==========================
    # TIMEOUT
    # ==========================

    async def on_timeout(self):

        self.game_over = True

        for child in self.children:
            child.disabled = True

        if self.message:

            try:

                await self.message.edit(
                    content="⌛ Game expired! Please start a new game.",
                    view=self
                )

            except discord.HTTPException:
                pass


# ==============================
# BOT READY
# ==============================

@bot.event
async def on_ready():

    print(f"Bot Online: {bot.user}")

    try:

        synced = await bot.tree.sync()

        print(f"Synced {len(synced)} Slash Commands")

    except Exception as error:

        print(f"Sync Error: {error}")


# ==============================
# TIC TAC TOE COMMAND
# ==============================

@bot.tree.command(
    name="tictactoe",
    description="Play Tic Tac Toe with your friend!"
)

@app_commands.describe(
    opponent="Select your opponent"
)

async def tictactoe(
    interaction: discord.Interaction,
    opponent: discord.Member
):

    if opponent.bot:

        await interaction.response.send_message(
            "❌ You cannot play against a bot!",
            ephemeral=True
        )
        return

    if opponent.id == interaction.user.id:

        await interaction.response.send_message(
            "❌ You cannot play against yourself!",
            ephemeral=True
        )
        return

    # Create game

    game = TicTacToe(
        interaction.user,
        opponent
    )

    await interaction.response.send_message(
        embed=game.get_embed(),
        view=game
    )

    game.message = await interaction.original_response()

from status import set_bot_status

@bot.event
async def on_ready():
    print(f"Bot Online: {bot.user}")

    await set_bot_status(bot)

    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} Slash Commands")

# ==============================
# RUN BOT
# ==============================

bot.run(TOKEN)