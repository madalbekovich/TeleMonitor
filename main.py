import os
from pyrogram import Client, filters, types
import re
from dotenv import load_dotenv

load_dotenv()

api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
session_name = os.getenv("SESSION_NAME")
source_chats = os.getenv("SOURCE_CHATS").split(",")
destination_channel = os.getenv("DESTINATION_CHANNEL")
keywords = os.getenv("KEYWORDS").split(",")
pattern = re.compile(rf'\b({"|".join(keywords)})\b', re.IGNORECASE)

app = Client(session_name, api_id=api_id, api_hash=api_hash)

@app.on_message(filters.chat(source_chats))
async def message_handler(client, message):
    if message.chat.username == destination_channel.lstrip("@"):
        return

    text = message.text or message.caption or ""
    if not pattern.search(text):
        return

    print(f"[+] Найдено сообщение: {text[:50]}...")
    # print(f"Отладка: chat_id={message.chat.id}, message_id={message.id}, media_group_id={message.media_group_id}")

    if message.media_group_id:
        try:
            if not isinstance(message.media_group_id, int) or message.media_group_id > 2_147_483_647:
                print(f"[!] Большой media_group_id: {message.media_group_id}, собираем группу вручную")
                message_ids = range(max(1, message.id - 5), message.id + 6)
                messages = await app.get_messages(message.chat.id, message_ids)

                media = []
                for msg in messages:
                    if msg and msg.media_group_id == message.media_group_id:
                        if msg.photo:
                            media.append(("photo", msg.photo.file_id))
                        elif msg.video:
                            media.append(("video", msg.video.file_id))

                if media:
                    print(f"[+] Найдено {len(media)} элементов в медиа-группе")
                    media_group = []
                    for i, (media_type, file_id) in enumerate(media):
                        if media_type == "photo":
                            media_group.append(types.InputMediaPhoto(media=file_id, caption=text if i == 0 else ""))
                        elif media_type == "video":
                            media_group.append(types.InputMediaVideo(media=file_id, caption=text if i == 0 else ""))
                    await app.send_media_group(destination_channel, media_group)
                else:
                    print("[!] Медиа в группе не найдено, отправляем текст")
                    await app.send_message(destination_channel, text)
            else:
                messages = await app.get_media_group(message.chat.id, message.media_group_id)
                media = []
                for msg in messages:
                    if msg.photo:
                        media.append(("photo", msg.photo.file_id))
                    elif msg.video:
                        media.append(("video", msg.video.file_id))
                if media:
                    media_group = []
                    for i, (media_type, file_id) in enumerate(media):
                        if media_type == "photo":
                            media_group.append(types.InputMediaPhoto(media=file_id, caption=text if i == 0 else ""))
                        elif media_type == "video":
                            media_group.append(types.InputMediaVideo(media=file_id, caption=text if i == 0 else ""))
                    await app.send_media_group(destination_channel, media_group)
                else:
                    await app.send_message(destination_channel, text)
        except Exception as e:
            print(f"[!] Ошибка при обработке медиа-группы: {e}, переход к одиночному сообщению")
            if message.photo:
                await app.send_photo(destination_channel, message.photo.file_id, caption=text)
            elif message.video:
                await app.send_video(destination_channel, message.video.file_id, caption=text)
            else:
                await app.send_message(destination_channel, text)
    else:
        if message.photo:
            await app.send_photo(destination_channel, message.photo.file_id, caption=text)
        elif message.video:
            await app.send_video(destination_channel, message.video.file_id, caption=text)
        else:
            await app.send_message(destination_channel, text)

print("[+] Скрипт запущен! Слушаю каналы...")
app.run()