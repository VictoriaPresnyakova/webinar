import json
from asyncio import sleep
from datetime import datetime, timezone, timedelta

from pyrogram import Client, filters
from pyrogram.errors import FloodWait

from database import StatusEnum
from dto import User
from service import list_users, save_user, list_alive_users, update_user

WAITING = [6 * 60, 39 * 60, 24 * 60 * 60 + 2 * 60 * 60]
TRIGGER = 'Тригер1'
FINISH = ['прекрасно', 'ожидать']
MESSAGES = ['Текст1', 'Текст2', 'Текст3']

with open(f"config.json", "r", encoding='utf-8') as file:
    config = json.load(file)


def log(s: str):  # функция логирования
    now = datetime.now()
    msg = f'Бот {config["username"]} {now.strftime("%Y-%m-%d %H:%M:%S")}: {s}\n\n'
    print(msg)
    with open(f'bot-{bot_id}.log', 'a', encoding='utf-8') as file:
        file.write(msg)


proxy = {
    'scheme': 'http',
    'hostname': config['proxy_host'],
    'port': config['proxy_port'],
    'username': config['proxy_username'],
    'password': config['proxy_password']
}

app = Client(
    name=config['name'],
    api_id=config['api_id'],
    api_hash=config['api_hash'],
    proxy=proxy
)


@app.on_message(filters.private & filters.incoming)
async def message_handle(app, message):
    try:
        now = datetime.now()
        user = await save_user(User(id=message.chat.id, created_at=now, status=StatusEnum.ALIVE,
                                    status_updated_at=now,
                                    msg_num=0, msg_to_send_at=now + timedelta(seconds=WAITING[0])))
    except Exception as ex:
        log(f'Ошибка сохранения пользователя {message.chat.id}: {ex}')


async def send_messages(app):
    while True:
        wait = min(WAITING)
        users = list_alive_users()
        async for user in users:
            if datetime.now() >= user.msg_to_send_at:
                try:
                    messages = [i.text.lower() async for i in app.get_chat_history(chat_id=user.id) if
                                i.from_user.is_self]
                    messages = ' '.join(messages)

                    for i in FINISH:
                        if i.lower() in messages:
                            user.status = StatusEnum.FINISHED
                            break

                    else:
                        now = datetime.now()

                        trigger_fix = 0

                        if not (user.msg_num == 1 and TRIGGER.lower() in messages):
                            await app.send_message(chat_id=user.id, text=MESSAGES[user.msg_num])
                        else:
                            trigger_fix = WAITING[user.msg_num]

                        user.msg_num += 1
                        user.status_updated_at = now

                        if user.msg_num == len(MESSAGES):
                            user.status = StatusEnum.FINISHED
                        else:
                            user.msg_to_send_at = (now + timedelta(seconds=WAITING[user.msg_num])
                                                   - timedelta(seconds=trigger_fix))
                    user = await update_user(user)

                except FloodWait as ex:
                    await sleep(ex.value)

                except Exception as e:
                    if 'deleted' in str(e) and 'target user' in str(e):
                        user.status_updated_at = datetime.now()
                        user.status = StatusEnum.DEAD
                        await update_user(user)

            wait = min(wait, (user.msg_to_send_at - datetime.now()).seconds)
        await sleep(wait)



if __name__ == '__main__':
    try:
        with app:
            app.loop.run_until_complete(send_messages(app))
    except Exception as ex:
        log(f'Упал бот: {ex}')
