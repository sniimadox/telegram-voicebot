from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import Update
from pytgcalls.types.stream import StreamAudioEnded
import os, asyncio

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
call = PyTgCalls(app)

@call.on_stream_end()
async def on_end(_, update: Update):
    print("Stream ended in", update.chat_id)

@app.on_message(filters.command("join"))
async def join_vc(_, message):
    chat_id = message.chat.id
    try:
        await call.join_group_call(chat_id)
        await call.mute_stream(chat_id)
        await message.reply_text("✅ Joined the voice chat and muted.")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

@app.on_message(filters.command("leave"))
async def leave_vc(_, message):
    chat_id = message.chat.id
    try:
        await call.leave_group_call(chat_id)
        await message.reply_text("👋 Left the voice chat.")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

@app.on_message(filters.command("mute"))
async def mute_vc(_, message):
    chat_id = message.chat.id
    try:
        await call.mute_stream(chat_id)
        await message.reply_text("🔇 Muted.")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

@app.on_message(filters.command("unmute"))
async def unmute_vc(_, message):
    chat_id = message.chat.id
    try:
        await call.unmute_stream(chat_id)
        await message.reply_text("🎙️ Unmuted.")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")

@app.on_message(filters.command("status"))
async def status(_, message):
    await message.reply_text("🤖 Bot is running and ready!")

async def main():
    await app.start()
    await call.start()
    print("Bot started.")
    await asyncio.get_event_loop().create_future()

asyncio.run(main())
