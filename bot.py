from pyrogram import Client, filters
import user
from config import BOT_TOKEN

bot = Client("bot", bot_token=BOT_TOKEN)

@bot.on_message(filters.command("start"))
async def start(_, m):
    await m.reply("Welcome!\nUse /authorize to login")

@bot.on_message(filters.command("authorize"))
async def auth(_, m):
    user.waiting_phone[m.from_user.id] = True
    await m.reply("Send your phone number with country code")

@bot.on_message(filters.command("incoming"))
async def incoming(_, m):
    user.waiting_in[m.from_user.id] = True
    await m.reply("Send SOURCE chat id / username")

@bot.on_message(filters.command("outgoing"))
async def outgoing(_, m):
    user.waiting_out[m.from_user.id] = True
    await m.reply("Send TARGET chat id / username")

@bot.on_message(filters.command("work"))
async def work(_, m):
    await user.start_forward()
    await m.reply("Auto forwarding started ✅")

bot.run()
