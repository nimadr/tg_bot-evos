from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ParseMode
from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from evos007_db import Datebase

db = Datebase()
# db.add_catalog()

button = [
    [KeyboardButton('🛒Buyurtma qilish')],
    [KeyboardButton('🛍Buyurtmalarim'), KeyboardButton('👨‍👩‍👦Evos Oilasi')],
    [KeyboardButton('✍️Fikir bilidrish'), KeyboardButton('⚙️Sozlamalar')]
]


def start(update, contex):
    update.message.reply_text('Buyurtma qilish',
                              reply_markup=ReplyKeyboardMarkup(button, resize_keyboard=True))
    return 1


def menu(update, contex):
    categories = db.null_catalog()
    buttons = [
        [InlineKeyboardButton('📖Barcha menyular', url='https://telegra.ph/EVOS-MENU-04-05-2')]
    ]
    a = table(categories, 'parent')
    buttons.extend(a)

    update.message.reply_text("Kategoryalardan birini talang<a href='https://telegra.ph/EVOS-MENU-04-05-2'>.</a>",
                              parse_mode='HTML', reply_markup=InlineKeyboardMarkup(buttons))
    return 2


def query(update, conetex):
    query_ = update.callback_query
    data = query_.data
    print((data))
    data_sp = data.split('_')
    if data_sp[0] == 'category':
        if data_sp[1] == 'parent':
            global ID
            ID = data_sp[2]
            categories = db.callback_query(int(data_sp[2]))
            buttons = table(categories, 'child')
            buttons.append([InlineKeyboardButton(f'back',callback_data='category_back')])
            query_.message.edit_text(
                "Kategoryalardan birini talang<a href='https://telegra.ph/EVOS-MENU-04-05-2'>.</a>",
                parse_mode='HTML', reply_markup=InlineKeyboardMarkup(buttons))
        elif data_sp[1] == 'child':
            types = db.get_type(int(data_sp[2]))
            Inlinebutton = []
            Ilb = []
            for type in types:
                Ilb.append(InlineKeyboardButton(f'{type["name"]}', callback_data=f"product_{data_sp[2]}_{type['id']}"))
                if len(Ilb) == 2:
                    Inlinebutton.append(Ilb)
                    Ilb = []
            if Ilb:
                Inlinebutton.append(Ilb)
            Inlinebutton.append([InlineKeyboardButton(f'back', callback_data=f'category_parent_{ID}')])
            query_.message.delete()
            query_.message.reply_text(
                "Kategoryalardan birini talang<a href='https://telegra.ph/EVOS-MENU-04-05-2'>.</a>",
                parse_mode='HTML', reply_markup=InlineKeyboardMarkup(Inlinebutton))

        elif data_sp[1] == 'back':
            query_.message.delete()
            menu(query_,conetex)
    elif data_sp[0] == 'product':
        ctg_id = int(data_sp[1])
        type_id = int(data_sp[2])
        product = db.get_product(ctg_id, type_id)
        button = []
        btn = []
        for i in range(1, 10):
            btn.append(InlineKeyboardButton(f'{i}', callback_data=f'count_{product["id"]}_{i}'))
            if len(btn) == 3:
                button.append(btn)
                btn = []
        button.append([
            InlineKeyboardButton(f'back', callback_data=f'category_child_{data_sp[1]}'),
            InlineKeyboardButton(f'menyu', callback_data=f'category_back')
        ])


        query_.message.delete()
        info = f"Narxi:{product['price']}\n Tarkibi: {product['description']}\n Miqdorni kiriting"
        query_.message.reply_photo(photo=open(f"{product['photo']}", "rb"), caption=info,
                                   reply_markup=InlineKeyboardMarkup(button))

    elif data_sp[0] == 'count':
        product_id = int(data_sp[1])
        soni = int(data_sp[2])
        summa = db.savatcha(product_id)
        narxi = int(f'{summa["price"]}')
        narxi_summa = (soni * narxi)
        query_.message.delete()
        print(summa["price"])
        query_.message.reply_text(
            f'Savatchada: \n\n\n Mahsulotlar: {narxi_summa}so`m\n Yetkazib berish: 9000so`m \n Jami: {narxi_summa + 9000}so`m')


def table(categories, holat):
    Inlinebutton = []
    Ilb = []
    for category in categories:
        Ilb.append(InlineKeyboardButton(f'{category["name"]}', callback_data=f"category_{holat}_{category['id']}"))
        if len(Ilb) == 2:
            Inlinebutton.append(Ilb)
            Ilb = []

    return Inlinebutton


def main():
    Token = '1779569322:AAHv_BFtiux-6WVV_-hIwUBhSN0GTJLmlG4'
    updater = Updater(Token)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start),
                      MessageHandler(Filters.regex('🛒Buyurtma qilish'), menu)
                      ],
        states={
            1: [MessageHandler(Filters.regex('🛒Buyurtma qilish'), menu)],
            2: [CallbackQueryHandler(query),
                CommandHandler('start', start),
                MessageHandler(Filters.regex('🛒Buyurtma qilish'), menu)
                ],
            3: []
        },
        fallbacks=[],
    )
    updater.dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
