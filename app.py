import telebot
from config import TOKEN
from extensions import CurrencyExchanger, ConvertionException, AvailableCurrencies


bot = telebot.TeleBot(TOKEN)


# приветствие пользователя и инструкция
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    text = 'Я новый банковский бот.\nЗнаю курсы Нац. Банка основных мировых валют\n' \
           'по отношению к белорусскому рублю.\nВведи буквенный код валюты и количество\n' \
           'Например usd 4\n' \
           'увидеть список валют - /values'
    bot.send_message(message.chat.id, f'Привет {message.chat.username}! \n{text}')


# вывод на экран списка доступной валюты
@bot.message_handler(commands=['values'])
def handle_values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    available_base = AvailableCurrencies.currencies()
    for key in available_base:
        text = "\n".join((text, f"{key['Cur_Name']} - {key['Cur_Abbreviation']}"))
    bot.send_message(message.chat.id, text)


# обработка запроса пользователя
@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.upper().split(' ')

        if len(values) != 2:
            raise ConvertionException('Неверное количество введенных даннных.')

        quote, amount = values
        total_base = CurrencyExchanger.exchange(quote, amount)

    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя:"\n" {e}')

    except Exception as e:
        bot.reply_to(message, f"Что-то случилось, может быть валюта неверная: '\n' {e}")

    else:
        result = (float(amount) * (total_base["Cur_OfficialRate"]))/total_base["Cur_Scale"] # вычтсление стоимости валюты. стоимость некоторой валюты указана не за 1
        text = f'{amount} {total_base["Cur_Name"]} - {result:.2f} белорусских рублей по курсу Нац.Банка'
        bot.send_message(message.chat.id, text)


bot.polling()

