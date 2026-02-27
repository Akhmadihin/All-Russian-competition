import random
import asyncio
import edge_tts
import pygame
import io
import sys
import os
from translate import Translator

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

list_irregular = []
listen_irregular = []

pygame_initialized = False

with open ('config.txt', 'r') as f:
    data = f.read()
    str(object='data')

def init_pygame():
    """Инициализирует pygame mixer"""
    global pygame_initialized
    if not pygame_initialized:
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            pygame_initialized = True
        except Exception as e:
            print(f"❌ Ошибка инициализации аудио: {e}")
            return False
    return True

def first_display():     
    print("Здравствуйте!")
    print("Это начальный экран Программы для изучения английских слов с ИИ")
    print("Выберите действие которое в будующем можно будет измениять в настройках")
    print("1. Писать перевод к каждому слову самому")
    print("2. Использовать встроенный переводчик")
    user = input("Введите номер команды: ")
    str(object='user')

    with open ('config.txt', 'r') as f:
        old_data = f.read()

    data = old_data.replace('0', user)

    with open ('config.txt', 'w') as f:
        f.write(data)

    return data

def start():
    print("="*10, "Программа для изучения английских слов с ИИ", "="*10)
    print("1. Учить свои слова")
    print("2. Учить неправильные глаголы нужные для сдачи ОГЭ|ЕГЭ")
    print("3. Прослушать неправильные глаголы")
    print("4. Ввести свои слова")
    print("5. Прослушать свои слова")
    print("6. Настройки")
    user = int(input("Введите номер команды: "))
    if user == 1:
        main()
    if user == 2:
        print_Irregular()
    if user == 3:
        init_pygame()
        listen_Irregular()
    if user == 4:
        redactor()
    if user == 5:
        init_pygame()
        speak()
    if user == 6:
        settings()

def speak():
    print("Введите слова которые хотите прослушать")
    print("Напишите 'выйти' что бы выйти")
    while True:
        user = input("Вводите: ")
        if user.lower() == 'выйти':
            break
        
        asyncio.run(svetlana_says(user))

def redactor():
    global translator

    user_input = []
    user_translation = []
    txt_files = []
    file = 0

    print("Хотите ли вы создать новый файл для слов или вы хотите изменить старые?")
    user = input('Напишите Создать|Сохранить: ')
    if user.lower() == 'создать':
        user = input("Напишите имя файла без разширения: ")
        open(f'{user}.txt', 'w').close()
        file = f'{user}.txt'
    else:
        directory = '.'
        for file in os.listdir(directory):
            if file.endswith('.txt'):
                txt_files.append(file)
        print(f'Какой файл вы хотите открыть и изменить?')
        for i in range(len(txt_files)):
            print(f'{i+1}. {txt_files[i]}')
        user = int(input("Введите номер файла: "))
        file = txt_files[user-1]

    with open(file, 'w') as f:
        f.write("")
            
    def manually(user_input, user_translation, file):
        print("Вы находитесь в ручном редакторе своих слов, что бы выйти напишите 'выйти'")
        print("Пишите в формате: 'hello - привет'")
        print("Каждое новое слово пишите в новой строке:")

        with open(file, 'w') as f:
            f.write("")
            
        while True:
            user = input()
            if user != 'выйти':
                user_input.append(user)
                
                with open (file, 'a', encoding='utf-8') as f:
                    f.write(f'{user_input[len(user_input)-1]}\n')
            else:
                break
        
    def auto(user_input, user_translation, file):
        print("Вы находитесь в автоматическом редакторе своих слов, что бы выйти напишите 'выйти'")
        print("Пишите в формате: 'hello', а перевод подберется сам!")
        print("Каждое новое слово пишите в новой строке:")
            
        translator = Translator(to_lang="ru")

        with open(file, 'w') as f:
            f.write("")
                
        while True:
            user = input()
            if user != 'выйти':
                translation = translator.translate(user)
                user_translation.append(translation)
                user_input.append(user)
                
                with open (file, 'a', encoding='utf-8') as f:
                    f.write(f'{user_input[len(user_input)-1]} - {user_translation[len(user_translation)-1]}\n')
            else:
                break

    if data == '1':
        manually(user_input, user_translation, file)
    if data == '2':
        auto(user_input, user_translation, file)

def settings():
    global data
    if data == "1":
        print("Сейчас выбрана функция 'Вручную'")
    if data == "2":
        print("Сейчас выбрана функция 'Автоматически'")
    print("Для изменения режима введите его номер")
    print("1. Писать перевод к каждому слову самому")
    print("2. Использовать встроенный переводчик")
    print("3. Выход")
    user = input("Введите номер команды: ")

    if user != "3":
        with open ('config.txt', 'r') as f:
            old_data = f.read()

        data = old_data.replace(data, user)

        with open ('config.txt', 'w') as f:
            f.write(data)
    else:
        start()

def listen_Irregular():
    with open("Irregular_listen.txt", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                listen_irregular.append(line)

    print("Вам будет проговариваться по одному слову в 3-х формах")
    print("Что бы начать прослушивание следующей группы глаголов вам нужно нажать Enter")
    print("Что бы выйти пишите 'выйти'")

    for i in range(len(listen_irregular)):
        
        verb_list = listen_irregular[i]
        
        asyncio.run(svetlana_says(verb_list))

        user = input()

        if user == "выйти":
            break

    start()

async def svetlana_says(text):
    text = f"{text}"
    communicate = edge_tts.Communicate(text, "en-GB-SoniaNeural")
    audio_chunks = []
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_chunks.append(chunk["data"])

    audio_data = b''.join(audio_chunks)
    audio_bytes = io.BytesIO(audio_data)

    pygame.mixer.music.load(audio_bytes)
    pygame.mixer.music.play()
        
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(2)

def print_Irregular():
    with open("Irregular_learn.txt", encoding="utf-8") as file:
        for line in file:
            list_irregular.append(line.strip())
        for i in range(len(list_irregular)):
            print(list_irregular[i])


def main():
    
    left_list = []
    right_list = []

    directory = '.'
    txt_files = []
    for file in os.listdir(directory):
        if file.endswith('.txt'):
            txt_files.append(file)
    print(f'Какой файл вы хотите открыть и повторить слова?')
    for i in range(len(txt_files)):
        print(f'{i+1}. {txt_files[i]}')
    user = int(input("Введите номер файла: "))
        
    with open(txt_files[user-1], encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if '-' in line:
                left, right = line.split('-', 1)
                left_list.append(left.strip())
                right_list.append(right.strip())

    total_words = len(left_list)
    
    if total_words == 0:
        print("Слова не найдены!")
        return
    
    used = [] 
    lose = []
    
    print(f"Всего слов: {total_words}")
    print("Начинаем тренировку:")
    
    all_indices = list(range(total_words))
    random.shuffle(all_indices)
    
    for i in all_indices:
        left = left_list[i]
        answer = input(f'{left} ---------- ').strip()
        
        if answer == right_list[i]:
            print('Правильно!')
        else:
            right = right_list[i]
            lose.append(i)
            print(f'Неправильно! {right}')
    
    while lose:
        print(f"\nНужно повторить {len(lose)} слов:")
        
        current_lose = lose.copy()
        lose = []
        
        random.shuffle(current_lose)
        
        for i in current_lose:
            left = left_list[i]
            answer = input(f'{left} ---------- ').strip()
            
            if answer == right_list[i]:
                print('Правильно!')
            else:
                right = right_list[i]
                lose.append(i)
                print(f'Неправильно! {right}')
    
    print("\nПоздравляем! Все слова выучены!")

while True:
    if data == "0":
        with open ('config.txt', 'r') as f:
            data = f.read()
            str(object='data')
        
    if data == "0":
        first_display()
    else:
        start()
