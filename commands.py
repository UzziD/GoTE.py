import os
from discord.ext import commands
from discord.ext.commands.core import is_owner
import requests
from dotenv import load_dotenv
load_dotenv()
IP = os.getenv('IP')

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name='log')
    async def logspirit(self, ctx, count: int, *items):

        if count <= 0:
            raise commands.BadArgument

        item = ' '.join(items)

        entryUrl = "http://" + IP + "/addEntry/"

        #snag csrf cookie for posting purposes and verifying this post req is safe
        connection = requests.session()
        connection.get(entryUrl)
        csrftoken = connection.cookies['csrftoken']

        userData = {'item':item, 'count':count, 'author':ctx.message.author.name, 'csrfmiddlewaretoken':csrftoken}

        status = connection.post(entryUrl,data=userData,headers=dict(Referrer=entryUrl))
        print(str(status.status_code) + " : received for url: " + status.url + " with request " + status.text)

        if status.status_code == 200:
            await ctx.send("Logged: {} {}".format(count, item))
        else:
            await ctx.send("There was an error. Server returned: %d" % status.status_code)

    @logspirit.error
    async def logspirit_error(self,ctx,error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Invalid arguments provided. Format: !log <item name> <positive count of item>")
        else:
            print("error on command: {}".format(ctx.command))
            print(error)
            await ctx.send("There was an error!")


    @commands.command(name='shutdown')
    @is_owner()
    async def shutdown(self, ctx):
        print("shutting down")
        await self.bot.close()

    @shutdown.error
    async def shutdown_error(self,ctx,error):
        if isinstance(error, commands.NotOwner):
            await ctx.send("Only the owner of the bot can shut it down.")
        else:
            print("error shutting down: {}".format(error))
            await ctx.send("Error shutting down, check terminal.")