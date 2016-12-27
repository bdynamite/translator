import requests
import glob
import os
import chardet

KEY = 'trnsl.1.1.20161216T160124Z.4a07c4b6a2f01566.ade260e6c684818698899fd08a9c15d72faca843'
URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
INPUT = 'input'
OUTPUT = 'output'


def translate_text(mytext, lang):
    params = {
        'key': KEY,
        'text': mytext,
        'lang': lang,
    }
    response = requests.get(URL, params=params)
    return response.json()


def code_detecter(path_to_file_text):
    with open(path_to_file_text, 'rb') as source:
        lines = source.read()
        result = chardet.detect(lines)
        if result['encoding'] is None:
            raise Exception("Неизвестная кодировка файла!")
        else:
            return result['encoding']


files = glob.glob(os.path.join(INPUT, "*.txt"))
for path in files:
    encoding = code_detecter(path)
    print('Перевод файла {}'.format(path))
    file_name = path.split('\\')[1]
    news_language = file_name.split('.')[0]
    with open(path, mode='r', encoding=encoding) as file:
        json = translate_text(file.readlines(), news_language + '-ru')
        ru_file = open('\\'.join((OUTPUT, file_name)), mode='w')
        ru_file.write(' '.join(json['text']))
        ru_file.close()




