import telebot
from telebot import types


class LanguageBot:
    def __init__(self):
        self._token = '6507913188:AAHx-QFkh87DrHqjcU27RzJnzPKdBdgFgMw'
        self._bot = telebot.TeleBot(self._token)

        def open_start_menu():
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            test_button = types.KeyboardButton('/test')
            markup.add(test_button)
            statistics_button = types.KeyboardButton('/statistics')
            markup.add(statistics_button)
            help_button = types.KeyboardButton('/help')
            markup.add(help_button)
            return markup

        def open_cancel_menu():
            cancel_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            cancel_btn = types.KeyboardButton('Отмена')
            cancel_markup.add(cancel_btn)
            return cancel_markup

        @self._bot.message_handler(commands=['start'])
        def bot_start(message):
            markup = open_start_menu()

            self._bot.send_message(message.chat.id, 'Добро пожаловать! Какие тесты мы пройдём сегодня?',
                                   reply_markup=markup)

        @self._bot.message_handler(commands=['test'])
        def bot_initiate_test(message):
            test_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            leveled_test = types.KeyboardButton('По уровню сложности')
            test_markup.add(leveled_test)
            endless_test = types.KeyboardButton('Бесконечный')
            test_markup.add(endless_test)
            send = self._bot.send_message(message.chat.id, 'Ну что, начнём тесты! Выберите подходящий тест.',
                                          reply_markup=test_markup)
            self._bot.register_next_step_handler(send, select_test_type)

        def select_test_type(message):
            if message.text == 'По уровню сложности':
                cancel_markup = open_cancel_menu()
                send = self._bot.send_message(message.chat.id, 'Введите уровень сложности. '
                                                               'Число от 1 до 5.',
                                              reply_markup=cancel_markup)
                self._bot.register_next_step_handler(send, select_difficulty_level)
            else:
                # TODO
                pass

        def select_difficulty_level(message):
            if message.text == 'Отмена':
                self._bot.send_message(message.chat.id, 'Что будем делать теперь?',
                                       reply_markup=open_start_menu())
                return
            try:
                diff_level = int(message.text)
                if not (1 <= diff_level <= 5):
                    cancel_markup = open_cancel_menu()
                    send = self._bot.send_message(message.chat.id,
                                                  'Уровень сложности некорректен! Пожалуйста, попробуйте ещё раз.',
                                                  reply_markup=cancel_markup)
                    self._bot.register_next_step_handler(send, select_difficulty_level)
                # TODO
            except ValueError:
                cancel_markup = open_cancel_menu()
                send = self._bot.send_message(message.chat.id,
                                              'Уровень сложности некорректен! Пожалуйста, попробуйте ещё раз.',
                                              reply_markup=cancel_markup)
                self._bot.register_next_step_handler(send, select_difficulty_level)

        @self._bot.message_handler(commands=['statistics'])
        def bot_show_statistics(message):
            self._bot.send_message(message.chat.id, 'Bla-bla!')

        @self._bot.message_handler(commands=['help'])
        def bot_show_help(message):
            self._bot.send_message(message.chat.id, 'Bla-bla!')

    def run(self):
        self._bot.infinity_polling()


if __name__ == '__main__':
    bot = LanguageBot()
    bot.run()
