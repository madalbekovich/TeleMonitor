# import os
# from pyrogram import Client, filters, types
# import re
# from dotenv import load_dotenv
#
# load_dotenv()
#
# api_id = os.getenv("API_ID")
# api_hash = os.getenv("API_HASH")
# session_name = os.getenv("SESSION_NAME")
# source_chats = os.getenv("SOURCE_CHATS").split(",")
# destination_channel = os.getenv("DESTINATION_CHANNEL")
# keywords = os.getenv("KEYWORDS").split(",")
# pattern = re.compile(rf'\b({"|".join(keywords)})\b', re.IGNORECASE)
#
# app = Client(session_name, api_id=api_id, api_hash=api_hash)
#
# @app.on_message(filters.chat(source_chats))
# async def message_handler(client, message):
#     print(f"[DEBUG] Получено сообщение из: {message.chat.username} — {message.text or message.caption}")
#     if message.chat.username == destination_channel.lstrip("@"):
#         return
#
#     text = message.text or message.caption or ""
#     if not pattern.search(text):
#         return
#
#     print(f"[+] Найдено сообщение: {text[:50]}...")
#     # print(f"Отладка: chat_id={message.chat.id}, message_id={message.id}, media_group_id={message.media_group_id}")
#
#     if message.media_group_id:
#         try:
#             if not isinstance(message.media_group_id, int) or message.media_group_id > 2_147_483_647:
#                 print(f"[!] Большой media_group_id: {message.media_group_id}, собираем группу вручную")
#                 message_ids = range(max(1, message.id - 5), message.id + 6)
#                 messages = await app.get_messages(message.chat.id, message_ids)
#
#                 media = []
#                 for msg in messages:
#                     if msg and msg.media_group_id == message.media_group_id:
#                         if msg.photo:
#                             media.append(("photo", msg.photo.file_id))
#                         elif msg.video:
#                             media.append(("video", msg.video.file_id))
#
#                 if media:
#                     print(f"[+] Найдено {len(media)} элементов в медиа-группе")
#                     media_group = []
#                     for i, (media_type, file_id) in enumerate(media):
#                         if media_type == "photo":
#                             media_group.append(types.InputMediaPhoto(media=file_id, caption=text if i == 0 else ""))
#                         elif media_type == "video":
#                             media_group.append(types.InputMediaVideo(media=file_id, caption=text if i == 0 else ""))
#                     await app.send_media_group(destination_channel, media_group)
#                 else:
#                     print("[!] Медиа в группе не найдено, отправляем текст")
#                     await app.send_message(destination_channel, text)
#             else:
#                 messages = await app.get_media_group(message.chat.id, message.media_group_id)
#                 media = []
#                 for msg in messages:
#                     if msg.photo:
#                         media.append(("photo", msg.photo.file_id))
#                     elif msg.video:
#                         media.append(("video", msg.video.file_id))
#                 if media:
#                     media_group = []
#                     for i, (media_type, file_id) in enumerate(media):
#                         if media_type == "photo":
#                             media_group.append(types.InputMediaPhoto(media=file_id, caption=text if i == 0 else ""))
#                         elif media_type == "video":
#                             media_group.append(types.InputMediaVideo(media=file_id, caption=text if i == 0 else ""))
#                     await app.send_media_group(destination_channel, media_group)
#                 else:
#                     await app.send_message(destination_channel, text)
#         except Exception as e:
#             print(f"[!] Ошибка при обработке медиа-группы: {e}, переход к одиночному сообщению")
#             if message.photo:
#                 await app.send_photo(destination_channel, message.photo.file_id, caption=text)
#             elif message.video:
#                 await app.send_video(destination_channel, message.video.file_id, caption=text)
#             else:
#                 await app.send_message(destination_channel, text)
#     else:
#         if message.photo:
#             await app.send_photo(destination_channel, message.photo.file_id, caption=text)
#         elif message.video:
#             await app.send_video(destination_channel, message.video.file_id, caption=text)
#         else:
#             await app.send_message(destination_channel, text)
#
# print("[+] Скрипт запущен! Слушаю каналы...")
# app.run()

# import os
# from pyrogram import Client, filters, types
# import re
# from dotenv import load_dotenv
#
# load_dotenv()
#
# api_id = os.getenv("API_ID")
# api_hash = os.getenv("API_HASH")
# session_name = os.getenv("SESSION_NAME")
# source_chats = os.getenv("SOURCE_CHATS").split(",")
# destination_channel = os.getenv("DESTINATION_CHANNEL")
# keywords = os.getenv("KEYWORDS").split(",")
# pattern = re.compile(rf'\b({"|".join(keywords)})\b', re.IGNORECASE)
#
# app = Client(session_name, api_id=api_id, api_hash=api_hash)
#
# print(f"[+] Скрипт запущен! Слушаю каналы...")
# print(f"[INFO] Source chats: {source_chats}")
# print(f"[INFO] Destination channel: {destination_channel}")
# print(f"[INFO] Keywords: {keywords}")
#
#
# # Лог всех сообщений, вообще любых, из любого чата
# @app.on_message()
# async def all_messages_log(client, message):
#     chat = message.chat
#     print(f"[ALL MESSAGES] Из чата: ID={chat.id} | Username={chat.username} | Title={chat.title} | Text={message.text or message.caption}")
#
#
# @app.on_message(filters.chat(source_chats))
# async def message_handler(client, message):
#     chat = message.chat
#     print(f"[DEBUG] Получено сообщение из: ID={chat.id} | Username={chat.username} | Title={chat.title} | Text={message.text or message.caption}")
#
#     if message.chat.username == destination_channel.lstrip("@"):
#         print("[DEBUG] Сообщение из канала назначения, пропускаем")
#         return
#
#     text = message.text or message.caption or ""
#     if not pattern.search(text):
#         print("[DEBUG] Сообщение не содержит ключевых слов, пропускаем")
#         return
#
#     print(f"[+] Найдено сообщение: {text[:50]}...")
#
#     try:
#         if message.media_group_id:
#             print(f"[DEBUG] Обнаружена media_group_id: {message.media_group_id}")
#             if not isinstance(message.media_group_id, int) or message.media_group_id > 2_147_483_647:
#                 print(f"[!] Большой media_group_id: {message.media_group_id}, собираем группу вручную")
#                 message_ids = range(max(1, message.id - 5), message.id + 6)
#                 messages = await app.get_messages(message.chat.id, message_ids)
#
#                 media = []
#                 for msg in messages:
#                     if msg and msg.media_group_id == message.media_group_id:
#                         if msg.photo:
#                             media.append(("photo", msg.photo.file_id))
#                         elif msg.video:
#                             media.append(("video", msg.video.file_id))
#
#                 if media:
#                     print(f"[+] Найдено {len(media)} элементов в медиа-группе")
#                     media_group = []
#                     for i, (media_type, file_id) in enumerate(media):
#                         if media_type == "photo":
#                             media_group.append(types.InputMediaPhoto(media=file_id, caption=text if i == 0 else ""))
#                         elif media_type == "video":
#                             media_group.append(types.InputMediaVideo(media=file_id, caption=text if i == 0 else ""))
#                     await app.send_media_group(destination_channel, media_group)
#                 else:
#                     print("[!] Медиа в группе не найдено, отправляем текст")
#                     await app.send_message(destination_channel, text)
#             else:
#                 messages = await app.get_media_group(message.chat.id, message.media_group_id)
#                 media = []
#                 for msg in messages:
#                     if msg.photo:
#                         media.append(("photo", msg.photo.file_id))
#                     elif msg.video:
#                         media.append(("video", msg.video.file_id))
#                 if media:
#                     media_group = []
#                     for i, (media_type, file_id) in enumerate(media):
#                         if media_type == "photo":
#                             media_group.append(types.InputMediaPhoto(media=file_id, caption=text if i == 0 else ""))
#                         elif media_type == "video":
#                             media_group.append(types.InputMediaVideo(media=file_id, caption=text if i == 0 else ""))
#                     await app.send_media_group(destination_channel, media_group)
#                 else:
#                     await app.send_message(destination_channel, text)
#         else:
#             if message.photo:
#                 print("[DEBUG] Сообщение с фото")
#                 await app.send_photo(destination_channel, message.photo.file_id, caption=text)
#             elif message.video:
#                 print("[DEBUG] Сообщение с видео")
#                 await app.send_video(destination_channel, message.video.file_id, caption=text)
#             else:
#                 print("[DEBUG] Текстовое сообщение")
#                 await app.send_message(destination_channel, text)
#
#     except Exception as e:
#         print(f"[!] Ошибка при обработке сообщения: {e}")
#
#
# app.run()




### WORK CODE BUT 1 PHOTO NOT MEDIA GROUP

# import logging
# from telethon import TelegramClient, events
# import asyncio
# from datetime import datetime, timedelta
#
# logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
#
# API_ID = 22234520
# API_HASH = '620be1ad698c8373fdf1a383e0c0bd71'
# SESSION_NAME = 'my_session'
#
# SOURCE_CHATS = [
#     'auto_donetskv',
#     'CarMarketDNR',
#     'DNR_AVTO_180',
#     'kanal_test_my',
#     'sotka_dnr_lnr'
# ]
# DESTINATION_CHANNEL = 'my_test_kanal_2'
#
# KEYWORDS = [
#     'Продаётся', 'продам', 'hyundai', 'Продается', 'Продаю',
#     'бензин', 'kia', 'ваз', 'Машина', 'Автомобиль', 'год',
#     'Год', 'Продам', 'Объем', 'Авто', 'Бот', 'Цена', 'цена'
# ]
#
# # Инициализация клиента
# client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
#
#
# async def check_chats():
#     last_check = {}
#     while True:
#         for chat_username in SOURCE_CHATS:
#             try:
#                 chat = await client.get_entity(chat_username)
#                 chat_id = chat.id
#                 logging.info(f"Проверяю чат: {chat_username} (ID={chat_id})")
#
#                 messages = await client.get_messages(chat, limit=10)
#                 last_message_id = last_check.get(chat_id, 0)
#
#                 for message in reversed(messages):
#                     if message.id <= last_message_id:
#                         continue
#
#                     msg_text = message.text or "Медиа"
#                     logging.info(f"[CHECK] ID={message.id} | Chat={chat_username} | Text={msg_text}")
#
#                     if message.text and any(keyword.lower() in message.text.lower() for keyword in KEYWORDS):
#                         if message.date > datetime.now(tz=message.date.tzinfo) - timedelta(minutes=5):
#                             logging.info(f"[FORWARD] Пересылаю из {chat_username}")
#                             await client.forward_messages(DESTINATION_CHANNEL, message)
#
#                 if messages:
#                     last_check[chat_id] = max(msg.id for msg in messages)
#
#             except Exception as e:
#                 logging.error(f"Ошибка при проверке {chat_username}: {e}")
#
#         await asyncio.sleep(30)
#
#
# async def main():
#     await client.start()
#     logging.info("🚀 Userbot запущен!")
#     me = await client.get_me()
#     logging.info(f"Я подключён как: {me.username} ({me.phone})")
#
#     await check_chats()
#
#
# if __name__ == '__main__':
#     client.loop.run_until_complete(main())
#



import logging
from telethon import TelegramClient
import asyncio
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME")
SOURCE_CHATS = os.getenv("SOURCE_CHATS").split(",")
DESTINATION_CHANNEL = os.getenv("DESTINATION_CHANNEL")
KEYWORDS = os.getenv("KEYWORDS").split(",")

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

async def check_chats():
    last_check = {}
    while True:
        for chat_username in SOURCE_CHATS:
            try:
                chat = await client.get_entity(chat_username)
                chat_id = chat.id
                logging.info(f"Проверяю чат: {chat_username} (ID={chat_id})")

                messages = await client.get_messages(chat, limit=10)
                last_message_id = last_check.get(chat_id, 0)

                processed_groups = set()  # Отслеживаем обработанные медиа-группы

                for message in reversed(messages):
                    if message.id <= last_message_id:
                        continue

                    msg_text = message.text or "Медиа"
                    logging.info(f"[CHECK] ID={message.id} | Chat={chat_username} | Text={msg_text}")

                    if message.text and any(keyword.lower() in message.text.lower() for keyword in KEYWORDS):
                        if message.date > datetime.now(tz=message.date.tzinfo) - timedelta(minutes=5):
                            # Проверяем, есть ли медиа-группа
                            if message.grouped_id and message.grouped_id not in processed_groups:
                                logging.info(f"[MEDIA GROUP] Обнаружена группа: {message.grouped_id}")
                                # Собираем все сообщения из медиа-группы
                                group_messages = [msg for msg in messages if msg.grouped_id == message.grouped_id]
                                processed_groups.add(message.grouped_id)

                                # Пересылаем группу
                                logging.info(f"[FORWARD] Пересылаю медиа-группу из {chat_username} ({len(group_messages)} элементов)")
                                await client.forward_messages(DESTINATION_CHANNEL, group_messages)
                            elif not message.grouped_id:
                                # Одиночное сообщение
                                logging.info(f"[FORWARD] Пересылаю одиночное сообщение из {chat_username}")
                                await client.forward_messages(DESTINATION_CHANNEL, message)

                if messages:
                    last_check[chat_id] = max(msg.id for msg in messages)

            except Exception as e:
                logging.error(f"Ошибка при проверке {chat_username}: {e}")

        await asyncio.sleep(30)

async def main():
    await client.start()
    logging.info("🚀 Userbot запущен!")
    me = await client.get_me()
    logging.info(f"Я подключён как: {me.username} ({me.phone})")

    await check_chats()

if __name__ == '__main__':
    client.loop.run_until_complete(main())