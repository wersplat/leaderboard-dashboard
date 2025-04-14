from ..utils.logging import setup_logging

logger = setup_logging()


class AdminControls(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="resend_game")
    async def resend_game(self, ctx, game_id: str):
        if not is_admin(ctx.author.id):
            logger.warning(f"Unauthorized attempt by {ctx.author} to use {ctx.command}.")
            await ctx.send("🚫 You do not have permission to use this command.")
            return

        await ctx.send(f"Game `{game_id}` re-sent to Google Sheets.")

def setup(bot):
    bot.add_cog(AdminControls(bot))
