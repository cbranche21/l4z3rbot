from redbot.core import checks, commands, Config, bank
import discord

class Tts(commands.Cog):
    """ fk tts """
    def __init__(self):
        self.config = Config.get_conf(self, identifier=674492245219)
        default_member = {
            "tokens": 2
        }

        self.config.register_member(**default_member)

    async def getTokens(self, user: discord.Member):
        return self.config.member(user).tokens()

    async def setTokens(self, user: discord.Member, amount):
        return self.config.member(user).tokens.set(amount)

    async def addTokens(self, user: discord.Member, amount):
        tokens_count_old = await self.getTokens(user)
        await self.config.member(user).tokens.set(tokens_count_old + amount)
        return await self.getTokens(user)

    async def subtractTokens(self, user: discord.Member, amount):
        tokens_count_old = await self.getTokens(user)
        await self.config.member(user).tokens.set(tokens_count_old - amount)
        return await self.getTokens(user)

    @bank.cost(1)
    @commands.command()
    async def buytokens(self, ctx, amount, user: discord.Member = None):
        if user is None:
            user = ctx.author

        new_tokens_balance =  self.addTokens(user, amount)
        tts_role = discord.utils.get(ctx.guild.roles, name = "TTS")
        if new_tokens_balance > 0 and tts_role not in user.roles:
            await user.add_roles(tts_role)


    @commands.command()
    @checks.admin_or_permissions(administrator=True)
    async def resettokens(self, ctx, member: discord.Member):
        pass

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.tts:
            if isinstance(message.channel, discord.abc.PrivateChannel):
                return

            author = message.author
            valid_user = isinstance(author, discord.Member) and not author.bot
            if not valid_user:
                return

            if discord.utils.get(author.roles, name = "TTS"):
                tokens_count_old = await self.getTokens(author)
                await self.config.member(author).tokens.set(tokens_count_old - 1)
                await self.setTokens(author, tokens_count_old - 1)
                tokens_count_new = await self.getTokens(author)
                if tokens_count_new is 0:
                    tts_role = discord.utils.get(author.roles, name = "TTS")
                    await author.remove_roles(tts_role)