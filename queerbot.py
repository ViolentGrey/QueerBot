#Read token from file and parse it
import asyncio
import json
token = ""
with open("../token.json") as file:
    tokenjson = json.load(file)
    token = tokenjson["Token"]



import hikari
import logging
import time
logging.basicConfig(filename="../QB.log")

bot = hikari.GatewayBot(token=token)
import badStrLib
async def egg_timer(wait_amnt: int, event):
    now =time.time()
    end = now + wait_amnt
    while True:
        time.sleep(0.5)
        if (time.time()>=end):
            break
    await event.message.respond("ding!")

class hard_boiled(hikari.events.base_events.Event):
    type = ""
    def __init__(self, type) -> None:
        self.type = type



tasks = []

#the hello world of bots, ping pong
@bot.listen()
async def ping(event: hikari.GuildMessageCreateEvent) -> None:
    # If a non-bot user sends a message "hk.ping", respond with "Pong!"
    # We check there is actually content first, if no message content exists,
    # we would get `None' here.
    if event.is_bot or not event.content:
        return

    if event.content.startswith("ping"):
        await event.message.respond("Pong!")
    
    if event.content.startswith("!et"):
        inp = int(badStrLib.keep(event.content, "0123456789"), 10)
        tasks.append(asyncio.create_task(egg_timer(inp, event)))
        

bot.run()