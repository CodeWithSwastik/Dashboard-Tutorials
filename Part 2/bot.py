import discord
from discord.ext import commands, ipc


class MyBot(commands.Bot):

	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)

		self.ipc = ipc.Server(self,secret_key = "Swas")

	async def on_ready(self):
		"""Called upon the READY event"""
		print("Bot is ready.")

	async def on_ipc_ready(self):
		"""Called upon the IPC Server being ready"""
		print("Ipc server is ready.")

	async def on_ipc_error(self, endpoint, error):
		"""Called upon an error being raised within an IPC route"""
		print(endpoint, "raised", error)


my_bot = MyBot(command_prefix = ">", intents = discord.Intents.default())


@my_bot.ipc.route()
async def get_guild_count(data):
	return len(my_bot.guilds) # returns the len of the guilds to the client

@my_bot.ipc.route()
async def get_guild_ids(data):
	final = []
	for guild in my_bot.guilds:
		final.append(guild.id)
	return final # returns the guild ids to the client


@my_bot.command()
async def hi(ctx):
	await ctx.send("Hi")

my_bot.ipc.start()
my_bot.run(TOKEN)