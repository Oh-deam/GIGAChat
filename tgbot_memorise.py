import time
import telebot
import sqlite3
import datetime
import schedule

bot = telebot.TeleBot("6771849352:AAFiFk-Ri4E9oVYkRdSFkCO4ge329kczfmI")

def find_near_date(tasks: list) -> str:
    near_tasks = []
    now = datetime.datetime.now()
    day, month = now.day, now.month
    print(f'tasks in fun', tasks)
    print(f'today is {day}.{month}')
    for el in tasks:
        day_task_start, month_task_start  = int(el.split(':')[1].split('.')[0]), int(el.split(':')[1].split('.')[1]) 
        if len(el.split(':')) < 3:
            day_task_end, month_task_end = day_task_start, month_task_start 
        else:
            day_task_end, month_task_end = int(el.split(':')[2].split('.')[0]), int(el.split(':')[2].split('.')[1])

        if int(day)+1 >= day_task_start and int(month) == month_task_start:
            near_tasks.append(el.replace(':', ' - '))

        elif day_task_start < int(day) < day_task_end and month_task_start <= int(month) <= month_task_end:
            near_tasks.append(el.replace(':', ' - '))
    return '\n'.join(near_tasks) 

def send_remember():
    db = sqlite3.connect('task_manager_data.db', check_same_thread=False)
    cursor = db.cursor()

    users_data = cursor.execute("""SELECT * FROM users_data""").fetchall()
    #print(users_data)

    users_id = []
    users_tasks = []

    for el in users_data:
        users_id.append(el[0])
        users_tasks.append(el[1])

    for id, task in zip(users_id,users_tasks):
        if id == 1061389532:
            print('skip')
            continue
        near_tasks = find_near_date(task.split(';'))
        message = 'Напоминаю, что вам нужно сделать:\n' + near_tasks
        bot.send_message(id, message)
        print('complete')

schedule.every(15).seconds.do(send_remember)

while True:
    schedule.run_pending()
    time.sleep(1)