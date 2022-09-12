from ast import While
import threading
import badStrLib
import call_worker
import hikari
import logging
import time
import asyncio
import json
import badStrLib
import call_worker

#Parse the private items like passwords from the .json and load them into memory
token = ""
worker_pw = ""
worker_url =""
with open("../private.json") as file:
    tokenjson = json.load(file)
    token = tokenjson["Token"]
    worker_pw = tokenjson["password"]
    worker_url =tokenjson["url"]


logging.basicConfig(filename="../QB.log")
bot = hikari.GatewayBot(token=token)
worker_mutex = threading.Lock()

#Wrapper function for calling the worker
async def easy_worker(content):
    global worker_pw
    global worker_url
    return call_worker.call_bot_worker(content, worker_pw, worker_url)

async def egg_timer(wait_amnt: int, event):
    now =time.time()
    end = now + wait_amnt
    while True:
        await asyncio.sleep(1)
        if (time.time()>=end):
            break
    await event.message.respond("ding!")

    
async def auto_caller_ini():
    print("autocaller set up!")


#Automatically calls the Cloud Flare worker every minute 
async def auto_call_worker():
    global worker_mutex
    payload = {
        "op": "AutoCall",
        "id": 0
    }
    task = asyncio.create_task(auto_caller_ini())
    # about every minute or so, call the worker to get an update
    while True:
        await task
        asyncio.sleep(59)
        worker_mutex.acquire()
        id = 0
        with open("../id.txt","r") as file:
            id = int(file.read())
        payload["id"] = id
        response = easy_worker(payload)
        task = asyncio.create_task(handle_auto_call(response))

#Handler for the response from the autocaller
async def handle_auto_call(response):
    #Check if we have a status code
    status_code = 0
    try:
        status_code = response.status_code
    except:
        worker_mutex.release
        return
    if response.status_code == 200:
        with open("../id.txt","r+") as file:
            id = int(file.read())
            id+=1
            file.write(str(id))
    else:
        #If IDs are out of sync, update them
        if response.text.startswith("False ID, expected: "):
            id = int(response.text[20:])
            with open("../id.txt","r+") as file:
                file.write(str(id))
    worker_mutex.release()
    #
    # Actual handling of response goes here
    #
    return

tasks = []

#Handle User messages
@bot.listen()
async def MessageHandler(event: hikari.GuildMessageCreateEvent) -> None:
    #Ignore the message if its a robot
    if event.is_bot or not event.content:
        return
    #Ping Pong, the hello world of discord bots
    if event.content.startswith("ping"):
        await event.message.respond("Pong!")
    #waits n seconds, then goes ding!
    if event.content.startswith("!et"):
        inp = int(badStrLib.keep(event.content, "0123456789"), 10)
        tasks.append(asyncio.create_task(egg_timer(inp, event)))

#inject the auto caller into the event loop     
tasks.append(asyncio.get_running_loop().call_soon(auto_call_worker))

bot.run()
