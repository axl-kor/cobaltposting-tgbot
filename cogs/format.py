import cog


class Handler(cog.Cog):
    def __init__(self, bot: cog.Bot):
        super().__init__(bot)

    @cog.regMessage(cog.F.text == "/format")
    async def command(self, message: cog.Message):
        await message.answer(
            "Sorry! This command is not yet implemented.\nBut you can contribute this bot on GitHub: https://github.com/okiscape/cobaltposting-tgbot"
        )


def setup(bot: cog.Bot):
    Handler(bot=bot).register()
