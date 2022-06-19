import logging
import asyncio
from telethon import TelegramClient, events, Button
from decouple import config
from telethon.tl.functions.users import GetFullUserRequest

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.INFO)

# start the bot
print("Starting...")
try:
    apiid = config("APP_ID", cast=int)
    apihash = config("API_HASH")
    bottoken = config("BOT_TOKEN")
    frm = config("FROM_CHANNEL", cast=int)
    tochnl = config("TO_CHANNEL", cast=int)
    SESSION = config("SESSION")
    datgbot = TelegramClient('bot', apiid, apihash).start(bot_token=bottoken)
    #datgbot = TelegramClient(StringSession(SESSION), apiid, apihash)
    #datgbot.start()
except:
    print("Environment vars are missing! Kindly recheck.")
    print("Bot is quiting...")
    exit()


@datgbot.on(events.NewMessage(pattern="/run"))
async def _(event):
    ok = await datgbot(GetFullUserRequest(event.sender_id))
    await event.reply(f"Hi `{ok.user.first_name}`!\n\nI am a channel auto-forward bot!! Read /info to know more!\n\nI can be used in only two channels (one user) at a time.", buttons=[Button.url("web", url="https://github.com"), Button.url("Group", url="https://t.me/cinemaforyou07")], link_preview=False)


@datgbot.on(events.NewMessage(pattern="/info"))
async def helpp(event):
    await event.reply("**Info**\n\nThis bot will send all new posts in one channel to the other channel. (without forwarded tag)!\nIt can be used only in two channels at a time, so kindly deploy your own bot from [here](https://github.com/soymadip).\n\nAdd me to both the channels and make me an admin in both, and all new messages would be autoposted on the linked channel!!", link_preview=False)

@datgbot.on(events.NewMessage(incoming=True, chats=frm)) 
async def _(event): 
    if not event.is_private:
        try:
            if event.poll:
                print("skipped poll.")
            if event.sticker:
                return
            if event.photo:
                print("skipped pic.")
            elif event.media:
                try:
                    if event.media.webpage:
                        print("skipped links.")
                except:
                    media = event.media.document
                    await datgbot.send_file(tochnl, media, caption = f"`{event.file.name}`", link_preview = False)
                    return
            else:
                print("skipped text.")
        except:
            print("TO_CHANNEL ID is wrong or I can't send messages there (make me admin).")



print("Bot started.")
datgbot.run_until_disconnected()
