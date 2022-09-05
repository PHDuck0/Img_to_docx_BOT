import logging
from pathlib import Path
from typing import List

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import MediaGroupFilter
from aiogram.types import ContentType

from aiogram_media_group import media_group_handler

from convert import save_as_docx

BASE_DIR = Path(__file__).resolve().parent
MEDIA_FOLDER = BASE_DIR / 'media'
DOCX_FOLDER = BASE_DIR / 'documents'

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
    await message.reply('''
    Привіт, я бот для конвертування фото твого конспекту в ворд.
Просто надішли одне або кілька фото одним повідомленням для конвертації.''')


@dp.message_handler(MediaGroupFilter(is_media_group=True), content_types=ContentType.PHOTO)
@media_group_handler
async def album_handler(messages: List[types.Message]):
    """
    Handle multiple photos
    """

    docx_filepath = DOCX_FOLDER / (messages[0].from_user.full_name + '.docx')

    # save photos from the message
    photo_paths = []
    for i, message in enumerate(messages):
        photo_filepath = MEDIA_FOLDER / (message.from_user.full_name + str(i) + '.jpg')
        photo_paths.append(photo_filepath)
        await message.photo[-1].download(destination_file=photo_filepath)

    save_as_docx(docx_filepath, photo_paths)
    await messages[-1].reply_document(open(str(docx_filepath), 'rb'))
    docx_filepath.unlink()


@dp.message_handler(content_types=ContentType.PHOTO)
async def one_photo_handler(message: types.Message):
    """
    Handle one photo
    """

    photo_filepath = MEDIA_FOLDER / (message.from_user.full_name + '.jpg')
    docx_filepath = DOCX_FOLDER / (message.from_user.full_name + '.docx')

    await message.photo[-1].download(destination_file=photo_filepath)
    save_as_docx(docx_filepath, [photo_filepath])
    await message.reply_document(open(str(docx_filepath), 'rb'))
    docx_filepath.unlink()


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
