from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Message
from telegram.ext import ContextTypes

bb = [InlineKeyboardButton("Назад", callback_data='back')]

# Определите структуру меню
MENU_BUTTONS = {
    'payment': {
        'name': 'Оплата услуги',
        'handler': 'handle_payment'
    },
    'referral': {
        'name': 'Реферальная ссылка',
        'handler': 'handle_referral'
    },
    'feedback': {
        'name': 'Обратная связь',
        'handler': 'handle_feedback'
    }
}
OTHER_BUTTONS = {
    'back': {
        'name': 'Назад',
        'handler': 'handle_back'
    }
}
def get_main_menu():
    keyboard = [[InlineKeyboardButton(item['name'], callback_data=key)] for key, item in MENU_BUTTONS.items()]
    return InlineKeyboardMarkup(keyboard)

# ///start2.1
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(f"Привет, {user.username}! Я твой бот. Выбери действие:", reply_markup=get_main_menu())
    context.user_data['menu_message_id'] = Message.message_id

# обработчики кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    callback_data = query.data
    handler_info = MENU_BUTTONS.get(callback_data) or OTHER_BUTTONS.get(callback_data)
    if handler_info:
        handler_name = handler_info.get('handler')
        handler = HANDLER_FUNCTIONS.get(handler_name)
        if handler:
            await handler(update, context)
        else:
            await query.message.reply_text("Обработчик для этой команды не найден.")
    else:
        await query.message.reply_text("Неизвестная команда.")


#meny/pay #добавить скрипт по удобной оплате
async def handle_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    payment_details = "Реквизиты для оплаты:\nНомер счета: 123456789\nБанк: Банк России"
    await update.callback_query.message.reply_text(payment_details, reply_markup=InlineKeyboardMarkup([bb]))

async def handle_referral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    referral_link = f"http://t.me/your_bot?start=referral_code"
    await update.callback_query.message.reply_text(f"Ваша реферальная ссылка:\n{referral_link}", reply_markup=InlineKeyboardMarkup([bb]))

#back skr
async def handle_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Ошибка в функционале", callback_data='error_in_functionality')],
        [InlineKeyboardButton("Иное", callback_data='other')],
        bb
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message = await update.callback_query.message.reply_text("Выберите тип ошибки:", reply_markup=reply_markup)
    context.user_data['feedback_message_id'] = message.message_id

# async def handle_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user = update.effective_user
#     await update.callback_query.message.reply_text(f"Вы вернулись в главное меню, {user.username}.", reply_markup=get_main_menu())
#     if 'feedback_message_id' in context.user_data:
#         await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=context.user_data['feedback_message_id'])
#         del context.user_data['feedback_message_id']


async def handle_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Получаем ID сообщения с меню из контекста пользователя
    menu_message_id = context.user_data.get('menu_message_id')

    # Если ID меню не найден, значит, это первое нажатие на кнопку "Назад"
    if not menu_message_id:
        return

    # Удаляем сообщения, начиная с текущего и до сообщения с меню
    while query.message.message_id != menu_message_id:
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=query.message.message_id)
        query = await context.bot.get_message(chat_id=update.effective_chat.id, message_id=query.message.message_id - 1)
    # Обновляем текст сообщения с меню
    await context.bot.edit_message_text(
        text=f"Вы вернулись в главное меню, {query.from_user.username}.",
        reply_markup=get_main_menu(),
        chat_id=update.effective_chat.id,
        message_id=menu_message_id
    )

async def handle_error_in_functionality(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.message.reply_text("Пожалуйста, опишите ошибку:")
    context.user_data['feedback_message_id'] = update.callback_query.message.message_id

async def handle_other_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.message.reply_text("Пожалуйста, опишите вашу проблему:")
    context.user_data['feedback_message_id'] = update.callback_query.message.message_id

def get_main_menu():
    keyboard = [
        [InlineKeyboardButton(item['name'], callback_data=key)] for key, item in MENU_BUTTONS.items()
    ]
    return InlineKeyboardMarkup(keyboard)

# Словарь для сопоставления названий обработчиков с функциями
HANDLER_FUNCTIONS = {
    'handle_payment': handle_payment,
    'handle_referral': handle_referral,
    'handle_feedback': handle_feedback,
    'handle_back': handle_back,
    'handle_error_in_functionality': handle_error_in_functionality,
    'handle_other_feedback': handle_other_feedback
}
