from typing import List
import discord
from discord.ext import commands


class TicTacToeButton(discord.ui.Button["TicTacToe"]):
    def __init__(self, x: int, y: int):
        super().__init__(style=discord.ButtonStyle.secondary,
                         label="\u200b",
                         row=y)
        self.x = x
        self.y = y

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if view.current_player == view.X:
            self.style = discord.ButtonStyle.danger
            self.label = "X"
            self.disabled = True
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = "It is now O turn"
        else:
            self.style = discord.ButtonStyle.success
            self.label = "O"
            self.disabled = True
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = f"It is now  X's turn"

        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = "x won!"
            elif winner == view.O:
                content = "o won!"
            else:
                content = "It's a tie! - Both of u are Equally Bad"
            for child in view.children:
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)


class TicTacToe(discord.ui.View):
    children: List[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self, ctx, p2):
        super().__init__()
        self.ctx = ctx
        self.p2 = p2
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        # Our board is made up of 3 by 3 TicTacToeButtons
        # The TicTacToeButton maintains the callbacks and helps steer
        # the actual game.
        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    # This method checks for the board winner -- it is used by the TicTacToeButton
    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check vertical
        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][
                line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check diagonals
        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        # If we're here, we need to check if a tie was made
        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None

    async def interaction_check(self, interaction) -> bool:
        if interaction.user == self.ctx.author or interaction.user == self.p2:
            return True
        else:
            if self.p2 is None :
                await interaction.response.send_message(
                    f"Hey, you can't click this. Its a Single player board for {self.ctx.author.name}",
                    ephemeral=True)
                return False
            else :    
                await interaction.response.send_message(
                    f"Hey, you can't click this. Its a match between {self.ctx.author.name} and {self.p2.name}",
                    ephemeral=True)
                return False


class tic(commands.Cog):
    @commands.command(aliases=['tic', 'tictactoe'])
    async def ttt(self, ctx: commands.Context, p2: discord.Member = None):
        """Starts a tic-tac-toe game with yourself."""
        p1 = ctx.message.author
        if p2 is None or p2 == p1:
            await ctx.send(f"Tic Tac Toe: {p1.mention} (Single Player Mode) ",
                           view=TicTacToe(ctx=ctx, p2=p2))
        elif p2 == ctx.message.guild.me:
            await ctx.send(
                f"You want to play? Alright lets play.\n**{ctx.message.guild.me} WIN!**\nI win, so quick you didn't even notice it."
            )
        else:
            await ctx.send(
                f"Tic Tac Toe(2 Player)[{p1.mention},{p2.mention}]:/n X goes first",
                view=TicTacToe(ctx=ctx, p2=p2))

def setup(client):
    client.add_cog(tic(client))
