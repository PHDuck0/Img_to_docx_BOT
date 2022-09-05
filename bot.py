import logging
from typing import List

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import MediaGroupFilter
from aiogram.types import ContentType

from aiogram_media_group import media_group_handler

with open('token.txt', 'r') as token_file:
    API_TOKEN = token_file.read()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)

# For example use simple MemoryStorage for Dispatcher.
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply(
        'Привіт, я бот для конвертування твого конспекту в ворд.\nПросто надішли одне або кілька фото для конвертації.')


@dp.message_handler(MediaGroupFilter(is_media_group=True), content_types=ContentType.PHOTO)
@media_group_handler
async def album_handler(messages: List[types.Message]):
    """
    Handle multiple photos
    """

    await messages[-1].reply('Надіслано більш ніж 1 фото')


@dp.message_handler(content_types=ContentType.PHOTO)
async def one_photo_handler(message: types.Message):
    """
    Handle one photo
    """
    print(message)
    await message.reply("Успішно.")


@dp.message_handler(content_types=['document'])
async def wrong_format(message: types.Message):
    """
    This handler will be called when user sends document instead of photo
    """

    await message.reply("Надішліть фото зі стисненням.")


@dp.message_handler()
async def echo(message: types.Message):
    await message.reply("Надішліть одне або декілька фото для вставки в docx file")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
