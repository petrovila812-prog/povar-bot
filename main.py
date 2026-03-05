import static_ffmpeg
static_ffmpeg.add_paths()
import asyncio
import os    
import yt_dlp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile

# Твій токен
API_TOKEN = "8520855795:AAF5eL84XicN5tZ8uLJHidMav3n0bcPbX9g"
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Налаштування для сервера (Render сам знайде ffmpeg)
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': '%(title)s.%(ext)s',
    'noplaylist': True,
}

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    photo_path = "artem.jpg"
    welcome_text = "👋 Салам. На зв'язку Повар.\n\nБот заряджений на пошук музики. Починай."
    if os.path.exists(photo_path):
        await message.answer_photo(photo=FSInputFile(photo_path), caption=welcome_text)
    else:
        await message.answer(welcome_text)

@dp.message()
async def search_music(message: types.Message):
    if not message.text or message.text.startswith('/'): return
    query = message.text
    status_msg = await message.answer(f"🔎 Шукаю: **{query}**...")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{query}", download=True)['entries'][0]
            filename = ydl.prepare_filename(info).rsplit('.', 1)[0] + '.mp3'
        await message.answer_audio(FSInputFile(filename))
        if os.path.exists(filename): os.remove(filename)
        await status_msg.delete()
    except Exception as e:
        await message.answer(f"❌ Помилка: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())