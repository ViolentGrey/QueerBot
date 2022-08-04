#Read token from file and parse it
import json
token = ""
with open("../token.json") as file:
    tokenjson = json.load(file)
    token = tokenjson["Token"]



import hikari
import logging
logging.basicConfig(filename="../QB.log")

bot = hikari.GatewayBot(token=token)

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

bot.run()