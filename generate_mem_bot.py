from aiogram import Bot, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, FSInputFile
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont
import os
import random
import asyncio

load_dotenv('tokens/BOT.env') # загрузка токена
TOKEN = os.getenv('TOKEN')

if not TOKEN:
    raise ValueError('not TOKEN')

DOWNLOAD_DIR = "images/user_photos" # создание папки если её нет
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

bot = Bot(token=TOKEN)
dp = Dispatcher()
folders = ['anger', 'sadness', 'cats', 'dogs', 'happy', 'quest'] # списки для хранения названий файлов
anger_images = ['1_anger.jpg', '2_anger.png', '3_anger.png', '4_cats_anger.jpg', '5_anger.png', '6_anger.jpg', '7_dogs_anger.png', '8_cats_anger.jpg', '9_anger.jpg', '10_anger.jpg']
sadness_images = ['1_sadness.jpg', '2_cats_sadness.jpg', '3_sadness.png', '4_sadness.png', '5_sadness.png', '6_sadness.jpg', '7_sadness.jpg', '8_sadness.jpg', '9_dogs_sadness.png', '10_cats_sadness.jpg']
cats_images = ['1_cats.jpg', '2_cats_sadness.jpg', '3_cats.jpg', '4_cats_anger.jpg', '5_cats.jpg', '6_cats.png', '7_cats.png', '8_cats_anger.jpg', '9_cats,jpg', '10_cats_sadness.jpg']
dogs_images = ['1_dogs.png', '2_dogs.png', '3_dogs.jpg', '4_dogs.jpeg', '5_dogs.png', '6_dogs.jpg', '7_dogs_anger.png', '8_dogs.jpg', '9_dogs_sadness.png', '10_dogs.png']
happy_images = ['1_happy.jpg', '2_happy.jpeg', '3_happy.jpg', '4_happy.jpg', '5_happy.png', '6_happy.jpeg', '7_happy.jpg', '8_happy.jpg', '9_happy.png', '10_happy.png']
quest_images = ['1_quest.jpg', '2_quest.png', '3_quest.jpg', '4_quest.png', '5_quest.jpg', '6_quest.jpg', '7_quest.jpg', '8_quest.png', '9_quest.png', '10_quest.png']
random_words = ['пиздец', 'нищий', 'срать', 'сухарики', 'ебать', 'бульбасик', 'чупеп', 'асфальт', 'какашечки', 'ахуеть', 'бан', 'мут', 'ебнулся', 'обосрался'] # рандомные слова как надписи
random_words_sadness = ['пукнул', 'это пиздец', 'не прощу', 'жаль', 'муки']
random_words_quest = ['за что?', 'почему?', 'куда?', 'зачем?', 'ладно']

class ImageInfo(StatesGroup):
    image_path = State()
    text = State()
    type = State()

@dp.message(lambda message: message.text == '/start') # команда приветствия
async def start(message: Message):
    await message.answer('Привет, я бот для генерации мемов. Напиши /mem и я сгенерирую тебе рандомный мем с текстом из своих картинок. Напиши /my_mem и я сгенерирую тебе твой личный мем')

@dp.message(lambda message: message.text == '/mem') # команда для генерации мема из изображений папок
async def mem(message: Message):
    folder = random.choice(folders)
    image_fon = Image.open('images/fon_quest/fon_quest.png')
    if folder == 'anger':
        random_image = random.choice(anger_images)
        image = Image.open('images/' + folder + '/' + random_image)
        image = image.resize((1200, 1300))
    elif folder == 'sadness':
        random_image = random.choice(sadness_images)
        image = Image.open('images/' + folder + '/' + random_image)
        image = image.resize((1200, 1300))
    elif folder == 'cats':
        random_image = random.choice(cats_images)
        image = Image.open('images/' + folder + '/' + random_image)
        image = image.resize((1200, 1300))
    elif folder == 'dogs':
        random_image = random.choice(dogs_images)
        image = Image.open('images/' + folder + '/' + random_image)
        image = image.resize((1200, 1300))
    elif folder == 'happy':
        random_image = random.choice(happy_images)
        image = Image.open('images/' + folder + '/' + random_image)
        image = image.resize((1200, 1300))
    elif folder == 'quest':
        random_image = random.choice(quest_images)
        image = Image.open('images/' + folder + '/' + random_image)
        image = image.resize((1200, 1300))
    else:
        raise ValueError('not image_path')

    if folder == 'quest':
        image_fon = image_fon.resize((1550, 2000))
        font = ImageFont.truetype('images/fonts/russian.ttf', 130)
        draw = ImageDraw.Draw(image_fon)
        image_fon.paste(image, (160, 180))
        draw.text((500, 1800), random.choice(random_words_quest), fill=(255, 255, 255), font=font)
        image_fon.save('images/save/result.png')
        photo = FSInputFile('images/save/result.png')
        await message.answer_photo(photo, caption=f'Вот сгенерированный мем. Тип: {folder}')

    elif folder == 'sadness':
        font = ImageFont.truetype('images/fonts/russian.ttf', 130)
        draw = ImageDraw.Draw(image)
        draw.text((300, 1150), random.choice(random_words_sadness), fill=(255, 255, 255), font=font)
        image.save('images/save/result.png')
        photo = FSInputFile('images/save/result.png')
        await message.answer_photo(photo, caption=f'Вот сгенерированный мем. Тип: {folder}')

    else:
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('images/fonts/russian.ttf', 130)
        draw.text((300, 1150), random.choice(random_words), fill=(255, 255, 255), font=font)
        image.save('images/save/result.png')
        photo = FSInputFile('images/save/result.png')
        await message.answer_photo(photo, caption=f'Вот сгенерированный мем. Тип: {folder}')

@dp.message(lambda message: message.text == '/my_mem') # команда для создания своего мема
async def image(message: Message, state: FSMContext):
    await state.set_state(ImageInfo.image_path)
    await message.answer('Отправь фото для того чтобы сделать из него мем')

@dp.message(ImageInfo.image_path)
async def text(message: Message, state: FSMContext):
    if message.photo:
        photo = message.photo[-1]

        file_info = await bot.get_file(photo.file_id)
        file_path = file_info.file_path

        filename = f"user_{message.from_user.id}_{photo.file_id}.jpg"
        save_path = os.path.join(DOWNLOAD_DIR, filename)

        await bot.download_file(file_path, save_path)
        await state.update_data(image_path=save_path)
        await state.set_state(ImageInfo.text)
        await message.answer('Теперь отправь мне текст для этого изображения (максимум 15 символов)')

@dp.message(ImageInfo.text)
async def type(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.set_state(ImageInfo.type)
    await message.answer('Теперь напиши мне тип твоего мема (quest или none)')

@dp.message(ImageInfo.type)
async def create_mem(message: Message, state: FSMContext):
    await state.update_data(type=message.text)
    data = await state.get_data()
    if len(data['text']) < 9:
        if data['type'] == 'quest':
            image = Image.open(str(data['image_path']))
            image_fon = Image.open('images/fon_quest/fon_quest.png')
            font = ImageFont.truetype('images/fonts/russian.ttf', 130)
            image = image.resize((1200, 1300))
            image_fon = image_fon.resize((1550, 2000))
            draw = ImageDraw.Draw(image_fon)
            image_fon.paste(image, (160, 180))
            draw.text((500, 1800), data['text'], fill=(255, 255, 255), font=font)
            image_fon.save(f'images/user_photos/{message.from_user.id}.png')
            photo = FSInputFile(f'images/user_photos/{message.from_user.id}.png')
            await message.answer_photo(photo=photo, caption='Вот ваш мем')
        else:
            image = Image.open(str(data['image_path']))
            font = ImageFont.truetype('images/fonts/russian.ttf', 130)
            image = image.resize((1200, 1300))
            draw = ImageDraw.Draw(image)
            draw.text((300, 1150), data['text'], fill=(255, 255, 255), font=font)
            image.save(f'images/user_photos/{message.from_user.id}.png')
            photo = FSInputFile(f'images/user_photos/{message.from_user.id}.png')
            await message.answer_photo(photo=photo, caption='Вот ваш мем')
    else:
        if data['type'] == 'quest':
            image = Image.open(str(data['image_path']))
            image_fon = Image.open('images/fon_quest/fon_quest.png')
            font = ImageFont.truetype('images/fonts/russian.ttf', 130)
            image = image.resize((1200, 1300))
            image_fon = image_fon.resize((1550, 2000))
            draw = ImageDraw.Draw(image_fon)
            image_fon.paste(image, (160, 180))
            draw.text((200, 1800), data['text'], fill=(255, 255, 255), font=font)
            image_fon.save(f'images/user_photos/{message.from_user.id}.png')
            photo = FSInputFile(f'images/user_photos/{message.from_user.id}.png')
            await message.answer_photo(photo=photo, caption='Вот ваш мем')
        else:
            image = Image.open(str(data['image_path']))
            font = ImageFont.truetype('images/fonts/russian.ttf', 130)
            image = image.resize((1200, 1300))
            draw = ImageDraw.Draw(image)
            draw.text((100, 1150), data['text'], fill=(255, 255, 255), font=font)
            image.save(f'images/user_photos/{message.from_user.id}.png')
            photo = FSInputFile(f'images/user_photos/{message.from_user.id}.png')
            await message.answer_photo(photo=photo, caption='Вот ваш мем')

async def main(): # главный цикл
    while True:
        try:
            print('Запуск бота')
            await dp.start_polling(bot)
        except Exception as e:
            print(f'Ошибка {e}')
            print('Перезапуск бота')
            await asyncio.sleep(3)


if __name__ == '__main__':
    asyncio.run(main())