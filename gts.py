from gtts import gTTS
#from playsound import playsound
from pydub import AudioSegment
from pydub.playback import play

name = input('Введите свое имя: ')
tts = gTTS(f'Добрый день {name}', lang='ru')
tts.save('hello.mp3')
sound = AudioSegment.from_mp3('hello.mp3')
play(sound)
#print(sound)