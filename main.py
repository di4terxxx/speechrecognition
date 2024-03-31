# импорты
import json
# from time import time

from googletrans import Translator
import pyaudio
from vosk import Model, KaldiRecognizer
# пересылка в тг
import requests

TOKEN = "6408988087:AAFF9BAzDysekMdkB9sXXW72OrsmXaC-0Zw"
chat_id = "6159916754"
# chat_id = "967517803"
# озвучка
import pyttsx3

engine = pyttsx3.init()
rate = engine.getProperty("rate")
engine.setProperty("rate", 100)
# перевод
translator = Translator()
# распознавание речи
model = Model('vosk_model_small')
# model = Model('vosk-model-ru-0.10')

rec = KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()


def listen():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if (rec.AcceptWaveform(data)) and (len(data) > 0):
            answer = json.loads(rec.Result())
            if (answer['text']):
                yield answer['text']


def translate(str):
    if to_translate:
        translation = translator.translate(str, dest='en')
        engine.say(translation.text)
        engine.runAndWait()
        return translation.text
    return  str


def send_to_tg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={text}"
    requests.get(url)  # можно сделать ассинхронно

def speak(text):
    if to_speak:
        engine.say(text)
        engine.runAndWait()

# начало основной программы
to_translate = False
to_speak = False

for text in listen():
    # a = time()
    text = translate(text)
    if text == 'стоп' or text=='Stop' or text=='stop':
        to_translate = False
        print('язык: Русский')
        continue
    elif text == 'пока' or text == 'Bye':
        speak("bye")
        quit()
    elif text == 'привет':
        speak('привет')
        print('-Привет!')
        continue
    elif text == 'переведи':
        print('язык: Английский')
        to_translate = True
        continue
    elif text == 'как дела':
        speak('хорошо')
        continue
    elif text == 'говори':
        print('озвучка включена')
        to_speak = True
        continue
    elif text == 'тихо':
        to_speak = False
        print("озвучка выключена")

        continue
    send_to_tg(text)
    # print('время на обработку =' + str(time() - a))
    speak(text)
    print(text)
# конец