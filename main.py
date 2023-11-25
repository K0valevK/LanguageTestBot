import telebot
from telebot import types


class LanguageBot:
    def __init__(self):
        self._token = '6507913188:AAHx-QFkh87DrHqjcU27RzJnzPKdBdgFgMw'
        self._bot = telebot.TeleBot(self._token)

        @self._bot.message_handler(commands=['start'])
        def start(message):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            test_button = types.KeyboardButton('/test')
            markup.add(test_button)
            statistics_button = types.KeyboardButton('/statistics')
            markup.add(statistics_button)
            help_button = types.KeyboardButton('/help')
            markup.add(help_button)

            self._bot.send_message(message.chat.id, 'Добро пожаловать, ', reply_markup=markup)

        @self._bot.message_handler(commands=['test'])
        def bot_test(message):
            test_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            leveled_test = types.KeyboardButton('leveled')
            test_markup.add(leveled_test)
            endless_test = types.KeyboardButton('endless')
            test_markup.add(endless_test)
            send = self._bot.send_message(message.chat.id, 'Ну что, начнём тесты! Выберите подходящий тест.',
                                          reply_markup=test_markup)
            self._bot.register_next_step_handler(send, select_test_type)

        def select_test_type(message):
            if message.text == 'leveled':
                send = self._bot.send_message(message.chat.id, 'Выберите уровень сложности.',
                                              reply_markup=types.ReplyKeyboardRemove())
                self._bot.register_next_step_handler(send, select_difficulty_level)
            else:
                pass

        def select_difficulty_level(message):
            pass

        @self._bot.message_handler(commands=['statistics'])
        def bot_help(message):
            self._bot.send_message(message.chat.id, 'Bla-bla!')

        @self._bot.message_handler(commands=['help'])
        def bot_help(message):
            self._bot.send_message(message.chat.id, 'Bla-bla!')

    def run(self):
        self._bot.infinity_polling()


if __name__ == '__main__':
    bot = LanguageBot()
    bot.run()
