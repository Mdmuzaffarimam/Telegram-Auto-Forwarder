from pyrogram import Client, filters
from config import API_ID, API_HASH, INCOMING, OUTGOING

waiting_phone = {}
waiting_code = {}
waiting_pass = {}
waiting_in = {}
waiting_out = {}

user = Client("user", api_id=API_ID, api_hash=API_HASH)

@user.on_message(filters.private)
async def handler(c, m):
    uid = m.from_user.id

    if waiting_phone.get(uid):
        waiting_phone.pop(uid)
        await c.send_code(m.text)
        waiting_code[uid] = True
        return await m.reply("Enter OTP")

    if waiting_code.get(uid):
        waiting_code.pop(uid)
        try:
            await c.sign_in(m.text)
            await m.reply("Login successful ✅")
        except:
            waiting_pass[uid] = True
            await m.reply("Send 2FA password")
        return

    if waiting_pass.get(uid):
        waiting_pass.pop(uid)
        await c.check_password(m.text)
        await m.reply("Login successful ✅")
        return

    if waiting_in.get(uid):
        waiting_in.pop(uid)
        INCOMING.append(m.text)
        return await m.reply("Source added")

    if waiting_out.get(uid):
        waiting_out.pop(uid)
        OUTGOING.append(m.text)
        return await m.reply("Target added")

async def start_forward():
    await user.start()

    for chat in INCOMING:
        @user.on_message(filters.chat(chat))
        async def forward(_, msg):
            for out in OUTGOING:
                await msg.copy(out)
