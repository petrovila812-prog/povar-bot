import asyncio
import os
import yt_dlp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import FSInputFile

# === НАЛАШТУВАННЯ ===
# Твій токен (взято з твого скрина image_85cbbc.png)
API_TOKEN = "8520855795:AAF5eL84XicN5tZ8uLJHidMav3n0bcPbX9g"
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Налаштування завантажувача музики
ydl_opts = {
    'format': 'bestaudio/best',
    'ffmpeg_location': './', 
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': '%(title)s.%(ext)s',
    'noplaylist': True,
}

# === ПРИВІТАННЯ ВІД ПОВАР ===
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Шлях до файлу в папці проєкту
    photo_path = "artem.jpg"
    
    welcome_text = (
        "👋 Салам. На зв'язку Повар.\n\n"
        "Бот заряджений на пошук музики. Скидаєш назву — отримуєш чистий MP3-файл.\n\n"
        "Все по справі. Починай."
    )

    if os.path.exists(photo_path):
        photo = FSInputFile(photo_path)
        await message.answer_photo(photo=photo, caption=welcome_text, parse_mode="Markdown")
    else:
        # Якщо фото забув покласти, бот просто напише текст
        await message.answer(welcome_text, parse_mode="Markdown")
        print(f"Помилка: Файл {photo_path} не знайдено в папці!")

# === ЛОГІКА ПОШУКУ ===
@dp.message()
async def search_music(message: types.Message):
    if not message.text or message.text.startswith('/'): return

    query = message.text
    status_msg = await message.answer(f"🔎 Шукаю: **{query}**...", parse_mode="Markdown")
    await bot.send_chat_action(message.chat.id, action="upload_voice")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{query}", download=True)['entries'][0]
            filename = ydl.prepare_filename(info).rsplit('.', 1)[0] + '.mp3'

        audio_file = FSInputFile(filename)
        await message.answer_audio(
            audio_file, 
            caption=f"✅ Готово для тебе!",
            title=info.get('title'),
            performer=info.get('uploader')
        )
        
        if os.path.exists(filename):
            os.remove(filename)
        await status_msg.delete()

    except Exception as e:
        await message.answer(f"❌ Помилка: {e}")
        if 'status_msg' in locals():
            await status_msg.delete()

async def main():
    print("Бот запущений! Повар на зв'язку.")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
