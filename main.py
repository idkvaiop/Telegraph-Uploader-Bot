import os
from telegraph import upload_file
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


Bot = Client(
    "Telegraph Uploader Bot",
    bot_token=os.environ.get("BOT_TOKEN"),
    api_id=int(os.environ.get("API_ID")),
    api_hash=os.environ.get("API_HASH")
)

DOWNLOAD_LOCATION = os.environ.get("DOWNLOAD_LOCATION", "./DOWNLOADS/")

START_TEXT = """Hello {},
I am Akira Telegraph Uploader Bot !

I can help you to make telegra.ph links of the image you sent in my PM.

"""

HELP_TEXT = """**About Me**

• Give me a media.
• After that, I will download it to my [server](https://telegram.me/Akira_News).
• I will then upload it to the telegraph.

Follow [Akira News](https://telegram.dog/Akira_News) to be updated !"""

ABOUT_TEXT = """**About Me**

- **Bot :** `Akira Telegraph Uploader`
- **Creator :** [Noob Akhil](https://telegram.me/AKH1LS)
- **Channel :** [JOIN](https://telegram.me/Akira_News)
- **Language :** [Python3](https://python.org)
- **Library :** [Pyrogram](https://pyrogram.org)"""

START_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Help', callback_data='help'),
            InlineKeyboardButton('About', callback_data='about'),
            InlineKeyboardButton('Close', callback_data='close')
        ]
    ]
)

HELP_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Home', callback_data='home'),
            InlineKeyboardButton('About', callback_data='about'),
            InlineKeyboardButton('Close', callback_data='close')
        ]
    ]
)

ABOUT_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Channel', url='https://telegram.me/Akira_News'),
            InlineKeyboardButton('Support', url='https://telegram.me/Akira_Support')
        ],
        [
            InlineKeyboardButton('Home', callback_data='home'),
            InlineKeyboardButton('Help', callback_data='help'),
            InlineKeyboardButton('Close', callback_data='close')
        ]
    ]
)


@Bot.on_callback_query()
async def cb_data(bot, update):
    
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=START_BUTTONS
        )
    
    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            disable_web_page_preview=True,
            reply_markup=HELP_BUTTONS
        )
    
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT,
            disable_web_page_preview=True,
            reply_markup=ABOUT_BUTTONS
        )
    
    else:
        await update.message.delete()
    

@Bot.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    
    await update.reply_text(
        text=START_TEXT.format(update.from_user.mention),
        disable_web_page_preview=True,
        quote=True,
        reply_markup=START_BUTTONS
    )


@Bot.on_message(filters.private & filters.media)
async def getmedia(bot, update):
    
    medianame = DOWNLOAD_LOCATION + str(update.from_user.id)
    
    try:
        message = await update.reply_message(
            text="`Processing...`",
            quote=True,
            disable_web_page_preview=True
        )
        await bot.download_media(
            message=update,
            file_name=medianame
        )
        response = upload_file(medianame)
        try:
            os.remove(medianame)
        except:
            pass
    except Exception as error:
        text=f"Error :- <code>{error}</code>"
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton('More Help', callback_data='help')]]
        )
        await message.edit_text(
            text=text,
            disable_web_page_preview=True,
            reply_markup=reply_markup
        )
        return
    
    text=f"**Link :-** `https://telegra.ph{response[0]}`\n\n**Join :-** @Akira_Support for any query !"
    reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="✓ get the telegra.ph link", url=f"https://telegra.ph{response[0]}"),
                InlineKeyboardButton(text="✓ share the telegra.ph link", url=f"https://telegram.me/share/url?url=https://telegra.ph{response[0]}")
            ],
            [
                InlineKeyboardButton(text="Creator", url="https://telegram.me/AKH1LS")
            ]
        ]
    )
    
    await message.edit_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )


Bot.run()
