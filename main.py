import vk_api
import pygame
from vk_api.longpoll import VkLongPoll, VkEventType
import os
import requests
import shutil
import pyperclip


pygame.init()
SONG = pygame.mixer.Sound('chechnya.mp3')
SONG_FILE = pygame.mixer.Sound('file_song.mp3')
TOKEN = 'vk1.a.0UrJgU1NK03XbyNXmGJ--YL409Ac7gJQC6QJpxV30UVFmw3KFoLquzwkboM75NVufo7jXxwBJr-_lPuQptq-ajxseFRxyx7js6490tVYalq13cJ3RNJj1TdmriL0yedxTsmcAMyQVOiWrzdcoU_fsvW3avRIg-4mL-VoDooNe8DQSMlNVGEU6UKKzLvABXQ3JJQEE7cmK-1vdxbunla2pw'
session = vk_api.VkApi(token=TOKEN)
vk = session.get_api()
shutil.rmtree('C:/Users/21/Desktop/printdocs')
os.chdir('C:/Users/21/Desktop')
os.mkdir('printdocs')
os.chdir('C:/Users/21/Desktop/printdocs')


def get_file(jsonfile, message, name):
    full_title = message.split("'")[0]
    form = full_title.split('.')[1]
    title = full_title.split('.')[0]
    url = jsonfile.split("'")[0]
    file = requests.get(url)
    with open(f'C:/Users/21/Desktop/printdocs/{name}/{title}.{form}', 'wb') as f:
        f.write(file.content)


def get_name_and_make_dir(person_id):
    data_person = vk.users.get(user_id=person_id)[0]
    name = data_person['first_name'] + " " + data_person['last_name']
    if not os.path.isdir(name):
        os.mkdir(name)
    return name


while True:
    try:
        for event in VkLongPoll(session).listen():
            if event.type == VkEventType.MESSAGE_NEW:
                try:
                    if event.chat_id == 1:
                        text = event.text.lower()
                        if ('кто' in text and 'печатает' in text) or ('кто' in text and 'распечатать' in text) or (
                                'кто' in text and 'распечатает' in text):
                            if 'цвет' not in text:
                                session.method('messages.send', {'chat_id': 1, 'message': 'Печатаю', 'random_id': 0})
                                SONG.play()
                                break
                except:
                    pass
                if event.user_id:
                    user_id = str(event.user_id)
                    last_message_titles = str(vk.messages.getHistory(peer_id=user_id, count=1)).split("title': '")
                    del last_message_titles[0]
                    last_message = str(vk.messages.getHistory(peer_id=user_id, count=1)).split("url': '")
                    del last_message[0]
                    count = 0
                    for doc in last_message:
                        person_name = get_name_and_make_dir(user_id)
                        get_file(doc, last_message_titles[count], person_name)
                        count += 1
                    if count != 0:
                        pyperclip.copy('Готово, +79218285997 / 66 блок 10 этаж ')
                        SONG_FILE.play()

    except:
        print('error')