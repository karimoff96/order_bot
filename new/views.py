import types
from telebot import *
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from telebot.types import InputMediaPhoto
from .models import *

# Create your views here.
bot = TeleBot('5057190321:AAHJ4XACu_8criwP2Qk2Kg5oySoBOL61KQQ', parse_mode="HTML")

hideBoard = types.ReplyKeyboardRemove()


@csrf_exempt
def index(request):
    if request.method == 'GET':
        return HttpResponse("<a href='http://t.me/dkarimoff96'>Created by</>")
    if request.method == 'POST':
        bot.process_new_updates([
            telebot.types.Update.de_json(
                request.body.decode("utf-8")
            )
        ])
        return HttpResponse(status=200)


@bot.message_handler(commands=["start"])
def start(message):
    if User.objects.filter(user_id=message.from_user.id).exists():
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        btn = types.KeyboardButton('Men')
        btn1 = types.KeyboardButton('Women')
        btn2 = types.KeyboardButton('Kids')
        btn3 = types.KeyboardButton('Home')
        markup.add(btn1, btn, btn2, btn3)
        bot.send_message(message.chat.id, "<b>📜Qaysi bo`limda e`lon berasiz?</b>", reply_markup=markup)
        bot_user = User.objects.get(user_id=message.from_user.id)
        order = Order.objects.create(
            user=bot_user
        )
        order.save()

    else:
        text = f'<i>Assalomu alaykum {message.from_user.first_name}.\n<b>📜Qaysi bo`limda e`lon berasiz?</b></i>'
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        btn = types.KeyboardButton('Men')
        btn1 = types.KeyboardButton('Women')
        btn2 = types.KeyboardButton('Kids')
        btn3 = types.KeyboardButton('Home')
        markup.add(btn1, btn, btn2, btn3)
        bot.send_message(message.chat.id, text, reply_markup=markup)
        bot_user = User.objects.create(user_id=message.from_user.id, username=message.from_user.username)
        bot_user.save()
        order = Order.objects.create(
            user=bot_user
        )
        order.save()


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot_user = User.objects.get(user_id=message.from_user.id)
    bot_order = Order.objects.get(user=bot_user, active=False)
    if message.text in ['Men', 'Women', 'Kids', 'Home']:
        bot_order.category = message.text
        bot_order.step = 1
        bot_order.save()
        text = f'<b><i>📋{bot_order.category}</i> bo`limini tanladingiz.\nSizga bir necha savollar beriladi.\nBarchasiga to`liq va aniq javob bering.</b> '
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        btn1 = types.KeyboardButton('🛑Bekor qilish')
        markup.add(btn1)
        bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.send_message(message.chat.id, "<b>Mahsulot nomini kiriting!</b>")
    elif bot_order.step == 1 and len(message.text) > 0 and message.text != '🛑Bekor qilish':
        bot_order.name = message.text
        bot_order.step = 2
        bot_order.save()
        bot.send_message(message.chat.id, "<b>💸Narxini kiriting:\nMasalan:</b> <i>260000</i>")
    elif bot_order.step == 2 and message.text.isdigit():
        bot_order.step = 3
        bot_order.price = message.text
        bot_order.save()
        bot.send_message(message.chat.id, 'Chegirma foizi(%) qancha? Masalan: 15')
    elif bot_order.step == 3 and message.text.isdigit():
        bot_order.step = 4
        bot_order.discount = message.text
        bot_order.save()
        bot.send_message(message.chat.id, 'Mavjud o`lchamlar: ')
    elif bot_order.step == 4 and len(message.text) > 0:
        bot_order.available_sizes = message.text
        bot_order.step = 5
        bot_order.save()
        bot.send_message(message.chat.id, 'Do’konimizda mavjud miqdori:')
    elif bot_order.step == 5 and message.text.isdigit():
        bot_order.available_amount = message.text
        bot_order.step = 6
        bot_order.save()
        bot.send_message(message.chat.id, 'Ishlab chiqarilgan sana: (DD:MM:YY)')
    elif bot_order.step == 6 and len(message.text) > 0:
        bot_order.date = message.text
        bot_order.step = 7
        bot_order.save()
        bot.send_message(message.chat.id, 'Mahsulot haqida qo`shimcha ma`lumotlar:')
    elif bot_order.step == 7 and len(message.text) > 0:
        bot_order.comment = message.text
        bot_order.step = 8
        bot_order.save()
        bot.send_message(message.chat.id, 'Mahsulot dastlabki sur`atini yuboring:')
    elif message.text == '🛑Bekor qilish':
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        btn = types.KeyboardButton('Men')
        btn1 = types.KeyboardButton('Women')
        btn2 = types.KeyboardButton('Kids')
        btn3 = types.KeyboardButton('Home')
        markup.add(btn1, btn, btn2, btn3)
        bot.send_message(message.chat.id, "<b>📜E`lon turini tanlang!</b>", reply_markup=markup)
        bot_order.step = 0
        bot_order.save()
    else:
        bot.send_message(message.chat.id, "<pre>‼️Iltimos to`g`ri ma`lumot kiriting!</pre>")


@bot.message_handler(content_types=['photo', 'file'])
def photo_handler(message):
    bot_user = User.objects.get(user_id=message.from_user.id)
    bot_order = Order.objects.get(user=bot_user, active=False)
    if bot_order.step == 8:
        raw = message.photo[1].file_id
        path = raw + ".jpg"
        file_info = bot.get_file(raw)
        downloaded_file = bot.download_file(file_info.file_path)
        content = ContentFile(downloaded_file)
        bot_order.image1.save(path, content, save=True)
        bot_order.step = 9
        bot_order.save()
        bot.send_message(message.from_user.id, "<b>Keyingi rasmni yuboring</b>")
    elif bot_order.step == 9:
        raw = message.photo[1].file_id
        path = raw + ".jpg"
        file_info = bot.get_file(raw)
        downloaded_file = bot.download_file(file_info.file_path)
        content = ContentFile(downloaded_file)
        bot_order.image2.save(path, content, save=True)
        bot_order.step = 10
        bot_order.save()
        bot.send_message(message.from_user.id, "<b>So`nggi rasmni yuboring</b>")
    elif bot_order.step == 10:
        raw = message.photo[1].file_id
        path = raw + ".jpg"
        file_info = bot.get_file(raw)
        downloaded_file = bot.download_file(file_info.file_path)
        content = ContentFile(downloaded_file)
        bot_order.image3.save(path, content, save=True)
        bot_order.step = 11
        bot_order.save()
        bot.send_message(message.from_user.id, "<b>☑️Rasmlar muvaffaqiyatli yuklandi</b>", reply_markup=hideBoard)
        text = f"<b>◽️Mahsulot nomi:</b> <i>{bot_order.name}.</i>\n" \
               f"<b>◾️Mahsulot to’lov raqami:</b><i> #{bot_order.id}</i>\n" \
               f"<b>◽️Chegirma foizi:</b> <i>{bot_order.discount} %</i>\n" \
               f"<b>◾️Mahsulot narxi</b> <i>{bot_order.price}</i> SUM\n" \
               f"<b>◽️Mavjud o’lchamlar:</b> <i>{bot_order.available_sizes} %</i>\n" \
               f"<b>◾️Do’konimizda mavjud:</b> <i>{bot_order.available_amount} dona%</i>\n" \
               f"<b>◽️Ishlab chiqarilgan muddat:</b> <i>{bot_order.date} %</i>\n" \
               f"<b>◾  Qo`shimcha:</b> <i>{bot_order.comment}</i> \n\n" \
               f"<b>🔻Sotib olish usullari:</b> \n" \
               f"<b>1️⃣Telegram to’lov tizimi orqali: https://t.me/..... </b> \n" \
               f"<b>2️⃣Saytimizdan sotib olish: link  </b> \n" \
               f"<b>3️⃣Qo’ng’iroq qilish orqali: nomer</b> \n\n" \
               f"<i>❗️Bizda 20 km bo’lgan masofadagi buyurtmachilarimizga tekin yetqazib beramiz!\n" \
               f"‼️Mahsulot sotib olingan kunning o’zida buyurtmachiga yetqaziladi!</i>\n\n" \
               f"<b>🔻Sizga yordam kerakmi?</b> @supportwemard\n\n" \
               f"<b>🔸Bizning kanal:</b> https://t.me/...."
        bot.send_media_group(chat_id=message.from_user.id,
                             media=[InputMediaPhoto(bot_order.image1, caption=f'{text}', parse_mode="HTML"),
                                    InputMediaPhoto(bot_order.image2),
                                    InputMediaPhoto(bot_order.image3)])
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn = types.InlineKeyboardButton('✅OK', callback_data='ok')
        btn1 = types.InlineKeyboardButton('♻️Qayta to`ldirish', callback_data='cancel')
        markup.add(btn, btn1)
        bot.send_message(message.from_user.id,
                         "<i>Ma`limotlaringiz barchasi to`g`ri bo`lsa 'OK' tugmasini bosing va e`loningiz kanalga yuboriladi!</i>",
                         reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def call_data(call):
    if call.data == "ok":
        bot_user = User.objects.get(user_id=call.from_user.id)
        bot_order = Order.objects.get(user=bot_user, active=False)
        bot_order.active = True
        bot_order.step = 8
        bot_order.save()
        text = f"<b>◽️Mahsulot nomi:</b> <i>{bot_order.name}.</i>\n" \
               f"<b>◾️Mahsulot to’lov raqami:</b><i> #{bot_order.id}</i>\n" \
               f"<b>◽️Chegirma foizi:</b> <i>{bot_order.discount} %</i>\n" \
               f"<b>◾️Mahsulot narxi</b> <i>{bot_order.price}</i> SUM\n" \
               f"<b>◽️Mavjud o’lchamlar:</b> <i>{bot_order.available_sizes} %</i>\n" \
               f"<b>◾️Do’konimizda mavjud:</b> <i>{bot_order.available_amount} dona%</i>\n" \
               f"<b>◽️Ishlab chiqarilgan muddat:</b> <i>{bot_order.date} %</i>\n" \
               f"<b>◾  Qo`shimcha:</b> <i>{bot_order.comment}</i> \n\n" \
               f"<b>🔻Sotib olish usullari:</b> \n" \
               f"<b>1️⃣Telegram to’lov tizimi orqali: https://t.me/..... </b> \n" \
               f"<b>2️⃣Saytimizdan sotib olish: link  </b> \n" \
               f"<b>3️⃣Qo’ng’iroq qilish orqali: nomer</b> \n\n" \
               f"<i>❗️Bizda 20 km bo’lgan masofadagi buyurtmachilarimizga tekin yetqazib beramiz!\n" \
               f"‼️Mahsulot sotib olingan kunning o’zida buyurtmachiga yetqaziladi!</i>\n\n" \
               f"<b>🔻Sizga yordam kerakmi?</b> @supportwemard\n\n" \
               f"<b>🔸Bizning kanal:</b> https://t.me/...."
        if bot_order.category == 'Men':
            bot.send_media_group(chat_id=-1001743819189,
                                 media=[InputMediaPhoto(bot_order.image1, caption=f'{text}', parse_mode="HTML"),
                                        InputMediaPhoto(bot_order.image2),
                                        InputMediaPhoto(bot_order.image3)])
        elif bot_order.category == 'Women':
            bot.send_media_group(chat_id=-1001680130917,
                                 media=[InputMediaPhoto(bot_order.image1, caption=f'{text}', parse_mode="HTML"),
                                        InputMediaPhoto(bot_order.image2),
                                        InputMediaPhoto(bot_order.image3)])
        elif bot_order.category == 'Kids':
            bot.send_media_group(chat_id=-1001797644710,
                                 media=[InputMediaPhoto(bot_order.image1, caption=f'{text}', parse_mode="HTML"),
                                        InputMediaPhoto(bot_order.image2),
                                        InputMediaPhoto(bot_order.image3)])
        elif bot_order.category == 'Home':
            bot.send_media_group(chat_id=-1001743786418,
                                 media=[InputMediaPhoto(bot_order.image1, caption=f'{text}', parse_mode="HTML"),
                                        InputMediaPhoto(bot_order.image2),
                                        InputMediaPhoto(bot_order.image3)])
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        btn = types.KeyboardButton('Men')
        btn1 = types.KeyboardButton('Women')
        btn2 = types.KeyboardButton('Kids')
        btn3 = types.KeyboardButton('Home')
        markup.add(btn1, btn, btn2, btn3)
        bot.send_message(call.from_user.id,
                         "<b>✅E`loningiz  https://t.me/.... kanaliga yuklanadi\nYangi e`lon berish uchun e`lon turini tanlang</b>",
                         reply_markup=markup)
        bot_user = User.objects.get(user_id=call.from_user.id)
        bot_order = Order.objects.create(
            user=bot_user
        )
        bot_order.save()

    elif call.data == 'cancel':
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        btn = types.KeyboardButton('Men')
        btn1 = types.KeyboardButton('Women')
        btn2 = types.KeyboardButton('Kids')
        btn3 = types.KeyboardButton('Home')
        markup.add(btn1, btn, btn2, btn3)
        bot.send_message(call.from_user.id, "<b>✅E`lon bekor qilindi!\nE`lon turini tanlang!</b>", reply_markup=markup)
        bot_user = User.objects.create(user_id=call.from_user.id, username=call.from_user.username)
        bot_user.save()
        bot_order = Order.objects.create(
            user=bot_user
        )
        bot_order.save()

