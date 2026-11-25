import telebot         
from telebot import types
import random
import os
import json
import sqlite3

DB_NAME = "db.db"
SPAM_WORDS = ["скам", "я депну африканских детей в казик", "купить", "розыгрыш"]

indx = 0
points = 0
game = False

with open('victorina.json', 'r', encoding = 'utf-8') as f:
    data = json.load(f)

with open('cities.txt', 'r', encoding='utf-8') as f:
    cities = [word.strip().lower() for word in f.readlines()]

TOKEN = '8548645128:AAHOsYL-trR9l_qedUJttDEzvnHBeEKD3IA'
bot = telebot.TeleBot(TOKEN)

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add('📜 Правила / РП Термины', 'вопрас ፼')
markup.add('🐍 Информатика (8 класс)', '❓ Помощь')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     "Хей привет! Я твой личный бот-помощник. Выбери нужный раздел:",
                     reply_markup=markup)


game_choice = ["камень", "ножницы", "бумага"]


@bot.message_handler(func=lambda x: x.text and x.text.lower() in game_choice)
def game_handler(message):
    user_choice = message.text.lower()
    bot_choice = random.choice(game_choice)
    if user_choice == bot_choice:
        result = "Ничья! 🤝"
    elif (user_choice == "камень" and bot_choice == "ножницы") or \
         (user_choice == "ножницы" and bot_choice == "бумага") or \
         (user_choice == "бумага" and bot_choice == "камень"):
        result = "Ты победил! 🎉"
    else:
        result = "Я победил! 🤖"
    bot.send_message(message.chat.id,
                     f"Ты выбрал: {user_choice}\nЯ выбрал: {bot_choice}\n\nРезультат: {result}")


def get_next_question(data, indx):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn0 = types.KeyboardButton(data[indx]['вариант'][0])
    btn1 = types.KeyboardButton(data[indx]['вариант'][1])
    btn2 = types.KeyboardButton(data[indx]['вариант'][2])
    btn3 = types.KeyboardButton(data[indx]['вариант'][3])

    markup.row(btn0, btn1)
    markup.row(btn2, btn3)

    markup.add(types.KeyboardButton("Выход"))

    return markup

@bot.message_handler(commands=['mafia'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     "start learning",
  reply_markup=markup)
    
@bot.message_handler(commands=['quizz'])
def quizz(message):
    global game, indx
    game = True
    indx = 0
    markup = get_next_question(data, indx)
    bot.send_message(message.chat.id, text=data[indx]['вопрос'], reply_markup=markup)


@bot.message_handler(func=lambda m: m.text and m.text == "Выход")
def quit_quizz(message):
    global game
    game = False
    bot.send_message(message.chat.id, 'Пока')


@bot.message_handler(content_types=['text'])
def vicktorinas(message):
    global game, indx, points
    if game:
        if message.text == data[indx]['ответ']:
            bot.send_message(message.chat.id, 'Правильно')
            points += 1
        elif message.text == "Выход":
            game = False
            bot.send_message(message.chat.id, 'Пока')
            return
        else:
            bot.send_message(
                message.chat.id, f'Неправильно! Правильный ответ - {data[indx]["ответ"]}'
            )
        print(indx)
        indx += 1
        if indx == len(data):
            game = False
            bot.send_message(message.chat.id, 'Пока')
            return
        markup = get_next_question(data, indx)
        bot.send_message(message.chat.id, text=data[indx]['вопрос'], reply_markup=markup)
        return

    # обычные текстовые ответы (бывший handle_text)
    if message.text == '📜 Правила / РП Термины':
        bot.send_message(message.chat.id, "Ссылка: https://powerpoint.cloud.microsoft/open/onedrive/?docId=1B6E44AA3ECE6FD6%21s9874d4f1c21e4b83849713178387ecfa&driveId=1b6e44aa3ece6fd6&usid=98619708-d7c1-43a6-b683-b8def56dbce5")
    elif message.text == '🐍 Информатика (8 класс)':
        bot.send_message(message.chat.id, "🐍 Операторы: for, while, if")
    elif message.text == '❓ Помощь':
        bot.send_message(message.chat.id, "Перезапусти бота в VS Code.")
    elif message.text == 'вопрас ፼':
        bot.send_message(message.chat.id, "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBwgHBgkIBwgKCgkLDRYPDQwMDRsUFRAWIB0iIiAdHx8kKDQsJCYxJx8fLT0tMTU3Ojo6Iys/RD84QzQ5OjcBCgoKDQwNGg8PGjclHyU3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3N//AABEIALwAxgMBIgACEQEDEQH/xAAcAAACAwEBAQEAAAAAAAAAAAAEBQIDBgEABwj/xAA/EAACAQMDAQYDBQUHAwUAAAABAgMABBESITEFBhMiQVFhMnGBFEJSkaEjYnLB4QdDgrHR8PEVJDMWJnWywv/EABkBAAMBAQEAAAAAAAAAAAAAAAABAgMEBf/EAB8RAQEAAwEAAgMBAAAAAAAAAAABAhEhMRJBA0JRIv/aAAwDAQACEQMRAD8A90C3guei2UUyg6rZN8fuiqeodGS0ZjGMA8GtH0yzgPY/pMyArJ9iiJx55UUuub9JbcpIm6+Zrzv2rquPOsreEQLhiM+lJLxmdG2FF9QkeW5cnOBwKEl22j8Qroxc1d6BErXTrIGIX2rVxWPiVpHGlcHc8ikfRpo7aJu7iAdmB1Zz/nToXYkTEmtQWwPYVpUyJ9x3LF1BZRz60wi7kjVkYG6MQCQflQCdRNqgMLBhnwu2x44xVcd93gdlKKBwxFOYnacrfW3d6ohk40uv0pZ1CGEyKsJeMPuMnOaXwSxqSJ3VizcUNcdQEDyLq1rFJrjPn8qqQrVkNvEJ+8dvD7D2IoyG9s4otEZER4Lc6t/61m/tU8mhiAFLZOD5VFpF/FS3A0n20OdMc5ZF9SATR0V8jhW0DIU69/u4rG29wiuMefG1X/8AUYraUhe81LuwI/SnuB9N6X1N0txFhHhA1AsMEN9PamMfUhIrBiQOQDy2/wDWvmth2hQMi6mT9wjY00tOud6+nIDMdIJPNFobu4whWcAtrTBkxkE4P+v60nvzECIwCUwHQ+hrsF+SDCrjwbKmcBq7cKbt9RwcjSAPIjf+dZWaaSgLZpGyrYdSMg+hq28hjnjYM654znzrhjNuAgVu8TZjnfz8qIulWO1doDn+Ie1EFYO+se7uGkJyo596z/WbdDKGA2b71bDqa6lZH2OOaxl7cJr7t894OM1tGVKNOl9m/SrQ49KqO0uk7H0qaHPFBJivV0iu09qj9BdBeZeyPR9EDOpsYcHG3wis912Moja0K/Otx2LuIm7JdGif7tjD5fuih+2fTreaxe4GFkVeBXB/mXcrq+Vs1XxG6YiVs7fOhs/i2+VEXvinZT8qFk252+dbRzX0ZaSK0WFwDq4o/vidIOwxmk9h4HbO9GhyDo+HbGOaMhEzcIS/eZ1jhjwNxVUV5HcNoKkoMnAOADVHUX7tAFU5Phzjy2qFswhRGSISOCG0eu9aS8Dz3lsJCpYhlOOPP0qKTRS7K2SudRJozql30i5gE0dsq3YG6SqQP02rNPJKbnWg8OfEeKrRW6NSSq6Quw43oUszyEA4I59qutr3v5F7xMDTxQ9zcpBNII42OoZ04pQtrUuFsJo2kXXhgcD0zWgu7ros9obuDuzcPyjjJ/Ssk7iV++jI1/gbmireZyQFiXJ4xsaehMkrkvLJ9oaPQM4VRRHTppVZdROkHINFW0OTrnw2NwDuc1AxpE6uAM+mKdDYdBnWRGm0li5BOTyT51oLPGp1UlUVsZ98gGsZ0e6w0QyAockgee21anpshaRtTagdRI4xvUVcFXaqZhISXjBwR7c71doDQmMkMdWAOcjeuywSYSTHgdAC3vVM2Y4FCJhtRGAccUodZS/RlfQ51HVz71huvxd1dawD8VbvqwJZipweaxvXQH0nzHI9a1njLIhkyDqJy1WwVHTq5FWqCvANATau15q9Qb9CdjLW9PZ3o7ongNlERn+AUx7Wxyr0SdjgyhdtNGdiB/7M6H/8fB/9BTO9ghmgZZgCh5rlz/BJNyui/lts3H5wvo8XL5GNPrQLgn4hmtB2pjjj6hKsWMajxSENq5p43jLKdQhfuXHnqph95WpXqw65+7RkU+rk8LtTpSr7iMSwsp+I7D2NC223hOzDgmrFYtya9cLtqSjG/R3+vTJG3iOkn5UsvFRX1HZR6eVHI7SHAwDQFxJGdRYEgbKPU+taTbPLQOL4tTYP8TVHu5LpwkPjYnGAxFNeldCm6pMIV8Or8LeKmPR7G2VXeJmlKvhGA0nA+taSJLJOyfVURGRVZj5K+T+tG2k/U+kqYOp2aXNuucxTDLf61tenXf2SxMNyneA/ebYj603tLLpvaSKSzIdZMF8ykZ1eWk85qtBg7DqPRJbrMNs1tn4VbcD1qXV7S3kPewMQvt8NOZ+zU/T7ju540SVmYh1I8fuR60GbU63I4PCjypVcBdKQxshIJH+u1aiymeFmCDcrgk+uaW2kSqgx9wg8e9NrK1MkMksbjS7aASdhvzUVRpDdMkTq8hKBccck4/lVki67AP8AecbH0PAoCNDqCochtsH1plYkyWMtuTpct4RjJJzUKY3rEb6/Fkc8VjOsbeI85xX0TrMXxr95awHaGLQcY35rSXjOkINFKAArGhlWikGpFzTKIyV6uyHevUKfpLsz1K06d2M6E17OseenwYBJ38AqPUe1PTJemTvby4YKcA+dfNekSy3HSLKOSViI7eNYweAMAVC9buho325PrXHlnbdNphrtLeq4kLO2SzEnNJnU4yAR4qeSMCniGaVXalSxA29KeN+k5z7LpMfz+lVhwj5ydPpXXRtY3+Kqjtzv/wA1qxGQyBnbJXejRIrJuKTK+l1x6UxtH7yLDHf+tKxUqq4buJda8DketFK1r3ojcjW/HtVDRCWTSaBv7u3trgso72Qcb8VWIyaXpcyQ3gkfKsv3vpQvQGIhbWMa2OfzPFLrXq0FzEY5j3cjDHqOPWiunOtoC0xKqN/Fv9K1lS0VzfQ2VrrnOPCPEaj2c7UWlveJKcKobJxuSKzd3aX/AF2ZO/JtbUfCnLN76fKnfRex/TY3RpJHZicAuSM/QVWw+ndZltuoWS9Wt5g9vnEsRHnj9DWMubZu8ZIvCPTmtGltaWvSY+k2kiNNPIDJofKqoqNwtlqdnZWIXGx+MnPHoBRZsb0z8KtCoSNwgJ3B8zR+tEs4YxlO8ZRn0AIqF5obSIpEbffTsBUU8csZk5AyFPlxUXipdmcKkXMWADk6h9N/yoiJ5FVXZgORgCl8bRi7JjaTGgjJ8tqLDaYn18Fdl9GH9TWdWA6uokYMBjyb51hO0Fvrj48VbW8JGpSSV0jfzzWZ62rd2zYqomsSFwMnirOE3qUi/tP3fSot+0428NUlBjXqjmvUzfbOl2EQ7KdJlRV3tIyx891BrHdQfXdZ1HHpW16YqHsL0+USEf8AZxAjPnpFfPrqTRctk58Vef8Ajl+V26s7NRc7tlVwKFu9WrOBiiD4wrVCRNaf79a1Z0hlyX3Gc5x5YodxjmmdyinTgYoCcVrKws0ob9nzvRdkxoM+Ln8WPpRcHgp3wsfRUQRpcu2BoK15ejW6SZuImkQbk6qnAdWrYV4HEZhSZ/GSNDjP5GjGrygw9g4Z27+K8aOAkYLR5xn60rurNOnTRQx3DXAZdTa/u7/0rc9G6ksXTVgcaxvHID5qRz9K+fdR7wdVuAxyFchT7ZOK2sQ0PSNF7cRJM5KswJkPpWjvoVtbZBNKRNG5QaW3xnOR7YrHdMPdS96WICckeW9adrZbzVMJss6kCTPPluMfzpY+CDLa6MVoy2sTgOcmU7k+xo63MZKawZ5ScNnbOeKVxTzwQKJHiPuM0z6fGY5e/uEViTlI+NJzsTVbCi+gVJfEmmTURp0+VVXIVWVi+fTfGk0f1AyzSCSU6mIyGYe2KWSYL4YghFxn1NZ1cEwXDIQNWWP3gPlTIuZoGcvqHxFeMEnypUy6njC+HR4iD5mmcLIIHB0gqpxnOfKoWX3OpkJIOR7Ui6hN+xOtRttTl0e4glkbw6eBms5cya45Y03bSR9aqJrMXid3NgDbVzQTZU4zRM7OjLEd2XjNDEYGo7k7mqQ7Xq6a9TN9SgvXteydhAT8dsjD2GkYrH3Epabf8VaXqNyjdnukKkZVo7GFW258I3rIFy029cmM7a1yv9Obc6oMnjTUsZh2rlsum0w2x96q77ClYiPD60qYOZcuoA23H1pfMvxU5lQNGjIedzSicfFWmNZZQGB46NUjRnFBqMP/AIqLiPh0+VXkiJxOV4owBSVkA3xk+1AjZNt/Oj4QjwqWyGB+IeQqZWl8WFpDhlIVRvsPiOKXmMyTtJKVBLb5NFPAyhZnkL4814ou3sulTpmRJCVzqANaS2o0BtZbSOQgynvxnCc6qeWcE3eYcfZ7U8lsnO44HlVEH2Ky26fZaHP94wyx39aLiklnbDA6RnAx6VfgN7GWC0bRar3jts0zqCwOPIUTAyxOzf8AkOoHOMbf7FLowkSMQV7s759+Ku+06dDBwSOfU80z0lfXYlKxKT5kn0FDwOq+/wA6onJIGkYJxg+1St1VishJ0jn35qKcMIRpGrk4xvRUDjModxnT/IUGrAPknbGcVyS4SOXvCoAK+IY5paUEe48Mitgbngc8VmOpTG3u2aPdWxxTe5m7ucqSDqz9KzfUZcvqG7JyB500UBeHvJ3b4lXz86HarW+9781XjPFMnq9XmrtM32O4sOmT9i+kyNMsV0vT4SE/F4BWKmS0jkVSqBveiFv+96baAu37K2RNPyXG35UsuZIwusRhm9TXNhLLYvLsRvJ3V1y4Cexpdc9RC6u7IrlzMZEON9PpSwgM+5rWYyo3Y0ljKrW6gtmq54QaBsroREKm+SFGaaAh4yc7JuT61n5Vewq7sO2RsK9E/hYedTnVY08OaHjOH3960Z+URA+TpOwouCQ5yOPSl+cnA2OKvikK8VGUVKYI+zad0/Ca5bzPFOCAMfeHrQ0U3g5opJEcbDDL+tPG6OmSSRSRsQFGdwMcH8qNtRqRXHi58Pzx5YpHbR5k2JK77U3gYIXRgwPmQ3BwK12RutmO6wzkLjOCPOofZjL4MqFPAHP51Wkasc98qk7nkjHvVyKFBYMd9h7AiiiISQhSqpvtjfzqAYIvA0+lXSnEaE7E8LQ84GSv4cH9aRptJrd98ad96DupQI5cknK7e2K5czohjG+X5/OkN/faQ8QJJRiCfUUFa497qKFtyAN/X1pTc5canbGNjjzNe1NoXf1qD5ZMkeeaZKyPiqKfsy2d6szUGG2qgkGr1dkr1NR9YaTbRFydOgbfSqLln8QJGPWu2UmYIkH4RUb3bWDx61l9nfC6ZyPh8+aoOn0qyRqGYHGc7VbPbyMTMuk433+WKd9KlEolAJIwBg1ntWltQpv0CXE7KVPiqc5xWN6IuR+mMUI4zxt4qY3yaX2oC48PH4qWNGUVa/FqqyOTj95ao/5re9jOl9nQka9cjd5p/hfcAD02p2wpLfGLhY0UHKjUBWi7bdlI+gzrddMZpOnyNtjlDWcimVjpPG1Fh7MLWbLrk/lTFHOpiZMozfD5Vn1kYfCCPDR1rJIE8WTS8M4jvpRqV84O4A/zo2JyUTBz6Ums0eSZYy33eac96kIC6dxyPSqhpzyqSEkzkbEj/KhjLGkjSl9CgeHJ5yaU9Sv+7n7tSSc7Y/nS7qFyzvoRzp0jamnaV51FpZVK8DGKCkDFmZjnVXMfDUnNBKT8FcJ8On04rretR/rTCBFcb4KnUXGeNqArn4WuV6SvU1GfSiF06iDpUV6+fBYncN5VXa+BUf1UZqu+YkaxuPQVj9nfAk5qkkadOam7ZXAOTVJrRkjIunii+iyEXBJYADnehmqds4R2Rhgt5ii9hy9aKb9oARuG3oCdPh/ioqG5EsPhHHFVY1c1nONL0BLsdI3Fa7pUwiubQ41IIwRny2rMNH4h+9T3p76unoznDxnRt7UZ3wsPW7LRdSspLW5OpZtvl7+1fKbqBrS5mgbOpHZPy2r6L2cl1tGX3FZ7+0TokvSuufaXwYLsmRGHmTyPzrXhVm0ZtHNGw3YCfwr4feglFVspXg0WbLbR215GkFuTgTOCDQw6v3srEgZZcceeKRSSFsaQRjON+M1KJW1as0aG187s8+oEY9htXgBq1KSc85rlTAoDgNRJ8f0rp/8A1USKQRb8PlUB8NSJ1c1GmHhUW+CpVWxoCtq9UXOW2r1UY1JMRKpP3RUSwCspINUFvAp89tqhqLbLvxxWWjtVTIQNSnFVSNRsqeDx7fOh30J6GqRQ/eVPVrbUNq47J+GqXBXg0yOen3AJ0422/QUYW1+1IunTd1NljseRTW4kw7Bdgaizq5eLnX4aZdLIeCdMjIOrHzH9KWHUSigE54x51pLLpV1aW0k8pQIVGUzk/wClTl4ePoroc7BTGpwytWs63b/+o+zE8TDXc2qd7Hkb5HI/LNYqwcJc7ELn1r6H2T7uaYQy5w4J2+97VeN3Ds6+JBsYz5c+1Rck8VtLzs1F07tZc292o+zK+pATsQdxxW96J0Ls9fSNA9nbSKMsCExn68/rVbR8XwvbiiFWvoPbT+zWaxka76NloDuYmO4+XrWEWKQSGMowcbFSNx9KdGtKwKkwxzUpiYjhkIPoRXEOVw25qQhJ8P8AiqJqUtQzTCs1GumommHQapY1MmqmoCIr1eAr1CoZo6GODUmDgKxKjgUPc3MYkZFxp/dG9X928tig0MUK4V1HniksoeBsb59RvWePaWS90e4bVwB97NUS/wDkxV8U/fR6EUhxz6GqjbXMjkRwNkckg7VcqNBi1czq5pqvRD3Yae5SLV+I1UbGyQ4e+DH90Zo3DkLUJD7Amtp0joF51W3SdlWGD70kp059MChOh2VtNI0Q71skMpdMYpr2hvWihjgjkZQjfCOMeVTbLeLkX29lbWhDxSrLoU4xkeLO3NUv1m+mu0tdWi3PMQ3BoCGZntssSCck49eapAKzRzAtlGGfep9thtL0yJRM2WQ44ya3PZO4torwySyZcfCBXzqOCFZw2tsnxBCc71o+k3MsTL4hq+VPC8GXpl2/j1dcgulHheLA9yCf6V3p3U3t7c6I0RRuxG7E586r61IbtLFXbLaWodY/+2YH4s5BPJFXiVfQuznU/wDqYeN8OI1HI5zmvnHa64PTu20nd28aNERhk/vAR5037LXktrdeFtvvClP9pqqOtWt+pA72LQfcg8/rRkIdX3Z2z7TdIa7kEcV2VBWRdjn3r5deWM9ncNDMpyONua13Tusui4Rm0/hzRtxbQ9QRXZB3nrRJwrOvnZiJzgHbnaqnXDZG49a3zdBiRGGNj+dAnoltpZcGmWqxBFRYHGcVqm7NRB8s50nhTXbvoKjxL8PpTKysiQfSuaKeXHTHh/uSaFa2AXSdj6UaIqYY52rtX3sYXSPnXqFzx37fc2sEZhYr5+1dg6lBNGxv7WNifDrh8Jx8uKTyyu8mCdthiuxr5ZJ8XnUTRU4Sz+0rr6RdqwH93KNDj+VCSL1GDMN0kgUtzxj6iuJaR64iGdc84OKbC7lguBb7SRHYrKNVTachBPFGSpM6Y9OTUUkEIzFEM/ibc1sZrK0+xC5S1hjkbnSu35UmF0Yn8EMI/wAFHyFgvsjNI8pDscr54r3W/G7KzAMfM0d0iUyRMxVQf3VApb1PxOpbc1nLvJUnF9tGRDsdXntv5Vx841DY/rUumKPszc/DUoPF+zbdTVT0HFtGJIleNvFgYJHFO7MyRjVIoPy/3ik/SvAuBx71ouikObkuoJRCy58jVYwUJ1GYpdxRuWyqnYL6+tObBILqzdoy2td2Qr5e1KepqDfbk/CBWm7JAN+zcalKtnNaRNCW1oYsSMhGdidO7YpH/aXFI79JQRMEXXv6cc1tRCsEDspYkZxqOfvf1pb1BmuJgJ2MgGSNW+KdEfP7G1mZGeIgFceE8mnVhdMEXV4flvT6bp9srzokYUBs7fOlQs4opyI9SiSTxYPvU60fp9FYNdWiyKhzjJ9t6pHSWf8Au8fP5077PDRAuWLhsghtxRN8NQZTxzQbI9RtVUqNWSvC4wT8zQsMLTOqsuFHmfLmo319LMdbhMsd8D93NMn/AGZW3QARld/WgArqOFkCxx687Ajas71LphkUyRqQVrXTKpQeEAjbI5pPcbO7DzXjypwrHzrqkTRSKGO+/P0r1Gdqjm8XYDnj6V6mU8f/2Q==")
    
    else:
        bot.send_message(message.chat.id, "Ой ну это не куда не годится!")


def insert_player(player_id, username):
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    sql = f"INSERT INTO players (player_id, username) VALUES ('{player_id}', '{username}')"
    cur.execute(sql)
    con.commit()
    con.close()


def players_amount():
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    sql = "SELECT COUNT(*) FROM players"
    cur.execute(sql)
    res = cur.fetchall()
    con.close()
    return res


def get_mafia_username():
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    sql = "SELECT username FROM players WHERE role = 'mafia'"
    cur.execute(sql)
    data = cur.fetchall()
    names = ''
    for row in data:
        name = row[0]
        names += name + '\n'
    con.close()
    return names


def get_players_roles():
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    sql = "SELECT player_id, role FROM players"
    cur.execute(sql)
    data = cur.fetchall()
    con.close()
    return data


# Модерация спама на telebot (вместо aiogram-хендлера)
@bot.message_handler(func=lambda m: m.chat.type in ["group", "supergroup"] and m.text)
def moderate_messages(message):
    text_lower = message.text.lower()
    if any(word in text_lower for word in SPAM_WORDS):
        try:
            bot.delete_message(message.chat.id, message.message_id)
            warning = bot.send_message(
                message.chat.id,
                f"@{message.from_user.username}, ваше сообщение удалено за спам."
            )
            # удалить предупреждение через 5 секунд
            import threading
            threading.Timer(
                5.0,
                lambda: bot.delete_message(warning.chat.id, warning.message_id)
            ).start()
        except Exception as e:
            print(f"Не удалось удалить сообщение: {e}")


if __name__ == "__main__":
    print("Бот успешно запущен!")
    bot.infinity_polling(none_stop=True)