import logging
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from handlers.button_hand import button_handler, start

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)
def main():
    application = ApplicationBuilder().token('').build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.run_polling()

if __name__ == '__main__':
    main()
