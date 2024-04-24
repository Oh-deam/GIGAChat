import telebot

import pandas as pd
import sqlite3 as sql

from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat


def is_user_in_db(user_id):
    pass


def check_avilable_create(user_id):
    pass


def is_quastion_about_tasks(
    message: str,
) -> (
    bool
):  # Вопрос к нейросети, чтобы она определила, является ли вопрос похожим на вопрос к таск-менедж.
    quastion = (
        f'"{message}". Это похоже на вопрос для таск менеджера? Ответь да или нет'
    )
    messages_for_check = [
        SystemMessage(
            content="Ты таск-менеджер, который помогает людям следить за сроками выполнения задач"
        )
    ]
    messages_for_check.append(HumanMessage(quastion))
    res = chat(messages_for_check).content
    print("Answer from AI:", res)
    if "да" in res.lower():
        return True
    else:
        return False


def make_Gant(
    data,
):  # Функция для создания диаргаммы Ганта (хз нужна она или нет), но просто делать было нехуй
    print(f"in make_gant : {data}")
    df = pd.DataFrame(columns=["name", "start", "end"])
    all_tasks = data.split(";")
    print(f"ALl tasks: {all_tasks}")
    for el in all_tasks[1:]:
        task_info = el.split(":")
        print(f"task info {task_info}")
        name = task_info[0]
        start = task_info[1]
        if len(task_info) == 2:
            end = task_info[1]
        else:
            end = task_info[2]
        df.loc[df.shape[0]] = [name, start, end]
    df.to_csv("df.csv", index=False)

    all_dates = df.start.to_list()
    # print(df.end.to_list())
    all_dates = all_dates + (df.end.to_list())
    print(type(all_dates))
    print(set(all_dates))


chat = GigaChat(
    credentials="MGRkNTg1Y2ItNjUyYi00YTlkLTgxYmUtYjA4NDdiNzIyMGNiOjIyMTQxOTYyLTQzMjAtNDI0MC04ZmQ0LTEwYTQ4MTE5ZjIxNQ==",
    verify_ssl_certs=False,
)

systemmessage = SystemMessage(
    content="Ты таск-менеджер, который помогает людям следить за сроками выполнения задач"
)
messages = {}

bot = telebot.TeleBot("6771849352:AAFiFk-Ri4E9oVYkRdSFkCO4ge329kczfmI")


@bot.message_handler(content_types=["text"])
def get_text_messages(got_message):
    user_id = got_message.from_user.id
    print(f"type user_id {type(user_id)}")

    if got_message.text == "/start":
        bot.send_message(
            got_message.from_user.id,
            "Привет, я ИИ-ассистен, созданный на базе GigaChat, смогу помочь тебе по любому вопросу",
        )

    elif got_message.text == "/help":
        print("qustion about documentation")
        with open("documentation.txt") as file:
            documentation = file.readlines()
            print(documentation)
            bot.send_message(user_id, "\n".join(documentation))

    elif "/task_manager" in got_message.text:
        # print(f'user id = {user_id}')

        task = got_message.text.replace("/task_manager\n", "").replace("\n", ";")

        if is_user_in_db(user_id):
            pass
        else:
            pass

        if check_avilable_create(user_id):
            try:
                user_tasks = ""
                if len(user_tasks) == 0:
                    pass
                else:
                    # new_user_tasks = user_tasks[0][0] + ';' + task
                    # cursor.execute(f"""UPDATE users_data SET tasks = '{new_user_tasks}' WHERE id = '{user_id}'""")
                    pass
                bot.send_message(user_id, "Задачи успешно добавлены")

            except Exception as e:
                print(e)
                bot.send_message(
                    user_id, "Произошла непредвиденная ошибка, попробуйте чуть позже"
                )
        else:
            bot.send_message(
                user_id, "Закончились свободные слоты для задач по вашей подписке"
            )

    elif got_message.text == "/del_task_manager":
        # cursor.execute(f"""
        # DELETE from users_data WHERE id = '{user_id}'
        # """)

        bot.send_message(user_id, "Задачи успешно удалены!")

    elif got_message.text == "/update_subscribe":
        # cursor.execute(f"""UPDATE users SET subscribe = 1 WHERE id = '{user_id}'""")

        bot.send_message(user_id, "Ваша подписка успешно оформлена!")

    elif got_message.text == "/make_gant":
        user_tasks = ""
        # cursor.execute(f"""SELECT tasks FROM users_data WHERE id = '{user_id}'""").fetchall()
        if len(user_tasks) == 0:
            bot.send_message(user_id, "У вас еще нет добавленных задач!")
        else:
            make_Gant(user_tasks[0][0])
            bot.send_message(user_id, "Создано")

    else:
        if is_quastion_about_tasks(got_message.text):
            request_from_db = ""
            # cursor.execute(f'SELECT tasks FROM users_data WHERE id = {user_id}').fetchall()
            if len(request_from_db) == 0:
                bot.send_message(user_id, "У вас нет ни одной добавленной задачи")
            else:
                user_tasks = request_from_db[0][0].replace(";", "\n")
                quastion = (
                    f"Передо мной стоят задачи: {user_tasks}\n {got_message.text}"
                )

                if user_id in messages:
                    messages[user_id].append(HumanMessage(content=quastion))
                else:
                    messages[user_id] = [systemmessage]
                    messages[user_id].append(
                        HumanMessage(content=quastion)
                    )  # messages[user_id] =

                res = chat(messages[user_id]).content
                bot.send_message(got_message.from_user.id, res)
        else:
            try:
                quastion = got_message.text
                if user_id in messages:
                    messages[user_id].append(HumanMessage(content=quastion))
                else:
                    messages[user_id] = [systemmessage]
                    messages[user_id].append(HumanMessage(content=quastion))
                res = chat(messages[user_id])
                bot.send_message(got_message.from_user.id, res.content)
            except Exception as e:
                print(e)
                bot.send_message(got_message.from_user.id, "Я вас не понял")


bot.polling(none_stop=True, interval=0)
